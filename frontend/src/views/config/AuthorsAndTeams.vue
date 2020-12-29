<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="9" xl="7">
        <CardWithHelp
            help_text=""
        >
          <v-col>
            <div class="card-heading">Author Information</div>
            <AuthorsConfig />
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
  mounted() {
    this.$store.dispatch('load_author_info');
  }
}
</script>
