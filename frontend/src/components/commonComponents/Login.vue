<template>
  <v-form
      ref="login_form"
      v-if="!$store.state.auth.is_logged_in"
      v-model="form_is_valid"
  >
    <v-text-field
        v-model="username"
        label="Username"
        @input="is_wrong = false"
        autocomplete="off"
        :rules="rules"
    ></v-text-field>
    <v-text-field
        v-model="password"
        label="Password"
        type="password"
        @input="is_wrong = false"
        :rules="rules"
    ></v-text-field>
    <v-fade-transition>
      <v-alert
          type="error"
          outlined
          v-show="is_wrong"
      >The given username/password combination was wrong.
      </v-alert>
    </v-fade-transition>
    <v-btn
        color="primary"
        @click="login"
        type="submit"
        class="float-right"
        :disabled="!form_is_valid"
    >Login
    </v-btn>
  </v-form>
</template>

<style scoped>

</style>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: '',
      password: '',
      is_wrong: false,
      form_is_valid: false,
      rules: [v => !!v || 'Cannot be empty!'],
    };
  },
  methods: {
    login(event) {
      event.preventDefault();

      if (!this.form_is_valid)
        return;

      let response = this.$store.dispatch('login', {username: this.username, password: this.password});
      response.then(
          () => {
            this.username = '';
            this.password = '';
          }
      ).catch(error => {
        if (error.response.status === 401) {
          this.is_wrong = true;
        }
      })
    },
  },
}
</script>
