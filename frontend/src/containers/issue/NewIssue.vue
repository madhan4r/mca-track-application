<template>
  <div class="d-flex justify-content-center mb-5">
    <div class="col-lg-10 mb-5">
      <div class="d-flex justify-content-between">
        <h5 class="font-weight-bold ml-3">
          <u>
            <a class="cursor-pointer" @click="navigateToProjects">Projects</a>
          </u>
          >
          <u>
            <a class="cursor-pointer" @click="navigateToIssues">{{
              getProjectName
            }}</a>
          </u>
          >
          <u>
            <a class="cursor-pointer" @click="navigateToIssues">Issues</a>
          </u>
          > New
        </h5>
      </div>
      <div class="text-right">
        <h6 class="text-primary-dark font-weight-bold">
          <u class="cursor-pointer" @click="navigateToIssues">Back To Issues</u>
        </h6>
      </div>
      <div class="card">
        <div class="card-body text-center">
          <h4 class="card-title font-weight-bold">New Issue</h4>
        </div>
        <ValidationObserver ref="createIssue" v-slot="{ handleSubmit }">
          <form id="create" @submit.prevent="handleSubmit()">
            <CRow class="pl-3 pr-3">
              <CCol md="12" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12">Title</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <TextInput
                        name="issue_title"
                        :value="issue.issue_title"
                        @input="handleInput"
                        :error="errors[0]"
                      />
                    </ValidationProvider>
                  </div>
                </CRow>
              </CCol>
            </CRow>
            <CRow class="pl-3 pr-3">
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12">Issue Type</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <Select
                        name="type_id"
                        :value="issue.type_id"
                        @input="handleChangeSelect"
                        :options="
                          options && options['type_id']
                            ? options['type_id']
                            : []
                        "
                        :taggable="false"
                        :multiple="false"
                        :clearable="false"
                        :error="errors[0]"
                      />
                    </ValidationProvider>
                  </div>
                </CRow>
              </CCol>
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12"
                    >Issue Status</label
                  >
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <Select
                        name="status_id"
                        :value="issue.status_id"
                        @input="handleChangeSelect"
                        :options="
                          options && options['status_id']
                            ? options['status_id']
                            : []
                        "
                        :taggable="false"
                        :multiple="false"
                        :clearable="false"
                        :error="errors[0]"
                        :disabled="true"
                      />
                    </ValidationProvider>
                  </div>
                </CRow>
              </CCol>
            </CRow>
            <CRow class="pl-3 pr-3">
              <CCol md="12" class="mb-3">
                <CRow class="row">
                  <label class="col-lg-12 col-md-12">Description</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <!--Whenever vue-editor is used Advert-section class name should be given which makes <strong> tag to bolder(visible) -->
                    <vue-editor
                      class="advert-section"
                      name="issue_description"
                      :value="issue.issue_description"
                      @input="handleEditor"
                    ></vue-editor>
                  </div>
                </CRow>
              </CCol>
            </CRow>
            <CRow class="pl-3 pr-3">
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12"
                    >Issue Module</label
                  >
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <Select
                        name="module_id"
                        :value="issue.module_id"
                        @input="handleChangeSelect"
                        :options="
                          options && options['module_id']
                            ? options['module_id']
                            : []
                        "
                        :taggable="false"
                        :multiple="false"
                        :clearable="false"
                        :error="errors[0]"
                      />
                    </ValidationProvider>
                  </div>
                </CRow>
              </CCol>
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="col-lg-12 col-md-12">Issue Priority</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <Select
                      name="priority_id"
                      :value="issue.priority_id"
                      @input="handleChangeSelect"
                      :options="
                        options && options['priority_id']
                          ? options['priority_id']
                          : []
                      "
                      :taggable="false"
                      :multiple="false"
                      :clearable="true"
                    />
                  </div>
                </CRow>
              </CCol>
            </CRow>
            <CRow class="pl-3 pr-3">
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="col-lg-12 col-md-12">Gitlab Issue ID</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <TextInput
                      name="gitlab_issue_id"
                      :value="issue.gitlab_issue_id"
                      type="number"
                      @input="handleInput"
                    />
                  </div>
                </CRow>
              </CCol>
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="col-lg-12 col-md-12">Assignee</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <Select
                      name="assigned_to"
                      :value="issue.assigned_to"
                      @input="handleChangeSelect"
                      :options="
                        options && options['assigned_to']
                          ? options['assigned_to']
                          : []
                      "
                      :taggable="false"
                      :multiple="false"
                      :clearable="true"
                    />
                  </div>
                </CRow>
              </CCol>
            </CRow>
            <CRow class="pl-3 pr-3">
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="col-lg-12 col-md-12">Milestone</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <Select
                      name="milestone_id"
                      :value="issue.milestone_id"
                      @input="handleChangeSelect"
                      :options="
                        options && options['milestone_id']
                          ? options['milestone_id']
                          : []
                      "
                      :taggable="false"
                      :multiple="false"
                      :clearable="true"
                      :disabled="getUserRole == Roles.customer"
                    />
                  </div>
                </CRow>
              </CCol>
            </CRow>
          </form>
        </ValidationObserver>
        <div class="d-flex m-3 mt-4 mb-4 p-1 justify-content-end">
          <CButton class="btn-secondary mr-3" @click="goingBack()"
            >Cancel</CButton
          >
          <CButton class="btn-primary" @click="submit()">Create Issue</CButton>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Vue from "vue";
import { mapActions, mapGetters } from "vuex";
import TextInput from "@/components/reusable/Fields/TextInput";
import Select from "@/components/reusable/Fields/Select";
import { Roles } from "@/helpers/helpers.js";

export default {
  name: "NewIssue",
  components: { TextInput, Select },
  data: () => ({
    issue: {},
    payload: {},
    Roles
  }),
  computed: {
    ...mapGetters([
      "getSelectedProject",
      "getIssueTypes",
      "getIssueStatus",
      "getIssuePriority",
      "getProjectMilestone",
      "getProjectModule",
      "getProjectUsers",
      "getUserRole"
    ]),
    getProjectName() {
      return this.getSelectedProject?.project_name || "Project";
    },
    options() {
      return {
        type_id: this.getIssueTypes || [],
        status_id: this.getIssueStatus || [],
        priority_id: this.getIssuePriority || [],
        milestone_id: this.getProjectMilestone || [],
        module_id: this.getProjectModule || [],
        assigned_to: this.getProjectUsers || []
      };
    }
  },
  watch: {
    getIssueStatus() {
      if (this.getIssueStatus?.length)
        this.handleChangeSelect("status_id", this.getIssueStatus[0]);
    }
  },
  methods: {
    ...mapActions(["showToast", "createIssue"]),
    handleInput(name, value) {
      Vue.set(this.issue, name, value);
      Vue.set(this.payload, name, value);
    },
    handleEditor(data) {
      // Replace All used to make strong tag more visible for <p> tag
      data = data
        .replaceAll("<strong>", '<strong style="font-weight:bold">')
        .replaceAll("<img ", '<img style="max-width: 100%;max-height: 400px"');
      Vue.set(this.issue, "issue_description", data);
      Vue.set(this.payload, "issue_description", data);
    },
    handleChangeSelect(name, value) {
      Vue.set(this.issue, name, value);
      let code = value ? value.id || value.code || value : null;
      this.payload = {
        ...this.payload,
        [name]: code
      };
    },
    async submit() {
      const isValid = await this.$refs.createIssue.validate();
      if (!isValid) {
        this.showToast({
          class: "bg-danger text-white",
          message: "Please fill mandatory fields!"
        });
        return;
      }
      const {
        params: { project_id }
      } = this.$route;
      let finalPayload = {
        project_id: project_id,
        ...this.payload
      };
      this.createIssue(finalPayload).then(() => {
        this.payload = {};
      });
    },
    goingBack() {
      this.$router.go(-1);
    },
    navigateToProjects() {
      this.$router.push({
        path: `/list-project`
      });
    },
    navigateToIssues() {
      const {
        params: { project_id }
      } = this.$route;
      this.$router.push({
        path: `/list-project-issue/${project_id}?page=%5B1%5D`
      });
    }
  },
  mounted() {
    if (this.getIssueStatus?.length)
      this.handleChangeSelect("status_id", this.getIssueStatus[0]);
  }
};
</script>
<style lang="scss" scoped>
label {
  font-weight: 600;
}
</style>
