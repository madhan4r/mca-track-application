<template>
  <div class="d-flex justify-content-center">
    <div class="col-lg-10">
      <div class="d-flex justify-content-between">
        <h5 class="font-weight-bold pt-2 pl-3 navigation">
          <u>
            <a class="cursor-pointer" @click="navigateToProjects">Projects</a>
          </u>
          >
          <u>
            <a class="cursor-pointer" @click="navigateToProjects"
              >{{ getProjectName }}
            </a>
          </u>
          >
          <u><a class="cursor-pointer" @click="back()">issues</a></u>
          #{{ getIssueID }}
          <CBadge
            :color="getBadgeColor(getType)"
            class="ml-2 rounded-1"
            style="font-size: 90%"
            v-c-tooltip="'Issue Type'"
            >{{ getType }}</CBadge
          >
        </h5>
        <CButton class="btn-primary-dark small" @click="editIssue()"
          >Edit Issue</CButton
        >
      </div>
      <div class="text-right mt-3">
        <h6 class="font-weight-bold back-navigation">
          <u class="cursor-pointer" @click="back()">Back</u>
        </h6>
      </div>
      <hr />
      <div class="pl-3">
        <CBadge
          class="rounded-2 p-2"
          style="font-size: 95%"
          :color="getBadgeColor(getStatus)"
          v-c-tooltip="'Issue Status'"
          >{{ getStatus }}</CBadge
        >
        <span class="ml-2"
          >Created {{ showTimeDiff(createdOn) }} ago by
          <b>{{ createdUser }}</b>
        </span>
      </div>
      <hr />
      <h4 class="font-weight-bold pl-3 issue-title dynamic-title">
        {{ getTitle }}
      </h4>
      <h6 class="pl-3 issue-data" v-html="getDescription"></h6>
      <hr />
      <CRow class="ml-3 issue-data">
        <CCol lg="3"><b>Module :</b> {{ getModule }} </CCol>
        <CCol lg="2"><b>Priority :</b> {{ getPriority }} </CCol>
        <CCol lg="2"><b>Assignee :</b> {{ getAssignee }} </CCol>
        <CCol lg="3"><b>Milestone :</b> {{ getMilestone }} </CCol>
        <CCol lg="2">
          <b>Gitlab Issue Id :</b>
          <a
            :href="`https://gitlab.com/screel/ohr/-/issues/${getGitlabIssueID}`"
            class="cursor-pointer"
            style="color: #3c4b64"
            target="_blank"
            v-if="getGitlabIssueID"
          >
            #{{ getGitlabIssueID }}
          </a>
          <a href="#" target="_self" style="color: #3c4b64" v-else> --</a>
        </CCol>
      </CRow>
      <hr />
      <div class="Audit-History">
        <div class="container timeline-scrolling" id="history-info">
          <div class="row">
            <div class="col-md-12">
              <ul
                class="timeline pt-3"
                v-for="item in getAudits"
                :key="item.audit_id"
              >
                <li v-if="item.audit_type == 'comments'">
                  <time class="time m-0">
                    <span>{{ formatTime(item.created_on) }}</span>
                    <span>{{ formatDate(item.created_on) }}</span>
                  </time>

                  <div class="icon" style="background-color: green">
                    <em
                      class="material-icons"
                      style="color: white;line-height: 40px"
                    >
                      comment
                    </em>
                  </div>
                  <div class="label">
                    <p class="h6">
                      <strong>
                        @{{ formatName(item.created_username) }}
                        {{
                          item.created_username_role == "developer"
                            ? "(developer) "
                            : ""
                        }}· {{ showTimeDiff(item.created_on) }} ago
                      </strong>
                    </p>
                    <p class="mb-0">
                      <span style="line-height: normal" v-html="item.comments">
                      </span>
                    </p>
                  </div>
                </li>
                <li v-if="item.audit_type == 'status_change'">
                  <time class="time m-0">
                    <span>{{ formatTime(item.created_on) }}</span>
                    <span>{{ formatDate(item.created_on) }}</span>
                  </time>

                  <div class="icon" style="background-color: saddlebrown">
                    <em
                      class="material-icons"
                      style="color: white;line-height: 40px"
                      >work
                    </em>
                  </div>
                  <div class="label">
                    <p>
                      <span class="h6">
                        <strong
                          >@{{ formatName(item.created_username) }}
                        </strong>
                      </span>
                      <span
                        >updated the status from
                        <b>{{ item.previous_status_name }}</b> to
                        <b>{{ item.updated_status_name }}</b>
                      </span>
                      ·
                      <strong>{{ showTimeDiff(item.created_on) }} ago</strong>
                    </p>
                  </div>
                </li>
                <li v-if="item.audit_type == 'type_change'">
                  <time class="time m-0">
                    <span>{{ formatTime(item.created_on) }}</span>
                    <span>{{ formatDate(item.created_on) }}</span>
                  </time>

                  <div class="icon" style="background-color: deepskyblue">
                    <em
                      class="material-icons"
                      style="color: white;line-height: 40px"
                      >sync_alt
                    </em>
                  </div>
                  <div class="label">
                    <p>
                      <span class="h6">
                        <strong>
                          @{{ formatName(item.created_username) }}
                        </strong>
                      </span>
                      <span
                        >updated the type from
                        <b>{{ item.previous_type_name }}</b> to
                        <b>{{ item.updated_type_name }}</b>
                      </span>
                      ·
                      <strong>{{ showTimeDiff(item.created_on) }} ago</strong>
                    </p>
                  </div>
                </li>
                <li v-if="item.audit_type == 'milestone_change'">
                  <time class="time m-0">
                    <span>{{ formatTime(item.created_on) }}</span>
                    <span>{{ formatDate(item.created_on) }}</span>
                  </time>

                  <div class="icon" style="background-color: tomato">
                    <em
                      class="material-icons"
                      style="color: white;line-height: 40px"
                    >
                      date_range
                    </em>
                  </div>
                  <div class="label">
                    <p>
                      <span class="h6">
                        <strong>
                          @{{ formatName(item.created_username) }}
                        </strong>
                      </span>
                      <span
                        >updated the milestone
                        <b>{{
                          item.previous_milestone_name
                            ? `from ${item.previous_milestone_name}`
                            : ""
                        }}</b>
                        to <b>{{ item.updated_milestone_name }}</b>
                      </span>
                      ·
                      <strong>{{ showTimeDiff(item.created_on) }} ago</strong>
                    </p>
                  </div>
                </li>
                <li v-if="item.audit_type == 'assignee_change'">
                  <time class="time m-0">
                    <span>{{ formatTime(item.created_on) }}</span>
                    <span>{{ formatDate(item.created_on) }}</span>
                  </time>

                  <div class="icon" style="background-color: darkviolet">
                    <em
                      class="material-icons"
                      style="color: white;line-height: 40px"
                    >
                      manage_accounts
                    </em>
                  </div>
                  <div class="label">
                    <p>
                      <span class="h6">
                        <strong>
                          @{{ formatName(item.created_username) }}
                          {{
                            item.created_username_role == "developer"
                              ? "(developer)"
                              : ""
                          }}
                        </strong>
                      </span>
                      <span>
                        updated the assignee
                        <strong>
                          {{
                            item.previous_assignee_name
                              ? `from ${item.previous_assignee_name}`
                              : ""
                          }}</strong
                        >
                        to <strong>{{ item.updated_assignee_name }}</strong>
                      </span>
                      ·
                      <strong>{{ showTimeDiff(item.created_on) }} ago</strong>
                    </p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <CRow class="pl-3 pr-3">
        <CCol md="12" class="mb-3">
          <CRow class="row">
            <div class="col-lg-12 col-md-12 col-sm-12">
              <!--Whenever vue-editor is used Advert-section class name should be given which makes <strong> tag to bolder(visible) -->
              <vue-editor
                class="advert-section"
                name="comments"
                :value="audit.comments"
                @input="handleEditor"
                placeholder="Write a comment"
              ></vue-editor>
            </div>
          </CRow>
        </CCol>
      </CRow>
      <CRow class="ml-3 mb-5 pb-3">
        <CButton
          class="btn-primary-dark"
          @click="createComment()"
          :disabled="!audit.comments"
          >Comment</CButton
        >
      </CRow>
    </div>
    <edit-issue-modal
      v-if="editModal.isShowPopup"
      :isShowPopup="editModal.isShowPopup"
      :issueData="editModal.issueData"
      @updateModalCallBack="modalCallBack"
    />
  </div>
</template>

<script>
import m from "moment";
import { mapActions, mapGetters } from "vuex";
import Vue from "vue";
import EditIssueModal from "./EditIssueModal.vue";
export default {
  components: { EditIssueModal },
  name: "IssueDetail",
  data: () => ({
    audit: {},
    payload: {},
    editModal: {
      isShowPopup: false,
      issueData: {}
    }
  }),
  computed: {
    ...mapGetters(["getSelectedIssue", "getAuditIssue"]),
    getProjectName() {
      return this.getSelectedIssue?.project?.project_name || "";
    },
    getIssueID() {
      return this.getSelectedIssue?.issue_id || "";
    },
    getStatus() {
      return this.getSelectedIssue?.status?.status || "";
    },
    getType() {
      return this.getSelectedIssue?.type?.type || "";
    },
    getModule() {
      return this.getSelectedIssue?.module?.module?.module_name || "--";
    },
    getGitlabIssueID() {
      return this.getSelectedIssue?.gitlab_issue_id || "";
    },
    getPriority() {
      return this.getSelectedIssue?.priority?.issue_priority || "--";
    },
    getMilestone() {
      return this.getSelectedIssue?.milestone_id
        ? `${
            this.getSelectedIssue?.milestone?.milestone?.milestone
          } / ${this.formatDate(
            this.getSelectedIssue?.milestone?.milestone?.milestone_date
          )}`
        : "--";
    },
    getAssignee() {
      return this.getSelectedIssue?.assigned_to
        ? `${this.getSelectedIssue?.assigned_to_user?.first_name} ${this.getSelectedIssue?.assigned_to_user?.last_name}`
        : "";
    },
    createdUser() {
      return (
        `${this.getSelectedIssue?.created_user?.first_name} ${this.getSelectedIssue?.created_user?.last_name}` ||
        ""
      );
    },
    createdOn() {
      return this.getSelectedIssue?.created_on || "";
    },
    getTitle() {
      return this.getSelectedIssue?.issue_title || "";
    },
    getDescription() {
      return this.getSelectedIssue?.issue_description || "---";
    },
    getAudits() {
      return this.getAuditIssue?.map(val => ({
        ...val,
        created_username: val?.created_user?.first_name,
        previous_status_name: val?.previous_status?.status,
        updated_status_name: val?.updated_status?.status,
        previous_type_name: val?.previous_type?.type,
        updated_type_name: val?.updated_type?.type,
        previous_milestone_name: val?.previous_milestone?.milestone_id
          ? `${
              val?.previous_milestone?.milestone?.milestone
            } / ${this.formatDate(
              val?.previous_milestone?.milestone?.milestone_date
            )}`
          : "",
        updated_milestone_name: `${
          val?.updated_milestone?.milestone?.milestone
        } / ${this.formatDate(
          val?.updated_milestone?.milestone?.milestone_date
        )}`,
        previous_assignee_name: val?.previous_assignee?.first_name,
        updated_assignee_name: val?.updated_assignee?.first_name,
        created_username_role: val?.created_user?.user_role
      }));
    }
  },
  methods: {
    ...mapActions([
      "createAuditIssues",
      "fetchInitialOptionForIssue",
      "updateIssue"
    ]),
    navigateToProjects() {
      this.$router.push({
        path: `/list-project`
      });
    },
    back() {
      this.$router.go(-1);
    },
    showTimeDiff(date) {
      return m
        .utc(date)
        .local()
        .fromNow(true);
    },
    formatTime(data) {
      return data
        ? m
            .utc(data)
            .local()
            .format("hh:mm A")
        : "--";
    },
    formatDate(data) {
      return data
        ? m
            .utc(data)
            .local()
            .format("DD-MMM-YYYY")
        : "--";
    },
    formatName(str) {
      return str?.replace(/\w\S*/g, function(txt) {
        return txt?.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
      });
    },
    getBadgeColor(key) {
      switch (key) {
        case "New Requirement":
        case "WIP":
          return "primary";
        case "Issue":
        case "Re-Open":
          return "danger";
        case "Change Request":
        case "Closed":
          return "amber";
        case "Support Request":
        case "Completed":
          return "medium-blue";
        case "Open":
          return "grey";
        case "On-Hold":
          return "darkturquoise";

        default:
          return "primary";
      }
    },
    handleEditor(data) {
      // Replace All used to make strong tag more visible for <p> tag
      data = data
        .replaceAll("<strong>", '<strong style="font-weight:bold">')
        .replaceAll("<img ", '<img style="max-width: 100%;max-height: 400px"');
      Vue.set(this.audit, "comments", data);
      Vue.set(this.payload, "comments", data);
    },
    createComment() {
      let auditPayload = {
        issue_id: this.getIssueID,
        audit_type: "comments",
        comments: this.payload?.comments
      };
      this.createAuditIssues(auditPayload).then(() => {
        this.audit = {};
        this.payload = {};
      });
    },
    async editIssue() {
      await this.fetchInitialOptionForIssue(this.getSelectedIssue?.project_id);
      this.editModal.issueData = this.getSelectedIssue;
      this.editModal.isShowPopup = true;
    },
    modalCallBack(action, value) {
      if (action) {
        this.updateIssue(value).then(() => {
          this.editModal.isShowPopup = false;
          setTimeout(() => {
            this.editModal.issueData = {};
          }, 100);
        });
      } else {
        this.editModal.isShowPopup = false;
        setTimeout(() => {
          this.editModal.issueData = {};
        }, 100);
      }
    }
  }
};
</script>
