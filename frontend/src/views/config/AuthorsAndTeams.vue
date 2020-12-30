<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="9" xl="7">
        <CardWithHelp
            help_text=""
            class="px-10 pb-5"
        >
          <v-col>
            <div class="card-heading">Author Information</div>
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
    };
  },
  methods: {
    save() {
      this.$store.dispatch('save_author_info');
    },
  },
  mounted() {
    this.$store.dispatch('load_author_info');
  }
}
</script>
