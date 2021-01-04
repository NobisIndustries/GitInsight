<template>
<div>
  <v-navigation-drawer
      v-if="show_sidebar"
      v-model="show_sidebar"
      app>
    <v-list>
      <v-list-item
          v-for="item in menu_items"
          :key="item.title"
          :to="item.path">
        <v-list-item-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-action>
        <v-list-item-content>{{ item.title }}</v-list-item-content>
      </v-list-item>
      <v-list-group
          v-for="item in menu_items_with_sub_items"
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
        <v-list-item>
          <v-switch
              v-model="$vuetify.theme.dark"
              inset
              label="Dark mode"
              persistent-hint
          ></v-switch>
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
        {{ title }}
      </router-link>
    </v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items class="hidden-sm-and-down">
      <v-btn
          v-for="item in menu_items"
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
          v-for="item in menu_items_with_sub_items"
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
          <v-list-item>
            <v-switch
                v-model="$vuetify.theme.dark"
                inset
                label="Dark mode"
                persistent-hint
            ></v-switch>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar-items>
  </v-app-bar>
</div>
</template>

<script>
export default {
  name: 'Navigation',
  props: {
    title: String,
    menu_items: Array,
    menu_items_with_sub_items: Array,
  },
  data() {
    return {
      show_sidebar: false,
    };
  }
}
</script>