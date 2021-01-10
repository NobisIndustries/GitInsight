<template>
  <v-container fluid>
    <v-row justify="center">
      <div class="change-pw-prompt">
        <h1 class="mt-8">Login</h1>
        <Login/>
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
import Login from "@/components/commonComponents/Login";

export default {
  name: 'LoginView',
  components: {Login},
  watch: {
    '$store.state.auth.is_logged_in': function (value) {
      if (value)
        this.$router.push('/');
    }
  }
}
</script>