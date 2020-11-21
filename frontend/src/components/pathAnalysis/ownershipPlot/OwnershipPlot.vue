<template>
  <div>
    <Plotly
        :data="plot_data"
        :layout="plot_layout"
        :display-mode-bar="false"
    ></Plotly>
  </div>
</template>

<style scoped>

</style>

<script>
import {Plotly} from 'vue-plotly';

export default {
  name: 'OwnershipPlot',
  components: {
    Plotly
  },
  data() {
    return {
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
              width: 3
            },
          },
          type: 'pie',
          name: 'Raw counts',
          hole: 0.5,
          direction: 'clockwise',
          sort: false,
          domain: {x: [0.15, 0.85], y: [0.15, 0.85]},
        },
        {
          values: weighted_values.toArray('aggregation'),
          labels: weighted_values.toArray('team_display_name'),
          marker: {
            colors: colors,
            line: {
              color: '#ffffff',
              width: 3
            },
          },
          type: 'pie',
          name: 'Weighted',
          hole: 0.7,
          direction: 'clockwise',
          sort: false,
        }
      ];

    }
  }
}
</script>
