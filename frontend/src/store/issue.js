import { issue } from "@/service/issue.js";
import router from "@/router";
import m from "moment";
import { getFilterQueryStringWithoutArray } from "@/helpers/helpers.js";

const state = {
  issueTypes: [],
  issueStatus: [],
  issuePriority: [],
  projectMilestone: [],
  projectModule: [],
  projectUsers: [],
  issues: [],
  issueCounts: 0,
  filteredIssuesCount: 0,
  selectedIssue: [],
  auditIssue: [],
  lastFetchedProjectModule: 0,
  lastFetchedProjectUsers: 0,
  recentUpdates: [],
  recentUpdatesPagination: {
    skip: 0,
    limit: 10,
    noMoreData: false
  },
  isFetchingRecentUpdates: false,
  issueCountsByStatus: [],
  issueCountsByProject: [],
  detailedIssueCounts: []
};

const getters = {
  getIssueTypes: state =>
    state.issueTypes?.map(val => ({
      id: val.issue_type_id,
      label: val.type
    })),
  getIssueStatus: state =>
    state.issueStatus?.map(val => ({
      id: val.issue_status_id,
      label: val.status
    })),
  getIssuePriority: state =>
    state.issuePriority?.map(val => ({
      id: val.issue_priority_id,
      label: val.issue_priority
    })),
  getProjectMilestone: state =>
    state.projectMilestone
      ?.map(val => ({
        id: val.project_milestone_id,
        label: `${val.milestone?.milestone} / ${m
          .utc(val.milestone?.milestone_date)
          .local()
          .format("DD-MMM-YYYY")}`,
        milestone_date: val.milestone?.milestone_date
      }))
      .sort((a, b) => {
        return new Date(a.milestone_date) - new Date(b.milestone_date);
      }),
  getProjectModule: state =>
    state.projectModule?.map(val => ({
      id: val.project_module_id,
      label: val.module?.module_name
    })),
  getProjectUsers: state =>
    state.projectUsers
      ?.map(val => ({
        id: val.user_id,
        label: `${val.first_name} ${val.last_name}`
      }))
      ?.sort((a, b) => {
        var textA = a.label.toUpperCase();
        var textB = b.label.toUpperCase();
        return textA < textB ? -1 : textA > textB ? 1 : 0;
      }),
  getListIssues: state => state.issues,
  getIssueCounts: state => state.issueCounts,
  getFilteredIssuesCount: state => state.filteredIssuesCount,
  getSelectedIssue: state => state.selectedIssue,
  getAuditIssue: state => state.auditIssue,
  getLastFetchedProjectModule: state => state.lastFetchedProjectModule,
  getLastFetchedProjectUsers: state => state.lastFetchedProjectUsers,
  getRecentUpdates: state => state.recentUpdates,
  getRecentUpdatesPagination: state => state.recentUpdatesPagination,
  isFetchingRecentUpdates: state => state.isFetchingRecentUpdates,
  getIssueCountsByStatus: state => state.issueCountsByStatus,
  getIssueCountsByProject: state => state.issueCountsByProject,
  getDetailedIssueCounts: state => state.detailedIssueCounts
};

const actions = {
  fetchIssueTypes({ commit }) {
    return issue
      .fetchIssueTypes()
      .then(res => {
        const { data } = res;
        commit("SET_ISSUE_TYPES", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching issue types", err);
        return err;
      });
  },
  fetchIssueStatus({ commit }) {
    return issue
      .fetchIssueStatus()
      .then(res => {
        const { data } = res;
        commit("SET_ISSUE_STATUS", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching issue Project", err);
        return err;
      });
  },
  fetchIssuePriority({ commit }) {
    return issue
      .fetchIssuePriority()
      .then(res => {
        const { data } = res;
        commit("SET_ISSUE_PRIORITY", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching issue priority", err);
        return err;
      });
  },
  fetchProjectMilestone({ commit }, project_id) {
    return issue
      .fetchProjectMilestone(project_id)
      .then(res => {
        const { data } = res;
        commit("SET_PROJECT_MILESTONE", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching project milestone", err);
        return err;
      });
  },
  fetchProjectModule({ commit, getters }, project_id) {
    let { getLastFetchedProjectModule } = getters;
    if (getLastFetchedProjectModule === project_id) return;
    return issue
      .fetchProjectModule(project_id)
      .then(res => {
        const { data } = res;
        commit("SET_PROJECT_MODULE", data);
        commit("LAST_FETCHED_PROJECT_MODULE", project_id);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching project module", err);
        return err;
      });
  },
  fetchProjectUsers({ commit, getters }, project_id) {
    let { getLastFetchedProjectUsers } = getters;
    if (getLastFetchedProjectUsers === project_id) return;
    let query = {
      organization_projects___project_id__in: project_id,
      user_role__in: ["lead", "developer"]
    };
    return issue
      .fetchProjectUsers(getFilterQueryStringWithoutArray(query))
      .then(res => {
        const { data } = res;
        commit("SET_PROJECT_USERS", data);
        commit("LAST_FETCHED_PROJECT_USERS", project_id);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching project users", err);
        return err;
      });
  },
  fetchInitialOptionForIssue({ getters, dispatch }, project_id) {
    let { getIssueTypes, getIssueStatus, getIssuePriority } = getters;
    let appendFilterAction = [];
    dispatch("showLoader");
    if (!getIssueTypes?.length) {
      appendFilterAction = [...appendFilterAction, dispatch("fetchIssueTypes")];
    }
    if (!getIssueStatus?.length) {
      appendFilterAction = [
        ...appendFilterAction,
        dispatch("fetchIssueStatus")
      ];
    }
    if (!getIssuePriority?.length) {
      appendFilterAction = [
        ...appendFilterAction,
        dispatch("fetchIssuePriority")
      ];
    }
    appendFilterAction = [
      ...appendFilterAction,
      dispatch("fetchProjectMilestone", project_id)
    ];
    appendFilterAction = [
      ...appendFilterAction,
      dispatch("fetchProjectModule", project_id)
    ];
    appendFilterAction = [
      ...appendFilterAction,
      dispatch("fetchProjectUsers", project_id)
    ];

    return Promise.all(appendFilterAction).then(res => {
      dispatch("hideLoader");
      return res;
    });
  },
  createIssue({ dispatch }, payload) {
    dispatch("showLoader");
    return issue
      .createIssue(payload)
      .then(res => {
        const { data } = res;
        dispatch("showToast", {
          class: "bg-success text-white",
          message: "Issue Created"
        });
        router.push(`/issue-detailed-view/${data?.issue_id}`);
        return res;
      })
      .catch(err => {
        console.log("Error while creating issue", err);
        dispatch("showToast", {
          class: "bg-danger text-white",
          message: "Error While Creating"
        });
        return err;
      })
      .finally(() => dispatch("hideLoader"));
  },
  updateIssue({ dispatch, commit }, payload) {
    return issue
      .updateIssue(payload)
      .then(res => {
        const { data } = res;
        dispatch("showToast", {
          class: "bg-success text-white",
          message: "Issue updated"
        });
        commit("SELECTED_ISSUE_ID", data);
        dispatch("fetchAuditRecords", data.issue_id);
        return res;
      })
      .catch(err => {
        console.log("Error while updating issue", err);
        dispatch("showToast", {
          class: "bg-danger text-white",
          message: "Error While Updating"
        });
        return err;
      });
  },
  fetchListIssues({ getters, dispatch, commit }, payload) {
    let { getOrganizationId } = getters;
    dispatch("showLoader");
    let { currentPage, ...rest } = payload;
    let dataPayload = {
      ...rest,
      skip: currentPage * 5 - 5,
      limit: 5,
      organization_projects___organization_id__in: getOrganizationId
    };
    let query = getFilterQueryStringWithoutArray(dataPayload);
    return issue
      .fetchListIssues(query)
      .then(res => {
        const { data } = res;
        commit("SET_ISSUES", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching project issues", err);
        return err;
      })
      .finally(() => dispatch("hideLoader"));
  },
  fetchIssueCounts({ getters, commit }, queryData) {
    let { getOrganizationId } = getters;
    let query = `organization_projects___organization_id__in=${getOrganizationId}&`;
    if (queryData) {
      query += getFilterQueryStringWithoutArray(queryData);
    }
    return issue
      .fetchIssueCounts({ query })
      .then(res => {
        const { data } = res;
        commit("SET_ISSUES_COUNT", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching issues count", err);
        return err;
      });
  },
  fetchFilteredIssuesCount({ getters, commit }, payload) {
    let { getOrganizationId } = getters;
    payload = {
      ...payload,
      organization_projects___organization_id__in: getOrganizationId
    };
    let query = getFilterQueryStringWithoutArray(payload);
    return issue
      .fetchIssueCounts({ query })
      .then(res => {
        const { data } = res;
        commit("SET_FILTERED_ISSUES_COUNT", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching project issues count", err);
        return err;
      });
  },
  fetchIssueByID({ commit }, issue_id) {
    return issue
      .fetchIssueByID(issue_id)
      .then(res => {
        const { data } = res;
        commit("SELECTED_ISSUE_ID", data);
        return res;
      })
      .catch(err => {
        console.log("Error while getting issue", err);
        return err;
      });
  },
  fetchAuditRecords({ dispatch, commit }, issue_id) {
    dispatch("showLoader");
    return issue
      .fetchAuditRecords(issue_id)
      .then(res => {
        const { data } = res;
        commit("SET_AUDIT_ISSUE_DATA", data);
        return res;
      })
      .catch(err => {
        console.log("Error while getting audit issue", err);
        return err;
      })
      .finally(() => dispatch("hideLoader"));
  },
  createAuditIssues({ dispatch }, payload) {
    dispatch("showLoader");
    return issue
      .createAuditIssues(payload)
      .then(res => {
        const { data } = res;
        dispatch("fetchAuditRecords", data.issue_id);
        return res;
      })
      .catch(err => {
        console.log("Error while getting audit issue", err);
        return err;
      })
      .finally(() => dispatch("hideLoader"));
  },
  fetchRecentUpdates({ dispatch, commit, getters }, filter) {
    const {
      getRecentUpdatesPagination,
      getRecentUpdates,
      getOrganizationId
    } = getters;
    commit("IS_FETCHING_RECENT_UPDATES", true);
    let { pagination, ...rest } = filter;
    if (!pagination) {
      commit("RESET_RECENT_UPDATES");
      commit("SET_RECENT_UPDATES_PAGINATION", {
        skip: 0,
        noMoreData: false
      });
    }
    let skip = pagination ? getRecentUpdatesPagination.skip : 0;
    let limit = getRecentUpdatesPagination.limit;
    let query = getFilterQueryStringWithoutArray({
      skip: skip,
      limit: limit,
      ...rest,
      organization_projects___organization_id__in: getOrganizationId
    });
    dispatch("showLoader");
    return issue
      .fetchRecentUpdates(query)
      .then(res => {
        const { data } = res;
        if (data.length < limit) {
          commit("SET_RECENT_UPDATES_PAGINATION", {
            noMoreData: true
          });
        } else {
          commit("SET_RECENT_UPDATES_PAGINATION", {
            skip: skip + limit,
            noMoreData: false
          });
        }
        if (pagination) {
          commit("SET_RECENT_UPDATES", getRecentUpdates.concat(data));
        } else {
          commit("SET_RECENT_UPDATES", data);
        }
        return res;
      })
      .catch(err => {
        console.log("Error while getting recent updates", err);
        return err;
      })
      .finally(() => {
        commit("IS_FETCHING_RECENT_UPDATES", false);
        dispatch("hideLoader");
      });
  },
  fetchIssueCountsByStatus({ commit }) {
    return issue
      .fetchIssueCountsByStatus()
      .then(res => {
        const { data } = res;
        commit("ISSUE_COUNTS_BY_STATUS", data);
        return res;
      })
      .catch(err => {
        console.log("Error while getting counts by issue", err);
        return err;
      });
  },
  fetchIssueCountsByProject({ commit }) {
    return issue
      .fetchIssueCountsByProject()
      .then(res => {
        const { data } = res;
        commit("ISSUE_COUNTS_BY_PROJECT", data);
        return res;
      })
      .catch(err => {
        console.log("Error while getting counts by project", err);
        return err;
      });
  },
  fetchDetailedIssueCounts({ commit }) {
    return issue
      .fetchDetailedIssueCounts()
      .then(res => {
        const { data } = res;
        commit("DETAILED_ISSUE_COUNTS", data);
        return res;
      })
      .catch(err => {
        console.log("Error while getting detailed issue counts", err);
        return err;
      });
  }
};

const mutations = {
  ["SET_ISSUE_TYPES"](state, data) {
    state.issueTypes = data;
  },
  ["SET_ISSUE_STATUS"](state, data) {
    state.issueStatus = data;
  },
  ["SET_ISSUE_PRIORITY"](state, data) {
    state.issuePriority = data;
  },
  ["SET_PROJECT_MILESTONE"](state, data) {
    state.projectMilestone = data;
  },
  ["SET_PROJECT_MODULE"](state, data) {
    state.projectModule = data;
  },
  ["SET_PROJECT_USERS"](state, data) {
    state.projectUsers = data;
  },
  ["SET_ISSUES"](state, data) {
    state.issues = data;
  },
  ["SET_ISSUES_COUNT"](state, data) {
    state.issueCounts = data;
  },
  ["SET_FILTERED_ISSUES_COUNT"](state, data) {
    state.filteredIssuesCount = data;
  },
  ["SELECTED_ISSUE_ID"](state, data) {
    state.selectedIssue = data;
  },
  ["SET_AUDIT_ISSUE_DATA"](state, data) {
    state.auditIssue = data;
  },
  ["LAST_FETCHED_PROJECT_MODULE"](state, data) {
    state.lastFetchedProjectModule = data;
  },
  ["LAST_FETCHED_PROJECT_USERS"](state, data) {
    state.lastFetchedProjectUsers = data;
  },
  ["SET_RECENT_UPDATES"](state, data) {
    state.recentUpdates = data;
  },
  ["RESET_RECENT_UPDATES"](state) {
    state.recentUpdates = [];
  },
  ["IS_FETCHING_RECENT_UPDATES"](state, data) {
    state.isFetchingRecentUpdates = data;
  },
  ["SET_RECENT_UPDATES_PAGINATION"](state, payload) {
    state.recentUpdatesPagination = {
      ...state.recentUpdatesPagination,
      ...payload
    };
  },
  ["ISSUE_COUNTS_BY_STATUS"](state, data) {
    state.issueCountsByStatus = data;
  },
  ["ISSUE_COUNTS_BY_PROJECT"](state, data) {
    state.issueCountsByProject = data;
  },
  ["DETAILED_ISSUE_COUNTS"](state, data) {
    state.detailedIssueCounts = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
