import Vue from 'vue';
import Router from 'vue-router';

const router_options = [
  { path: '/', component: 'Landing' },
  { path: '/details', component: 'DetailAnalysis' },
  { path: '/overview', component: 'OverviewAnalysis' },
  { path: '/config/db_update', component: 'config/DatabaseUpdate', meta: { requiresAuth: true } },
  { path: '/config/authors_and_teams', component: 'config/AuthorsAndTeams', meta: { requiresAuth: true } },
  { path: '/config/security', component: 'config/Security', meta: { requiresAuth: true } },
  { path: '*', component: 'NotFound' }
];

const routes = router_options.map(route => {
  return {
    ...route,
    component: () => import(`../views/${route.component}.vue`)
  };
});

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes
});
