<template>
  <div class="d-flex">
    <v-textarea
        v-if="edit_mode"
        label="Markdown text"
        v-model="text_computed"
        outlined
        height="600"
    ></v-textarea>
    <VueMarkdown
        v-else
        linkify
        class="text-justify"
        :key="text"
    >{{ text }}</VueMarkdown>
    <v-btn
        v-if="can_edit"
        @click="toggle_edit_mode"
        class="ml-2"
        icon
    >
      <v-icon v-if="!edit_mode">mdi-pencil</v-icon>
      <v-icon v-else>mdi-pencil-off</v-icon>
    </v-btn>
  </div>
</template>

<style scoped>
</style>

<script>
import VueMarkdown from '@adapttive/vue-markdown'

export default {
  name: 'EditableMarkdown',
  components: {VueMarkdown},
  props: {
    text: String,
    can_edit: {
      type: Boolean,
      required: false,
      default: true,
    }
  },
  data() {
    return {
      internal_text: null,
      edit_mode: false,
    };
  },
  methods: {
    toggle_edit_mode() {
      if (this.edit_mode)
        this.$emit('update', (this.internal_text ? this.internal_text : this.text));
      this.edit_mode = !this.edit_mode
    },
  },
  computed: {
    text_computed: {
      get() {
        return this.text;
      },
      set(value) {
        this.internal_text = value;
      }
    }
  }
}
</script>
