<template>
  <v-container fluid>
    <v-col align="center">
      <v-row justify="center">
        <v-col cols="12" md="3">
          <BranchSelector/>
        </v-col>
        <v-col cols="12" md="3">
          <DaysSelector/>
        </v-col>
      </v-row>
      <v-row justify="center">
        <v-col cols="12" lg="10">
        <OverviewTreeMap/>
        </v-col>
      </v-row>
    </v-col>
  </v-container>
</template>

<script>
import BranchSelector from "@/components/detailAnalysisComponents/BranchSelector";
import DaysSelector from "@/components/overviewComponents/DaysSelector";
import OverviewTreeMap from "@/components/overviewComponents/treeMap/OverviewTreeMap";

export default {
  name: "OverviewAnalysis",
  components: {OverviewTreeMap, DaysSelector, BranchSelector},
  data() {
    return {};
  },
  watch: {
    '$store.state.common.current_branch': function () {
      this.$store.dispatch('load_count_and_team_of_dirs');
    },
    '$store.state.overview.last_days': function () {
      this.$store.dispatch('load_count_and_team_of_dirs');
    }
  }
}
</script>

<style scoped>

</style>