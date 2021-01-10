<template>
  <v-container fluid>
    <v-row justify="center">
      <div class="change-pw-prompt">
        <h1 class="mt-8">Change Password</h1>
        <v-form
            ref="change_pw_form"
            v-if="$store.state.auth.is_logged_in"
            v-model="form_is_valid"
        >
          <v-text-field
              v-model="old_password"
              label="Old password"
              type="password"
              @input="old_pw_is_wrong = false"
              :rules="rules"
          ></v-text-field>
          <v-text-field
              v-model="new_password"
              label="New password"
              type="password"
              :rules="rules"
          ></v-text-field>
          <v-text-field
              v-model="new_password_retyped"
              label="Enter new password again"
              :rules="rules.concat([v => v === new_password  || 'Does not match the new password'])"
              type="password"
          ></v-text-field>

          <v-fade-transition>
            <v-alert
                type="error"
                outlined
                v-show="old_pw_is_wrong"
            >The old password was wrong.
            </v-alert>
          </v-fade-transition>
          <v-btn
              color="primary"
              @click="change_password"
              type="submit"
              class="float-right"
              :disabled="!form_is_valid"
          >Change Password
          </v-btn>

          <v-snackbar
              v-model="success"
              color="success"
          >Password changed!</v-snackbar>

        </v-form>
      </div>
    </v-row>
  </v-container>

</template>

<style scoped>
.change-pw-prompt {
  max-width: 25rem;
  flex-grow: 1;
}
</style>

<script>
export default {
  name: 'ChangePassword',
  data() {
    return {
      old_password: '',
      old_pw_is_wrong: false,
      new_password: '',
      new_password_retyped: '',
      form_is_valid: false,
      rules: [v => !!v || 'Cannot be empty!'],
      success: false,
    };
  },
  methods: {
    change_password(event) {
      event.preventDefault();

      if (!this.form_is_valid)
        return;

      let response = this.$store.dispatch('change_password', {old_password: this.old_password,
        new_password: this.new_password});
      response.then(
          () => {
            this.success = true;

          }
      ).catch(error => {
        if (error.response.status === 406) {
          this.old_pw_is_wrong = true;
        }
      })
    },
  }
}
</script>
