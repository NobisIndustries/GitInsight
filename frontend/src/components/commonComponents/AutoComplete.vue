<template>
  <div class="autocomplete">
    <input
        :placeholder="label_text"
        v-model="search"
        class="autocomplete-input"
        @input="on_change()"
        @keydown.down="on_arrow_down()"
        @keydown.up="on_arrow_up()"
        @keydown.enter="on_enter()"
        @focus="on_focus()"
        autocomplete="off"
    >
    <ul
        v-show="is_open"
        class="autocomplete-results"
        :class="$vuetify.theme.dark ? 'theme--dark' : 'theme--light'"
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
    <div
        v-if="results.length === 0" class="autocomplete-not-found">
      No results found...
    </div>
    </ul>
    <div class="overlay" @click="is_open = false" v-if="is_open"></div>
  </div>
</template>

<style>
.autocomplete {
  position: relative;
  margin: 0.5rem;
}

.autocomplete-input {
  width: 100%;
  color: #ffffff;
}

.autocomplete-input::placeholder {
  color: #ffffff;
  opacity: 0.8;
}

.autocomplete-input:focus {
  outline: none;
}

.autocomplete-results {
  margin-top: 1rem;
  padding: 0.5rem !important;
  border: 0.02rem solid var(--v-accent-lighten1);
  border-radius: 0.3rem;
  overflow: auto;
  position: absolute;
  z-index: 1000;
  width: 100%;
}

.autocomplete-results.theme--light {
  background: #ffffff;
}

.autocomplete-results.theme--dark {
  background: #121212;
}

.autocomplete-result {
  list-style: none;
  text-align: left;
  padding: 0.5rem;
  cursor: pointer;
  border-radius: 0.3rem;
}

.theme--light .autocomplete-result.is-active,
.theme--light .autocomplete-result:hover {
  background-color: var(--v-accent-lighten4);
}
.theme--dark autocomplete-result.is-active,
.theme--dark .autocomplete-result:hover {
  background-color: var(--v-accent-darken4);
}

.autocomplete_highlight {
  font-weight: bold;
  color: var(--v-accent-base);
}

.autocomplete-not-found {
  color: var(--v-accent-lighten3);
  font-size: 85%;
  font-style: italic;
}
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
  z-index: 10;
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
      default: 0,
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
      triggered_from_result_select: false,
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
      this.triggered_from_result_select = true;
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
      this.set_result(this.results[this.arrow_counter]);
      this.arrow_counter = 0;
    },
    on_focus() {
      if (this.search.length >= this.min_length)
        this.on_change();
    },
  },
  watch: {
    search() {
      this.$emit('change', {
            search_term: this.search,
            triggered_from_result_select: this.triggered_from_result_select
          });
      this.triggered_from_result_select = false;
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

