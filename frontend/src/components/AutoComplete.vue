<template>
  <div class="autocomplete">
    <v-text-field
        :label="label_text"
        v-model="search"
        @input="on_change()"
        @keydown.down="on_arrow_down()"
        @keydown.up="on_arrow_up()"
        @keydown.enter="on_enter()"
        @focus="on_focus()"
        @blur="on_defocus()"
    ></v-text-field>
    <ul
        v-show="is_open"
        class="autocomplete-results"
    >
      <li
          v-for="(result, i) in results"
          :key="i"
          @click="set_result(result)"
          class="autocomplete-result"
          :class="{ 'is-active': i === arrow_counter }"
          v-html="style_result(result)"
      >
      </li>
    </ul>
  </div>
</template>

<style>
.autocomplete {
  position: relative;
}

.autocomplete-results {
  padding: 0.5rem !important;
  margin: 0.5rem;
  background-color: #ffffff;
  border: 0.02rem solid var(--v-secondary-lighten1);
  overflow: auto;
  position: absolute;
  z-index: 1000;
  width: 100%;
}

.autocomplete-result {
  list-style: none;
  text-align: left;
  padding: 0.5rem;
  cursor: pointer;
}

.autocomplete-result.is-active,
.autocomplete-result:hover {
  background-color: var(--v-primary-lighten3);
}

.autocomplete_highlight {
  font-weight: bold;
  color: var(--v-primary-base);
}
</style>

<script>

export default {
  name: 'AutoComplete',
  props: {
    initial_value: {
      type: String,
      required: false,
      default: '',
    },
    available_elements: {
      type: Array,
      required: false,
      default: () => [],
    },
    min_length: {
      type: Number,
      required: false,
      default: 2,
    },
    label_text: {
      type: String,
      required: false,
      default: '',
    }
  },
  data() {
    return {
      search: this.initial_value,
      results: [],
      is_open: false,
      arrow_counter: 0,
    };
  },
  methods: {
    on_change() {
      if (this.search.length < this.min_length) {
        this.is_open = false;
        return;
      }
      this.is_open = true;
      this.results = filter_elements(this.search, this.available_elements);
    },
    set_result(result) {
      this.search = result;
      this.is_open = false;
    },
    style_result(entry) {
      return style(entry, this.search)
    },
    on_arrow_down() {
      if (this.arrow_counter < this.results.length) {
        this.arrow_counter = this.arrow_counter + 1;
      }
    },
    on_arrow_up() {
      if (this.arrow_counter > 0) {
        this.arrow_counter = this.arrow_counter - 1;
      }
    },
    on_enter() {
      if (!this.is_open)
        return;
      this.search = this.results[this.arrow_counter];
      this.is_open = false;
      this.arrow_counter = 0;
    },
    on_focus() {
      if (this.search.length >= this.min_length)
        this.is_open = true;
    },
    on_defocus() {
      // Wait for a bit before hiding the results window, so that a possible click on a result can be recognized
      setTimeout(() => this.is_open = false, 200);
    },
  },
  watch: {
    search() {
      this.$emit('change', this.search);
    }
  },
}

function filter_elements(search_text, available_elements) {
  search_text = search_text.toLowerCase();
  let match_score = available_elements.map(element => {
    let match_index = element.toLowerCase().indexOf(search_text);
    if (match_index < 0)
      return null;
    return match_index + (element.length - search_text.length);  // Lower is better
  });
  let elements_and_score = zip([available_elements, match_score]);
  elements_and_score = elements_and_score.filter(line => line[1] !== null);
  elements_and_score = elements_and_score.sort((a, b) => a[1] - b[1]);

  return elements_and_score.map(line => line[0]).slice(0, 10);
}

function style(entry, search_text) {
  let regex = new RegExp(search_text, 'gi');
  return entry.replace(regex, match => `<span class="autocomplete_highlight">${match}</span>`);
}

function zip(arrays) {
  return arrays[0].map(function (_, i) {
    return arrays.map(function (array) {
      return array[i]
    })
  });
}
</script>

