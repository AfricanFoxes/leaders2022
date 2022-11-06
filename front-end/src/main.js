import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router/main';
import axios from 'axios';
// import * as dotenv from 'dotenv';
// dotenv.config();

const app = createApp(App);

axios.defaults.baseURL = 'http://localhost:8080';
// axios.defaults.baseURL = import.meta.env.VITE_api_url;0

app.use(router);

app.mount('#app');