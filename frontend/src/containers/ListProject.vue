<template>
  <div class="list-project-body">
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-12">
          <div
            class="d-flex justify-content-center align-items-center activity"
          >
            <h4 class="font-weight-bold ml-3">Projects</h4>
          </div>
          <div class="search_div row ml-0 mt-4">
            <div class="search col-lg-12 d-flex my-1">
              <div class="text-input w-100">
                <input
                  type="text"
                  name="searchTerm"
                  placeholder="Search Issue by Title, ID"
                  onkeydown=""
                  autocomplete=""
                  class="m-0 form-control"
                  @input="handleSearchInput($event.target.value)"
                  v-on:keyup.enter="routeToListGlobalIssuePage()"
                  :value="searchTerm"
                />
              </div>
              <CButton
                class="btn-primary ml-2 px-3"
                @click="routeToListGlobalIssuePage()"
              >
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
          </div>
          <div class="mt-3 mb-5 pb-3">
            <ul class="list list-inline">
              <li
                class="d-flex justify-content-between"
                v-for="item in getProject"
                :key="item.project_id"
              >
                <div class="d-flex flex-row align-items-center">
                  <div class="d-flex flex-column mr-2">
                    <div class="profile-image">
                      <img
                        class="rounded-circle"
                        src="img/techno_icon.png"
                        width="30"
                        alt="project_logo"
                      />
                    </div>
                  </div>
                  <div class="ml-2">
                    <h5
                      class="mb-0 cursor-pointer font-weight-bold"
                      @click="navigateToIssue(item)"
                    >
                      {{ item.project_name }}
                      {{ item.issue_count ? ` [${item.issue_count}]` : "" }}
                    </h5>
                  </div>
                </div>
                <div
                  class="d-flex flex-row align-items-center"
                  v-if="item.open_issue_count"
                >
                  <strong v-c-tooltip="'Issue Status'" style="color: #2da160">{{
                    item.open_issue_count
                      ? `(Open ${item.open_issue_count})`
                      : ""
                  }}</strong>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "ListProject",
  data: () => ({ searchTerm: "" }),
  computed: {
    ...mapGetters(["getProjects"]),
    getProject() {
      return (
        this.getProjects?.map(val => ({
          project_id: val.project_id,
          project_name: val?.project_name,
          issue_count: val.issue_count,
          open_issue_count: val.open_issue_count
        })) || []
      );
    }
  },
  methods: {
    navigateToIssue(item) {
      this.$router.push({
        path: `/list-project-issue/${item?.project_id}?page=%5B1%5D`
      });
    },
    handleSearchInput(value) {
      this.searchTerm = value;
    },
    routeToListGlobalIssuePage() {
      if (this.searchTerm) {
        this.$router.push({
          path: `/global-issues?searchTerm=%5B${this.searchTerm}%5D&page=%5B1%5D`
        });
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.list-group li {
  margin-bottom: 12px;
}

.list li {
  list-style: none;
  padding: 15px;
  border: 1px solid #e3dada;
  margin-top: 12px;
  border-radius: 5px;
  background: #fff;
}

.checkicon {
  color: green;
  font-size: 19px;
}

.date-time {
  font-size: 12px;
}

.profile-image img {
  margin-left: 3px;
}

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
</style>
