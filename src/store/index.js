import Vue from 'vue';
import Vuex from 'vuex';

import axios from 'axios';
import DataFrame from "dataframe-js";

Vue.use(Vuex)

let API_BASE_PATH = 'http://127.0.0.1:8000/api'

export default new Vuex.Store({
  state: {
    available_branches: [],
    current_branch: null,

    available_entry_paths_of_current_branch: [],
    current_entry_path: null,
    current_entry_history: null,
    history_is_loading: false

  },
  mutations: {
    set_available_branches(state, branches) {
      state.available_branches = branches;
    },
    set_current_branch(state, branch) {
      state.current_branch = branch;
    },
    set_available_entries(state, entry_paths) {
      state.available_entry_paths_of_current_branch = entry_paths;
    },
    set_current_entry_path(state, path) {
      state.current_entry_path = path;
    },
    set_current_entry_history(state, history) {
      state.current_entry_history = history;
    },
    set_history_is_loading(state, is_loading) {
      state.history_is_loading = is_loading;
    }
  },
  actions: {
    load_branches(context) {
      let request = axios.get(`${API_BASE_PATH}/availableBranches`).then(response => {
        context.commit('set_available_branches', JSON.parse(response.data));
      });
      return request;
    },
    switch_branch(context, new_branch) {
      context.commit('set_current_branch', new_branch);
      
      let url = `${API_BASE_PATH}/availableEntries/${btoa(new_branch)}`;
      let request = axios.get(url).then(response => {
        let entries = JSON.parse(response.data);
        entries.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
        context.commit('set_available_entries', entries);
      });
      return request;
    },
    load_info_of_entry(context, entry_path) {
      context.commit('set_history_is_loading', true);
      context.commit('set_current_entry_path', entry_path);
      
      let url = `${API_BASE_PATH}/history/${btoa(context.state.current_branch)}/${btoa(entry_path)}`;
      let request = axios.get(url).then(response => {
        let df = new DataFrame(JSON.parse(response.data));
        context.commit('set_current_entry_history', df);
        context.commit('set_history_is_loading', false);
      });
      return request;
    }

  },
  modules: {
  }
})
