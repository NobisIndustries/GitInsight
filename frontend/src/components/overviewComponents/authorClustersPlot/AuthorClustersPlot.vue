<template>
  <CardWithHelp
      help_text="<p>Find out which contributors do similar work. This analysis leverages state of the art unsupervised
      machine learning approaches* to cluster together authors with similar commit patterns (e.g. contributed to
      similar files at similar times). Authors grouped together have most likely the same project priorities, even if
      they do not belong to the same team officially.</p>
      <p>The marker size corresponds to the number of commits the author made in the given time. To get better results,
      authors with less than 10 commits in the given time are filtered out, as well as big commits.</p>
      <p>(* Actually it uses TF-IDF statistics with some UMAP dimensionality reduction sprinkled on top, but that
      sounds less marketable. The interesting thing is that we do not give the algorithm any information about the
      official teams, so its output is only dependent on the intrinsic commit patterns itself.)</p>"
  >
    <v-col align="center">
      <div class="card-heading">Similar Authors</div>
      <v-skeleton-loader
          v-show="is_loading"
          type="image"
          class="ma-5"
      ></v-skeleton-loader>
      <div v-show="!is_loading & !has_data">No data found.</div>
      <PlotlyGraph
          v-show="!is_loading & has_data"
          :data="plot_data"
          :layout="plot_layout"
      ></PlotlyGraph>
    </v-col>
  </CardWithHelp>
</template>

<script>
import CardWithHelp from "@/components/commonComponents/CardWithHelp";
import {PLOTLY_MODE_BAR_BUTTONS_TO_REMOVE} from "@/store/constants";
import PlotlyGraph from "@/components/commonComponents/PlotlyGraph";

export default {
  name: 'AuthorClustersPlot',
  components: {
    PlotlyGraph,
    CardWithHelp,
  },
  data() {
    return {
      selected_file_types: [],
      mode_bar_buttons_to_remove: PLOTLY_MODE_BAR_BUTTONS_TO_REMOVE,
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
        margin: {
          t: 0,
          b: 0,
          l: 0,
          r: 0
        },
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

      let plot_data = [];
      let groupKey, group;
      for ({groupKey, group} of clusters_data.groupBy('team_display_name')) {
        plot_data.push(create_single_plot(groupKey.team_display_name, group));
      }
      return plot_data;
    },
    is_loading() {
      return this.$store.state.overview.author_clusters_is_loading;
    },
    has_data() {
      return this.$store.state.overview.author_clusters_data !== null;
    }
  },
}

function create_single_plot(label, data) {
  return {
    x: data.toArray('x'),
    y: data.toArray('y'),
    hoverinfo: 'text',
    hovertext: data.toArray('text'),
    name: label,
    marker: {
      size: data.toArray('scale'),
      color: data.toArray('team_display_color'),
    },
    mode: 'markers',
    type: "scatter",
  };
}

</script>
