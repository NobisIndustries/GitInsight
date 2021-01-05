<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" lg="7" xl="5">
        <EditableMarkdown
            :text="$store.state.common.start_page_text"
            @update="save_start_page_text($event)"
            class="mt-8"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

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
  }
}
</script>

<style scoped>

</style>