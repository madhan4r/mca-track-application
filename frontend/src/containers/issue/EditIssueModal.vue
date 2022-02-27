<template>
  <div>
    <CModal
      color="primary"
      :show.sync="isShowPopup"
      :close-on-backdrop="false"
      :centered="true"
      size="xl"
    >
      <template #header>
        <h6 class="modal-title">EDIT ISSUE</h6>
        <CButtonClose @click="cancel" class="text-black" />
      </template>
      <template #footer>
        <CButton color="secondary" @click="cancel">Cancel</CButton>
        <CButton color="primary" type="Submit" @click="updateIssue()"
          >Update</CButton
        >
      </template>
      <div>
        <ValidationObserver ref="updateIssue" v-slot="{ handleSubmit }">
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
                        :disabled="isFieldsEditable"
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
                        :disabled="isFieldsEditable"
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
                        :disabled="isFieldsEditable"
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
                      :disabled="isFieldsEditable"
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
                        :disabled="isFieldsEditable"
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
                      :disabled="isFieldsEditable"
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
                      :disabled="isFieldsEditable"
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
                      :disabled="
                        getUserRole == Roles.customer || isFieldsEditable
                      "
                    />
                  </div>
                </CRow>
              </CCol>
            </CRow>
          </form>
        </ValidationObserver>
      </div>
    </CModal>
  </div>
</template>

<script>
import m from "moment";
import Vue from "vue";
import TextInput from "@/components/reusable/Fields/TextInput";
import Select from "@/components/reusable/Fields/Select";
import { mapGetters, mapActions } from "vuex";
import { Roles } from "@/helpers/helpers.js";

export default {
  name: "EditIssueModal",
  props: {
    isShowPopup: {
      type: Boolean,
      default: false
    },
    issueData: {
      type: Object,
      default: () => []
    }
  },
  components: {
    TextInput,
    Select
  },
  data() {
    return {
      issue: {},
      payload: {},
      Roles
    };
  },
  computed: {
    ...mapGetters([
      "getIssueTypes",
      "getIssueStatus",
      "getIssuePriority",
      "getProjectMilestone",
      "getProjectModule",
      "getProjectUsers",
      "getUserRole"
    ]),
    options() {
      return {
        type_id: this.getIssueTypes || [],
        status_id: this.getIssueStatus || [],
        priority_id: this.getIssuePriority || [],
        milestone_id: this.getProjectMilestone || [],
        module_id: this.getProjectModule || [],
        assigned_to: this.getProjectUsers || []
      };
    },
    isFieldsEditable() {
      if (this.getUserRole == this.Roles.developer) return true;
      return false;
    }
  },
  methods: {
    ...mapActions(["showToast"]),
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
    async updateIssue() {
      const isValid = await this.$refs.updateIssue.validate();
      if (!isValid) {
        this.showToast({
          class: "bg-danger text-white",
          message: "Please fill mandatory fields!"
        });
        return;
      }
      let finalPayload = {
        ...this.payload,
        issue_id: this.issue?.issue_id
      };
      this.$emit("updateModalCallBack", true, finalPayload);
    },
    cancel() {
      this.$emit("updateModalCallBack", false);
    }
  },
  mounted() {
    let data = this.issueData;
    this.issue = {
      ...data,
      type_id: data?.type_id
        ? { id: data?.issue_type_id, label: data?.type?.type }
        : [],
      status_id: data?.status_id
        ? { id: data?.issue_status_id, label: data?.status?.status }
        : [],
      milestone_id: data?.milestone_id
        ? {
            id: data?.milestone_id,
            label: `${data.milestone?.milestone?.milestone} / ${m
              .utc(data?.milestone.milestone_date)
              .local()
              .format("DD-MMM-YYYY")}`
          }
        : [],
      priority_id: data?.priority_id
        ? { id: data?.priority_id, label: data?.priority?.issue_priority }
        : [],
      module_id: data?.module_id
        ? { id: data?.module_id, label: data?.module?.module?.module_name }
        : [],
      assigned_to: data?.assigned_to
        ? {
            id: data?.assigned_to,
            label: `${data?.assigned_to_user?.first_name} ${data?.assigned_to_user?.last_name}`
          }
        : []
    };
  }
};
</script>
