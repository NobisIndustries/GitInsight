<template>
  <div>
    <v-navigation-drawer
        v-if="show_sidebar"
        v-model="show_sidebar"
        color="dark"
        dark
        app>
      <v-list>
        <v-list-item
            v-for="item in menu_items"
            :key="item.title"
            :to="item.path"
            v-show="item.show"
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>{{ item.title }}</v-list-item-content>
        </v-list-item>
        <v-list-group
            v-for="item in menu_items_with_sub_items"
            :key="item.title"
            v-show="item.show"
        >
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
              v-show="subItem.show"
          >
            <v-list-item-title>{{ subItem.title }}</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="item.title === 'Configuration'">
            <DarkModeSwitch />
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
        app
        color="dark"
        dark
    >
      <span class="hidden-md-and-up">
        <v-app-bar-nav-icon @click="show_sidebar = !show_sidebar">
        </v-app-bar-nav-icon>
      </span>
      <EditableTitle
          :title="$store.state.common.repo_name"
          @update="save_repo_name($event)"
          :can_edit="$store.state.auth.edit_all"
      />
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn
            v-for="item in menu_items"
            :key="item.title"
            :to="item.path"
            v-show="item.show"
            color="dark"
            dark
        >
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
                color="dark"
                dark
                class="nav-button"
                v-show="item.show"
            >
              <v-icon left dark>{{ item.icon }}</v-icon>
              <span v-show="!item.icon_only">{{ item.title }}</span>
            </v-btn>
          </template>

          <v-list>
            <v-list-item
                v-for="subItem in item.children"
                :key="subItem.title"
                :to="subItem.path"
                v-show="subItem.show"
                class="sub-item"
            >
              <v-list-item-title>{{ subItem.title }}</v-list-item-title>
            </v-list-item>
            <v-list-item v-if="item.title === 'Configuration'" class="sub-item">
              <DarkModeSwitch />
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar-items>
    </v-app-bar>
  </div>
</template>

<style scoped>
.sub-item {
  width: 15rem;
}
</style>


<script>
import EditableTitle from "@/components/infoComponents/EditableTitle";
import DarkModeSwitch from "@/components/commonComponents/DarkModeSwitch";

export default {
  name: 'Navigation',
  components: {DarkModeSwitch, EditableTitle},
  props: {
    menu_items: Array,
    menu_items_with_sub_items: Array,
  },
  data() {
    return {
      show_sidebar: false,
    };
  },
  methods: {
    save_repo_name(name) {
      this.$store.commit('set_repo_name', name);
      this.$store.dispatch('save_description');
    },
  },
  mounted() {
    this.$store.dispatch('load_description');
  }
}
</script>