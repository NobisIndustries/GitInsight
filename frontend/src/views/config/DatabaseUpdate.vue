<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" xl="7">
        <CardWithHelp
            help_text="<p>Configure your update settings here. GitInsight parses all commits and related data to
                       a database to speed up calculations. This database has to be updated regularly with the
                       newest repository data. This update can be triggered:</p><p><ul>
                       <li><b>Manually</b>: Click on the &quotSave & Update now&quot button.</li>
                       <li><b>Periodically</b>: Update at a given time or interval. Specify the time with crontab
                       syntax.</li>
                       <li><b>With webhook</b>: Send a POST request to <i>[gitinsight-url]/api/crawl/update_webhook</i>
                       with body:<br>{&quottoken&quot: &quot[webhook token]&quot}. </li></ul></p>
                       <p>By default you fetch the recent changes from the remote before updating the database -
                       in normal operation there is no need to change that, but you can if you want to test things or
                       provide your own local repo as base. You can also choose if you want
                       to track &quotold&quot branches - e.g. branches that had no commits in a configurable
                       timespan.</p>"
            class="px-10 pb-5"
        >
          <v-col>
            <div class="card-heading">Update Configuration</div>
            <div class="card-subheading">Current Status</div>
            <UpdateProgress class="settings-block"/>
            <div class="card-subheading">Base Settings</div>
            <div class="settings-block">
              <v-switch
                  v-model="crawl_config.update_before_crawl"
                  label="Fetch newest repo version before updating"
              ></v-switch>
              <DaysSelector
                  label="Only track branches with changes in the last"
                  :init_value="crawl_config.limit_tracked_branches_days_last_activity"
                  @change="crawl_config.limit_tracked_branches_days_last_activity = $event"
              />
            </div>
            <div class="card-subheading">Update Trigger Settings</div>
            <div class="settings-block">
              <v-row no-gutters>
                <v-switch
                    v-model="crawl_config.crawl_periodically_active"
                    label="Update periodically"
                    class="inline_switch"
                ></v-switch>
                <v-text-field
                    v-model="crawl_config.crawl_periodically_crontab"
                    :disabled="!crawl_config.crawl_periodically_active"
                    label="Update rate (crontab syntax)"
                    type="text"
                ></v-text-field>
              </v-row>
              <v-row no-gutters>
                <v-switch
                    v-model="crawl_config.webhook_active"
                    label="Update via webhook"
                    class="inline_switch"
                ></v-switch>
                <v-text-field
                    v-model="crawl_config.webhook_token"
                    :disabled="!crawl_config.webhook_active"
                    append-icon="mdi-dice-5-outline"
                    label="Webhook token"
                    type="text"
                    @click:append="get_new_token"
                ></v-text-field>
              </v-row>
            </div>
            <div align="right">
              <v-btn
                  @click="trigger_update"
                  color="primary"
                  class="mr-5"
                  :disabled="$store.state.config.crawl_status.is_crawling"
              >Save & Update now
              </v-btn>
              <v-btn
                  @click="save_config"
              >Save
              </v-btn>
            </div>
          </v-col>
        </CardWithHelp>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.inline_switch {
  width: 14rem;
}

.settings-block {
  margin-left: 2rem;
  margin-bottom: 2rem;
}


</style>

<script>
import axios from "axios";
import {API_BASE_PATH} from '@/store/constants'

import CardWithHelp from "@/components/commonComponents/CardWithHelp";
import DaysSelector from "@/components/commonComponents/DaysSelector";
import UpdateProgress from "@/components/configComponents/UpdateProgress";

export default {
  name: "DatabaseUpdateConfig",
  components: {UpdateProgress, DaysSelector, CardWithHelp},
  data() {
    return {
      crawl_config: {},
    };
  },
  methods: {
    trigger_update() {
      this.save_config().then(() => {
        this.$store.dispatch('update_db');
      });
    },
    save_config() {
      return this.$store.dispatch('save_crawl_config', this.crawl_config);
    },
    get_new_token() {
      axios.get(`${API_BASE_PATH}/crawl/random_token`).then(response => {
        this.crawl_config.webhook_token = response.data;
      });
    }
  },
  mounted() {
    this.$store.dispatch('load_crawl_config').then(() => {
      this.crawl_config = this.$store.state.config.crawl_config;
    });
  },
}
</script>
