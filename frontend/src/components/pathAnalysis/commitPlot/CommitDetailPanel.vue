<template>
  <v-card elevation="2">
    <v-card-text v-if="commit_info_row !== null">
      <div>
        {{ commit_info_row.get('authored_date_time') }}
      </div>
      <div class="d-flex">
        <div>
          <div class="text-h5">
        <span v-if="commit_info_row.get('person_contact_link') === ''">
          {{ commit_info_row.get('author') }}</span>
            <span v-else><a v-bind:href="commit_info_row.get('person_contact_link')">
          {{ commit_info_row.get('author') }}</a>
        </span>
            (
            <span v-if="commit_info_row.get('team_contact_link') === ''">
          {{ commit_info_row.get('team_display_name') }}
        </span>
            <span v-else><a v-bind:href="commit_info_row.get('team_contact_link')">
          {{ commit_info_row.get('team_display_name') }}</a>
        </span>
            )
          </div>
          <div class="ml-5">
            <div>
              {{ commit_info_row.get('person_description') }}
            </div>
            <div>
              {{ commit_info_row.get('team_description') }}
            </div>
          </div>
        </div>
        <div v-if="commit_info_row.get('person_image_url') !== ''">
          <img :src="commit_info_row.get('person_image_url')" alt="Author image" width="80">
        </div>
      </div>
      <div class="text-subtitle-1 mt-5">
        {{ commit_info_row.get('hash').substring(0, 8) }}
        ({{ commit_info_row.get('number_affected_files')}}
        {{ commit_info_row.get('number_affected_files') > 1? 'files': 'file'}} affected)
      </div>
      <div class="small-hash">
        {{ commit_info_row.get('hash') }}
      </div>
      <div class="ml-5 preserve-whitespace">{{ commit_info_row.get('message').trim() }}</div>
    </v-card-text>
    <v-card-text v-else>
      Click on an entry in the graph above to display more information.
    </v-card-text>
  </v-card>
</template>

<style scoped>
.preserve-whitespace {
  white-space: pre;
}
.small-hash {
  color: var(--v-secondary-lighten4);
  font-size: 70%;
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