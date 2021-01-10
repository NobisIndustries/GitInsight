<template>
  <CardWithHelp
      help_text="<p>Shows the team ownership of the selected file or directory according to its commit history.</p>
               <p>There are two variants. In the simplest case, the raw edit counts of each team are plotted. A more
               advanced (but more subjective) method weights these edits against each other based on the number of
               affected files of the containing commit (more files are less relevant) as well as the age (older
               commits are less relevant).</p>"
  >
    <v-col align="center">
      <div class="card-heading">Ownership</div>
      <v-skeleton-loader
          v-show="$store.state.entry_details.history_is_loading"
          type="image"
          class="ma-5"
      ></v-skeleton-loader>
      <div class="plot-max-width">
        <PlotlyGraph
            v-show="!$store.state.entry_details.history_is_loading"
            :data="plot_data"
            :layout="plot_layout"
        ></PlotlyGraph>
      </div>
    </v-col>
  </CardWithHelp>
</template>

<style scoped>
.plot-max-width {
  max-width: 900px;
}
</style>

<script>
import CardWithHelp from "@/components/commonComponents/CardWithHelp";
import PlotlyGraph from "@/components/commonComponents/PlotlyGraph";

export default {
  name: 'OwnershipPlot',
  components: {
    PlotlyGraph,
    CardWithHelp,
  },
  data() {
    return {
      plot_layout: {
        width: 900,
        margin: {
          t: 30,
          b: 20,
          l: 10,
          r: 10
        },
        grid: {rows: 1, columns: 2},
        legend: {
          orientation: 'h'
        },
        annotations: [
          {
            font: {size: 14},
            showarrow: false,
            text: 'Raw counts',
            x: 0.195,
            y: 0.5
          },
          {
            font: {size: 14},
            showarrow: false,
            text: 'Weighted',
            x: 0.795,
            y: 0.5
          }
        ]
      }
    };
  },
  computed: {
    plot_data() {
      let entry_history = this.$store.getters.get_current_entry_history_dataframe;
      if (!entry_history)
        return [];
      entry_history = entry_history.sortBy('authored_timestamp');

      const first_commit_relative_weight = 0.6;  // Older commits are less important than newer ones
      const total_entries = entry_history.count();
      let entry_counter = 0;
      entry_history = entry_history.withColumn('weighted', row => {
        entry_counter++;
        let affected_files_weight = 1 / (Math.pow(row.get('number_affected_files'), 0.5));
        let commit_age_weight = (1 - (entry_counter / total_entries)) * first_commit_relative_weight;
        return affected_files_weight * commit_age_weight;
      });

      let grouped_by_team = entry_history.groupBy('team_display_name');
      let normal_values = grouped_by_team.aggregate(sub_df => sub_df.count());
      let weighted_values = grouped_by_team.aggregate(sub_df => sub_df.stat.sum('weighted'));
      let colors = grouped_by_team.aggregate(sub_df => sub_df.getRow(0).get('team_display_color')).toArray('aggregation');
      return [
        {
          values: normal_values.toArray('aggregation'),
          labels: normal_values.toArray('team_display_name'),
          marker: {
            colors: colors,
            line: {
              color: '#ffffff',
              width: 2
            },
          },
          type: 'pie',
          name: 'Raw counts',
          hole: 0.4,
          sort: false,
          domain: {x: [0, 0.49]},
        },
        {
          values: weighted_values.toArray('aggregation'),
          labels: weighted_values.toArray('team_display_name'),
          marker: {
            colors: colors,
            line: {
              color: '#ffffff',
              width: 2
            },
          },
          type: 'pie',
          name: 'Weighted',
          hole: 0.4,
          sort: false,
          domain: {x: [0.51, 1]},
        }
      ];

    }
  }
}
</script>
