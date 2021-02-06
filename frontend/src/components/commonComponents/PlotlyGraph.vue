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
      let font_color = this.$vuetify.theme.dark ? '#cccccc' : '#000000';

      let base_layout = {
        hovermode: 'closest',
        legend: {
          itemsizing: 'constant',
          font: {
            color: font_color
          }
        },
        paper_bgcolor: bg_color,
        plot_bgcolor: bg_color,
        xaxis: {
          color: font_color,
          tickfont: {
            color: font_color
          },
        },
        yaxis: {
          color: font_color,
          tickfont: {
            color: font_color
          },
        }
      };
      return merge_deep(base_layout, this.layout);
    },
  },
}

function is_object(item) {
  return (item && typeof item === 'object' && !Array.isArray(item));
}

function merge_deep(target, source) {
  let output = Object.assign({}, target);
  if (is_object(target) && is_object(source)) {
    Object.keys(source).forEach(key => {
      if (is_object(source[key])) {
        if (!(key in target))
          Object.assign(output, { [key]: source[key] });
        else
          output[key] = merge_deep(target[key], source[key]);
      } else {
        Object.assign(output, { [key]: source[key] });
      }
    });
  }
  return output;
}
</script>

