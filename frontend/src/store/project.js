import { project } from "@/service/project.js";

const state = {
  projects: [],
  selectedProject: []
};

const getters = {
  getProjects: state => state.projects,
  getSelectedProject: state => state.selectedProject
};

const actions = {
  fetchProjects({ commit }) {
    return project
      .fetchProjects()
      .then(res => {
        const { data } = res;
        commit("SET_PROJECTS", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching projects", err);
        return err;
      });
  },
  fetchProjectByID({ commit }, project_id) {
    return project
      .fetchProjectByID(project_id)
      .then(res => {
        const { data } = res;
        commit("SET_SELECTED_PROJECT", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching project", err);
        return err;
      });
  }
};

const mutations = {
  ["SET_PROJECTS"](state, data) {
    state.projects = data;
  },
  ["SET_SELECTED_PROJECT"](state, data) {
    state.selectedProject = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
