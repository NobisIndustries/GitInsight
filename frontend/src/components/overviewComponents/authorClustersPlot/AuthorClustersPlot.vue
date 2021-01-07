<template>
  <CardWithHelp
      help_text="<p>Funky machine learning magic. Use at own risk.</p>"
  >
    <v-col align="center">
      <div class="card-heading">Author Clusters</div>
      <v-skeleton-loader
          v-show="$store.state.overview.author_clusters_is_loading"
          type="image"
          class="ma-5"
      ></v-skeleton-loader>
      <Plotly
          v-show="!$store.state.overview.author_clusters_is_loading & $store.state.overview.author_clusters_data !== null"
          :data="plot_data"
          :layout="plot_layout"
          :display-mode-bar="false"
      ></Plotly>
    </v-col>
  </CardWithHelp>
</template>

<script>
import {Plotly} from 'vue-plotly';
import CardWithHelp from "@/components/commonComponents/CardWithHelp";

export default {
  name: 'AuthorClustersPlot',
  components: {
    CardWithHelp,
    Plotly
  },
  data() {
    return {
      selected_file_types: [],
      plot_layout: {
        hovermode: 'closest',
        xaxis: {
          showgrid: false,
          zeroline: false,
          visible: false,
        },
        yaxis: {
          showgrid: false,
          zeroline: false,
          visible: false,
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: {
          t: 0,
          b: 0
        }
      },
    };
  },
  computed: {
    plot_data() {
      let clusters_data = this.$store.getters.get_author_clusters_dataframe;
      if (!clusters_data)
        return [];

      const min_size = 4;
      clusters_data = clusters_data.withColumn('scale',
          row => (min_size + 0.5 * Math.pow(row.get('commit_count'), 0.5)));

      clusters_data = clusters_data.withColumn('text', row => (
          `${row.get('author')}<br>`
          + `${row.get('team_display_name')}<br>`
          + `${row.get('commit_count')} commits`
      ));

      return [{
        x: clusters_data.toArray('x'),
        y: clusters_data.toArray('y'),
        hoverinfo: 'text',
        hovertext: clusters_data.toArray('text'),
        marker: {
          size: clusters_data.toArray('scale'),
          color: clusters_data.toArray('team_display_color'),
        },
        mode: 'markers',
        type: "scatter",
      }];
    },
  },
}

</script>
