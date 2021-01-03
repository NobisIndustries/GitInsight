<template>
  <div>
    <div
        class="color-indicator"
        :style="{background: color}"
        @click="show_picker = !show_picker"
    ></div>
    <div class="overlay" @click="update" v-if="show_picker"></div>
    <v-scroll-x-transition>
      <v-color-picker
          v-model="color"
          v-show="show_picker"
          hide-mode-switch
          mode="hexa"
          class="color-picker"
      ></v-color-picker>
    </v-scroll-x-transition>
  </div>
</template>

<style scoped>
.color-indicator {
  width: 2rem;
  height: 2rem;
  border-radius: 2rem;
}

.color-picker {
  position: absolute;
  margin-top: -1rem;
  margin-left: 2.5rem;
  z-index: 100;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  z-index: 10;
}
</style>

<script>
export default {
  name: 'ColorInput',
  props: {
    value: String,
  },
  data() {
    return {
      color: this.value,
      show_picker: false,
    };
  },
  methods: {
    update() {
      this.$emit('input', this.color);
      this.show_picker = false;
    }
  }
}
</script>
