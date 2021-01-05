<template>
  <div class="search-box">
    <AutoComplete
        :initial_value="$store.state.entry_details.current_entry_path"
        :available_elements="$store.state.entry_details.available_entry_paths_of_current_branch"
        label_text="Search file or directory..."
        @change="search_change($event)"
        class="flex-grow-0 flex-shrink-1 full-width"
    />
    <v-btn
        @click="load_entry()"
        color="white"
        icon
        :loading="$store.state.entry_details.history_is_loading"
        :disabled="$store.state.entry_details.history_is_loading || new_path === ''"
    >
      <v-icon>mdi-magnify</v-icon>
    </v-btn>
    <v-snackbar
        v-model="is_empty_notification"
        :timeout="6000"
        color="warning"
    >
      No results have been found.
    </v-snackbar>
    <v-snackbar
        v-model="too_many_results_notification"
        :timeout="6000"
        color="warning"
    >
      Found too many results. Only display last {{ limit_results_to }} file changes.
    </v-snackbar>
  </div>
</template>

<style scoped>
.search-box {
  display: flex;
  flex-direction: row;
  align-items: center;

  background: var(--v-accent-base);
  border-radius: 20rem;
  padding-left: 1rem;
}
</style>

<script>
import AutoComplete from "@/components/commonComponents/AutoComplete";

export default {
  name: 'PathSelector',
  components: {
    AutoComplete
  },
  data() {
    return {
      new_path: this.$store.state.entry_details.current_entry_path,
      is_empty_notification: false,
      too_many_results_notification: false,
      limit_results_to: 3000
    };
  },
  methods: {
    search_change({search_term, triggered_from_result_select}) {
      this.new_path = search_term;
      if (triggered_from_result_select)
        this.load_entry();
    },
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
