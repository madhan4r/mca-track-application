<template>
  <div class="d-flex justify-content-center mb-5 list-issue-page">
    <div class="col-lg-10">
      <div class="d-flex justify-content-between">
        <h5 class="font-weight-bold ml-3 navigation">
          <u>
            <a class="cursor-pointer" @click="NavigateToProjects">Projects</a>
          </u>
          >
          <u>
            <a class="cursor-pointer" @click="NavigateToIssues">
              {{ getProjectName }}
            </a>
          </u>
          > Issues
        </h5>
        <CButton
          class="btn-primary-dark small"
          v-if="getUserRole != Roles.developer"
          @click="NavigateToNewIssue()"
        >
          New Issue
        </CButton>
      </div>
      <div class="card mt-3">
        <div class="card-body text-center">
          <h4 class="card-title m-b-0">Issues</h4>
        </div>
        <issue-page-filter :reqFilters="reqFilters" />
        <div
          class="d-flex mt-3 mb-2 justify-content-between"
          style="white-space: pre"
        >
          <div class="row ml-0">
            <h5 class="font-weight-bold mr-2">
              Total Issues: {{ getIssueCounts }}
            </h5>
            <h5 class="font-weight-bold">
              Search Results:
              {{ getFilteredIssuesCount }}
            </h5>
          </div>
          <h6 class="font-weight-bold mr-2">
            <u class="cursor-pointer" @click="back()">Back</u>
          </h6>
        </div>
        <ul class="list-style-none pl-0 list-issue">
          <issue-card
            v-for="item in getIssues"
            :item="item"
            :key="item.issue_id"
          />
        </ul>
        <div v-if="getIssueCounts">
          <ul class="pagination justify-content-center">
            <li class="page-item" v-if="paginationControl.currentPage != 1">
              <a
                rel="prev"
                class="page-link"
                @click="updateUrlPageNumber(paginationControl.currentPage - 1)"
              >
                Prev
              </a>
            </li>
            <li
              class="page-item js-pagination-page"
              v-for="item in paginationControl.pages"
              :key="item"
              :class="item == paginationControl.currentPage ? 'active' : ''"
            >
              <a
                class="page-link active"
                :class="item == paginationControl.currentPage ? 'active' : ''"
                @click="updateUrlPageNumber(item)"
                >{{ item }}</a
              >
            </li>
            <li
              class="page-item js-next-button"
              v-if="
                paginationControl.currentPage < paginationControl.totalPages
              "
            >
              <a
                rel="next"
                class="page-link"
                @click="updateUrlPageNumber(paginationControl.currentPage + 1)"
                >Next
              </a>
            </li>
          </ul>
        </div>
        <h5 class="text-center font-weight-bold" v-if="!getIssues.length">
          No Issues Found!
        </h5>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import IssuePageFilter from "../components/reusable/Filter/IssuePageFilter.vue";
import IssueCard from "../components/reusable/IssueCard.vue";
import {
  decodePathUrlDataToObject,
  isEmptyObjectCheck,
  getFilterQueryString,
  Roles
} from "@/helpers/helpers.js";

export default {
  name: "ListIssue",
  components: { IssuePageFilter, IssueCard },
  data: () => ({
    currentPagePagination: 0,
    paginationControl: {},
    reqFilters: ["status_id__in", "type_id__in", "module_id__in"],
    Roles
  }),
  computed: {
    ...mapGetters([
      "getSelectedProject",
      "getListIssues",
      "getIssueCounts",
      "getFilteredIssuesCount",
      "getUserRole"
    ]),
    getProjectName() {
      return this.getSelectedProject?.project_name || "Project";
    },
    getIssues() {
      return (
        this.getListIssues.map(val => ({
          ...val,
          project_: val.project?.project_name,
          status_: val.status?.status,
          type_: val.type?.type,
          created_user_: `${val?.created_user?.first_name} ${val?.created_user?.last_name}`
        })) || []
      );
    }
  },
  watch: {
    "$route.query"() {
      this.fetchIssues();
    }
  },
  methods: {
    ...mapActions([
      "fetchListIssues",
      "fetchIssueCounts",
      "fetchFilteredIssuesCount"
    ]),
    back() {
      this.$router.go(-1);
    },
    NavigateToProjects() {
      this.$router.push({
        path: `/list-project`
      });
    },
    NavigateToIssues() {
      this.$router.push({
        path: `/list-project-issue/${this.getSelectedProject?.project_id}?page=%5B1%5D`
      });
    },
    NavigateToNewIssue() {
      this.$router.push({
        path: `/new-issue/project/${this.getSelectedProject?.project_id}`
      });
    },
    updateUrlPageNumber(pageNumber) {
      let { path, query } = this.$route;
      let encodedQuery = decodePathUrlDataToObject(query);
      encodedQuery["page"] = pageNumber;
      this.$router.push({
        path: `${path}?${getFilterQueryString(encodedQuery)}`
      });
    },
    async fetchIssues() {
      let {
        params: { project_id },
        query
      } = this.$route;
      let encodedQuery = decodePathUrlDataToObject(query);
      let { page, ...rest } = encodedQuery;
      if (!isEmptyObjectCheck(rest)) {
        await this.fetchFilteredIssuesCount({ project_id, ...rest });
        this.paginationControl = this.paginate(
          this.getFilteredIssuesCount,
          page
        );
      } else {
        this.$store.commit("SET_FILTERED_ISSUES_COUNT", 0);
        this.paginationControl = this.paginate(this.getIssueCounts, page);
      }
      if (page != this.paginationControl.currentPage) {
        this.updateUrlPageNumber(this.paginationControl.currentPage);
      } else {
        this.fetchListIssues({
          project_id,
          currentPage: this.paginationControl.currentPage,
          ...rest
        });
      }
    },
    paginate(totalItems, currentPage) {
      let pageSize = 5;
      let maxPages = 5;
      // calculate total pages
      let totalPages = Math.ceil(totalItems / pageSize);

      // ensure current page isn't out of range
      if (currentPage < 1) {
        currentPage = 1;
      } else if (currentPage > totalPages) {
        currentPage = totalPages;
      }
      let startPage, endPage;
      if (totalPages <= maxPages) {
        // total pages less than max so show all pages
        startPage = 1;
        endPage = totalPages;
      } else {
        // total pages more than max so calculate start and end pages
        let maxPagesBeforeCurrentPage = Math.floor(maxPages / 2);
        let maxPagesAfterCurrentPage = Math.ceil(maxPages / 2) - 1;
        if (currentPage <= maxPagesBeforeCurrentPage) {
          // current page near the start
          startPage = 1;
          endPage = maxPages;
        } else if (currentPage + maxPagesAfterCurrentPage >= totalPages) {
          // current page near the end
          startPage = totalPages - maxPages + 1;
          endPage = totalPages;
        } else {
          // current page somewhere in the middle
          startPage = currentPage - maxPagesBeforeCurrentPage;
          endPage = currentPage + maxPagesAfterCurrentPage;
        }
      }

      // calculate start and end item indexes
      let startIndex = (currentPage - 1) * pageSize;
      let endIndex = Math.min(startIndex + pageSize - 1, totalItems - 1);

      // create an array of pages to ng-repeat in the pager control
      let pages = Array.from(Array(endPage + 1 - startPage).keys()).map(
        i => startPage + i
      );

      // return object with all pager properties required by the view
      return {
        totalItems: totalItems,
        currentPage: currentPage || 1,
        pageSize: pageSize,
        totalPages: totalPages,
        startPage: startPage,
        endPage: endPage,
        startIndex: startIndex,
        endIndex: endIndex,
        pages: pages
      };
    }
  },
  async mounted() {
    let {
      params: { project_id }
    } = this.$route;
    await this.fetchIssueCounts({ project_id: project_id });
    this.fetchIssues();
  }
};
</script>

<style lang="scss" scoped>
.page-link {
  color: black !important;
}
</style>
