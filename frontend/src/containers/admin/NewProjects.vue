<template>
  <div>
    <CModal
      color="primary"
      :show.sync="isShowPopup"
      :close-on-backdrop="false"
      :centered="true"
    >
      <template #header>
        <h6 class="modal-title">New User</h6>
        <CButtonClose @click="cancel" class="text-black" />
      </template>
      <template #footer>
        <CButton color="secondary" @click="cancel">Cancel</CButton>
        <CButton color="primary" type="Submit" @click="NewProject()">
          Create
        </CButton>
      </template>
      <div>
        <CRow class="pl-3 pr-3">
          <CCol md="12" class="mb-3">
            <CRow class="row">
              <label class="required col-lg-12 col-md-12">Project Title</label>
              <div class="col-lg-12 col-md-12 col-sm-12">
                <TextInput
                  name="project_name"
                  :value="payload.project_name"
                  @input="handleInput"
                />
              </div>
            </CRow>
          </CCol>
        </CRow>
      </div>
    </CModal>
  </div>
</template>
<script>
import TextInput from "@/components/reusable/Fields/TextInput";
import { mapActions } from "vuex";
export default {
  name: "NewProject",
  components: { TextInput },
  props: {
    isShowPopup: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    payload: {}
  }),
  methods: {
    ...mapActions(["createProject"]),
    handleInput(name, value) {
      this.payload[name] = value;
    },
    NewProject() {
      this.createProject(this.payload).then(() => {
        this.$emit("modalCallBack", true);
      });
    },
    cancel() {
      this.$emit("modalCallBack", false);
    }
  },
  mounted() {
    this.payload = {};
  }
};
</script>
