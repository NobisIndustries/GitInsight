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
        :disabled="$store.state.history_is_loading || new_path===''"
    >
      Search
    </v-btn>
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
      new_path: ''
    };
  },
  methods: {
    load_entry: function () {
      this.$store.dispatch('load_info_of_entry', this.new_path);
    }
  }
}

</script>
