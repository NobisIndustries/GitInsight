<template>
  <div>
    <Plotly
        :data="plot_data"
        :layout="layout"
        :display-mode-bar="false"
        v-show="show_plot"
    ></Plotly>
  </div>
</template>

<script>
  import { Plotly } from 'vue-plotly';
  import DataFrame from "dataframe-js";

  export default {
    name: 'CommitPlot',
    components: {
      Plotly
    },
    data() {
      return {
        layout: {}
      };
    },
    methods: {
    },
    computed: {
      show_plot() {
        return this.$store.state.current_entry_history !== null;
      },
      plot_data() {
        let entry_history = this.$store.state.current_entry_history;
        if (!entry_history)
          return {};

        const min_size = 2;
        const max_size = 25;
        entry_history = entry_history.withColumn('scale',
            row => min_size + (max_size - min_size) / (Math.pow(row.get('number_affected_files'), 0.5)));
        entry_history = entry_history.withColumn('description',
            row => `${row.get('author')}<br>${row.get('authored_date_time')}<br>------------<br>${row.get('message')}`.replace('\n', '<br>'));

        let plot_data = [{
              x: entry_history.toArray('authored_date_time'),
              y: entry_history.toArray('author'),
              marker: {
                size: entry_history.toArray('scale'),
              },
              hoverinfo: 'text',
              hovertext: entry_history.toArray('description'),
              type: "scatter",
              mode: 'markers',
            }];
        return plot_data;
      }
    }
  }

</script>
