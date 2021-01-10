<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="11" lg="9" xl="7">
        <CardWithHelp
            help_text="<p>Here you can manage the accounts of your users. There is a default account called
            <b>__GUEST__</b> which represents unauthenticated visitors.</p>
            <p>There are different types of permissions: <ul>
            <li><b>Nothing</b>: The account can not access anything besides the landing page.</li>
            <li><b>View Analysis</b>: The account can view and interact with the analysis section.</li>
            <li><b>Edit Authors & Teams</b>: Like &quotView Analysis&quot, but the account can additionally edit the
            available teams and authors.</li>
            <li><b>Admin</b>: The account can do everything.</li>
            </ul></p>"
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
                :key="new_user_count"
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
          <v-snackbar color="success" v-model="added_user" timeout="2000">Added user</v-snackbar>
          <v-snackbar color="info" v-model="updated_user" timeout="2000">Modified user</v-snackbar>
          <v-snackbar color="warning" v-model="deleted_user" timeout="2000">Deleted user</v-snackbar>
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
      added_user: false,
      updated_user: false,
      deleted_user: false,
      new_user_count: 0,
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
      this.added_user = true;
      this.new_user_count++;
    },
    update_user(data) {
      this.$store.dispatch('update_user', data).then(() => this.load_users());
      this.updated_user = true;
    },
    delete_user(username) {
      this.$store.dispatch('delete_user', username).then(() => this.load_users());
      this.deleted_user = true;
    },
  },
  mounted() {
    this.load_users();
  }
}
</script>
