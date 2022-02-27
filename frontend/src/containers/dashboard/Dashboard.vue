<template>
  <div class="d-flex justify-content-center mb-5 list-issue-page">
    <div class="col-lg-10">
      <div class="card border-1">
        <div class="card-body text-center">
          <h4 class="card-title m-b-0">
            Dashboard
          </h4>
        </div>
        <CRow>
          <CCol lg="5" id="leftChart">
            <h5 class="mt-3 text-center" style="font-weight: 600">
              Total Issues
            </h5>
            <hr />
            <custom-pie-chart
              class="col-12"
              :PieChartData="issueCountsByStatus"
              :PieChartLegendData="issueCountsByStatus"
            />
          </CCol>
          <CCol lg="7" id="rightChart">
            <h5 class="mt-3 text-center" style="font-weight: 600">
              Issues By Project
            </h5>
            <hr />
            <custom-pie-chart
              class="col-12"
              :PieChartData="issueCountsByProject"
              :PieChartLegendData="issueCountsByProject"
              :useRandomColors="true"
            />
          </CCol>
        </CRow>
        <CRow class="mt-5" style="padding: 1.25rem">
          <h4 class="mt-3 text-center w-100" style="font-weight: 700">
            Detailed View
          </h4>
          <CRow class="w-100 justify-content-center ml-0">
            <div
              class="col-lg-5 col-md-5 col-sm-5 mt-3"
              style="font-weight: 600"
            >
              <Select
                name="selectedProject"
                :value="selectedProject"
                @input="handleProject"
                :options="
                  options && options['selectedProject']
                    ? options['selectedProject']
                    : []
                "
                :taggable="false"
                :multiple="false"
                :clearable="false"
              />
            </div>
          </CRow>
        </CRow>
        <hr />
        <custom-pie-chart
          class="col-12"
          :PieChartData="selectedProjectIssueCount"
          :PieChartLegendData="selectedProjectIssueCount"
        />
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import CustomPieChart from "./CustomPieChart.vue";
import Select from "@/components/reusable/Fields/Select";

export default {
  name: "Dashboard",
  components: { CustomPieChart, Select },
  data: () => ({
    selectedProject: [],
    selectedProjectIssueCount: []
  }),
  computed: {
    ...mapGetters([
      "getIssueCountsByStatus",
      "getIssueCountsByProject",
      "getDetailedIssueCounts"
    ]),
    options() {
      return {
        selectedProject: this.getProjectsTitles || [],
        selectedProjectIssueCount: []
      };
    },
    issueCountsByStatus() {
      return (
        this.getIssueCountsByStatus?.map(val => {
          return {
            label: "Total Issue",
            displayName: val?.status,
            name: val?.status
              .split(" ")
              .join("")
              .replace(/[^a-zA-Z ]/g, "_")
              .toLowerCase(),
            id: 1,
            count: val?.count,
            value: val?.count,
            urlToGlobalIssues: `status_id__in=%5B${val?.status_id}%5D&page=%5B1%5D`
          };
        }) || []
      );
    },
    issueCountsByProject() {
      return (
        this.getIssueCountsByProject?.map(val => {
          return {
            label: "Project Issues",
            displayName: val?.project_name,
            name: val?.project_name
              .split(" ")
              .join("")
              .replace(/[^a-zA-Z ]/g, "_")
              .toLowerCase(),
            id: 1,
            count: val?.count,
            value: val?.count,
            urlToGlobalIssues: `project_id__in=%5B${val?.project_id}%5D&page=%5B1%5D`
          };
        }) || []
      );
    },
    getProjectsTitles() {
      let temp = [];
      this.getDetailedIssueCounts?.forEach(ele => {
        if (!temp.some(val => val.id == ele.project_id)) {
          temp.push({ label: ele.project_name, id: ele.project_id });
        }
      });
      return temp;
    }
  },
  watch: {
    getProjectsTitles() {
      this.handleProject("selectedProject", this.getProjectsTitles[0]);
    }
  },
  methods: {
    ...mapActions([
      "fetchIssueCountsByStatus",
      "fetchIssueCountsByProject",
      "fetchDetailedIssueCounts",
      "showLoader",
      "hideLoader"
    ]),
    handleProject(name, value) {
      this.selectedProject = value;
      this.selectedProjectIssueCount = this.getDetailedIssueCounts
        ?.filter(el => el.project_id == value.id)
        .map(val => {
          return {
            label: "Detailed Project Issues",
            displayName: val?.status,
            name: val?.status
              .split(" ")
              .join("")
              .replace(/[^a-zA-Z ]/g, "_")
              .toLowerCase(),
            id: 1,
            count: val?.count,
            value: val?.count,
            urlToGlobalIssues: `project_id__in=%5B${val?.project_id}%5D&status_id__in=%5B${val?.status_id}%5D&page=%5B1%5D`
          };
        });
    }
  },
  mounted() {
    this.showLoader();
    let appendActions = [];
    appendActions.push(this.fetchIssueCountsByStatus());
    appendActions.push(this.fetchIssueCountsByProject());
    appendActions.push(this.fetchDetailedIssueCounts());
    Promise.all([appendActions]).then(() => this.hideLoader());
  }
};
</script>
