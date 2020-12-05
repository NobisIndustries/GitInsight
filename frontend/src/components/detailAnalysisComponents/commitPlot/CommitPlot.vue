<template>
  <v-card elevation="2" class="pt-3">
    <v-col align="center">
      <div class="text-h5 pb-2">File Operations</div>
      <PlotBySelector
          :options="plot_by_options"
          @change="selected_plot_type = $event"
      ></PlotBySelector>
      <Plotly
          :data="plot_data"
          :layout="plot_layout"
          :display-mode-bar="false"
          @click="select_commit($event)"
      ></Plotly>
    </v-col>
  </v-card>
</template>

<script>
import {Plotly} from 'vue-plotly';
import PlotBySelector from "@/components/commonComponents/PlotBySelector";

export default {
  name: 'CommitPlot',
  components: {
    PlotBySelector,
    Plotly
  },
  data() {
    return {
      selected_plot_type: undefined,
      plot_by_options: [
        {key: 'authors', text: 'Authors'},
        {key: 'files', text: 'Files'},
        {key: 'renames', text: 'Moves & Renames'},
      ],
      clicked_commit_info: null,
      plot_layout: {
        hovermode: 'closest',
        yaxis: {
          automargin: true,
        },
        margin: {
          t: 10,
          b: 30
        }
      }
    };
  },
  methods: {
    select_commit(clicked_points) {
      let point_id = clicked_points.points[0].id;
      let entry_history = this.$store.getters.get_current_entry_history_dataframe;
      let selected_row = entry_history.filter({'index': point_id}).getRow(0);
      this.$store.commit('set_selected_commit_detail_data', selected_row)
    }
  },
  computed: {
    plot_data() {
      let entry_history = this.$store.getters.get_current_entry_history_dataframe;
      if (!entry_history)
        return [];

      const min_size = 2;
      const max_size = 25;
      entry_history = entry_history.withColumn('scale',
          row => min_size + (max_size - min_size) / (Math.pow(row.get('number_affected_files'), 0.5)));
      entry_history = entry_history.withColumn('description',
          row => (`${row.get('author')} (${row.get('team_display_name')})<br>`
              + `${row.get('authored_date_time')}<br>`
              + `Edited files: ${row.get('number_affected_files')}<br>`
              + `Historical file path: ${row.get('new_path')}<br>`
              + `<br>------------<br>`
              + `${word_wrap(row.get('message'))}`.replace('\n', '<br>')));

      const plot_options = {
        'authors': ['author', 'team_display_name', false],
        'files': ['current_path', 'team_display_name', false],
        'renames': ['new_path', 'new_path', true]
      };
      let [y_column, group_by_column, show_lines] = plot_options[this.selected_plot_type];

      return generate_plot_data(entry_history, y_column, group_by_column, show_lines);
    }
  }
}

function generate_plot_data(data_frame, y_column, group_by_column, show_lines) {
  let plot_data = [];
  let groupKey, group;
  for ({groupKey, group} of data_frame.groupBy(group_by_column)) {
    plot_data.push(generate_single_plot_data(group, y_column, groupKey[group_by_column], show_lines));
  }
  return plot_data;
}

function generate_single_plot_data(data_frame, y_column, name, show_lines) {
  return {
    x: data_frame.toArray('authored_date_time'),
    y: data_frame.toArray(y_column),
    ids: data_frame.toArray('index'),
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

function word_wrap(text, break_after_chars = 100) {
  let new_words = [];
  let current_line_length = 0;
  for (let word of text.split(' ')) {
    let word_length = word.length;
    if (current_line_length + word_length > break_after_chars) {
      word = '<br>' + word;
      current_line_length = 0;
    }
    new_words.push(word);
    current_line_length += word_length;
  }
  return new_words.join(' ');
}
</script>
