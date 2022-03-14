import { auth } from "@/service/auth.js";
import { user } from "@/service/user.js";
import router from "@/router";
import { parseJwt } from "../helpers/helpers";

const state = {
  isLoading: false,
  userData: JSON.parse(localStorage.getItem("token")) || "",
  error: "",
  user: []
};

const getters = {
  isLoginFetching: state => state.isLoading,
  getUserData: state => state.userData || {},
  getUserDetails: (state, getters) => {
    let { getUserData } = getters;
    if (getUserData && getUserData.access_token) {
      return parseJwt(getUserData.access_token);
    } else {
      return {};
    }
  },
  getUserId(state, getters) {
    let { getUserDetails } = getters;
    return getUserDetails.user_id;
  },
  getUserRole(state, getters) {
    let { getUserDetails } = getters;
    return getUserDetails.user_role;
  },
  currentActiveUser(state, getters) {
    let { getUserId } = getters;
    return getUserId ? true : false;
  },
  getUserName(state) {
    return state.user?.first_name || "User";
  }
};

const actions = {
  logIn({ dispatch, commit }, { email, password }) {
    localStorage.removeItem("token");
    dispatch("showToast", {
      class: "bg-success text-white",
      message: "Loading...",
      autoHide: 3000
    });
    const payload = new URLSearchParams();
    payload.append("username", email);
    payload.append("password", password);
    return auth
      .logInGetToken(payload)
      .then(res => {
        let { data } = res;
        localStorage.setItem("token", JSON.stringify(data));
        dispatch("showToast", {
          class: "bg-success text-white",
          message: "Login Successful!"
        });
        commit("LOGIN_SUCCESS", data);
        data = parseJwt(data.access_token);
        if (data.is_superuser) {
          router.push("/admin-home");
        } else {
          router.push("/list-project");
        }
        return res;
      })
      .catch(err => {
        if (err?.response?.status === 400) {
          dispatch("showToast", {
            class: "bg-danger text-white",
            message: err.response.data.detail
          });
        }
        console.error("error in login", err);
        commit("LOGINERROR", err);
        return err;
      });
  },
  logout({ dispatch, commit }) {
    localStorage.removeItem("token");
    commit("LOGOUT");
    router.push("/login");
    dispatch("showToast", {
      class: "bg-success text-white",
      message: "Logout Successful!"
    });
  },
  fetchUser({ commit }) {
    return user
      .fetchUser()
      .then(res => {
        let { data } = res;
        commit("SET_USER", data);
        return res;
      })
      .catch(err => {
        console.error("error fetching user", err);
        return err;
      });
  }
};

const mutations = {
  ["LOGINERROR"](state, error) {
    state.error = error;
    state.isLoading = false;
    state.userData = "";
  },
  ["LOGIN_SUCCESS"](state, payload) {
    state.error = false;
    state.isLoading = false;
    state.userData = payload;
  },
  ["LOGIN"](state) {
    state.error = false;
    state.isLoading = true;
    state.userData = "";
  },
  ["LOGOUT"](state) {
    state.error = false;
    state.isLoading = false;
    state.userData = "";
    state.user = [];
  },
  ["SET_USER"](state, payload) {
    state.user = payload;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
