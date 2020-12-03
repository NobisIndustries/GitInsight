import axios from "axios";

import { API_BASE_PATH } from '@/store/constants'

export const common_store = {
    state: {
        available_branches: [],
        current_branch: null,
    },
    mutations: {
        set_available_branches(state, branches) {
            state.available_branches = branches;
        },
        set_current_branch(state, branch) {
            state.current_branch = branch;
        }
    },

    actions: {
        load_branches(context) {
            let request = axios.get(`${API_BASE_PATH}/entries/availableBranches`).then(response => {
                context.commit('set_available_branches', JSON.parse(response.data));
            });
            return request;
        },
        switch_branch(context, new_branch) {
            context.commit('set_current_branch', new_branch);

            let url = `${API_BASE_PATH}/entries/availableEntries/${btoa(new_branch)}`;
            let request = axios.get(url).then(response => {
                let entries = JSON.parse(response.data);
                entries.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));
                context.commit('set_available_entries', entries);
                context.commit('reset_entry_data');
            });
            return request;
        }
    }
};