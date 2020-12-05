<template>
  <v-btn-toggle
      v-model="selected"
      @change="send_change()"
      mandatory
  >
    <v-btn
        small
        v-for="option in options"
        :key="option.key"
    >
      {{ option.text }}
    </v-btn>
  </v-btn-toggle>

</template>


<script>
export default {
  name: 'PlotBySelector',
  props: {
    options: Array
  },
  data() {
    return {
      selected: undefined,
    }
  },
  methods: {
    send_change() {
      this.$emit('change', this.options[this.selected].key);
    }
  }

}
</script>
