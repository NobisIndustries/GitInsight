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
        const max_size = 20;
        let marker_scale = new DataFrame({raw: entry_history.toArray('number_affected_files'), scale: [0]})
        marker_scale = marker_scale.map(row => row.set('scale',
            min_size + (max_size - min_size) / (Math.pow(row.get('raw'), 0.5))));
        let plot_data = [{
              x: entry_history.toArray('authored_date_time'),
              y: entry_history.toArray('author'),
              marker: {
                size: marker_scale.toArray('scale'),
              },
              type: "scatter",
              mode: 'markers',
            }];
        return plot_data;
      }
    }
  }

</script>
