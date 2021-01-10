<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="11" lg="9" xl="7">
        <CardWithHelp
            help_text=""
            class="px-10 pb-5"
        >
          <v-col>
            <div class="card-heading">Manage Users</div>
            <div class="card-subheading">Create a new user</div>
            <SingleUser
                username_init=""
                :permissions_init="new_user_init_permissions"
                :existing_usernames="existing_usernames"
                :is_new_user="true"
                class="user"
                @add="add_user($event)"
            />
            <div class="card-subheading">Modify existing users</div>
            <SingleUser
                v-for="user in available_users"
                :key="user.username"
                :username_init="user.username"
                :permissions_init="user.permissions"
                :can_edit="user.username !== $store.state.auth.username"
                :is_guest_user="user.username === guest_username"
                class="user"
                @update="update_user($event)"
                @delete="delete_user(user.username)"
            />
          </v-col>
        </CardWithHelp>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.user {
  margin-left: 2rem;
}
</style>


<script>
import CardWithHelp from "@/components/commonComponents/CardWithHelp";
import SingleUser from "@/components/configComponents/SingleUser";
import {GUEST_USERNAME} from "@/store/constants";

export default {
  name: 'Users',
  components: {SingleUser, CardWithHelp},
  data() {
    return {
      new_user_init_permissions: {view_analysis: true, edit_contributors: false, edit_all: false},
      guest_username: GUEST_USERNAME,
    };
  },
  computed: {
    available_users() {
      return this.$store.state.config.users;
    },
    existing_usernames() {
      return this.available_users.map(u => u.username);
    },
  },
  methods: {
    load_users() {
      this.$store.dispatch('load_users');
    },
    add_user(data) {
      this.$store.dispatch('add_user', data).then(() => this.load_users());
    },
    update_user(data) {
      this.$store.dispatch('update_user', data).then(() => this.load_users());
    },
    delete_user(username) {
      this.$store.dispatch('delete_user', username).then(() => this.load_users());
    },
  },
  mounted() {
    this.load_users();
  }
}
</script>
