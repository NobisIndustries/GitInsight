<template>
  <div>
    <PlotBySelector
        @change="selected_plot_type = $event"
    ></PlotBySelector>
    <Plotly
        :data="plot_data"
        :layout="layout"
        :display-mode-bar="false"
        v-show="show_plot"
    ></Plotly>
  </div>
</template>

<script>
import {Plotly} from 'vue-plotly';
import PlotBySelector from "@/components/pathAnalysis/commitPlot/PlotBySelector";

export default {
  name: 'CommitPlot',
  components: {
    PlotBySelector,
    Plotly
  },
  data() {
    return {
      selected_plot_type: undefined,
      layout: {
        hovermode: 'closest',
        yaxis: {
          automargin: true,
        }
      }
    };
  },
  methods: {},
  computed: {
    show_plot() {
      return this.$store.state.current_entry_history !== null;
    },
    plot_data() {
      let entry_history = this.$store.getters.get_current_entry_history_dataframe;
      if (!entry_history)
        return [];

      const min_size = 2;
      const max_size = 25;
      entry_history = entry_history.withColumn('scale',
          row => min_size + (max_size - min_size) / (Math.pow(row.get('number_affected_files'), 0.5)));
      entry_history = entry_history.withColumn('description',
          row => (`${row.get('author')}<br>${row.get('team_display_name')}<br>`
              + `${row.get('authored_date_time')}<br>------------<br>`
              + `${row.get('message')}`.replace('\n', '<br>')));

      const plot_options = {'authors': ['author', 'team_display_name', false],
                            'files': ['current_path', 'team_display_name', false],
                            'renames': ['new_path', 'new_path', true]};
      let [y_column, group_by_column, show_lines] = plot_options[this.selected_plot_type];

      return generate_plot_data(entry_history, y_column, group_by_column, show_lines);
    }
  }
}

function generate_plot_data(data_frame, y_column, group_by_column, show_lines) {
  let grouped_frame = data_frame.groupBy(group_by_column);
  let plot_data = [];
  let groupKey, group;
  for ({groupKey, group} of grouped_frame) {
    plot_data.push(generate_single_plot_data(group, y_column, groupKey[group_by_column], show_lines));
  }
  return plot_data;
}

function generate_single_plot_data(data_frame, y_column, name, show_lines) {
  return {
    x: data_frame.toArray('authored_date_time'),
    y: data_frame.toArray(y_column),
    marker: {
      size: data_frame.toArray('scale'),
      color: data_frame.toArray('team_display_color'),
    },
    hoverinfo: 'text',
    hovertext: data_frame.toArray('description'),
    type: "scatter",
    mode: (show_lines ? 'markers+lines' : 'markers'),
    name: name,
  }
}
</script>
