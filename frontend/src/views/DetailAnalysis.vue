<template>
  <v-container fluid>
    <v-col align="center">
      <v-row justify="center">
        <v-col cols="12" md="3">
          <BranchSelector/>
        </v-col>
        <v-col cols="12" md="6" xl="5">
          <PathSelector/>
        </v-col>
      </v-row>
      <div v-show="show_plot">
        <v-row justify="center">
          <v-col cols="12" lg="10">
            <CommitPlot/>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col cols="12" md="5" lg="4">
            <CommitDetailPanel
                :commit_info_row="$store.state.entry_details.selected_commit_detail_data"
            />
          </v-col>
          <v-col cols="12" md="7" lg="6">
            <OwnershipPlot/>
          </v-col>
        </v-row>
      </div>
    </v-col>
  </v-container>
</template>

<script>
import BranchSelector from '@/components/detailAnalysisComponents/BranchSelector.vue';
import PathSelector from '@/components/detailAnalysisComponents/PathSelector.vue';
import CommitPlot from "@/components/detailAnalysisComponents/commitPlot/CommitPlot";
import OwnershipPlot from "@/components/detailAnalysisComponents/ownershipPlot/OwnershipPlot";
import CommitDetailPanel from "@/components/detailAnalysisComponents/commitPlot/CommitDetailPanel";

export default {
  name: 'PathAnalyze',
  components: {
    CommitDetailPanel,
    OwnershipPlot,
    CommitPlot,
    BranchSelector,
    PathSelector
  },
  mounted() {
    let branches_request = this.$store.dispatch('load_branches');
    branches_request.then(() => {
      let available_branches = this.$store.state.common.available_branches;
      let standard_branch = available_branches[0];
      if (available_branches.indexOf('master') > -1)
        standard_branch = 'master';
      this.$store.dispatch('switch_branch', standard_branch);
    });
  },
  computed: {
    show_plot() {
      return this.$store.state.entry_details.current_entry_history !== null;
    },
  }
}
</script>


