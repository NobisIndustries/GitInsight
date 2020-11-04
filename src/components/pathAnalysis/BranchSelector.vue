<template>
  <v-select
    :value="$store.state.current_branch"
    :items="$store.state.available_branches"
    @change="switch_branch($event)"
    label="Branches"
  ></v-select>
</template>

<script>
  export default {
    name: 'BranchSelector',
    methods: {
      switch_branch: function(new_branch) {
        this.$store.dispatch('switch_branch', new_branch);
      }
    }
  }

</script>
