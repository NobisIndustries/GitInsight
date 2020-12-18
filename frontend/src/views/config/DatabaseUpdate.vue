<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" md="8" xl="7">
        <CardWithHelp
            help_text=""
            class="px-10 pb-5"
        >
          <v-card-title>Update Status</v-card-title>
          <div>
            <v-progress-linear
                :value="$store.state.common.crawl_percentage"
                :color="$store.state.common.is_crawling ? 'primary' : 'grey lighten-1'"
            ></v-progress-linear>
            <v-card-text>
              {{ $store.state.common.crawl_status_message }}
            </v-card-text>
          </div>
          <v-alert
              type="error"
              outlined
              v-show="$store.state.common.crawl_error_message !== ''"
          >
            An error occured while updating:<br>
            {{ $store.state.common.crawl_error_message }}
          </v-alert>
          <v-switch
              v-model="crawl_config.update_before_crawl"
              label="Fetch newest repo version before updating"
          ></v-switch>
          <v-text-field
              v-model="crawl_config.webhook_token"
              append-icon="mdi-dice-5-outline"
              label="Webhook Token"
              type="text"
              @click:append="get_new_token"
          ></v-text-field>
            <DaysSelector
              label="Only track branches with changes in the last"
              :init_value="crawl_config.limit_tracked_branches_days_last_activity"
              @change="crawl_config.limit_tracked_branches_days_last_activity = $event"
            />
          <v-btn
              @click="trigger_update"
              color="primary"
              class="mr-5"
              :disabled="$store.state.common.is_crawling"
          >Save & Update now
          </v-btn>
          <v-btn
              @click="save_config"
          >Save
          </v-btn>
        </CardWithHelp>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import {API_BASE_PATH} from '@/store/constants'

import CardWithHelp from "@/components/commonComponents/CardWithHelp";
import DaysSelector from "@/components/commonComponents/DaysSelector";

export default {
  name: "DatabaseUpdateConfig",
  components: {DaysSelector, CardWithHelp},
  data() {
    return {
      crawl_config: {},
      crawl_updater: null,
    }
  },
  methods: {
    trigger_update() {
      this.save_config().then(() => {
        axios.put(`${API_BASE_PATH}/crawl/update`);
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
    this.crawl_updater = setInterval(() => {
      this.$store.dispatch('load_crawl_status')
    }, 1000);

    this.$store.dispatch('load_crawl_config').then(() => {
      this.crawl_config = this.$store.state.common.crawl_config;
    });
  },
  beforeDestroy() {
    clearInterval(this.crawl_updater);
  }
}
</script>
