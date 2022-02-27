import axios from "axios";
import { BASE_URL } from "@/service_urls";

export const auth = {
  logInGetToken: payload => {
    return axios.post(`${BASE_URL}/login/access-token`, payload);
  }
};
