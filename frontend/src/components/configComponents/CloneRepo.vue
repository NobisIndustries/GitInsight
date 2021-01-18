<template>
  <div>
    <v-text-field
        v-model="repo_url"
        label="Repo URL"
        outlined
    ></v-text-field>
    <v-fade-transition>
      <v-alert
          type="error"
          outlined
          v-show="!repo_address_format_valid"
      >You have to use the SSH repo address format (<i>git@...</i>) to use authentication.
      </v-alert>
    </v-fade-transition>
    <v-switch
        v-model="use_deploy_key"
        label="Needs Authentication"
    ></v-switch>
    <v-textarea
        v-model="deploy_key"
        v-show="use_deploy_key"
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
        :disabled="is_cloning || !repo_address_format_valid"
    >Clone
    </v-btn>
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
      use_deploy_key: false,
      is_cloning: false,
    };
  },
  methods: {
    clone_repo() {
      this.is_cloning = true;
      this.$store.dispatch('clone_repo', {repo_url: this.repo_url,
        deploy_key: this.use_deploy_key ? this.deploy_key : ''}).then(
          () => {
            this.is_cloning = false;
            this.$store.dispatch('load_repo_is_cloned');
            this.$store.dispatch('load_description');
          });
    }
  },
  computed: {
    repo_address_format_valid() {
      if(this.use_deploy_key)
        return !this.repo_url.startsWith('https');
      return true
    }
  }
}
</script>
