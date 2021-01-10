<template>
  <Plotly
      :data="data"
      :layout="layout_internal"
      :mode-bar-buttons-to-remove="mode_bar_buttons_to_remove"
      :displaylogo="false"
      :show-link="false"
      :display-mode-bar="true"
      @click="$emit('click', $event)"
  ></Plotly>
</template>

<style>
</style>

<script>
import {Plotly} from 'vue-plotly';

export default {
  name: 'PlotlyGraph',
  components: {Plotly},
  props: {
    data: Array,
    layout: Object,
  },
  data() {
    return {
      mode_bar_buttons_to_remove: ['sendDataToCloud', 'autoScale2d', 'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines', 'toImage', 'zoom3d', 'pan3d', 'orbitRotation', 'tableRotation', 'handleDrag3d', 'hoverClosestGeo', 'toggleHover', 'select2d', 'lasso2d'],
    };
  },
  computed: {
    layout_internal() {
      let bg_color = this.$vuetify.theme.dark ? '#1E1E1E' : '#ffffff';
      let base_layout = {
        hovermode: 'closest',
        legend: {
          itemsizing: 'constant',
          yanchor: 'top',
          y: 0.93,
        },
        paper_bgcolor: bg_color,
        plot_bgcolor: bg_color,
      };
      return Object.assign(base_layout, this.layout);
    },
  },
}
</script>

