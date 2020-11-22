<template>
  <div>
    <AutoComplete
        :initial_value="$store.state.current_entry_path"
        :available_elements="$store.state.available_entry_paths_of_current_branch"
        label_text="Search file or directory..."
        @change="new_path = $event"
    />
    <v-btn
        @click="load_entry()"
        color="primary"
        elevation="2"
        :loading="$store.state.history_is_loading"
        :disabled="$store.state.history_is_loading || new_path === ''"
    >
      Search
    </v-btn>
    <v-snackbar
        v-model="is_empty_notification"
        :timeout="6000"
        color="info"
        top
    >
      No results have been found.
    </v-snackbar>
    <v-snackbar
        v-model="too_many_results_notification"
        :timeout="6000"
        color="info"
        top
    >
      Found too many results. Only display last {{ limit_results_to }} file changes.
    </v-snackbar>
  </div>
</template>

<script>
import AutoComplete from "@/components/AutoComplete";

export default {
  name: 'PathSelector',
  components: {
    AutoComplete
  },
  data() {
    return {
      new_path: '',
      is_empty_notification: false,
      too_many_results_notification: false,
      limit_results_to: 3000
    };
  },
  methods: {
    async load_entry() {
      await this.$store.dispatch('load_info_of_entry', this.new_path, this.limit_results_to);

      const entry_history = this.$store.getters.get_current_entry_history_dataframe;
      if (!entry_history) {
        this.is_empty_notification = true;
        return;
      }
      this.too_many_results_notification = entry_history.count() === this.limit_results_to;
    }
  }
}

</script>
