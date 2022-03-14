import axios from "axios";
import { BASE_URL } from "@/service_urls";

export const project = {
  fetchProjects: () => {
    return axios.get(`${BASE_URL}/project/get`);
  },
  fetchProjectByID: project_id => {
    return axios.get(`${BASE_URL}/project/get/${project_id}`);
  },
  createProject: payload => {
    return axios.post(`${BASE_URL}/project/create`, payload);
  }
};
