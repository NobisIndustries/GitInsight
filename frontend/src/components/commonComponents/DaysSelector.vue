<template>
  <div>
    <v-autocomplete
        v-model="selected_option"
        :items="options"
        item-value="value"
        :label="label"
    />
  </div>
</template>

<script>

const OPTION_ALL = 'all';

export default {
  name: 'DaysSelector',
  props: {
    label: String,
    init_value: Number,
  },
  data() {
    return {
      options: [
        {value: 7, text: '1 week'},
        {value: 30, text: '1 month'},
        {value: 90, text: '3 months'},
        {value: 180, text: '6 months'},
        {value: 365, text: '1 year'},
        {value: 365 * 2, text: '2 years'},
        {value: 365 * 3, text: '3 years'},
        {value: OPTION_ALL, text: 'All'}
      ],
    };
  },
  computed: {
    selected_option: {
      get() {
        const last_days = this.init_value;
        if (last_days === null)
          return OPTION_ALL;
        return last_days;
      },
      set(selected) {
        let last_days = selected;
        if (selected === OPTION_ALL)
          last_days = null;
        this.$emit('change', last_days)
      }
    },

  },
}
</script>
