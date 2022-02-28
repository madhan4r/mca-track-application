import axios from "axios";
import { BASE_URL } from "@/service_urls";

export const issue = {
  fetchIssueTypes: () => {
    return axios.get(`${BASE_URL}/issue/type/`);
  },
  fetchIssueStatus: () => {
    return axios.get(`${BASE_URL}/issue/status/`);
  },
  fetchIssuePriority: () => {
    return axios.get(`${BASE_URL}/issue/priority/`);
  },
  fetchProjectModule: project_id => {
    return axios.get(`${BASE_URL}/project/module/?project_id=${project_id}`);
  },
  fetchListIssues: query => {
    return axios.get(
      `${BASE_URL}/issue/?${query}&order_by=-issue_id&all_rows=false`
    );
  },
  fetchIssueCounts: ({ query }) => {
    return axios.get(`${BASE_URL}/issue/count/?${query}`);
  },
  fetchIssueByID: issue_id => {
    return axios.get(`${BASE_URL}/issue/${issue_id}/get`);
  },
  createIssue: payload => {
    return axios.post(`${BASE_URL}/issue/`, payload);
  },
  updateIssue: payload => {
    return axios.put(`${BASE_URL}/issue/`, payload);
  },
  createAuditIssues: payload => {
    return axios.post(`${BASE_URL}/issue/audit/`, payload);
  },
  fetchAuditRecords: issue_id => {
    return axios.get(`${BASE_URL}/issue/audit/?issue_id=${issue_id}`);
  },
  fetchRecentUpdates: query => {
    return axios.get(
      `${BASE_URL}/view/audit_view?order_by=-created_on&${query}`
    );
  },
  fetchIssueCountsByStatus: () => {
    return axios.get(`${BASE_URL}/issue/count_by_status/`);
  },
  fetchIssueCountsByProject: () => {
    return axios.get(`${BASE_URL}/issue/count_by_project/`);
  },
  fetchDetailedIssueCounts: () => {
    return axios.get(`${BASE_URL}/issue/count_by_detail/`);
  }
};
