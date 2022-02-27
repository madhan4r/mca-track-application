import axios from "axios";
import { BASE_URL } from "@/service_urls";

export const user = {
  fetchUser: () => {
    return axios.get(`${BASE_URL}/users/me`);
  },
  updateUser: payload => {
    return axios.put(`${BASE_URL}/users/me`, payload);
  },
  fetchUsersByOrganization: query => {
    return axios.get(
      `${BASE_URL}/users/get_users/by/organization?all_rows=true&is_superuser__in=null,false&${query}`
    );
  }
};
