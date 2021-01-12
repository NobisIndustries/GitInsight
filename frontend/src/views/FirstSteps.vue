<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="7" xl="5">
        <h1 class="mt-6">First steps</h1>
        <div class="mb-6">Welcome to GitInsight! To initialize it with your repository, we have to do a few simple
          steps...
        </div>
        <v-stepper v-model="step_number">
          <v-stepper-header>
            <v-stepper-step :complete="step_number > 1" step="1">Login</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step :complete="step_number > 2" step="2">Clone Repo</v-stepper-step>
            <v-divider></v-divider>
            <v-stepper-step step="3">Update Database</v-stepper-step>
          </v-stepper-header>
          <v-stepper-items>
            <v-stepper-content step="1" class="">
              <h2 class="mt-4">Login</h2>

              <v-card-text class="mb-4">Login with an admin account. If you do not have an admin account and have
                started GitInsight for the very first time, credentials for a base admin account can be found
                in the application log.<br>
                If you cannot find it in the log, go to your mounted directory or volume, delete configs/users.json
                and restart the app.
              </v-card-text>
              <div class="full-width d-flex justify-center">
                <Login class="login flex-grow-1"/>
              </div>
            </v-stepper-content>

            <v-stepper-content step="2">
              <h2 class="mt-4">Clone Repo</h2>

              <v-card-text class="mb-4">Now it's time to clone your repository!</v-card-text>
              <div class="full-width d-flex justify-center">
                <CloneRepo class="flex-grow-1 mx-4 mb-5"/>
              </div>
            </v-stepper-content>

            <v-stepper-content step="3">
              <h2 class="mt-4">Update Database for first usage</h2>

              <v-card-text class="mb-4">GitInsight caches all commits and related information into a database.
                Now it is initialized for the first time. Depending on the repository size, this may take a while -
                but database updates after that will be much faster.
              </v-card-text>
              <div class="full-width d-flex justify-center">
                <UpdateProgress class="flex-grow-1 mx-4 mb-5" />
              </div>
            </v-stepper-content>
            <v-stepper-content step="4">
              <h1 class="mt-4 text-center">Finished!</h1>

              <v-card-text class="mb-4">Congrats, everything is ready now! Click <router-link to="/">here</router-link>
                or on the big GitInsight logo on the top left corner of this site to get to the main page.
              </v-card-text>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.login {
  max-width: 25rem;
}
</style>

<script>
import Login from "@/components/commonComponents/Login";
import CloneRepo from "@/components/configComponents/CloneRepo";
import UpdateProgress from "@/components/configComponents/UpdateProgress";

export default {
  name: 'FirstSetup',
  components: {UpdateProgress, CloneRepo, Login},
  data() {
    return {};
  },
  computed: {
    step_number() {
      if (!this.$store.state.auth.edit_all)
        return 1;
      if (!this.$store.state.common.repo_is_cloned)
        return 2;
      if (this.$store.state.config.crawl_status.is_crawling)
        return 3;
      return 4;
    },
  },
  mounted() {
    this.$store.dispatch('load_repo_is_cloned');
  }
}
</script>

