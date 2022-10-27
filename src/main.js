import { createApp } from 'vue';
import './style.css';
import App from './App.vue';
import router from './router/main';
import axios from 'axios';

const app = createApp(App);

axios.defaults.baseURL = import.meta.env.VITE_SERVER_ENPOINT;

app.use(router);

app.mount('#app');