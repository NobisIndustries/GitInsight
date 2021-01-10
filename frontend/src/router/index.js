import Vue from 'vue';
import Router from 'vue-router';

const router_options = [
  { path: '/', component: 'Landing' },
  { path: '/details', component: 'DetailAnalysis' },
  { path: '/overview', component: 'OverviewAnalysis' },
  { path: '/user/login', component: 'user/LoginView' },
  { path: '/user/logout', component: 'user/Logout' },
  { path: '/user/change_password', component: 'user/ChangePassword' },
  { path: '/config/db_update', component: 'config/DatabaseUpdate'},
  { path: '/config/authors_and_teams', component: 'config/AuthorsAndTeams'},
  { path: '/config/users', component: 'config/Users'},
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
