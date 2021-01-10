<template>
  <v-app>
    <Navigation
        :menu_items="menu_items"
        :menu_items_with_sub_items="menu_items_with_sub_items"
    />

    <v-main>
      <router-view></router-view>
    </v-main>

  </v-app>
</template>

<script>
import Navigation from "@/components/commonComponents/Navigation";

export default {
  name: 'App',
  components: {Navigation},
  computed: {
    menu_items() {
      let auth = this.$store.state.auth;
      return [
        {title: 'Detail Analysis', path: '/details', icon: 'mdi-chart-scatter-plot', show: auth.view_analysis},
        {title: 'Repo Overview', path: '/overview', icon: 'mdi-chart-tree', show: auth.view_analysis},
      ];
    },
    menu_items_with_sub_items() {
      let auth = this.$store.state.auth;
      return [
        {
          title: 'Configuration', icon: 'mdi-cog', icon_only: true, show: true, children: [
            {title: 'Database Update', path: '/config/db_update', show: auth.edit_all},
            {title: 'Authors and Teams', path: '/config/authors_and_teams', show: auth.edit_contributors},
            {title: 'Security', path: '/config/security', show: auth.edit_all},
          ]
        },
        {
          title: 'User', icon: 'mdi-account-circle', icon_only: true, show: true, children: [
            {title: `Hello ${auth.username}!`, path: '', show: auth.is_logged_in},
            {title: 'Login', path: '/user/login', show: !auth.is_logged_in},
            {title: 'Change Password', path: '/user/change_password', show: auth.is_logged_in},
            {title: 'Logout', path: '/user/logout', show: auth.is_logged_in},
          ]
        },

      ];
    },
  },
  mounted() {
    if (localStorage.getItem('dark_mode') === null)
      localStorage.dark_mode = JSON.stringify(false);
    this.$vuetify.theme.dark = JSON.parse(localStorage.dark_mode);

    this.$store.dispatch('get_current_user');
  },
};
</script>