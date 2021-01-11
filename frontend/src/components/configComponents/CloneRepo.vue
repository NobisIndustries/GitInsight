<template>
  <div>
    <v-text-field
        v-model="repo_url"
        label="Repo URL"
        outlined
    ></v-text-field>
    <v-switch
        v-model="show_deploy_key"
        label="Needs Authentication"
    ></v-switch>
    <v-textarea
        v-model="deploy_key"
        v-show="show_deploy_key"
        filled
        label="Deploy key"
        hint="A private deploy key for your repo without password"
    ></v-textarea>
    <v-fade-transition>
      <v-alert
          type="error"
          outlined
          v-show="$store.state.config.clone_result.error_msg !== '' && !is_cloning"
      >Something went wrong:<br>{{ $store.state.config.clone_result.error_msg }}
      </v-alert>
    </v-fade-transition>
    <v-btn
        color="primary"
        @click="clone_repo"
        class="float-right"
        :loading="is_cloning"
        :disabled="is_cloning"
    >Clone</v-btn>
  </div>
</template>

<style scoped>

</style>

<script>
export default {
  name: 'CloneRepo',
  data() {
    return {
      repo_url: '',
      deploy_key: '',
      show_deploy_key: false,
      is_cloning: false,
    };
  },
  methods: {
    clone_repo() {
      this.is_cloning = true;
      this.$store.dispatch('clone_repo', {repo_url: this.repo_url, deploy_key: this.deploy_key}).then(
          () => {
            this.is_cloning = false;
            if (this.$store.state.config.clone_result)
              this.$store.dispatch('update_db');

            this.$store.dispatch('load_repo_is_cloned');
          });

    }
  }
}
</script>
