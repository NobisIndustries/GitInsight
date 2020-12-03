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
            let history = state.current_entry_history;
            if(history)
                return new DataFrame(history);
            return null;
        },
    },
    actions: {
        load_info_of_entry(context, entry_path, limit_results_to) {
            context.commit('set_history_is_loading', true);
            context.commit('set_current_entry_path', entry_path);

            let url = `${API_BASE_PATH}/entries/history/${btoa(context.rootState.common.current_branch)}/${btoa(entry_path)}`;
            let request = axios.get(url, {params: {limit: limit_results_to}}).then(response => {
                context.commit('set_current_entry_history', JSON.parse(response.data));
                context.commit('set_history_is_loading', false);
            });
            return request;
        }
    }
};