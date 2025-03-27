<!-- <script setup>
import { ref } from 'vue';
import axios from 'axios';

const requests = ref([]);
const responses = ref([]);
const simulating = ref(false);
let intervalId = null;

const startSimulation = async () => {
  simulating.value = true;
  intervalId = setInterval(async () => {
    try {
      const methods = ['GET', 'POST', 'PUT', 'DELETE'];
      const endpoints = [
                ("GET", "/api/coaches/", {}),
                ("GET", "/api/teams/", {}),
                ("GET", "/api/athletes/", {}),
                ("GET", "/api/tournaments/", {}),
                ("GET", "/api/games/", {}),
                // # ("GET", "/api/teamsingames/", {}),
                ("GET", "/api/trainings/", {}),
                ("GET", "/api/results/", {}),
                ("GET", "/api/attendance/", {}),
                ("GET", "/api/applications/", {}),
                // # ("GET", "/api/athletesfromresults/", {}),
                // # ("GET", "/api/trainings-by-team/", {}),
                // # ("GET", "/api/athletes-in-games/", {}),

                ("POST", "/api/coaches/", {}),
                ("POST", "/api/teams/", {}),
                ("POST", "/api/athletes/", {}),
                ("POST", "/api/tournaments/", {}),
                ("POST", "/api/games/", {}),

                ("PUT", "/api/coaches/", {}),
                ("PUT", "/api/teams/", {}),
                ("PUT", "/api/athletes/", {}),
                ("PUT", "/api/tournaments/", {}),

                ("DELETE", "/api/coaches/", {}),
                ("DELETE", "/api/teams/", {}),
                ("DELETE", "/api/athletes/", {}),
                ("DELETE", "/api/tournaments/", {}),
            ];

      const randomIndex = Math.floor(Math.random() * endpoints.length);
      const [method, endpoint, filters] = endpoints[randomIndex]; // Деструктуризация кортежа

      let url = `http://127.0.0.1:8000${endpoint}`;

      if (method === 'GET' && Object.keys(filters).length > 0) {
        const queryString = Object.keys(filters)
          .map(key => `${key}=${filters[key]}`)
          .join('&');
        url += `?${queryString}`;
      }

      let response;
      if (method === 'GET') {
        response = await axios.get(url);
      } else if (method === 'POST') {
        response = await axios.post(url, {}); // Или данные для POST запроса
      } else if (method === 'PUT') {
        response = await axios.put(url, {});  // Или данные для PUT запроса
      } else if (method === 'DELETE') {
        response = await axios.delete(url);
      }


      requests.value.push(`${method} ${url}`); // Добавляем URL с фильтрами, если есть
      responses.value.push(JSON.stringify(response.data, null, 2));
    } catch (error) {
      console.error('Ошибка при выполнении запроса:', error);
    }
  }, 1000);
};

const stopSimulation = () => {
  simulating.value = false;
  clearInterval(intervalId);
};

const clearLogs = () => {
  requests.value = [];
  responses.value = [];
};
</script>

<template>
  <div>
    <button @click="startSimulation">Start Simulation</button>
    <button @click="stopSimulation" :disabled="!simulating">Stop Simulation</button>
    <button @click="clearLogs">Clear Logs</button>

    <div style="display: flex; margin-top: 20px;">
      <div style="flex: 1; margin-right: 20px; overflow-y: auto; max-height: 600px;">
        <h3>Запросы</h3>
        <ul>
          <li v-for="(request, index) in requests" :key="index">{{ request }}</li>
        </ul>
      </div>
      <div style="flex: 1; overflow-y: auto; max-height: 600px;">
        <h3>Ответы</h3>
        <ul>
          <pre v-for="(response, index) in responses" :key="index"><code>{{ response }}</code></pre>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 8px;
  border: 1px solid #ccc;
  margin-bottom: 5px;
  font-family: monospace;
  white-space: pre-wrap;
}

pre {
  padding: 8px;
  border: 1px solid #ccc;
  margin-bottom: 5px;
  white-space: pre-wrap;
  font-family: monospace;
}

code {
  white-space: pre-wrap;
}
</style> -->