<template>
  <v-form
      ref="user_form"
      v-model="form_is_valid"
  >
    <v-row class="align-center" no-gutters>
      <div class="field">
        <div v-if="!is_new_user">{{ username }}</div>
        <v-text-field
            v-else
            v-model="username"
            label="New user"
            :rules="username_rules"
            :disabled="!edit_mode"
        ></v-text-field>
      </div>
      <v-text-field
          v-model="new_password"
          v-if="!is_guest_user"
          label="New password"
          type="password"
          :hint="is_new_user ? '' : 'Leave this empty if you do not want to change the password'"
          :rules="password_rules"
          :disabled="!edit_mode"
          class="field"
      ></v-text-field>
      <PermissionsSelector
          v-model="permissions"
          :disabled="!edit_mode"
          class="field"
      />
      <v-btn
          v-if="is_new_user"
          @click="add_user"
          class="mx-2"
          icon
      >
        <v-icon color="success">mdi-plus-circle</v-icon>
      </v-btn>
      <v-btn
          v-if="!is_new_user"
          :disabled="!can_edit"
          @click="toggle_edit_mode"
          class="mx-2"
          icon
      >
        <v-icon v-if="edit_mode" color="primary">mdi-pencil-off</v-icon>
        <v-icon v-else>mdi-pencil</v-icon>
      </v-btn>
      <v-btn
          icon
          :disabled="!can_edit"
          v-if="!is_new_user && !is_guest_user"
          class="delete-button"
          @click="$emit('delete')"
      >
        <v-icon>mdi-trash-can-outline</v-icon>
      </v-btn>
    </v-row>
  </v-form>
</template>

<style scoped>
.field {
  max-width: 15rem;
  min-width: 6rem;
  flex-grow: 1;
  margin-right: 1rem;
}

.delete-button:hover {
  color: var(--v-error-base)
}
</style>

<script>
import PermissionsSelector from "@/components/configComponents/PermissionsSelector";

export default {
  name: 'SingleUser',
  components: {PermissionsSelector},
  props: {
    username_init: String,
    permissions_init: Object,
    existing_usernames: Array,
    can_edit: {
      type: Boolean,
      required: false,
      default: true,
    },
    is_new_user: {
      type: Boolean,
      required: false,
      default: false,
    },
    is_guest_user: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      username: this.username_init,
      permissions: this.permissions_init,
      form_is_valid: false,
      username_rules: [
        v => !!v || 'Username cannot be empty',
        v => this.existing_usernames.indexOf(v) < 0 || 'Username already exists',
        v => v.indexOf(' ') < 0 || 'Username cannot contain spaces'
      ],
      password_rules: [v => (this.is_new_user ? !!v : true) || 'Password cannot be empty'],
      new_password: '',
      edit_mode: this.is_new_user,
    };
  },
  methods: {
    toggle_edit_mode() {
      if (this.edit_mode) {
        this.$emit('update', {
          username: this.username, new_password: this.new_password,
          permissions: this.permissions
        });
        this.new_password = '';
      }
      this.edit_mode = !this.edit_mode;
    },
    add_user() {
      if (!this.form_is_valid)
        return;
      this.$emit('add', {
        username: this.username, new_password: this.new_password,
        permissions: this.permissions
      });
    },
  },
}
</script>

