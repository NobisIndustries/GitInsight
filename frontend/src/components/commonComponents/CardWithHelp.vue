<template>
  <v-card elevation="2" class="pt-3">
    <v-tooltip
        left
        color="#333333"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            v-bind="attrs"
            v-on="on"
            fab
            absolute
            icon
            small
            class="tooltip-position"
        >
          <v-icon>mdi-help-circle</v-icon>
        </v-btn>
      </template>
      <div
          class="tooltip-content"
          v-html="help_text"
      >
      </div>
    </v-tooltip>

    <slot></slot>

  </v-card>
</template>

<style scoped>
.tooltip-position {
  right: 1rem;
  top: 1rem;
}
.tooltip-content {
  max-width: 30rem;
}
</style>

<script>
export default {
  name: 'CardWithHelp',
  props: {
    help_text: String,
  }
}
</script>

