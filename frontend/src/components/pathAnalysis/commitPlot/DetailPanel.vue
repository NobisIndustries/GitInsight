<template>
  <v-card
      elevation="2"
      v-if="commit_info_row !== null"
  >
    <v-card-text>
      <div>
        {{ commit_info_row.get('authored_date_time') }}
      </div>
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
      <div class="text-subtitle-1">
        {{ commit_info_row.get('hash') }}
      </div>

      <v-list-item-avatar
          tile
          size="80"
          color="grey"
      ></v-list-item-avatar>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'DetailPanel',
  props: {
    commit_info_row: null
  }

}
</script>

<style scoped>

</style>