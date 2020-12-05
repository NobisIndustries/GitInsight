<template>
  <v-card elevation="2" class="pt-3">
    <v-col align="center">
      <div class="text-h5 pb-2">Lines of Code vs Edit Count</div>
      <v-autocomplete
          v-model="selected_file_types"
          :items="available_file_types"
          label="Filter file types"
          chips
          multiple
          clearable
          deletable-chips
          small-chips
          class="max-width-input"
      ></v-autocomplete>
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
.max-width-input {
  max-width: 30rem;
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
      selected_file_types: [],
      plot_layout: {
        hovermode: 'closest',
        xaxis: {
          title: 'Lines in File',
        },
        yaxis: {
          title: 'Number of Edits',
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

      const selected_file_types = this.selected_file_types;
      if (selected_file_types.length > 0) {
        loc_edit_counts_data = loc_edit_counts_data.filter(row => (
            selected_file_types.some(type => row.get('current_path').endsWith(type))));
      }

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
    available_file_types() {
      let loc_edit_counts_data = this.$store.getters.get_loc_vs_edit_counts_dataframe;
      if (!loc_edit_counts_data)
        return [];

      let file_extension_counts = {};
      for (let file_path of loc_edit_counts_data.toArray('current_path')) {
        let file_path_items = file_path.split('/');
        let file_name = file_path_items[file_path_items.length - 1];

        let file_name_items = file_name.split('.')
        let file_extension = file_name_items[file_name_items.length - 1];
        if (file_name_items.length > 1)  // we want .py for something like a.py, but not .Dockerfile for Dockerfile
          file_extension = '.' + file_extension;
        if (!(file_extension in file_extension_counts))
          file_extension_counts[file_extension] = 0;
        file_extension_counts[file_extension] += 1;
      }

      let file_types_by_popularity = Object.keys(file_extension_counts).sort(
          (a, b) => {
            return file_extension_counts[b] - file_extension_counts[a]
          });
      return file_types_by_popularity;
    }
  }
}

</script>
