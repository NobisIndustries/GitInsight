<template>
  <v-app>
    <Navigation
        :title="app_title"
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
  data() {
    return {
      app_title: 'GitInsight',

      menu_items: [
        {title: 'Detail Analysis', path: '/details', icon: 'mdi-chart-scatter-plot'},
        {title: 'Repo Overview', path: '/overview', icon: 'mdi-chart-tree'},
      ],
      menu_items_with_sub_items: [
        {
          title: 'Configuration', icon: 'mdi-cog', children: [
            {title: 'Database Update', path: '/config/db_update'},
            {title: 'Authors and Teams', path: '/config/authors_and_teams'},
            {title: 'Security', path: '/config/security'},
          ]
        },
      ]
    }
  },
};
</script>