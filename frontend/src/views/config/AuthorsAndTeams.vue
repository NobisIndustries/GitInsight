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
            <AuthorsConfig/>
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

export default {
  name: 'AuthorsAndTeamsConfig',
  components: {AuthorsConfig, CardWithHelp},
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
