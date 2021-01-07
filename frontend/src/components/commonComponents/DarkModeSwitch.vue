<template>
  <v-switch
      v-model="$vuetify.theme.dark"
      inset
      label="Dark mode"
      @change="write_to_local_storage"
  ></v-switch>
</template>

<style scoped>

</style>

<script>
export default {
  name: 'DarkModeSwitch',
  methods: {
    write_to_local_storage() {
      localStorage.dark_mode = JSON.stringify(this.$vuetify.theme.dark);
    },
  }
}
</script>
