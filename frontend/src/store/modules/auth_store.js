import axios from "axios";

import {API_BASE_PATH, GUEST_USERNAME} from '@/store/constants'

export const auth_store = {
    state: {
        is_logged_in: false,
        username: null,

        view_analysis: false,
        edit_contributors: false,
        edit_all: false
    },
    mutations: {
        set_user_data(state, user_data) {
            state.is_logged_in = user_data.username !== GUEST_USERNAME

            state.username = user_data.username;
            state.view_analysis = user_data.permissions.view_analysis;
            state.edit_contributors = user_data.permissions.edit_contributors;
            state.edit_all = user_data.permissions.edit_all;
        }
    },

    actions: {
        get_current_user(context) {
            axios.defaults.headers.common = {Authorization: 'Bearer ' + localStorage.auth_jwt};
            let request = axios.get(`${API_BASE_PATH}/auth/current_user`).then(response => {
                context.commit('set_user_data', response.data);
            }).catch(error => {
                if (error.response.status === 401) {
                    this.dispatch('login', {username: GUEST_USERNAME, password: 'dummy_password'});
                }
            });
            return request;
        },
        login(context, {username, password}) {
            let form_data = new FormData();
            form_data.append('username', username);
            form_data.append('password', password);

            let request = axios.post(`${API_BASE_PATH}/auth/token`, form_data).then(response => {
                localStorage.auth_jwt = response.data.access_token;
                this.dispatch('get_current_user');
            });
            return request;
        },
        logout() {
            localStorage.auth_jwt = null;
            axios.defaults.headers.common = {};
            this.dispatch('get_current_user');
        },
        change_password(context, {old_password, new_password}) {
            const data = {old_password: old_password, new_password: new_password};
            let request = axios.put(`${API_BASE_PATH}/auth/current_user/password`, data);
            return request;
        },
    },
};
