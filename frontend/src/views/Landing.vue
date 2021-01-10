<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="7" xl="5">
        <EditableMarkdown
            :text="$store.state.common.start_page_text"
            @update="save_start_page_text($event)"
            class="mt-8"
            :can_edit="$store.state.auth.edit_all"
        />
      </v-col>
    </v-row>
    <div class="app-version">
      GitInsight v{{ $store.state.common.app_version }}
      <v-btn
          href="https://github.com/fabianproductions/GitInsight"
          target="_blank"
          icon
          fab
          small
      >
        <v-icon>mdi-github</v-icon>
      </v-btn>
    </div>
  </v-container>
</template>

<style scoped>
.app-version {
  font-size: 0.9rem;
  opacity: 0.8;
  position: absolute;
  bottom: 0.6rem;
  right: 1rem;
}
</style>

<script>
import EditableMarkdown from "@/components/infoComponents/EditableMarkdown";

export default {
  name: "Landing",
  components: {EditableMarkdown},
  methods: {
    save_start_page_text(text) {
      this.$store.commit('set_start_page_text', text);
      this.$store.dispatch('save_description');
    },
  },
  mounted() {
    this.$store.dispatch('load_description');
    this.$store.dispatch('load_app_version');
  },
}
</script>

<style scoped>

</style>