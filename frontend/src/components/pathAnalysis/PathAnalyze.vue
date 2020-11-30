<template>
  <v-col>
    <v-row justify="center">
      <v-col cols="12" md="3">
        <BranchSelector/>
      </v-col>
      <v-col cols="12" md="6" xl="5">
        <PathSelector/>
      </v-col>
    </v-row>
    <div v-show="show_plot">
    <CommitPlot/>
    <v-row align="start" align-self="stretch">
      <v-col cols="12" md="6">
        <CommitDetailPanel
            :commit_info_row="$store.state.selected_commit_detail_data"
        />
      </v-col>
      <v-col cols="12" md="6">
        <OwnershipPlot/>
      </v-col>
    </v-row>
    </div>
  </v-col>
</template>

<script>
import BranchSelector from '@/components/pathAnalysis/BranchSelector.vue';
import PathSelector from '@/components/pathAnalysis/PathSelector.vue';
import CommitPlot from "@/components/pathAnalysis/commitPlot/CommitPlot";
import OwnershipPlot from "@/components/pathAnalysis/ownershipPlot/OwnershipPlot";
import CommitDetailPanel from "@/components/pathAnalysis/commitPlot/CommitDetailPanel";

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
      let available_branches = this.$store.state.available_branches;
      let standard_branch = available_branches[0];
      if (available_branches.indexOf('master') > -1)
        standard_branch = 'master';
      this.$store.dispatch('switch_branch', standard_branch);
    });
  },
  computed: {
    show_plot() {
      return this.$store.state.current_entry_history !== null;
    },
  }
}
</script>


