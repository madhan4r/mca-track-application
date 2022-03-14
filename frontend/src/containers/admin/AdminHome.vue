<template>
  <div>
    <div class="container mt-3 mb-4">
      <div class="col-lg-12 mt-4 mt-lg-0">
        <CRow class="justify-content-end mr-0 mb-3">
          <CButton class="btn-primary mr-2" @click="createUser()"
            >New User</CButton
          >
          <CButton class="btn-primary" @click="createProject()"
            >New Project</CButton
          >
        </CRow>
        <CTabs variant="pills" :active-tab="0" :fill="true">
          <CTab title="Users">
            <div class="row">
              <div class="col-md-12">
                <div
                  class="user-dashboard-info-box table-responsive mb-0 bg-white p-4 shadow-sm"
                >
                  <table class="table manage-candidates-top mb-0">
                    <tbody>
                      <tr
                        class="candidates-list"
                        v-for="item in getUsers"
                        :key="item.id"
                      >
                        <td class="title">
                          <div class="thumb">
                            <img
                              class="img-fluid"
                              src="https://bootdey.com/img/Content/avatar/avatar2.png"
                              alt=""
                            />
                          </div>
                          <div class="candidate-list-details">
                            <div class="candidate-list-info">
                              <div class="candidate-list-title">
                                <h5 class="mb-0">{{ item.label }}</h5>
                              </div>
                              <div class="candidate-list-option">
                                <ul class="list-unstyled">
                                  <li v-c-tooltip="'Email'">
                                    {{ item.email }}
                                  </li>
                                  <li v-c-tooltip="'Role'">
                                    {{
                                      item.user_role == " lead"
                                        ? "Leader"
                                        : "Developer"
                                    }}
                                  </li>
                                </ul>
                              </div>
                            </div>
                          </div>
                        </td>
                        <td class="candidate-list-favourite-time text-center">
                          <span class="candidate-list-time order-1"
                            >Active</span
                          >
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </CTab>
          <CTab title="Projects">
            <div class="row">
              <div class="col-md-12">
                <div
                  class="user-dashboard-info-box table-responsive mb-0 bg-white p-4 shadow-sm"
                >
                  <table class="table manage-candidates-top mb-0">
                    <tbody>
                      <tr
                        class="candidates-list"
                        v-for="item in getProjects"
                        :key="item.project_id"
                      >
                        <td class="title">
                          <div class="thumb">
                            <img
                              class="img-fluid"
                              src="img/techno_icon.png"
                              alt=""
                            />
                          </div>
                          <div class="candidate-list-details">
                            <div class="candidate-list-info">
                              <div class="candidate-list-title">
                                <h5 class="mb-0">{{ item.project_name }}</h5>
                              </div>
                            </div>
                          </div>
                        </td>
                        <td class="candidate-list-favourite-time text-center">
                          <span class="candidate-list-time order-1">
                            Total Issues: {{ item.issue_count }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </CTab>
        </CTabs>
      </div>
    </div>
    <new-user :isShowPopup="popupForUser" @modalCallBack="userModalCallBack" />
    <new-projects
      :isShowPopup="popupForProject"
      @modalCallBack="projectModalCallBack"
    />
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import NewUser from "./NewUser.vue";
import NewProjects from "./NewProjects.vue";
export default {
  components: { NewUser, NewProjects },
  name: "AdminHome",
  data: () => ({
    popupForUser: false,
    popupForProject: false
  }),
  computed: {
    ...mapGetters(["getUsers", "getProjects"]),
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
    ...mapActions(["fetchUsers", "fetchProjects"]),
    createProject() {
      this.popupForProject = true;
    },
    createUser() {
      this.popupForUser = true;
    },
    userModalCallBack(action) {
      if (action) {
        this.fetchUsers();
      }
      this.popupForUser = false;
    },
    projectModalCallBack(action) {
      if (action) {
        this.fetchProjects();
      }
      this.popupForProject = false;
    }
  },
  mounted() {
    this.fetchUsers();
    this.fetchProjects();
  }
};
</script>
<style scoped>
body {
  background-color: #f8f9fa !important;
}
.p-4 {
  padding: 1.5rem !important;
}
.mb-0,
.my-0 {
  margin-bottom: 0 !important;
}
.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}
/* user-dashboard-info-box */
.user-dashboard-info-box .candidates-list .thumb {
  margin-right: 20px;
}
.user-dashboard-info-box .candidates-list .thumb img {
  width: 80px;
  height: 80px;
  -o-object-fit: cover;
  object-fit: cover;
  overflow: hidden;
  border-radius: 50%;
}

.user-dashboard-info-box .title {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  padding: 30px 0;
}

.user-dashboard-info-box .candidates-list td {
  vertical-align: middle;
}

.user-dashboard-info-box td li {
  margin: 0 4px;
}

.user-dashboard-info-box .table thead th {
  border-bottom: none;
}

.table.manage-candidates-top th {
  border: 0;
}

.user-dashboard-info-box
  .candidate-list-favourite-time
  .candidate-list-favourite {
  margin-bottom: 10px;
}

.table.manage-candidates-top {
  min-width: 650px;
}

.user-dashboard-info-box .candidate-list-details ul {
  color: #969696;
}

/* Candidate List */
.candidate-list {
  background: #ffffff;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  border-bottom: 1px solid #eeeeee;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  padding: 20px;
  -webkit-transition: all 0.3s ease-in-out;
  transition: all 0.3s ease-in-out;
}
.candidate-list:hover {
  -webkit-box-shadow: 0px 0px 34px 4px rgba(33, 37, 41, 0.06);
  box-shadow: 0px 0px 34px 4px rgba(33, 37, 41, 0.06);
  position: relative;
  z-index: 99;
}
.candidate-list:hover a.candidate-list-favourite {
  color: #e74c3c;
  -webkit-box-shadow: -1px 4px 10px 1px rgba(24, 111, 201, 0.1);
  box-shadow: -1px 4px 10px 1px rgba(24, 111, 201, 0.1);
}

.candidate-list .candidate-list-image {
  margin-right: 25px;
  -webkit-box-flex: 0;
  -ms-flex: 0 0 80px;
  flex: 0 0 80px;
  border: none;
}
.candidate-list .candidate-list-image img {
  width: 80px;
  height: 80px;
  -o-object-fit: cover;
  object-fit: cover;
}

.candidate-list-title {
  margin-bottom: 5px;
}

.candidate-list-details ul {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  margin-bottom: 0px;
}
.candidate-list-details ul li {
  margin: 5px 10px 5px 0px;
  font-size: 13px;
}

.candidate-list .candidate-list-favourite-time {
  margin-left: auto;
  text-align: center;
  font-size: 13px;
  -webkit-box-flex: 0;
  -ms-flex: 0 0 90px;
  flex: 0 0 90px;
}
.candidate-list .candidate-list-favourite-time span {
  display: block;
  margin: 0 auto;
}
.candidate-list .candidate-list-favourite-time .candidate-list-favourite {
  display: inline-block;
  position: relative;
  height: 40px;
  width: 40px;
  line-height: 40px;
  border: 1px solid #eeeeee;
  border-radius: 100%;
  text-align: center;
  -webkit-transition: all 0.3s ease-in-out;
  transition: all 0.3s ease-in-out;
  margin-bottom: 20px;
  font-size: 16px;
  color: #646f79;
}
.candidate-list .candidate-list-favourite-time .candidate-list-favourite:hover {
  background: #ffffff;
  color: #e74c3c;
}

.candidate-banner .candidate-list:hover {
  position: inherit;
  -webkit-box-shadow: inherit;
  box-shadow: inherit;
  z-index: inherit;
}

.bg-white {
  background-color: #ffffff !important;
}
.p-4 {
  padding: 1.5rem !important;
}
.mb-0,
.my-0 {
  margin-bottom: 0 !important;
}
.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}

.user-dashboard-info-box .candidates-list .thumb {
  margin-right: 20px;
}
</style>
