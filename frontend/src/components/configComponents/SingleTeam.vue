<template>
  <div>
    <div class="d-flex flex-row align-center">
      <v-btn
          icon
          @click="show_more = !show_more"
      >
        <v-icon>{{ show_more ? 'mdi-chevron-down' : 'mdi-chevron-right' }}</v-icon>
      </v-btn>
      <ColorInput v-model="team_info.team_display_color" class="mr-4 ml-1"/>
      <div class="team-name">
        {{ team_name }}
      </div>
      <v-text-field
          v-model="team_info.team_display_name"
          label="Actual team name"
          hint="This name is used in the analysis charts"
          class="team-display-name"
      ></v-text-field>
      <v-btn
          icon
          :disabled="!deletable"
          class="delete-button"
          @click="$emit('delete')"
      >
        <v-icon>mdi-trash-can-outline</v-icon>
      </v-btn>
    </div>
    <div v-show="show_more" class="details">
      <v-text-field
          v-model="team_info.team_description"
          label="Description"
          placeholder="Add optional free text here"
          dense
      ></v-text-field>
      <v-text-field
          v-model="team_info.team_contact_link"
          label="Contact link"
          placeholder="Mail, website, chat, ..."
          dense
      ></v-text-field>
    </div>

  </div>
</template>

<style scoped>
.team-name {
  width: 15rem;
}
.team-display-name {
  width: 15rem;
}

.details {
  margin-left: 3rem;
  padding-left: 1rem;
  border-left: 0.02rem solid #ccc;
  width: 30rem;
  margin-right: 1rem;
  margin-bottom: 1rem;
  padding-top: 1rem;
}
.delete-button:hover {
  color: var(--v-error-base)
}
</style>

<script>
import ColorInput from "@/components/configComponents/ColorInput";
import {UNKNOWN_TEAM_ID} from "@/store/constants";

export default {
  name: 'SingleTeam',
  components: {ColorInput},
  props: {
    team_name: String,
    team_info_init: Object,
  },
  data() {
    let team_info = this.team_info_init;
    if (!team_info.team_display_name)
      team_info.team_display_name = this.team_name;

    return {
      team_info: this.team_info_init,
      show_more: false,
    };
  },
  computed: {
    deletable() {
      return this.team_name !== UNKNOWN_TEAM_ID;
    },
  },
  watch: {
    team_info: {
      handler: function () {
        this.$emit('update', this.team_info);
      },
      deep: true,
    }
  },
}
</script>
