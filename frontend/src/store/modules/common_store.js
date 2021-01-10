import axios from "axios";

import {API_BASE_PATH} from '@/store/constants'

export const common_store = {
    state: {
        available_branches: [],
        current_branch: null,

        repo_name: null,
        start_page_text: null,

        app_version: '',
    },
    mutations: {
        set_available_branches(state, branches) {
            state.available_branches = branches;
        },
        set_current_branch(state, branch) {
            state.current_branch = branch;
        },
        set_repo_name(state, name) {
            state.repo_name = name;
        },
        set_start_page_text(state, text) {
            state.start_page_text = text;
        },
        set_app_version(state, version) {
            state.app_version = version;
        }
    },

    actions: {
        load_branches(context) {
            let request = axios.get(`${API_BASE_PATH}/entries/availableBranches`).then(response => {
                context.commit('set_available_branches', response.data);
            });
            return request;
        },
        load_description(context) {
            let request = axios.get(`${API_BASE_PATH}/descriptions/description`).then(response => {
                context.commit('set_repo_name', response.data.repo_name);
                context.commit('set_start_page_text', response.data.start_page_text);
            });
            return request;
        },
        save_description(context) {
            const data = {repo_name: context.state.repo_name, start_page_text: context.state.start_page_text}
            let request = axios.put(`${API_BASE_PATH}/descriptions/description`, data);
            return request;
        },
        load_app_version(context) {
            let request = axios.get(`${API_BASE_PATH}/descriptions/version`).then(response => {
                context.commit('set_app_version', response.data);
            });
            return request;
        }

    },
};
