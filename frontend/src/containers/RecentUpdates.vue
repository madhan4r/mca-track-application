<template>
  <div class="d-flex justify-content-center mb-5 list-issue-page">
    <div class="col-lg-10 mb-4">
      <div class="d-flex justify-content-between">
        <h5 class="font-weight-bold ml-3 navigation">
          <u>
            <a class="cursor-pointer" @click="NavigateToProjects">Projects</a>
          </u>
          > Recent Updates
        </h5>
      </div>
      <div class="card mt-2" style="border: 1px solid grey;border-radius: 10px">
        <div class="card-body text-center">
          <h4 class="card-title m-b-0">Recent Updates</h4>
        </div>
        <CRow class="pl-3 pr-3">
          <CCol md="4" class="mb-3">
            <CRow class="row">
              <label class="col-lg-12 col-md-12">Projects</label>
              <div class="col-lg-12 col-md-12 col-sm-12">
                <Select
                  name="project_id"
                  :value="audit.project_id"
                  @input="handleChangeSelect"
                  :options="
                    options && options['project_id']
                      ? options['project_id']
                      : []
                  "
                  :taggable="false"
                  :multiple="false"
                  :clearable="false"
                />
              </div>
            </CRow>
          </CCol>
          <CCol md="4" class="mb-3">
            <CRow class="row">
              <label class="col-lg-12 col-md-12">Type</label>
              <div class="col-lg-12 col-md-12 col-sm-12">
                <Select
                  name="audit_type"
                  :value="audit.audit_type"
                  @input="handleChangeSelect"
                  :options="
                    options && options['audit_type']
                      ? options['audit_type']
                      : []
                  "
                  :taggable="false"
                  :multiple="false"
                  :clearable="false"
                />
              </div>
            </CRow>
          </CCol>
          <CCol md="4" class="mb-3">
            <CRow class="row">
              <label class="col-lg-12 col-md-12">Date Range</label>
              <div class="col-lg-12 col-md-12 col-sm-12">
                <VueDatePicker
                  v-model="audit.date"
                  color="#9de077"
                  noHeader
                  range
                  style="border: 1px solid rgba(60, 60, 60, 0.26);border-radius: 4px;"
                  @onChange="handleDatePicker()"
                ></VueDatePicker>
              </div>
            </CRow>
          </CCol>
        </CRow>
        <hr class="mb-0" />
        <div
          class="container pt-3"
          id="container"
          style="max-height: 500px;overflow-y: auto;"
        >
          <div class="row">
            <div class="col-md-12">
              <div
                v-if="getRecentUpdates && getRecentUpdates.length"
                class="comment-card p-2"
              >
                <ul
                  class="list-unstyled"
                  v-for="(data, index) in getRecentUpdates"
                  :key="index"
                >
                  <li
                    class="media pb-4"
                    v-if="data.audit_view_type === 'issue'"
                  >
                    <span class="round">
                      <img
                        src="https://img.icons8.com/bubbles/100/000000/check-male.png"
                        class="align-self-start mr-3"
                        alt="dummy-logo"
                      />
                    </span>
                    <div class="media-body">
                      <div class="row d-flex">
                        <h6 class="project">
                          {{ data.project_name }}
                          -
                          <a @click="navigateToIssueDetail(data.issue_id)">
                            #{{ data.issue_id }} {{ data.issue_title }}
                          </a>
                        </h6>
                        <div class="ml-auto">
                          <p class="text">
                            {{ showTimeDiff(data.created_on) }} ago
                          </p>
                        </div>
                      </div>
                      <p class="text">
                        Issue created by
                        <strong>
                          {{ data.created_by_name }}
                        </strong>
                      </p>
                    </div>
                  </li>
                  <li
                    class="media pb-4"
                    v-if="data.audit_type === 'status_change'"
                  >
                    <span class="round">
                      <img
                        src="https://img.icons8.com/bubbles/100/000000/check-male.png"
                        class="align-self-start mr-3"
                        alt="dummy-logo"
                      />
                    </span>
                    <div class="media-body">
                      <div class="row d-flex">
                        <h6 class="project">
                          {{ data.project_name }}
                          -
                          <a @click="navigateToIssueDetail(data.issue_id)">
                            #{{ data.issue_id }} {{ data.issue_title }}
                          </a>
                        </h6>
                        <div class="ml-auto">
                          <p class="text">
                            {{ showTimeDiff(data.created_on) }} ago
                          </p>
                        </div>
                      </div>
                      <p class="text">
                        <strong>
                          {{ data.created_by_name }}
                        </strong>
                        updated the status from
                        <strong>{{ data.previous_status_name }}</strong> to
                        <strong>{{ data.updated_status_name }}</strong>
                      </p>
                    </div>
                  </li>
                  <li class="media pb-4" v-if="data.audit_type == 'comments'">
                    <span class="round">
                      <img
                        src="https://img.icons8.com/bubbles/100/000000/check-male.png"
                        class="align-self-start mr-3"
                        alt="dummy-logo"
                      />
                    </span>
                    <div class="media-body">
                      <div class="row d-flex">
                        <h6 class="project">
                          {{ data.project_name }}
                          -
                          <a @click="navigateToIssueDetail(data.issue_id)">
                            #{{ data.issue_id }} {{ data.issue_title }}
                          </a>
                        </h6>
                        <div class="ml-auto">
                          <p class="text">
                            {{ showTimeDiff(data.created_on) }} ago
                          </p>
                        </div>
                      </div>
                      <p class="text">
                        <strong>{{ data.created_by_name }}</strong> commented as
                      </p>
                      <div class="media mt-3 comment">
                        <div class="media-body">
                          <p class="reply" v-html="data.comments"></p>
                        </div>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
              <h6 v-else class="text-center">No Data Found</h6>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import moment from "moment";
import { mapActions, mapGetters } from "vuex";
import Select from "@/components/reusable/Fields/Select";
import {
  getFilterQueryString,
  decodePathUrlDataToObject
} from "@/helpers/helpers.js";

export default {
  name: "RecentUpdates",
  components: { Select },
  data: () => ({
    audit: {
      project_id: { id: "all", label: "All" },
      audit_type: { id: "all", label: "All" },
      date: {
        start: moment()
          .subtract(7, "days")
          .format("YYYY-MM-DD"),
        end: moment().format("YYYY-MM-DD")
      }
    },
    filter_code: {}
  }),
  computed: {
    ...mapGetters([
      "getProjects",
      "getRecentUpdates",
      "getRecentUpdatesPagination",
      "isFetchingRecentUpdates"
    ]),
    options() {
      return {
        project_id: [
          { id: "all", label: "All" },
          ...this.getProjects?.map(val => ({
            id: val.project_id,
            label: val?.project_name
          }))
        ],
        audit_type: [
          { id: "all", label: "All" },
          { id: "issue", label: "New Issue" },
          { id: "status_change", label: "Status Change" },
          { id: "comments", label: "Comments" }
        ]
      };
    }
  },
  beforeDestroy() {
    const ele = document.getElementById("container");
    if (ele) {
      ele.removeEventListener("scroll", this.onBodyScroll);
    }
  },
  methods: {
    ...mapActions(["fetchRecentUpdates","fetchProjects"]),
    showTimeDiff(date) {
      return moment
        .utc(date)
        .local()
        .fromNow(true);
    },
    handleChangeSelect(name, value) {
      Vue.set(this.audit, name, value);
      let code = value ? value.id || value.code || value : null;
      if (code == "all") code = "";
      this.filter_code = {
        ...this.filter_code,
        [name]: code
      };
      this.updateUrlWithRangeDate();
    },
    handleDatePicker() {
      this.updateUrlWithRangeDate();
    },
    updateUrlWithRangeDate() {
      let { path } = this.$route;
      let queryPayload = {
        ...this.filter_code,
        ...this.audit.date
      };
      this.$router.push(`${path}?${getFilterQueryString(queryPayload)}`);
    },
    setFilterValues() {
      let { query } = this.$route;
      this.filter_code = decodePathUrlDataToObject(query);
      for (const [key, value] of Object.entries(this.filter_code)) {
        let temp = [];
        if (key == "start" || key == "end") {
          this.audit.date[key] = value;
          continue;
        }
        if (Array.isArray(value)) {
          value.forEach(item => {
            temp = [
              ...temp,
              this.options[key].filter(val => item == val.id)[0]
            ];
          });
        } else {
          temp = this.options[key].filter(val => value == val.id)[0];
        }
        this.audit[key] = temp;
      }
      this.fetchUpdates(false);
    },
    fetchUpdates(pagination) {
      let filter = {
        project_id: this.filter_code?.project_id || "",
        date_field: "created_on",
        from_date: this.audit?.date?.start,
        to_date: this.audit?.date?.end,
        audit_view_type: this.filter_code?.audit_type == "issue" ? "issue" : "",
        audit_type:
          this.filter_code?.audit_type != "issue"
            ? this.filter_code?.audit_type || ""
            : "",
        pagination: pagination
      };
      this.fetchRecentUpdates(filter);
    },
    NavigateToProjects() {
      this.$router.push({
        path: `/list-project`
      });
    },
    navigateToIssueDetail(id) {
      this.$router.push({
        path: `/issue-detailed-view/${id}`
      });
    },
    onBodyScroll(e) {
      if (
        this.isFetchingRecentUpdates ||
        this.getRecentUpdatesPagination?.noMoreData
      )
        return;
      if (
        e.target.scrollHeight - e.target.scrollTop <=
        e.target.clientHeight + 1
      ) {
        this.fetchUpdates(true);
      }
    }
  },
  watch: {
    "$route.query": function() {
      this.setFilterValues();
    }
  },
  async mounted() {
    await this.fetchProjects();
    this.setFilterValues();
    const ele = document.getElementById("container");
    if (ele) {
      ele.addEventListener("scroll", this.onBodyScroll);
    }
  }
};
</script>

<style lang="scss" scoped>
h3 {
  margin-top: 2%;
  margin-left: 27%;
  font-weight: bold;
}
.comment-card {
  border: none;
  border-radius: 20px;
}
img {
  border-radius: 10px;
  padding-right: 5px;
  width: 60px;
  height: 55px;
}
img:hover {
  cursor: pointer;
}
.round .align-self-start {
  border-radius: 100%;
  width: 45px;
  height: 40px;
}
.media .comment {
  background: #f4f4f4;
  border: none;
  border-radius: 10px;
}
h6.project {
  font-size: 15px !important;
  padding-left: 15px !important;
  margin-bottom: 0;
  font-weight: 600;
}
p.text {
  margin-bottom: 0;
  color: #8a8a8a !important;
  font-size: 14px;
}
.ml-auto {
  margin-right: 10px;
}
p .reply {
  color: #5c5c5c;
  font-size: 15px;
}
</style>
