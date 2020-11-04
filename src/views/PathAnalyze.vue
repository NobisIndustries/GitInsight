<template>
  <div>
    Hi there
    <BranchSelector />
    <PathSelector />
    <div>{{$store.state.current_entry_history}}</div>
  </div>
</template>

<script>
import BranchSelector from '@/components/pathAnalysis/BranchSelector.vue'
import PathSelector from '@/components/pathAnalysis/PathSelector.vue'
export default {
  name: 'PathAnalyze',
  components: {
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
}
</script>


