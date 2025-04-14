<script setup>
import { ref, onMounted } from "vue";

const cities = ref([]);
const selectedCity = ref(null);
const accuracyData = ref(null);

const fetchWeatherData = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/data"); // Flask backend
    const data = await response.json();
    cities.value = data.map(city => city.city_name);
    selectedCity.value = cities.value[0]; // Default selection
    updateAccuracy(selectedCity.value);
  } catch (error) {
    console.error("Error fetching weather data:", error);
  }
};

const updateAccuracy = (cityName) => {
  fetch("http://127.0.0.1:5000/data")
    .then(res => res.json())
    .then(data => {
      accuracyData.value = data.find(city => city.city_name === cityName);
    });
};

onMounted(fetchWeatherData);
</script>

<template>
  <div class="container">
    <h1>Weather API Accuracy</h1>
    
    <label for="city">Select City:</label>
    <select v-model="selectedCity" @change="updateAccuracy(selectedCity)">
      <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
    </select>

    <div v-if="accuracyData" class="accuracy-box">
      <h2>Accuracy for {{ accuracyData.city_name }}</h2>
      <p>📡 OpenWeather: {{ accuracyData.openweather_accuracy_avg.toFixed(2) }} degrees prediction error.</p>
      <p>🌍 WeatherBit: {{ accuracyData.weatherbit_accuracy_avg.toFixed(2) }} degrees prediction error.</p>
      <p>☁️ WeatherAPI: {{ accuracyData.weatherapi_accuracy_avg.toFixed(2) }} degrees prediction error.</p>
    </div>
  </div>
</template>

<style scoped>
.container {
  text-align: center;
  font-family: Arial, sans-serif;
}

.accuracy-box {
  background: #f4f4f4;
  padding: 20px;
  border-radius: 8px;
  display: inline-block;
  margin-top: 20px;
}
</style>
