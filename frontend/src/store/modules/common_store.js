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
    }
};