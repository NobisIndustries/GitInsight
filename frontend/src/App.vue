<template>
  <v-app>
    <v-navigation-drawer
        v-model="show_sidebar"
        app>
      <v-list>
        <v-list-item
            v-for="item in menuItems"
            :key="item.title"
            :to="item.path">
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>{{ item.title }}</v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app>
      <span class="hidden-md-and-up">
        <v-app-bar-nav-icon @click="show_sidebar = !show_sidebar">
        </v-app-bar-nav-icon>
      </span>
      <v-toolbar-title>
        <router-link to="/" tag="span" style="cursor: pointer">
          {{ app_title }}
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn
            flat
            v-for="item in menuItems"
            :key="item.title"
            :to="item.path">
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <v-content>
      <router-view></router-view>
    </v-content>

  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      app_title: 'GitInsight',
      show_sidebar: false,
      menuItems: [
        {title: 'Detail Analysis', path: '/details', icon: 'mdi-chart-scatter-plot'},
        {title: 'Repo Overview', path: '/overview', icon: 'mdi-chart-tree'},
        {title: 'Configuration', path: '/configuration', icon: 'mdi-cog'}
      ]
    }
  },
};
</script>
<style>

</style>
