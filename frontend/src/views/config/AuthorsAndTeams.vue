<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="9" xl="7">
        <CardWithHelp
            help_text=""
        >
          <v-col>
            <div class="card-heading">Author Information</div>
            <v-text-field
                v-model="name_filter"
                label="Filter names"
                clearable
            ></v-text-field>
            <div>
              <SingleAuthor
                  v-for="author_name in currently_displayed_author_names"
                  :author_name="author_name"
                  :author_info="$store.state.config.authors[author_name]"
                  :available_teams="available_teams"
                  :key="author_name"
              />
              <v-pagination
                  v-model="author_page"
                  :length="number_author_pages"
                  total-visible="7"
              ></v-pagination>
            </div>
          </v-col>
        </CardWithHelp>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CardWithHelp from '@/components/commonComponents/CardWithHelp';
import SingleAuthor from "@/components/configComponents/SingleAuthor";

const AUTHORS_PER_PAGE = 10;

export default {
  name: 'AuthorsAndTeamsConfig',
  components: {SingleAuthor, CardWithHelp},
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
      const all_authors = Object.keys(this.$store.state.config.authors);
      if(!this.name_filter)
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
  mounted() {
    this.$store.dispatch('load_teams');
    this.$store.dispatch('load_authors');
  }
}
</script>
