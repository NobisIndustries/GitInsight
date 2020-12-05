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
      <v-row justify="center">
        <v-col cols="12" lg="10">
          <LocVsEditCountsPlot/>
        </v-col>
      </v-row>
    </v-col>
  </v-container>
</template>

<script>
import BranchSelector from "@/components/detailAnalysisComponents/BranchSelector";
import DaysSelector from "@/components/overviewComponents/DaysSelector";
import OverviewTreeMap from "@/components/overviewComponents/treeMap/OverviewTreeMap";
import LocVsEditCountsPlot from "@/components/overviewComponents/locVsEditCountsPlot/LocVsEditCountsPlot";

export default {
  name: "OverviewAnalysis",
  components: {LocVsEditCountsPlot, OverviewTreeMap, DaysSelector, BranchSelector},
  data() {
    return {};
  },
  methods: {
    load_data() {
      this.$store.dispatch('load_count_and_team_of_dirs');
      this.$store.dispatch('load_loc_vs_edit_counts');
    }
  },
  watch: {
    '$store.state.common.current_branch': function () {
      this.load_data();
    },
    '$store.state.overview.last_days': function () {
      this.load_data();
    },
  },
  mounted() {
    if(!this.$store.state.common.current_branch)
      return;  // Branch not set - the loading will be triggered by watch once the BranchSelector has finished loading
    this.load_data();
  },
}
</script>

<style scoped>

</style>