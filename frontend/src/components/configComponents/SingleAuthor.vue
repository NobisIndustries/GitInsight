<template>
  <div>
  <div class="d-flex flex-row align-center">
    <v-btn
    icon
    @click="show_more = !show_more"
    >
      <v-icon>{{ show_more ? 'mdi-chevron-down' : 'mdi-chevron-right' }}</v-icon>
    </v-btn>
    <div class="author-name">
      {{ author_name }}
    </div>
    <div
        class="color-swatch"
        :style="{ background: team_color }"
    ></div>
    <v-autocomplete
        v-model="author_info.team_id"
        :items="available_teams"
        item-text="name"
        item-value="name"
        label="Is in team"
        dense
        class="team-selector"
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
  <div v-show="show_more">
aaa
  </div>
  </div>
</template>

<style scoped>
.author-name {
  width: 15rem;
}

.color-swatch {
  display: inline;
  width: 1rem;
  max-width: 1rem;
  height: 1rem;
  margin: 0.5rem;
  padding: 0;
  border-radius: 1rem;
}

.team-selector {
  max-width: 20rem;
}
</style>

<script>
export default {
  name: 'SingleAuthor',
  props: {
    author_name: String,
    author_info_init: Object,
    available_teams: Array,
  },
  data() {
    return {
      author_info: this.author_info_init,
      show_more: false,
    };
  },
  computed: {
    team_color() {
      for (let team_info of this.available_teams) {
        if (team_info.name === this.author_info.team_id)
          return team_info.color;
      }
      return 'red';
    }
  },
  watch: {
    author_info: {
      handler: function () {
        this.$emit('update', this.author_info);
      },
      deep: true,
    }
  },

}
</script>
