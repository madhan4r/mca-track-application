import { user } from "@/service/user.js";
import { getFilterQueryStringWithoutArray } from "@/helpers/helpers.js";

const state = {
  lastFetchedOrganizationUsers: 0,
  organizationUsers: []
};

const getters = {
  getLastFetchedOrganizationUsers: state =>
    state.getLastFetchedOrganizationUsers,
  getOrganizationUsers: state =>
    state.organizationUsers
      ?.map(val => ({
        id: val.user_id,
        label: `${val.first_name} ${val.last_name}`
      }))
      ?.sort((a, b) => {
        var textA = a.label.toUpperCase();
        var textB = b.label.toUpperCase();
        return textA < textB ? -1 : textA > textB ? 1 : 0;
      })
};

const actions = {
  updateUser({ dispatch, commit }, payload) {
    return user
      .updateUser(payload)
      .then(res => {
        const { data } = res;
        dispatch("showToast", {
          class: "bg-success text-white",
          message: "Password changed successfully!"
        });
        commit("SET_USER", data);
        return res;
      })
      .catch(err => {
        if (err?.response?.status === 400) {
          dispatch("showToast", {
            class: "bg-danger text-white",
            message: err.response.data.detail
          });
        }
        console.error("error in password change", err);
        return err;
      });
  },
  fetchOrganizationUsers({ commit, getters }, organization_id) {
    let { getLastFetchedOrganizationUsers } = getters;
    if (getLastFetchedOrganizationUsers === organization_id) return;
    let query = {
      organization_id: organization_id,
      user_role__in: ["lead", "developer"]
    };
    return user
      .fetchUsersByOrganization(getFilterQueryStringWithoutArray(query))
      .then(res => {
        const { data } = res;
        commit("SET_ORGANIZATION_USERS", data);
        commit("LAST_FETCHED_ORGANIZATION_USERS", organization_id);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching organization users", err);
        return err;
      });
  }
};

const mutations = {
  ["SET_ORGANIZATION_USERS"](state, data) {
    state.organizationUsers = data;
  },
  ["LAST_FETCHED_ORGANIZATION_USERS"](state, data) {
    state.lastFetchedOrganizationUsers = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
