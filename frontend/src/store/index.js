import Vue from 'vue';
import Vuex from 'vuex';
import {entry_details_store} from "@/store/modules/entry_details_store";
import {common_store} from "@/store/modules/common_store";


Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    common: common_store,
    entry_details: entry_details_store,
  }
})
