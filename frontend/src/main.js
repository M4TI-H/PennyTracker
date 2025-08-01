import './globals.css';
import 'primeicons/primeicons.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue'
import Dashboard from './pages/Dashboard.vue';
import Expenses from './pages/Expenses.vue';
import Savings from './pages/Savings.vue';
import Options from './pages/Options.vue';
import Login from './pages/Login.vue';
import Budget from './pages/Budget.vue';

const routes = [
  { path: "/", component: Dashboard},
  { path: "/expenses", component: Expenses},
  { path: "/savings", component: Savings},
  { path: "/options", component: Options},
  { path: "/login", component: Login},
  { path: "/budget", component: Budget},
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

createApp(App).use(router).mount('#app');