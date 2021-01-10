<template>
  <div class="pt-5">
    <div class="d-flex flex-row">
      <v-text-field
          v-model="new_team_input"
          :rules="new_team_rules"
          label="Add team"
          placeholder="New team ID"
          hint="This is a unique identifier that cannot be changed afterwards"
          append-icon="mdi-plus-circle"
          @click:append="add_team"
          outlined
          class="team-id-input"
      ></v-text-field>
    </div>
    <SingleTeam
        v-for="team_name in currently_displayed_teams"
        :team_name="team_name"
        :team_info_init="$store.state.config.teams[team_name]"
        :key="team_name"
        @update="update_team(team_name, $event)"
        @delete="delete_team_with_confirmation(team_name)"
    />
    <v-pagination
        v-model="team_page"
        :length="number_team_pages"
        total-visible="7"
    ></v-pagination>
    <v-dialog
        v-model="show_delete_warning"
        persistent
        max-width="500"
    >
      <v-card>
        <v-card-title class="headline">Delete Team?</v-card-title>
        <v-card-text>
          <p>This team has <b>{{ authors_assigned_to_team_to_delete.length }}</b> authors assigned to it.</p>
          <p>If you delete it, these authors will be assigned to the base team "UNKNOWN".</p>
          Affected authors:
          <p class="affected-authors">{{ authors_assigned_to_team_to_delete.join(', ') }}</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="error"
              text
              @click="show_delete_warning = false; delete_team()"
          >
            Delete
          </v-btn>
          <v-btn
              color="secondary"
              text
              @click="show_delete_warning = false"
          >
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.team-id-input {
  width: 15rem;
}

.affected-authors {
  opacity: 0.7;
  font-size: 80%;
}
</style>

<script>
import SingleTeam from "@/components/configComponents/SingleTeam";

const TEAMS_PER_PAGE = 7;

export default {
  name: "TeamsConfig",
  components: {SingleTeam},
  data() {
    return {
      team_page: 1,
      new_team_input: '',
      newly_created_team: null,
      new_team_rules: [
        value => (!this.available_teams.includes(value) || 'This team already exists!'),
      ],

      show_delete_warning: false,
      team_to_delete: null,
      authors_assigned_to_team_to_delete: [],
    };
  },
  computed: {
    available_teams() {
      return Object.keys(this.$store.state.config.teams).sort(this.compare_team_names);
    },
    number_team_pages() {
      return Math.ceil(this.available_teams.length / TEAMS_PER_PAGE);
    },
    currently_displayed_teams() {
      let start_index = (this.team_page - 1) * TEAMS_PER_PAGE;
      let end_index = Math.min(this.available_teams.length, start_index + TEAMS_PER_PAGE);
      return this.available_teams.slice(start_index, end_index);
    },
  },
  methods: {
    compare_team_names(a, b) {
      if (a === this.newly_created_team)
        return -1;
      if (b === this.newly_created_team)
        return 1;
      a = a.toLowerCase();
      b = b.toLowerCase();
      if (a < b)
        return -1;
      if (a > b)
        return 1;
      return 0;
    },
    update_team(team_name, team_info) {
      this.$store.commit('update_team_info', {team_name, team_info});
    },
    add_team() {
      if (!this.new_team_input || this.available_teams.includes(this.new_team_input))
        return;

      let empty_team_info = {
        team_display_name: '',
        team_display_color: random_color(),
        team_description: '',
        team_contact_link: ''
      };
      this.update_team(this.new_team_input, empty_team_info);

      this.newly_created_team = this.new_team_input;
      this.new_team_input = '';
      this.team_page = 1;
    },
    get_authors_in_team(team_name) {
      let authors = []
      for (const [author_name, author_info] of Object.entries(this.$store.state.config.authors)) {
        if (author_info.team_id === team_name)
          authors.push(author_name);
      }
      return authors.sort();
    },
    delete_team_with_confirmation(team_name) {
      this.team_to_delete = team_name;
      this.authors_assigned_to_team_to_delete = this.get_authors_in_team(team_name);
      if (this.authors_assigned_to_team_to_delete.length > 0)
        this.show_delete_warning = true;
      else
        this.delete_team();
    },
    delete_team() {
      this.$store.commit('delete_team', {
        team_name: this.team_to_delete,
        author_names_to_reset: this.authors_assigned_to_team_to_delete
      });
    }
  },
}

function random_color() {  // https://stackoverflow.com/a/1152508
  return '#' + (0x1000000 + (Math.random()) * 0xffffff).toString(16).substr(1, 6);
}
</script>

