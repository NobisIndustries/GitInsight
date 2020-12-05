<template>
  <v-card elevation="2" class="pt-3">
    <v-col align="center">
      <div class="text-h5 pb-2">Lines of Code and Edit Count</div>
      <v-skeleton-loader
          v-show="$store.state.overview.loc_vs_edict_counts_is_loading"
          type="image"
          class="ma-5"
      ></v-skeleton-loader>
      <Plotly
          v-show="!$store.state.overview.loc_vs_edict_counts_is_loading & $store.state.overview.loc_vs_edict_counts_data !== null"
          :data="plot_data"
          :layout="plot_layout"
          :display-mode-bar="false"
      ></Plotly>
    </v-col>
  </v-card>
</template>

<style scoped>
.switch-small {
  max-width: 15rem;
  transform: scale(0.9);
  margin: 0;
  padding: 0;
  margin-top: 0.5rem;
}
</style>

<script>
import {Plotly} from 'vue-plotly';

export default {
  name: 'LocVsEditCountsPlot',
  components: {
    Plotly
  },
  data() {
    return {
      plot_layout: {
        hovermode: 'closest',
        yaxis: {
          automargin: true,
        },
        margin: {
          t: 10,
          b: 30
        }
      },
    };
  },
  computed: {
    plot_data() {
      let loc_edit_counts_data = this.$store.getters.get_loc_vs_edit_counts_dataframe;
      if (!loc_edit_counts_data)
        return [];

      loc_edit_counts_data = loc_edit_counts_data.withColumn('text', row => (
          `${row.get('current_path')}<br>`
          + `Lines: ${row.get('line_count')}<br>`
          + `Edits: ${row.get('edit_count')}`
      ));

      return [{
        x: loc_edit_counts_data.toArray('line_count'),
        y: loc_edit_counts_data.toArray('edit_count'),
        hoverinfo: 'text',
        hovertext: loc_edit_counts_data.toArray('text'),
        mode: 'markers',
        type: "scatter",
      }];
    },
  }
}

</script>
