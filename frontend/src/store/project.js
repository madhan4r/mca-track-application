import { project } from "@/service/project.js";

const state = {
  organizationProjects: [],
  selectedProject: []
};

const getters = {
  getOrganizationProjects: state => state.organizationProjects,
  getSelectedProject: state => state.selectedProject
};

const actions = {
  fetchOrganizationProject({ commit }, organization_id) {
    return project
      .fetchOrganizationProject({ query: `organization_id=${organization_id}` })
      .then(res => {
        const { data } = res;
        commit("SET_ORGANIZATION_PROJECTS", data);
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
  ["SET_ORGANIZATION_PROJECTS"](state, data) {
    state.organizationProjects = data;
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
