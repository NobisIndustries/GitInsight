<template>
  <v-container fluid>
    <v-tabs
        v-model="active_tab"
        background-color="deep-purple accent-4"
        centered
        dark
    >
      <v-tabs-slider></v-tabs-slider>

      <v-tab key="details_tab">
        Detail Analysis
      </v-tab>

      <v-tab key="overview_tab">
        Overview
      </v-tab>

      <v-tab key="configuration_tab">
        Configuration
      </v-tab>

      <v-tab-item key="details_tab">
        <PathAnalyze/>
      </v-tab-item>
      <v-tab-item key="overview_tab">
        Here is some overview stuff
      </v-tab-item>
      <v-tab-item key="configuration_tab">
        Here is some config stuff
      </v-tab-item>
    </v-tabs>
  </v-container>
</template>

<script>
import PathAnalyze from "@/components/pathAnalysis/PathAnalyze";

export default {
  name: "Main",
  components: {PathAnalyze},
  data() {
    return {
      active_tab: null
    };
  },
}
</script>

<style scoped>

</style>