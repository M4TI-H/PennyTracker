import './globals.css';
import 'primeicons/primeicons.css'
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue'
import Dashboard from './pages/Dashboard.vue';
import Expenses from './pages/Expenses.vue';
import Savings from './pages/Savings.vue';
import Incomes from './pages/Incomes.vue';

const routes = [
  { path: "/", component: Dashboard},
  { path: "/expenses", component: Expenses},
  { path: "/savings", component: Savings},
  { path: "/incomes", component: Incomes}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

createApp(App).use(router).mount('#app');