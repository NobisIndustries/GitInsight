<template>
  <div>
    <v-autocomplete
        v-model="selected_option"
        :items="options"
        item-value="value"
        @change="on_select_change"
        label="Limit edits to last"
    />
  </div>
</template>

<script>

const OPTION_ALL = 'all';

export default {
  name: 'DaysSelector',
  data() {
    return {
      options: [
        {value: 7, text: '1 week'},
        {value: 30, text: '1 month'},
        {value: 90, text: '3 months'},
        {value: 365, text: '1 year'},
        {value: 365 * 3, text: '3 years'},
        {value: OPTION_ALL, text: 'All'},
      ],
      selected_option: this.map_last_days_to_selected_option(),
    };
  },
  methods: {
    map_last_days_to_selected_option() {
      const last_days = this.$store.state.overview.last_days;
      if (last_days === null)
        return OPTION_ALL;
      return last_days;
    },
    on_select_change() {
      let last_days = this.selected_option;
      if (this.selected_option === OPTION_ALL)
        last_days = null;
      this.$store.commit('set_last_days', last_days);
    }
  }

}
</script>
