<template>
  <v-container fluid>
    <v-col align="center">
      <v-row justify="center">
        <v-col cols="12" md="6" xl="4">
          <PathSelector/>
        </v-col>
        <v-col cols="12" md="3" xl="2">
          <BranchSelector/>
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
  computed: {
    show_plot() {
      return this.$store.state.entry_details.current_entry_history !== null;
    },
  },
  watch: {
    '$store.state.common.current_branch': function () {
      this.$store.dispatch('load_available_entry_paths');
    },
  },
  mounted() {
    if(!this.$store.state.common.current_branch)
      return;  // Branch not set - the loading will be triggered by watch once the BranchSelector has finished loading
    this.$store.dispatch('load_available_entry_paths');
  }
}
</script>


