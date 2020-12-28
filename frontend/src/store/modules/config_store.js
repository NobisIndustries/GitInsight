import axios from "axios";

import {API_BASE_PATH} from '@/store/constants'

export const config_store = {
    state: {
        crawl_status: {
            is_crawling: false,
            percentage: 0,
            status_message: '',
            error_message: '',
        },
        crawl_config: {},

        authors: {},
        teams: {}
    },
    mutations: {
        calculate_crawl_progress(state, status) {
            state.crawl_status.is_crawling = true;
            switch (status.current_operation) {
                case 'CLONE_REPO':
                    state.crawl_status.percentage = 0;
                    state.crawl_status.status_message = 'Clone repo for first usage...';
                    break;
                case 'UPDATE_REPO':
                    state.crawl_status.percentage = 10;
                    state.crawl_status.status_message = 'Updating to newest repo version...';
                    break;
                case 'GET_PREVIOUS_COMMITS':
                    state.crawl_status.percentage = 20;
                    state.crawl_status.status_message = 'Caching previous data from database...';
                    break;
                case 'EXTRACT_COMMITS':
                    state.crawl_status.percentage = 20 + 60 * status.commits_processed / status.commits_total;
                    state.crawl_status.status_message = (`Processing commit ${number_with_separator(status.commits_processed)} `
                        + `of ${number_with_separator(status.commits_total)}...`);
                    break;
                case 'CALCULATE_PATHS':
                    state.crawl_status.percentage = 80
                    state.crawl_status.status_message = 'Following file moves and renames...';
                    break;
                case 'SAVE_TO_DB':
                    state.crawl_status.percentage = 90;
                    state.crawl_status.status_message = 'Writing changes to database...';
                    break;
                case 'IDLE':
                    state.crawl_status.percentage = 100;
                    state.crawl_status.status_message = 'Idle';
                    state.crawl_status.is_crawling = false;
                    break;
            }

            state.crawl_status.error_message = status.error_message;
            if (status.error_message)
                state.crawl_status.is_crawling = false;
        },
        set_crawl_config(state, config) {
            state.crawl_config = config;
        },
        set_authors(state, authors) {
            state.authors = authors;
        },
        set_teams(state, teams) {
            state.teams = teams;
        },

    },

    actions: {
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
        },
        load_crawl_status(context) {
            let request = axios.get(`${API_BASE_PATH}/crawl/status`).then(response => {
                context.commit('calculate_crawl_progress', response.data);
            });
            return request;
        },
        load_authors(context) {
            let request = axios.get(`${API_BASE_PATH}/authors/authors`).then(response => {
                context.commit('set_authors', response.data['authors']);
            });
            return request;
        },
        load_teams(context) {
            let request = axios.get(`${API_BASE_PATH}/authors/teams`).then(response => {
                context.commit('set_teams', response.data['teams']);
            });
            return request;
        },
    },
};

function number_with_separator(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}