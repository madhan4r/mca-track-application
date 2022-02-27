import Vue from "vue";
import Vuex from "vuex";
import Toaster from "./toaster";
import AuthModule from "./auth";
import UserModule from "./user";
import ProjectModule from "./project";
import IssueModule from "./issue";
import FilterModule from "./filter";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    darkMode: false,
    isLoading: false,
    showSideBar: false,
    showFilter: false,
    color: {
      open: "rgb(105, 132, 238)",
      closed: "rgb(229, 86, 102)",
      wip: "rgb(242, 183, 89)",
      completed: "rgb(125, 91, 212)",
      on_hold: "rgb(148, 153, 35)",
      re_open: "rgb(191, 115, 168)"
    },
    randomColor: {
      0: "rgb(105, 132, 238)",
      1: "#ff66cc",
      2: "rgb(229, 86, 102)",
      3: "rgb(242, 183, 89)",
      4: "rgb(148, 153, 35)",
      5: "rgb(191, 115, 168)",
      6: "#03A9F4",
      7: "#af4bce",
      8: "#ea7369",
      9: "#29066B",
      10: "#a05195",
      11: "rgb(149, 202, 87)",
      12: "#488f31",
      13: "rgb(125, 91, 212)",
      14: "#dbc667",
      15: "#de425b"
    }
  },
  getters: {
    getColor: state => key => state.color[key],
    getRandomColor: state => key => state.randomColor[key],
    isLoading: state => state.isLoading,
    showSideBar: state => state.showSideBar,
    showFilter: state => state.showFilter,
    darkMode: state => state.darkMode
  },
  actions: {
    showLoader({ commit }) {
      commit("SET_LOADER", true);
    },
    hideLoader({ commit }) {
      commit("SET_LOADER", false);
    },
    toggleSideBar({ state, commit }) {
      commit("SET_SIDE_BAR", !state.showSideBar);
    },
    toggleFilterBar({ state, commit }) {
      commit("SET_FILTER_SIDE_BAR", !state.showFilter);
    },
    toggleDarkMode({ state, commit }) {
      commit("SET_DARK_MODE", !state.darkMode);
    }
  },
  mutations: {
    ["SET_LOADER"](state, payload) {
      state.isLoading = payload;
    },
    ["SET_SIDE_BAR"](state, payload) {
      state.showSideBar = payload;
    },
    ["SET_FILTER_SIDE_BAR"](state, payload) {
      state.showFilter = payload;
    },
    ["SET_DARK_MODE"](state, mode) {
      state.darkMode = mode;
    }
  },
  modules: {
    Toaster,
    UserModule,
    AuthModule,
    ProjectModule,
    IssueModule,
    FilterModule
  }
});
