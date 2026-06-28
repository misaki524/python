import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/monthly' },
  { path: '/monthly', name: 'monthly', component: () => import('../views/MonthlyView.vue') },
  { path: '/weekly', name: 'weekly', component: () => import('../views/WeeklyView.vue') },
  { path: '/annual', name: 'annual', component: () => import('../views/AnnualView.vue') },
  { path: '/income', name: 'income', component: () => import('../views/IncomeView.vue') },
  { path: '/budget', name: 'budget', component: () => import('../views/BudgetView.vue') },
  { path: '/work', name: 'work', component: () => import('../views/WorkView.vue') },
  { path: '/debt', name: 'debt', component: () => import('../views/DebtView.vue') },
  { path: '/analysis', name: 'analysis', component: () => import('../views/AnalysisView.vue') },
  { path: '/import', name: 'import', component: () => import('../views/ImportView.vue') },
  { path: '/settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
