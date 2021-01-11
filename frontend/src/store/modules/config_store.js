import Vue from 'vue'
import axios from "axios";

import {API_BASE_PATH, UNKNOWN_TEAM_ID} from '@/store/constants'

export const config_store = {
    state: {
        crawl_status: {
            is_crawling: false,
            percentage: 0,
            status_message: '',
            error_message: '',
        },
        crawl_config: {},
        clone_result: {
            successful: false,
            error_msg: '',
        },

        authors: {},
        teams: {},

        users: [],
    },
    mutations: {
        calculate_crawl_progress(state, status) {
            state.crawl_status.is_crawling = true;
            switch (status.current_operation) {
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
        set_clone_result(state, result) {
            state.clone_result = result;
        },

        set_authors(state, authors) {
            state.authors = authors;
        },
        update_author_info(state, {author_name, author_info}) {
            // Preserves reactivity, see https://vuejs.org/v2/guide/reactivity.html#For-Objects
            Vue.set(state.authors, author_name, author_info);
        },
        set_teams(state, teams) {
            state.teams = teams;
        },
        update_team_info(state, {team_name, team_info}) {
            // Preserves reactivity, see https://vuejs.org/v2/guide/reactivity.html#For-Objects
            Vue.set(state.teams, team_name, team_info);
        },
        delete_team(state, {team_name, author_names_to_reset}) {
            for (let author_name of author_names_to_reset)
                state.authors[author_name].team_id = UNKNOWN_TEAM_ID;
            Vue.delete(state.teams, team_name);
        },

        set_users(state, users) {
            state.users = users;
            state.users.sort((a, b) => a.username.toLowerCase().localeCompare(b.username.toLowerCase()));
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
        update_db() {
            return axios.put(`${API_BASE_PATH}/crawl/update`);
        },
        clone_repo(context, {repo_url, deploy_key}) {
            const data = {repo_url: repo_url, deploy_key: deploy_key}
            let request = axios.put(`${API_BASE_PATH}/crawl/clone`, data).then(response => {
                context.commit('set_clone_result', response.data);
            });
            return request;
        },

        load_author_info(context) {
            let request = axios.get(`${API_BASE_PATH}/authors/info`).then(response => {
                context.commit('set_teams', response.data['teams']);
                context.commit('set_authors', response.data['authors']);
            });
            return request;
        },
        save_author_info(context) {
            const data = {authors: context.state.authors, teams: context.state.teams};
            let request = axios.put(`${API_BASE_PATH}/authors/info`, data);
            return request;
        },

        load_users(context) {
            let request = axios.get(`${API_BASE_PATH}/auth/users`).then(response => {
                context.commit('set_users', response.data);
            });
            return request;
        },
        add_user(context, {username, new_password, permissions}) {
            const data = {password: new_password, permissions: permissions};
            let request = axios.post(`${API_BASE_PATH}/auth/users/${username}`, data);
            return request;
        },
        update_user(context, {username, new_password, permissions}) {
            const data = {password: new_password, permissions: permissions};
            let request = axios.put(`${API_BASE_PATH}/auth/users/${username}`, data);
            return request;
        },
        delete_user(context, username) {
            let request = axios.delete(`${API_BASE_PATH}/auth/users/${username}`);
            return request;
        }
    },
};

function number_with_separator(n) {
    return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}