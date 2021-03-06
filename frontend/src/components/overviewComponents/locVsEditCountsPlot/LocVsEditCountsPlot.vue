<template>
  <CardWithHelp
      help_text="<p>This chart correlates the line count of a file with its edit count. Outliers with high line count,
                 high edit count or both will be well visible here.</p>
                 <p>Big source code files can be bad (and more often than not smell like god objects). Big
                 files that are edited often are definitely not good and indicate problems with the application
                 architecture.</p>
                 <p>Oftentimes bigger modules/files/classes tend to be core parts of the application. In a healthy
                 architecture, these core modules should be relatively stable (i.e. changed less often) while change
                 frequency can increase in outer layers where the bulk of new feature development happens.</p>"
  >
    <v-col align="center">
      <div class="card-heading">Edits and Line Counts</div>
        <v-skeleton-loader
            v-show="is_loading"
            type="image"
            class="ma-5"
        ></v-skeleton-loader>
      <div v-show="!is_loading & !has_data">No data found.</div>
      <div v-show="!is_loading & has_data">
        <v-autocomplete
            v-model="selected_file_types"
            :items="available_file_types"
            item-text="file_type"
            item-value="file_type"
            label="Filter file types"
            chips
            multiple
            clearable
            deletable-chips
            small-chips
            class="max-width-input"
        >
          <template v-slot:item="{ item }">
            <v-list-item-content>
              <v-list-item-title v-text="item.file_type"></v-list-item-title>
              <v-list-item-subtitle>{{ item.file_count }} {{ item.file_count > 1 ? 'files' : 'file' }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </template>
        </v-autocomplete>
        <PlotlyGraph
            :data="plot_data"
            :layout="plot_layout"
        ></PlotlyGraph>
      </div>
    </v-col>
  </CardWithHelp>
</template>

<style scoped>
.max-width-input {
  max-width: 30rem;
}
</style>

<script>
import CardWithHelp from "@/components/commonComponents/CardWithHelp";
import PlotlyGraph from "@/components/commonComponents/PlotlyGraph";

export default {
  name: 'LocVsEditCountsPlot',
  components: {
    PlotlyGraph,
    CardWithHelp,
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

      let file_types_by_number = [];
      for (let file_type in file_extension_counts)
        file_types_by_number.push({file_type: file_type, file_count: file_extension_counts[file_type]});

      file_types_by_number.sort((a, b) => b.file_count - a.file_count);
      return file_types_by_number;
    },
    is_loading() {
      return this.$store.state.overview.loc_vs_edict_counts_is_loading;
    },
    has_data() {
      return this.$store.state.overview.loc_vs_edict_counts_data !== null;
    }
  }
}

</script>
