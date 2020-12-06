<template>
  <CardWithHelp
    help_text="<p>Your repository as a tree map. It includes two modes:<ul>
               <li><b>Code Ownership</b>: Similar to the operations in the Detail Analysis section, this chart tells you
               which team has the most impact on the contents of a given directory based on the commits of its members.
               If multiple teams have made similar contributions, it will be tagged as 'Inconclusive'.</li>
               <li><b>Edit Frequency</b>: Which parts of the repository are most active? Here you can also switch
               the color dimension between absolute edit counts per directory and the relative amount of edits
               compared to all the edits made in its parent directory..</li></ul></p>
               <p>Only directories are shown, but the metrics are of course based on all included files.
               Too zoom in on a specific directory, simply click it. With the arrow on the top of this chart you can
               zoom out again.</p>"
  >
    <v-col align="center">
      <div class="text-h5 pb-2">Repo Overview</div>
      <PlotBySelector
          :options="plot_by_options"
          @change="selected_plot_type = $event"
      ></PlotBySelector>
      <v-switch
          v-model="show_relative_edit_counts"
          v-show="selected_plot_type === 'counts'"
          label="Color relative edit counts"
          class="switch-small"
          dense
      ></v-switch>
      <v-skeleton-loader
          v-show="$store.state.overview.count_and_team_is_loading"
          type="image"
          class="ma-5"
      ></v-skeleton-loader>
      <Plotly
          v-show="!$store.state.overview.count_and_team_is_loading & $store.state.overview.count_and_team_of_dirs_data !== null"
          :data="plot_data"
          :layout="plot_layout"
          :display-mode-bar="false"
      ></Plotly>
    </v-col>
  </CardWithHelp>
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
import PlotBySelector from "@/components/commonComponents/PlotBySelector";
import CardWithHelp from "@/components/commonComponents/CardWithHelp";

export default {
  name: 'OverviewTreeMap',
  components: {
    CardWithHelp,
    PlotBySelector,
    Plotly
  },
  data() {
    return {
      plot_by_options: [
        {key: 'teams', text: 'Code Ownership'},
        {key: 'counts', text: 'Edit Frequency'},
      ],
      selected_plot_type: undefined,
      show_relative_edit_counts: false,
      plot_layout: {
        margin: {
          t: 30,
          b: 10,
          l: 10,
          r: 10
        }
      }
    };
  },
  computed: {
    plot_data() {
      let treemap_data = this.$store.getters.get_count_and_team_of_dirs_dataframe;
      if (!treemap_data)
        return [];

      const branch = this.$store.state.common.current_branch;

      treemap_data = treemap_data.withColumn('dir_path', row => {
        const dir_path = row.get('dir_path');
        return dir_path ? dir_path : branch;
      });

      treemap_data = treemap_data.withColumn('parent_element', row => {
        const dir_path = row.get('dir_path');
        if (dir_path === branch)
          return '';
        let path_elements = dir_path.split('/');
        if (path_elements.length === 1)
          return branch;
        return path_elements.slice(0, -1).join('/');
      });
      if (this.selected_plot_type === 'teams') {
        return get_plot_data_teams(treemap_data);
      } else {
        return get_plot_data_counts(treemap_data, branch, this.show_relative_edit_counts);
      }
    },
  }
}

function get_plot_data_counts(treemap_data, branch, color_relative) {
  // Convert the data dir_path: edit_count to an array, since we will need to look it up quite a bit when calculating
  // the relative edit count. So O(1) is much better than O(n) when scanning the whole data frame.
  const dir_edit_count_array = treemap_data.select('dir_path', 'edit_count').toArray();
  let dir_edit_count = {};
  for (let row of dir_edit_count_array)
    dir_edit_count[row[0]] = row[1];

  treemap_data = treemap_data.withColumn('relative_edit_count', row => {
    if (row.get('dir_path') === branch)
      return 1;
    return row.get('edit_count') / dir_edit_count[row.get('parent_element')];
  });

  treemap_data = treemap_data.withColumn('text', row => (
        `${(row.get('relative_edit_count') * 100).toFixed(1)}% of edits in parent dir<br>`
        + `Total edit count: ${row.get('edit_count')}`));

  const value_column = color_relative ? 'relative_edit_count' : 'edit_count';
  const colorbar_title = color_relative ? 'Fraction of all<br>edits in parent dir' : 'Total edits'
  return [{
    type: 'treemap',
    maxdepth: 3,
    labels: treemap_data.toArray('dir_path'),
    parents: treemap_data.toArray('parent_element'),
    values: treemap_data.toArray(value_column),
    text: treemap_data.toArray('text'),
    marker: {
      colorscale: 'Greens',
      showscale: true,
      reversescale: true,
      colorbar: {
        title: colorbar_title
      }
    }
  }];
}

function get_plot_data_teams(treemap_data) {
  treemap_data = treemap_data.withColumn('text', row => {
    return (`Most significant team: ${row.get('best_team')}`);
  });

  return [{
    type: 'treemap',
    maxdepth: 3,
    labels: treemap_data.toArray('dir_path'),
    parents: treemap_data.toArray('parent_element'),
    hoverinfo: 'text',
    text: treemap_data.toArray('text'),
    marker: {
      colors: treemap_data.toArray('team_display_color'),
    }
  }];
}
</script>
