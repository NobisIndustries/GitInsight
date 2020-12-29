<template>
  <div>
    <v-text-field
        v-model="name_filter"
        label="Filter names"
        @input="author_page = 1"
        clearable
    ></v-text-field>
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

const AUTHORS_PER_PAGE = 10;

export default {
  name: 'AuthorsConfig',
  components: {SingleAuthor},
  data() {
    return {
      author_page: 1,
      name_filter: '',
    };
  },
  computed: {
    available_teams() {
      let team_names = Object.keys(this.$store.state.config.teams);
      return team_names.map(name => ({name: name, color: this.$store.state.config.teams[name].team_display_color}));
    },
    available_authors() {
      const all_authors = Object.keys(this.$store.state.config.authors).sort();
      if (!this.name_filter)
        return all_authors;
      return all_authors.filter(name => (name.toLowerCase().indexOf(this.name_filter.toLowerCase()) >= 0));
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
  },
}
</script>
