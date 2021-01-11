<template>
  <div>
    <v-progress-linear
        :value="$store.state.config.crawl_status.percentage"
        :color="$store.state.config.crawl_status.is_crawling ? 'primary' : 'grey lighten-1'"
    ></v-progress-linear>
    <div
        class="message-text"
        :class="{'message-text-active': $store.state.config.crawl_status.is_crawling}"
    >
      {{ $store.state.config.crawl_status.status_message }}
    </div>
    <v-alert
        type="error"
        outlined
        v-show="$store.state.config.crawl_status.error_message !== ''"
    >
      An error occured while updating:<br>
      {{ $store.state.config.crawl_status.error_message }}
    </v-alert>
  </div>
</template>

<style scoped>
.message-text {
  font-size: 0.8rem;
  opacity: 0.7;
  margin-top: 0.5rem;
}

.message-text-active {
  color: var(--v-primary-base);
  opacity: 1;
}
</style>

<script>
export default {
  name: 'UpdateProgress',
  data() {
    return {
      crawl_updater: null,
    };
  },
  mounted() {
    this.crawl_updater = setInterval(() => {
      this.$store.dispatch('load_crawl_status')
    }, 1000);
  },
  beforeDestroy() {
    clearInterval(this.crawl_updater);
  }
}
</script>
