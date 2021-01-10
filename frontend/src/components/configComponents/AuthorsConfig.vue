<template>
  <div>
    <div class="d-flex flex-row">
      <v-text-field
          v-model="name_filter"
          label="Filter names"
          @input="author_page = 1"
          clearable
          outlined
          class="mr-5 mt-2"
      ></v-text-field>
      <v-switch
          v-model="only_unknown_filter"
          label="Only show unknown authors"
      ></v-switch>
    </div>
    <div>
      <SingleAuthor
          v-for="author_name in currently_displayed_author_names"
          :author_name="author_name"
          :author_info_init="$store.state.config.authors[author_name]"
          :available_teams="available_teams"
          :key="author_name"
          @update="update_author(author_name, $event)"
      />
      <v-pagination
          v-model="author_page"
          :length="number_author_pages"
          total-visible="7"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import SingleAuthor from "@/components/configComponents/SingleAuthor";
import {UNKNOWN_TEAM_ID} from "@/store/constants";

const AUTHORS_PER_PAGE = 10;

export default {
  name: 'AuthorsConfig',
  components: {SingleAuthor},
  data() {
    return {
      author_page: 1,
      name_filter: '',
      only_unknown_filter: false,
    };
  },
  computed: {
    available_teams() {
      let team_names = Object.keys(this.$store.state.config.teams);
      return team_names.map(name => ({name: name, color: this.$store.state.config.teams[name].team_display_color}));
    },
    available_authors() {
      const all_authors = Object.keys(this.$store.state.config.authors).sort();
      return all_authors.filter(this.determine_author_visibility);
    },
    number_author_pages() {
      return Math.ceil(this.available_authors.length / AUTHORS_PER_PAGE);
    },
    currently_displayed_author_names() {
      let start_index = (this.author_page - 1) * AUTHORS_PER_PAGE;
      let end_index = Math.min(this.available_authors.length, start_index + AUTHORS_PER_PAGE);
      return this.available_authors.slice(start_index, end_index);
    },
  },
  methods: {
    update_author(author_name, author_info) {
      this.$store.commit('update_author_info', {author_name, author_info: author_info});
    },
    determine_author_visibility(author_name) {
      let name_match = true;
      if (this.name_filter)
        name_match = author_name.toLowerCase().indexOf(this.name_filter.toLowerCase()) >= 0;
      let show_unknown_match = true;
      if (this.only_unknown_filter)
        show_unknown_match = this.$store.state.config.authors[author_name].team_id === UNKNOWN_TEAM_ID;
      return name_match && show_unknown_match;
    },
  },
}
</script>
