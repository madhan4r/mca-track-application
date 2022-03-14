import axios from "axios";
import { BASE_URL } from "@/service_urls";

export const user = {
  fetchUser: () => {
    return axios.get(`${BASE_URL}/users/me`);
  },
  updateUser: payload => {
    return axios.put(`${BASE_URL}/users/me`, payload);
  },
  fetchUsers: query => {
    return axios.get(
      `${BASE_URL}/users/?all_rows=true&is_superuser__in=null,false&${query}`
    );
  },
  createUsers: payload => {
    return axios.post(`${BASE_URL}/users/`, payload);
  }
};
