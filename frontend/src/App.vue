<template>
  <v-app>
    <v-navigation-drawer
        v-if="show_sidebar"
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
        <v-list-group
            v-for="item in menuItemsWithSubItems"
            :key="item.title">
          <template v-slot:activator>
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>{{ item.title }}</v-list-item-content>
          </template>
          <v-list-item
              v-for="subItem in item.children"
              :key="subItem.title"
              :to="subItem.path"
          >
            <v-list-item-title>{{ subItem.title }}</v-list-item-title>
          </v-list-item>
        </v-list-group>
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
            v-for="item in menuItems"
            :key="item.title"
            :to="item.path">
          <v-icon left dark>{{ item.icon }}</v-icon>
          {{ item.title }}
        </v-btn>
        <v-menu
            bottom
            left
            open-on-hover
            offset-y
            v-for="item in menuItemsWithSubItems"
            :key="item.title"

        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                v-bind="attrs"
                v-on="on"
            >
              <v-icon left dark>{{ item.icon }}</v-icon>
              {{ item.title }}
            </v-btn>
          </template>

          <v-list>
            <v-list-item
                v-for="subItem in item.children"
                :key="subItem.title"
                :to="subItem.path"
            >
              <v-list-item-title>{{ subItem.title }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar-items>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>

  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      app_title: 'GitInsight',
      show_sidebar: false,
      menuItems: [
        {title: 'Detail Analysis', path: '/details', icon: 'mdi-chart-scatter-plot'},
        {title: 'Repo Overview', path: '/overview', icon: 'mdi-chart-tree'},
      ],
      menuItemsWithSubItems: [
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