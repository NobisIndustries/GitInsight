<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="9" xl="7">
        <CardWithHelp
            help_text="<p>Here you can edit the teams/groups that contribute to your repository and to link individual
                       contributors to these teams. Necessary data is always visible, optional metadata can be edited
                       by expanding an entry and is used in the Detail Analysis section.</p>
                       <p><b>Teams</b><br>
                       Each team has a unique, immutable team ID which is used for internal identification. You can
                       edit the actual team name and color that are displayed in the charts.<br>
                       To create a new team, enter the desired ID into the &quotAdd team&quot box and click on the plus
                       on the right. You can also delete teams by clicking on its trash symbol on the right. There is
                       always a backup team called &quotUNKNOWN&quot, which unassigned authors will default to.</p>
                       <p><b>Authors</b><br>
                       Here you can find all authors that ever have contributed to the repository and link each one
                       to a team. New authors will default to team &quotUNKNOWN&quot.</p>"
            class="px-10 pb-5"
        >
          <v-col>
            <div class="card-heading">Available Authors & Teams</div>
            <v-tabs v-model="active_tab" fixed-tabs>
              <v-tab key="author">Edit Authors</v-tab>
              <v-tab key="team">Edit Teams</v-tab>
            </v-tabs>
            <v-tabs-items v-model="active_tab" class="pa-5">
              <v-tab-item key="author"><AuthorsConfig/></v-tab-item>
              <v-tab-item key="team"><TeamsConfig/></v-tab-item>
            </v-tabs-items>
            <div align="right">
              <v-btn
                  @click="save"
                  color="primary"
              >Save
              </v-btn>
              <v-snackbar timeout="2000" color="info" v-model="saved">Saved</v-snackbar>
            </div>
          </v-col>
        </CardWithHelp>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import CardWithHelp from '@/components/commonComponents/CardWithHelp';
import AuthorsConfig from "@/components/configComponents/AuthorsConfig";
import TeamsConfig from "@/components/configComponents/TeamsConfig";

export default {
  name: 'AuthorsAndTeamsConfig',
  components: {TeamsConfig, AuthorsConfig, CardWithHelp},
  data() {
    return {
      active_tab: null,
      saved: false,
    };
  },
  methods: {
    save() {
      this.$store.dispatch('save_author_info');
      this.saved = true;

    },
  },
  mounted() {
    this.$store.dispatch('load_author_info');
  }
}
</script>
