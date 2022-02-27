import axios from "axios";
import { BASE_URL } from "@/service_urls";

export const project = {
  fetchOrganizationProject: ({ query }) => {
    return axios.get(`${BASE_URL}/organization/projects/?${query}`);
  },
  fetchProjectByID: project_id => {
    return axios.get(`${BASE_URL}/project/get/${project_id}`);
  }
};
