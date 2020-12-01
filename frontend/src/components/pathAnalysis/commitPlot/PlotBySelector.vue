<template>
  <v-btn-toggle
      v-model="selected"
      @change="send_change()"
      mandatory
  >
    <v-btn small>
     Authors
    </v-btn>
    <v-btn small>
      Files
    </v-btn>
    <v-btn small>
      Moves & Renames
    </v-btn>
  </v-btn-toggle>

</template>


<script>
export default {
  name: 'PlotBySelector',
  data() {
    return {
      selected: undefined,
    }
  },
  methods: {
    send_change() {
      const options = {0: 'authors', 1: 'files', 2: 'renames'};
      this.$emit('change', options[this.selected]);
    }
  }

}
</script>
