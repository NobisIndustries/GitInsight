import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        dark: true,
        themes: {
            dark: {
                primary: '#21CFF3',
                accent: '#f65d67',
                secondary: '#FFE18D',
                success: '#4CAF50',
                info: '#2196F3',
                warning: '#FB8C00',
                error: '#FF5252',
                dark: '#003049'
            },
            light: {
                primary: '#457b9d',
                accent: '#f65d67',
                secondary: '#a8dadc',
                success: '#4CAF50',
                info: '#2196F3',
                warning: '#f77f00',
                error: '#d62828',
                dark: '#003049'
            },
        },
        options: {
            customProperties: true
        }
    }
});
