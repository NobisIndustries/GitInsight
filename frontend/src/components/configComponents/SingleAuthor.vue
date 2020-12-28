<template>
  <div class="d-flex flex-row">
    <div class="author-name">
      {{ author_name }}
    </div>
    <v-autocomplete
        :value="author_info.team_id"
        :items="available_teams"
        color="primary"
        label="Belongs to team"
        dense
    ></v-autocomplete>
  </div>
</template>

<style scoped>
.author-name {
  width: 20rem;
}
</style>

<script>
export default {
  name: 'SingleAuthor',
  props: {
    author_name: String,
    author_info: Object,
    available_teams: Array,
  },

}
</script>
