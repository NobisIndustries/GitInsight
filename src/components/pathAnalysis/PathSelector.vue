<template>
  <div>
    <v-autocomplete
      :value="$store.state.current_entry_path"
      :items="$store.state.available_entry_paths_of_current_branch"
      @change="new_path = $event"
      rounded
      filled
      label="Search file or directory..."
    ></v-autocomplete>
    <v-btn
      @click="load_entry()"
      color="primary"
      elevation="2"
      :loading="$store.state.history_is_loading"
      :disabled="$store.state.history_is_loading || new_path===''"
    >
      Search
    </v-btn>
  </div>
</template>

<script>
  export default {
    name: 'PathSelector',
    data() {
      return {
        new_path: ''
      };
    },
    methods: {
      load_entry: function() {
        this.$store.dispatch('load_info_of_entry', this.new_path);
      }
    }
  }

</script>
