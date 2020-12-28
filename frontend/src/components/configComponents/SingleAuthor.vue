<template>
  <div class="d-flex flex-row">
    <div class="author-name">
      {{ author_name }}
    </div>
    <v-autocomplete
        :value="author_info.team_id"
        :items="available_teams"
        item-text="name"
        item-value="name"
        label="Belongs to team"
        dense
    >
      <template v-slot:item="{ item }">
        <v-list-item-content>
          <div
              class="color-swatch"
              :style="{ background: item.color }"
          ></div>
          {{ item.name }}
        </v-list-item-content>
      </template>
    </v-autocomplete>
  </div>
</template>

<style scoped>
.author-name {
  width: 20rem;
}
.color-swatch {
  display: inline;
  max-width: 1rem;
  height: 1rem;
  margin: 0.5rem;
  padding: 0;
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
