<template>
  <v-autocomplete
    :value="$store.state.common.current_branch"
    :items="$store.state.common.available_branches"
    @change="switch_branch($event)"
    label="Branches"
  ></v-autocomplete>
</template>

<script>
  export default {
    name: 'BranchSelector',
    methods: {
      switch_branch: function(new_branch) {
        this.$store.commit('set_current_branch', new_branch);
      }
    },
    mounted() {
      if(this.$store.state.common.current_branch)
        return;

      let branches_request = this.$store.dispatch('load_branches');
      branches_request.then(() => {
        let available_branches = this.$store.state.common.available_branches;
        let standard_branch = available_branches[0];
        if (available_branches.indexOf('master') > -1)
          standard_branch = 'master';
        this.$store.commit('set_current_branch', standard_branch);
      });
    },
  }

</script>
