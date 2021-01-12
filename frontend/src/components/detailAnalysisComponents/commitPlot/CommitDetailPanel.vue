<template>
  <v-card elevation="2">
    <v-card-text v-if="commit_info_row !== null" class="text-left pa-8">
      <div class="d-flex justify-space-between px-4">
        <div>
          <div>
            {{ commit_info_row.authored_date_time }}
          </div>
          <div class="d-flex mr-5">
            <div>
              <div class="heading-light my-2">
              <span v-if="commit_info_row.person_contact_link === ''">
                {{ commit_info_row.author }}</span>
                <span v-else><a v-bind:href="commit_info_row.person_contact_link" class="mr-1" target="_blank">
                {{ commit_info_row.author }}</a>
              </span>
                <span v-if="commit_info_row.team_contact_link === ''">
                ({{ commit_info_row.team_display_name }})
              </span>
                <span v-else>(<a v-bind:href="commit_info_row.team_contact_link" target="_blank"
                >{{ commit_info_row.team_display_name }}</a>)</span>
              </div>
              <div class="ml-5">
                <div v-if="commit_info_row.person_description !== ''">
                  {{ commit_info_row.person_description }}
                </div>
                <div v-if="commit_info_row.team_description !== ''">
                  {{ commit_info_row.team_description }}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="commit_info_row.person_image_url !== ''">
          <img :src="commit_info_row.person_image_url" alt="Author image" height="100">
        </div>
      </div>
      <v-card
          class="pa-4 mt-4"
          color="rgba(127, 127, 127, 0.12)"
          elevation="0"
      >
        <div class="heading-light">
          {{ commit_info_row.hash.substring(0, 8) }}
          ({{ commit_info_row.number_affected_files }}
          {{ commit_info_row.number_affected_files > 1 ? 'files' : 'file' }} edited)
        </div>
        <div class="small-caption mb-5">
          {{ commit_info_row.hash }}
        </div>
        <div class="ml-5 mb-1 preserve-whitespace low-opacity">{{ commit_info_row.message.trim() }}</div>
      </v-card>
    </v-card-text>
    <v-card-text v-else>
      Click on an entry in the graph above to display more information.
    </v-card-text>
  </v-card>
</template>

<style scoped>
.small-caption {
  font-size: 70%;
  opacity: 0.6;
}

.heading-light {
  font-size: 1.1rem;
  font-weight: 350;
}

.low-opacity {
  opacity: 0.7;
}
</style>

<script>
export default {
  name: 'CommitDetailPanel',
  props: {
    commit_info_row: null
  }

}
</script>