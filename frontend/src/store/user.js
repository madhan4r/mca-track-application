import { user } from "@/service/user.js";
import { getFilterQueryStringWithoutArray } from "@/helpers/helpers.js";

const state = {
  users: []
};

const getters = {
  getUsers: state =>
    state.users
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
  fetchUsers({ commit }) {
    let query = {
      user_role__in: ["lead", "developer"]
    };
    return user
      .fetchUsers(getFilterQueryStringWithoutArray(query))
      .then(res => {
        const { data } = res;
        commit("SET_USERS", data);
        return res;
      })
      .catch(err => {
        console.log("Error while fetching users", err);
        return err;
      });
  }
};

const mutations = {
  ["SET_USERS"](state, data) {
    state.users = data;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
