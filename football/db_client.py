import random
import asyncio
import aiohttp
from datetime import datetime, timedelta, date
from faker import Faker
from urllib.parse import urlencode

fake = Faker(['ru_RU'])

class AsyncDBClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def execute_query(self, endpoint, method="GET", data=None, filters=None):
        url = self.base_url + endpoint  # Базовый URL добавляется только здесь

        if method == "GET" and filters:
            url += "?" + urlencode(filters)

        try:
            if method == "GET":
                async with self.session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 404:
                        return None
                    else:
                        error_text = await response.text() # Получаем текст ошибки
                        print(f"Ошибка при GET запросе к {url}: {response.status}, error: {error_text}") # Выводим ошибку
                        return None
            elif method == "POST":
                async with self.session.post(url, json=data) as response:
                    if response.status == 201:
                        created_object = await response.json()
                        return created_object
                    else:
                        error_text = await response.text()
                        print(f"Ошибка при POST запросе к {url}: {response.status}, data: {data}, error: {error_text}")
                        return None
            elif method == "PUT":
                async with self.session.put(url, json=data) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        print(f"Ошибка при PUT запросе к {url}: {response.status}, data: {data}, error: {error_text}")
                        return None
            elif method == "DELETE":
                async with self.session.delete(url) as response:
                    if response.status == 204:  # 204 - No Content
                        return True
                    else:
                        error_text = await response.text()
                        print(f"Ошибка при DELETE запросе к {url}: {response.status}, error: {error_text}")
                        return None
            else:
                print(f"Неподдерживаемый метод: {method}")
                return None

        except aiohttp.ClientError as e:
            print(f"Ошибка сети: {e}")
            return None

    async def get_total_count(self, endpoint):
        """Получает общее количество записей для указанного эндпоинта."""
        result = await self.execute_query(endpoint)
        if result:
            return result['count'] if isinstance(result, dict) and 'count' in result else len(result) # Обработка пагинации и обычного списка
        return 0


    
    async def get_random_id(self, endpoint):
        """Получает случайный существующий ID через API"""
        try:
            # Сначала получаем общее количество записей
            count = await self.get_total_count(endpoint)
            if not count or count == 0:
                print(f"Нет данных в {endpoint} для выбора случайного ID")
                return None
                
            # Выбираем случайный ID в пределах общего количества
            random_id = random.randint(1, count)
            
            # Проверяем существование этого ID
            check_url = f"{endpoint}{random_id}/"
            response = await self.session.get(self.base_url + check_url)
            
            if response.status == 200:
                return random_id
            elif response.status == 404:
                # Если ID не существует, пробуем еще раз
                return await self.get_random_id(endpoint)
            else:
                error_text = await response.text()
                print(f"Ошибка при проверке ID {random_id} в {endpoint}: {response.status}, error: {error_text}")
                return None
                
        except Exception as e:
            print(f"Ошибка при получении случайного ID из {endpoint}: {e}")
            return None


async def simulate_user_activity(client, queries, weights):
    while True:
        method, endpoint, _ = random.choices(queries, weights=weights)[0]
        original_endpoint = endpoint
        today = date.today()

        result = None
        data = {}

        if method == "POST":
            if endpoint == "/api/athletes/":
                data["fullname"] = fake.name()
                data["dateofbirth"] = fake.date_between(start_date='-40y', end_date='-18y').strftime('%Y-%m-%d')
                data["weight"] = random.randint(50, 100)
                data["height"] = random.randint(150, 200)
                data["gender"] = random.choice(['Male', 'Female'])
            elif endpoint == "/api/coaches/":
                data["fullname"] = fake.name()
                data["dateofbirth"] = fake.date_between(start_date='-70y', end_date='-30y').strftime('%Y-%m-%d')
            elif endpoint == "/api/teams/":
                # Получаем случайный ID тренера
                coach_id = await client.get_random_id("/api/coaches/")
                if coach_id:
                    data["coachid"] = coach_id
                data["name"] = fake.company()
                data["rating"] = random.randint(1, 100)
                data["wins"] = random.randint(0, 50)
                data["losses"] = random.randint(0, 50)
                data["draws"] = random.randint(0, 50)
            elif endpoint == "/api/tournaments/":
                data["name"] = fake.word().capitalize() + " Турнир"
                data["location"] = fake.city()
                data["startdate"] = fake.date_between(start_date='-30y', end_date='today').strftime('%Y-%m-%d')
                data["enddate"] = fake.date_between(start_date='-30y', end_date='today').strftime('%Y-%m-%d')
                data["rating"] = random.randint(1, 100)
            elif endpoint == "/api/games/":
                # Получаем случайный ID турнира
                tournament_id = await client.get_random_id("/api/tournaments/")
                if tournament_id:
                    data["tournamentid"] = tournament_id
                data["date"] = fake.date_between(start_date='-30y', end_date='today').strftime('%Y-%m-%d')
                data["location"] = fake.city()
                data["score"] = f"{random.randint(0, 5)}-{random.randint(0, 5)}"
                data["hierarchy"] = random.randint(1, 10)
            elif endpoint == "/api/teamsingames/":
                # Получаем случайные ID команды и игры
                team_id = await client.get_random_id("/api/teams/")
                game_id = await client.get_random_id("/api/games/")
                if team_id and game_id:
                    data["teamid"] = team_id
                    data["gameid"] = game_id
            elif endpoint == "/api/trainings/":
                # Получаем случайный ID команды
                team_id = await client.get_random_id("/api/teams/")
                if team_id:
                    data["teamid"] = team_id
                data["name"] = fake.word().capitalize() + " Тренировка"
                data["date"] = fake.date_between(start_date='-30y', end_date='today').strftime('%Y-%m-%d')
            elif endpoint == "/api/results/":
                # Получаем случайный ID атлета
                athlete_id = await client.get_random_id("/api/athletes/")
                if athlete_id:
                    data["athleteid"] = athlete_id
                data["athleteplace"] = random.randint(1, 100)
                data["goalsscored"] = random.randint(0, 10)
            elif endpoint == "/api/attendance/":
                # Получаем случайный ID атлета
                athlete_id = await client.get_random_id("/api/athletes/")
                if athlete_id:
                    data["athleteid"] = athlete_id
                data["pressrating"] = random.randint(1, 10)
                data["captainrating"] = random.randint(1, 10)
                data["coachrating"] = random.randint(1, 10)
            elif endpoint == "/api/applications/":
                # Получаем случайный ID турнира
                tournament_id = await client.get_random_id("/api/tournaments/")
                if tournament_id:
                    data["tournamentid"] = tournament_id
                data["status"] = random.choice(['Pending', 'Approved', 'Rejected'])

            
            result = await client.execute_query(endpoint, method, data.copy())


        



        elif method == "GET":
            filters = {}

            if endpoint == "/api/coaches/":
                filters = {
                    "fullname__contains": fake.last_name(),
                    "dateofbirth__year__lt": 1965
                }
            elif endpoint == "/api/teams/":
                filters = {
                    "wins": 30,
                    "losses": 5,
                }
            elif endpoint == "/api/athletes/":
                filters = {
                    "dateofbirth__year__gt": 2000,
                    "weight": 74,
                    "height": 190,
                }
            elif endpoint == "/api/tournaments/":
                filters = {
                    "startdate__year__gt": 2022, 
                    "rating": 80
                }
                
            elif endpoint == "/api/games/":
                filters = {
                    "date__year__gt": 2023,  
                    "hierarchy": 9,
                    "score": "4-1"
                }
            elif endpoint == "/api/teamsingames/":
                    filters = {
                    }
            elif endpoint == "/api/trainings/":
                filters = {
                    "date__year__gt": 2024, 
                }
            elif endpoint == "/api/results/":
                filters = {
                    "athleteplace": 10,  
                    "goalsscored": 3
                }
            elif endpoint == "/api/attendance/":
                filters = {
                    "coachrating": 10,
                    "captainrating": 10,
                    "pressrating": 10
                }
            elif endpoint == "/api/applications/":
                tournament_id = await client.get_random_id("/api/tournaments/")
                if tournament_id:
                    filters = {
                        "status": 'Approved',
                        "tournamentid__gt": 10000  
                    }

            elif endpoint == "/api/athletes-trainings/":
                filters = {
                    "gender": 'Male',
                    "weight": 80,
                    "height": 170  
                }    
            elif endpoint == "/api/coaches-tournaments/":
                filters = {
                    "startdate__year": 2023,
                    "dateofbirth__year": 1970,
                }   

                     
            else:  # Для всех остальных GET запросов, если они есть
                filters = {
                    "id__ge": random.randint(1, 5)
                }
                print(f"Неизвестный endpoint для GET запроса: {endpoint}")

            # Преобразуем фильтры в строку URL
            filter_str = urlencode(filters)

            # Исправляем формирование URL
            if filters:  # Если есть фильтры, добавляем их к endpoint
                endpoint += "?" + urlencode(filters)

            result = await client.execute_query(endpoint, method)





        
        elif method == "PUT":
            # Получаем случайный ID для соответствующей сущности
            random_id = await client.get_random_id(endpoint)
            if random_id:
                # Формируем endpoint с ID
                endpoint += f"{random_id}/"

                # Подготавливаем данные для обновления
                data = {}  # Очищаем словарь data на каждой итерации
                if endpoint.startswith("/api/athletes/"):
                    data["dateofbirth"] = fake.date_between(start_date='-40y', end_date='-18y').strftime('%Y-%m-%d')
                    data["weight"] = random.randint(50, 150) # Расширенный диапазон веса
                    data["height"] = random.randint(140, 220) # Расширенный диапазон роста
                elif endpoint.startswith("/api/coaches/"):
                    data["fullname"] = fake.name()
                    data["dateofbirth"] = fake.date_between(start_date='-40y', end_date='-18y').strftime('%Y-%m-%d')
                elif endpoint.startswith("/api/teams/"):
                    data["name"] = fake.company()
                    data["rating"] = random.randint(1, 100)
                    data["wins"] = random.randint(0, 50)
                elif endpoint.startswith("/api/tournaments/"):
                    data["name"] = fake.word().capitalize() + " Турнир"
                    data["location"] = fake.city()
                    data["startdate"] = fake.date_between(start_date='-40y', end_date='-18y').strftime('%Y-%m-%d')
                    data["enddate"] = fake.date_between(start_date='-40y', end_date='-18y').strftime('%Y-%m-%d')
                elif endpoint.startswith("/api/games/"):
                    data["score"] = f"{random.randint(0, 5)}-{random.randint(0, 5)}"
                    data["location"] = fake.city()
                elif endpoint.startswith("/api/trainings/"):
                    data["name"] = fake.word().capitalize() + " Тренировка"
                elif endpoint.startswith("/api/results/"):
                    data["goalsscored"] = random.randint(0, 10)
                    data["athleteplace"] = random.randint(1, 20)
                elif endpoint.startswith("/api/attendance/"):
                    data["pressrating"] = random.randint(1, 10)
                    data["captainrating"] = random.randint(1, 10)
                elif endpoint.startswith("/api/applications/"):
                    data["status"] = random.choice(['Pending', 'Approved', 'Rejected'])

                # Выполняем PUT запрос
                result = await client.execute_query(endpoint, method, data.copy())
            else:
                print(f"Не удалось получить ID для обновления из {endpoint}")
       
        
        
        elif method == "DELETE":
            # Получаем случайный ID для соответствующей сущности
            random_id = await client.get_random_id(endpoint)
            if random_id:
                # Формируем endpoint с ID
                endpoint += f"{random_id}/"

                # Выполняем DELETE запрос
                result = await client.execute_query(endpoint, method)

                if result:  # Проверяем успешность удаления
                    print(f"Успешно удалена запись с ID {random_id} из {original_endpoint}") # original_endpoint для вывода без id
                else:
                    print(f"Не удалось удалить запись с ID {random_id} из {original_endpoint}")
            else:
                print(f"Не удалось получить ID для удаления из {endpoint}")


        if result is not None:
            print(f"{method} Result: {result}") 
            print("\n\n")
            
        await asyncio.sleep(random.uniform(0.1, 0.2))

async def main():
    try:
        async with AsyncDBClient("http://127.0.0.1:8000") as client:
            # Пример пула запросов
            queries = [
                # GET запросы
                ("GET", "/api/coaches/", {}),
                ("GET", "/api/teams/", {}),
                ("GET", "/api/athletes/", {}),
                ("GET", "/api/tournaments/", {}),
                ("GET", "/api/games/", {}),
                ("GET", "/api/teamsingames/", {}),
                ("GET", "/api/trainings/", {}),
                ("GET", "/api/results/", {}),
                ("GET", "/api/attendance/", {}),
                # # ("GET", "/api/applications/", {}),
                # ("GET", "/api/athletes-in-games/", {}), 
                # ("GET", "/api/trainings-by-team/", {}),
                # ("GET", "/api/athletes-with-tournaments/", {}),
                ("GET", "/api/athletes-trainings/", {}),
                ("GET", "/api/coaches-tournaments/", {}),

                # POST запросы
                ("POST", "/api/coaches/", {}),
                ("POST", "/api/teams/", {}),
                ("POST", "/api/athletes/", {}),
                # ("POST", "/api/tournaments/", {}),
                ("POST", "/api/games/", {}),

                # # PUT запросы
                ("PUT", "/api/coaches/", {}),
                ("PUT", "/api/teams/", {}),
                ("PUT", "/api/athletes/", {}),
                ("PUT", "/api/tournaments/", {}),

                # DELETE запросы
                ("DELETE", "/api/coaches/", {}),
                ("DELETE", "/api/teams/", {}),
                ("DELETE", "/api/athletes/", {}),
                ("DELETE", "/api/tournaments/", {}),
            ]

            weights = [50] * 11  + [25] * 4 + [10] * 4 + [1] * 4  # Веса для запросов
            tasks = [simulate_user_activity(client, queries, weights) for _ in range(5)]  # 5 одновременных пользователей

            await asyncio.wait_for(asyncio.gather(*tasks), timeout=240.0)

    except KeyboardInterrupt:
        print("Программа завершена пользователем.")
    except Exception as e:
        print(f"{e}")
    finally:
        print("Завершение работы...")

if __name__ == "__main__":
    asyncio.run(main())
