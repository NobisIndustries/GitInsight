import axios from "axios";

import {API_BASE_PATH} from '@/store/constants'

export const common_store = {
    state: {
        available_branches: [],
        current_branch: null,

        is_crawling: false,
        crawl_percentage: 0,
        crawl_status_message: '',
        crawl_error_message: '',

        crawl_config: {},
    },
    mutations: {
        set_available_branches(state, branches) {
            state.available_branches = branches;
        },
        set_current_branch(state, branch) {
            state.current_branch = branch;
        },
        calculate_crawl_progress(state, status) {
            switch (status.current_operation) {
                case 'GET_PREVIOUS_COMMITS':
                    state.is_crawling = true;
                    state.crawl_percentage = 10;
                    state.crawl_status_message = 'Caching previous data from database...';
                    break;
                case 'EXTRACT_COMMITS':
                    state.is_crawling = true;
                    state.crawl_percentage = 10 + 70 * status.commits_processed / status.commits_total;
                    state.crawl_status_message = (`Processing commit ${status.commits_processed} `
                        + `of ${status.commits_total}...`);
                    break;
                case 'CALCULATE_PATHS':
                    state.is_crawling = true;
                    state.crawl_percentage = 80
                    state.crawl_status_message = 'Following file moves and renames...';
                    break;
                case 'SAVE_TO_DB':
                    state.is_crawling = true;
                    state.crawl_percentage = 90;
                    state.crawl_status_message = 'Writing changes to database...';
                    break;
                case 'IDLE':
                    state.is_crawling = false;
                    state.crawl_percentage = 100;
                    state.crawl_status_message = '';
                    break;
            }

            state.crawl_error_message = status.error_message;
            if (status.error_message)
                state.is_crawling = false;
        },
        set_crawl_config(state, config) {
            state.crawl_config = config;
        }

    },

    actions: {
        load_branches(context) {
            let request = axios.get(`${API_BASE_PATH}/entries/availableBranches`).then(response => {
                context.commit('set_available_branches', JSON.parse(response.data));
            });
            return request;
        },
        load_crawl_status(context) {
            let request = axios.get(`${API_BASE_PATH}/crawl/status`).then(response => {
                context.commit('calculate_crawl_progress', response.data);
            });
            return request;
        },
        load_crawl_config(context) {
            let request = axios.get(`${API_BASE_PATH}/crawl/config`).then(response => {
                context.commit('set_crawl_config', response.data);
            });
            return request;
        },
        save_crawl_config(context, config) {
            context.commit('set_crawl_config', config)
            let request = axios.put(`${API_BASE_PATH}/crawl/config`, config);
            return request;
        }
    }
};