import axios from "axios";

import { API_BASE_PATH } from '@/store/constants'
import DataFrame from "dataframe-js";

export const entry_details_store = {
    state: {
        available_entry_paths_of_current_branch: [],
        current_entry_path: '',
        current_entry_history: null,
        selected_commit_detail_data: null,
        history_is_loading: false

    },
    mutations: {
        set_available_entries(state, entry_paths) {
            state.available_entry_paths_of_current_branch = entry_paths;
        },
        set_current_entry_path(state, path) {
            state.current_entry_path = path;
        },
        set_current_entry_history(state, history) {
            state.current_entry_history = history;
        },
        set_selected_commit_detail_data(state, commit_detail_data) {
            state.selected_commit_detail_data = commit_detail_data;
        },
        set_history_is_loading(state, is_loading) {
            state.history_is_loading = is_loading;
        },
        reset_entry_data(state) {
            state.current_entry_history = null;
            state.selected_commit_detail_data = null;
        }
    },
    getters: {
        get_current_entry_history_dataframe(state) {
            // If we simply persisted the already initialized DataFrame in the store and use it in our modules,
            // all mutations would affect the same instance and trigger infinite loops. Even though the dataframe-js
            // doc explicitly states that a DataFrame is immutable...
            let data = state.current_entry_history;
            if(data)
                return new DataFrame(data);
            return null;
        },
    },
    actions: {
        load_available_entry_paths(context) {
            const branch = context.rootState.common.current_branch;
            let url = `${API_BASE_PATH}/entries/availableEntries/${btoa(branch)}`;
            let request = axios.get(url).then(response => {
                let entries = response.data;
                entries.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
                context.commit('set_available_entries', entries);
                context.commit('reset_entry_data');
            });
            return request;
        },
        load_info_of_entry(context, entry_path, limit_results_to) {
            context.commit('set_history_is_loading', true);
            context.commit('set_current_entry_path', entry_path);

            const branch = context.rootState.common.current_branch;
            let url = `${API_BASE_PATH}/entries/history/${btoa(branch)}/${btoa(entry_path)}`;
            let request = axios.get(url, {params: {limit: limit_results_to}}).then(response => {
                context.commit('set_current_entry_history', response.data);
                context.commit('set_history_is_loading', false);
            });
            return request;
        }
    }
};