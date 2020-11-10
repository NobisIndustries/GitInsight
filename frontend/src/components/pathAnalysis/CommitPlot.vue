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

  export default {
    name: 'CommitPlot',
    components: {
      Plotly
    },
    data() {
      return {
        layout: {
          hovermode: 'closest',
          yaxis: {
            automargin: true,
          }
        }
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
          return [];

        const min_size = 2;
        const max_size = 25;
        entry_history = entry_history.withColumn('scale',
            row => min_size + (max_size - min_size) / (Math.pow(row.get('number_affected_files'), 0.5)));
        entry_history = entry_history.withColumn('description',
            row => (`${row.get('author')}<br>${row.get('team_display_name')}<br>`
                         + `${row.get('authored_date_time')}<br>------------<br>`
                         + `${row.get('message')}`.replace('\n', '<br>')));

        let plot_data = [];

        let entries_by_teams = entry_history.groupBy('team_display_name');
        let groupKey, group;
        for({groupKey, group} of entries_by_teams) {
          plot_data.push(
              {
                x: group.toArray('authored_date_time'),
                y: group.toArray('author'),
                marker: {
                  size: group.toArray('scale'),
                  color: group.toArray('team_display_color'),
                },
                hoverinfo: 'text',
                hovertext: group.toArray('description'),
                type: "scatter",
                mode: 'markers',
                name: groupKey['team_display_name'],
              }
          );
        }
        return plot_data;
      }
    }
  }

</script>
