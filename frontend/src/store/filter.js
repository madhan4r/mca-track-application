const state = {};
const getters = {};
const actions = {
  initIssuePageFilterOptions({ dispatch, getters }, payload) {
    let { getIssueTypes, getIssueStatus, getOrganizationId } = getters;
    let { project_id, filters } = payload;
    let appendFilterAction = [];
    dispatch("showLoader");
    if (!getIssueTypes?.length && filters.includes("type_id__in")) {
      appendFilterAction = [...appendFilterAction, dispatch("fetchIssueTypes")];
    }
    if (!getIssueStatus?.length && filters.includes("status_id__in")) {
      appendFilterAction = [
        ...appendFilterAction,
        dispatch("fetchIssueStatus")
      ];
    }
    if (project_id && filters.includes("module_id__in")) {
      appendFilterAction = [
        ...appendFilterAction,
        dispatch("fetchProjectModule", project_id)
      ];
    }
    if (filters.includes("project_id__in")) {
      appendFilterAction = [
        ...appendFilterAction,
        dispatch("fetchOrganizationProject", getOrganizationId)
      ];
    }
    if (filters.includes("assigned_to__in")) {
      appendFilterAction = [
        ...appendFilterAction,
        dispatch("fetchOrganizationUsers", getOrganizationId)
      ];
    }

    return Promise.all(appendFilterAction).then(res => {
      dispatch("hideLoader");
      return res;
    });
  }
};
const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations
};
