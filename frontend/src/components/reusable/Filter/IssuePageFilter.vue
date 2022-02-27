<template>
  <div>
    <div class="search_div row ml-0">
      <div class="search col-lg-10 d-flex my-1">
        <div class="text-input w-100">
          <input
            type="text"
            name="searchTerm"
            placeholder="Search Issue by Title, ID"
            onkeydown=""
            autocomplete=""
            class="m-0 form-control"
            @input="handleSearchInput($event.target.value)"
            v-on:keyup.enter="updateUrlWithSearch()"
            :value="searchTerm"
          />
        </div>
        <CButton class="btn-primary ml-2 px-3" @click="updateUrlWithSearch()">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-search"
            viewBox="0 0 16 16"
          >
            <path
              d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"
            />
          </svg>
        </CButton>
      </div>
      <div class="col-2 my-1">
        <button
          type="button"
          class="btn d-flex btn-primary"
          @click="toggleFilterBar()"
        >
          Filter
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            role="img"
            class="c-icon c-icon-sm"
          >
            <path
              d="M11.186 23.25h-2.186v-11.352l-7.875-9.375v-1.773h21.375v1.763l-7.5 9.375v7.548zM10.5 21.75h0.064l2.936-2.936v-7.452l7.29-9.112h-17.935l7.646 9.102z"
            ></path>
          </svg>
        </button>
      </div>
    </div>
    <div>
      <div class="mt-2 filter-details d-inline-block" v-if="payload.searchTerm">
        <div class="filter-details-item d-flex vs__selected-options">
          <span>Search Term:</span>
          <div class="m-0 ml-1 vs__selected">
            {{ payload.searchTerm }}
            <button
              type="button"
              class="vs__deselect"
              @click="
                searchTerm = '';
                updateUrlWithSearch();
              "
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">
                <path
                  d="M6.895455 5l2.842897-2.842898c.348864-.348863.348864-.914488 0-1.263636L9.106534.261648c-.348864-.348864-.914489-.348864-1.263636 0L5 3.104545 2.157102.261648c-.348863-.348864-.914488-.348864-1.263636 0L.261648.893466c-.348864.348864-.348864.914489 0 1.263636L3.104545 5 .261648 7.842898c-.348864.348863-.348864.914488 0 1.263636l.631818.631818c.348864.348864.914773.348864 1.263636 0L5 6.895455l2.842898 2.842897c.348863.348864.914772.348864 1.263636 0l.631818-.631818c.348864-.348864.348864-.914489 0-1.263636L6.895455 5z"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div
        v-for="(value, index) of this.filters"
        :key="index"
        class="d-inline-block"
      >
        <div v-if="value.length" class="d-inline-block">
          <div class="mt-2 filter-details d-inline-block">
            <div class="filter-details-item d-flex vs__selected-options">
              <span>{{ value[0].display_text }}:</span>
              <div
                class="m-0 ml-1 vs__selected"
                v-for="item in value"
                :key="item.id"
              >
                {{ item.label }}
                <button
                  type="button"
                  class="vs__deselect"
                  @click="removeSelectedFilter(index, item)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="10"
                    height="10"
                  >
                    <path
                      d="M6.895455 5l2.842897-2.842898c.348864-.348863.348864-.914488 0-1.263636L9.106534.261648c-.348864-.348864-.914489-.348864-1.263636 0L5 3.104545 2.157102.261648c-.348863-.348864-.914488-.348864-1.263636 0L.261648.893466c-.348864.348864-.348864.914489 0 1.263636L3.104545 5 .261648 7.842898c-.348864.348863-.348864.914488 0 1.263636l.631818.631818c.348864.348864.914773.348864 1.263636 0L5 6.895455l2.842898 2.842897c.348863.348864.914772.348864 1.263636 0l.631818-.631818c.348864-.348864.348864-.914489 0-1.263636L6.895455 5z"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="d-inline-block">
          <div class="mt-2 filter-details d-inline-block">
            <div class="filter-details-item d-flex vs__selected-options">
              <span>{{ value.display_text }}:</span>
              <div class="m-0 ml-1 vs__selected">
                {{ value.label }}
                <button
                  type="button"
                  class="vs__deselect"
                  @click="removeSelectedFilter(index, value)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="10"
                    height="10"
                  >
                    <path
                      d="M6.895455 5l2.842897-2.842898c.348864-.348863.348864-.914488 0-1.263636L9.106534.261648c-.348864-.348864-.914489-.348864-1.263636 0L5 3.104545 2.157102.261648c-.348863-.348864-.914488-.348864-1.263636 0L.261648.893466c-.348864.348864-.348864.914489 0 1.263636L3.104545 5 .261648 7.842898c-.348864.348863-.348864.914488 0 1.263636l.631818.631818c.348864.348864.914773.348864 1.263636 0L5 6.895455l2.842898 2.842897c.348863.348864.914772.348864 1.263636 0l.631818-.631818c.348864-.348864.348864-.914489 0-1.263636L6.895455 5z"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <sidebar :show="showFilter" :toggleSideBar="toggleFilterBar">
      <template #header>
        <div class="mt-2 p-2 d-flex">
          <CButton
            @click="toggleFilterBar()"
            class="btn-primary pl-1 pr-1 pt-1 pb-0"
          >
            <span class="material-icons">
              arrow_forward
            </span>
          </CButton>
          <h5 class="w-100 pt-2 text-center font-weight-bold">
            Custom Filter
          </h5>
        </div>
      </template>
      <div>
        <CRow
          class="pl-3 pr-3 pt-2"
          v-if="
            reqFilters.includes('assigned_to__in') &&
              options &&
              options['assigned_to__in']
          "
        >
          <label class="col-lg-12 col-md-12 font-weight-bold">Assignee</label>
          <div class="col-lg-12 col-md-12 col-sm-12">
            <Select
              name="assigned_to__in"
              :value="filters.assigned_to__in"
              @input="handleChangeSelect"
              :options="
                options && options['assigned_to__in']
                  ? options['assigned_to__in']
                  : []
              "
              :taggable="false"
              :multiple="true"
              :clearable="true"
              placeholder="All"
            />
          </div>
        </CRow>
        <CRow
          class="pl-3 pr-3 pt-3"
          v-if="reqFilters.includes('project_id__in')"
        >
          <label class="col-lg-12 col-md-12 font-weight-bold">Project</label>
          <div class="col-lg-12 col-md-12 col-sm-12">
            <Select
              name="project_id__in"
              :value="filters.project_id__in"
              @input="handleChangeSelect"
              :options="
                options && options['project_id__in']
                  ? options['project_id__in']
                  : []
              "
              :taggable="false"
              :multiple="true"
              :clearable="true"
              placeholder="All"
            />
          </div>
        </CRow>
        <CRow
          class="pl-3 pr-3 pt-3"
          v-if="reqFilters.includes('status_id__in')"
        >
          <label class="col-lg-12 col-md-12 font-weight-bold"
            >Issue Status</label
          >
          <div class="col-lg-12 col-md-12 col-sm-12">
            <Select
              name="status_id__in"
              :value="filters.status_id__in"
              @input="handleChangeSelect"
              :options="
                options && options['status_id__in']
                  ? options['status_id__in']
                  : []
              "
              :taggable="false"
              :multiple="true"
              :clearable="true"
              placeholder="All"
            />
          </div>
        </CRow>
        <CRow class="pl-3 pr-3 pt-2" v-if="reqFilters.includes('type_id__in')">
          <label class="col-lg-12 col-md-12 font-weight-bold">Issue Type</label>
          <div class="col-lg-12 col-md-12 col-sm-12">
            <Select
              name="type_id__in"
              :value="filters.type_id__in"
              @input="handleChangeSelect"
              :options="
                options && options['type_id__in'] ? options['type_id__in'] : []
              "
              :taggable="false"
              :multiple="true"
              :clearable="true"
              placeholder="All"
            />
          </div>
        </CRow>
        <CRow
          class="pl-3 pr-3 pt-2"
          v-if="reqFilters.includes('module_id__in')"
        >
          <label class="col-lg-12 col-md-12 font-weight-bold"
            >Issue Module</label
          >
          <div class="col-lg-12 col-md-12 col-sm-12">
            <Select
              name="module_id__in"
              :value="filters.module_id__in"
              @input="handleChangeSelect"
              :options="
                options && options['module_id__in']
                  ? options['module_id__in']
                  : []
              "
              :taggable="false"
              :multiple="true"
              :clearable="true"
              placeholder="All"
            />
          </div>
        </CRow>
      </div>
    </sidebar>
  </div>
</template>
<script>
import Vue from "vue";
import { mapActions, mapGetters } from "vuex";
import Sidebar from "./Sidebar.vue";
import Select from "../Fields/Select.vue";
import {
  getFilterQueryString,
  decodePathUrlDataToObject
} from "@/helpers/helpers.js";
export default {
  name: "IssuePageFilter",
  props: {
    reqFilters: {
      type: Array,
      default: () => ["status_id__in", "type_id__in"]
    }
  },
  data: () => ({
    filters: {},
    payload: {},
    searchTerm: ""
  }),
  components: { Sidebar, Select },
  computed: {
    ...mapGetters([
      "showFilter",
      "getIssueTypes",
      "getIssueStatus",
      "getProjectModule",
      "getOrganizationProjects",
      "getOrganizationUsers"
    ]),
    options() {
      return {
        type_id__in:
          this.getIssueTypes?.map(val => ({
            ...val,
            display_text: "Issue Type"
          })) || [],
        status_id__in:
          this.getIssueStatus?.map(val => ({
            ...val,
            display_text: "Issue Status"
          })) || [],
        module_id__in:
          this.getProjectModule?.map(val => ({
            ...val,
            display_text: "Module"
          })) || [],
        project_id__in:
          this.getOrganizationProjects?.map(val => ({
            id: val.project_id,
            label: val?.project?.project_name,
            display_text: "Project"
          })) || [],
        assigned_to__in:
          this.getOrganizationUsers?.map(val => ({
            ...val,
            display_text: "Assignee"
          })) || []
      };
    }
  },
  methods: {
    ...mapActions(["toggleFilterBar", "initIssuePageFilterOptions"]),
    handleSearchInput(value) {
      this.searchTerm = value;
    },
    handleChangeSelect(name, value) {
      Vue.set(this.filters, name, value);
      let code = null;
      if (Array.isArray(value)) {
        code = value?.map(val => (val ? val.id || val.code || val : null));
        if (!code.length) code = "";
      } else {
        code = value ? value.id || value.code || value : null;
      }
      this.payload = {
        ...this.payload,
        [name]: code
      };
      this.updateUrl();
    },
    updateUrl() {
      let { path } = this.$route;
      this.$router.push(
        `${path}?${getFilterQueryString(this.payload)}&page=%5B1%5D`
      );
    },
    updateUrlWithSearch() {
      let { path } = this.$route;
      let queryPayload = {
        ...this.payload,
        searchTerm: this.searchTerm
      };
      this.$router.push(
        `${path}?${getFilterQueryString(queryPayload)}&page=%5B1%5D`
      );
    },
    setFilterValues() {
      let { query } = this.$route;
      delete query.page;
      this.filters = {};
      this.payload = decodePathUrlDataToObject(query);
      for (const [key, value] of Object.entries(this.payload)) {
        let temp = [];
        if (key == "searchTerm") {
          this.searchTerm = value;
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
        this.filters[key] = temp;
      }
    },
    removeSelectedFilter(key, value) {
      if (Array.isArray(this.payload[key]) && this.payload[key]?.length > 1) {
        const index = this.payload[key].indexOf(value.id);
        this.payload[key].splice(index, 1);
      } else {
        this.payload[key] = "";
      }
      this.updateUrl();
    }
  },
  watch: {
    "$route.query": function() {
      this.setFilterValues();
    }
  },
  mounted() {
    let {
      params: { project_id }
    } = this.$route;
    this.initIssuePageFilterOptions({
      project_id: project_id || "",
      filters: this.reqFilters
    }).then(() => {
      this.setFilterValues();
    });
  }
};
</script>
<style lang="scss" scoped>
.search_div {
  width: 100%;
  display: flex;
  padding: 4px 0;
  border: 1px solid #c9cbce;
  color: #00626a;
  background-color: var(--search-div);
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
}
.vs__selected-options {
  -ms-flex-preferred-size: 100%;
  flex-basis: 100%;
  -webkit-box-flex: 1;
  -ms-flex-positive: 1;
  flex-grow: 1;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  padding: 0 2px;
  position: relative;
}
</style>
