<template>
  <v-toolbar-title class="d-flex align-center">
    <router-link
        to="/"
        tag="span"
        style="cursor: pointer"
        class="d-flex align-center"
    >
      <img src="logo.svg" width="30" class="mr-2"/>
      <div class="mr-1 font-weight-thin">GitInsight -</div>
      <input
          type="text"
          v-show="edit_mode"
          class="title-input"
          v-model="title_computed"/>
      <div v-show="!edit_mode">{{ title }}</div>
    </router-link>
    <v-btn
        v-if="can_edit"
        @click="toggle_edit_mode"
        class="ml-2"
        icon
        dark
        x-small
    >
      <v-icon v-if="!edit_mode">mdi-pencil</v-icon>
      <v-icon v-else>mdi-pencil-off</v-icon>
    </v-btn>
  </v-toolbar-title>
</template>

<style scoped>
.title-input {
  border: none;
  border-bottom: 0.02rem solid rgba(255, 255, 255, 0.4);
  color: #ffffff;
  margin: 0;
}

.title-input:focus {
  outline: none;
}
</style>

<script>
export default {
  name: 'EditableTitle',
  props: {
    title: String,
    can_edit: {
      type: Boolean,
      required: false,
      default: true,
    }
  },
  data() {
    return {
      internal_title: null,
      edit_mode: false,
    };
  },
  methods: {
    toggle_edit_mode() {
      if (this.edit_mode)
        this.$emit('update', (this.internal_title ? this.internal_title : this.title));
      this.edit_mode = !this.edit_mode
    },
  },
  computed: {
    title_computed: {
      get() {
        return this.title;
      },
      set(value) {
        this.internal_title = value;
      }
    }
  }
}
</script>
