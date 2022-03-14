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
        <h6 class="modal-title">New User</h6>
        <CButtonClose @click="cancel" class="text-black" />
      </template>
      <template #footer>
        <CButton color="secondary" @click="cancel">Cancel</CButton>
        <CButton color="primary" type="Submit" @click="newUser()">
          Create
        </CButton>
      </template>
      <div>
        <ValidationObserver ref="createUser" v-slot="{ newUser }">
          <form id="create" @submit.prevent="newUser()">
            <CRow class="pl-3 pr-3">
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12">First Name</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <TextInput
                        name="first_name"
                        :value="user.first_name"
                        @input="handleInput"
                        :error="errors[0]"
                      />
                    </ValidationProvider>
                  </div>
                </CRow>
              </CCol>
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12">Last Name</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <TextInput
                        name="last_name"
                        :value="user.last_name"
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
                  <label class="required col-lg-12 col-md-12">Email</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider
                      rules="required|validateEmail"
                      v-slot="{ errors }"
                    >
                      <TextInput
                        name="email"
                        :value="user.email"
                        @input="handleInput"
                        :error="errors[0]"
                      />
                    </ValidationProvider>
                  </div>
                </CRow>
              </CCol>
              <CCol md="6" class="mb-3">
                <CRow class="row">
                  <label class="required col-lg-12 col-md-12">Role</label>
                  <div class="col-lg-12 col-md-12 col-sm-12">
                    <ValidationProvider rules="required" v-slot="{ errors }">
                      <Select
                        name="user_role"
                        :value="user.user_role"
                        @input="handleChangeSelect"
                        :options="
                          options && options['user_role']
                            ? options['user_role']
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
            </CRow>
          </form>
        </ValidationObserver>
      </div>
    </CModal>
  </div>
</template>
<script>
import { mapActions } from "vuex";
import TextInput from "@/components/reusable/Fields/TextInput";
import Select from "@/components/reusable/Fields/Select";
import Vue from "vue";
import { extend } from "vee-validate";
extend("validateEmail", {
  validate(value) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(value).toLowerCase());
  },
  message: "Enter valid email",
  computesRequired: true
});

export default {
  name: "NewUser",
  components: {
    TextInput,
    Select
  },
  props: {
    isShowPopup: {
      type: Boolean,
      default: false
    }
  },
  data: () => ({
    user: {},
    payload: {}
  }),
  computed: {
    options: () => ({
      user_role: [
        { label: "Lead", code: "lead" },
        { label: "Developer", code: "developer" }
      ]
    })
  },
  methods: {
    ...mapActions(["createUsers", "showToast"]),
    handleInput(name, value) {
      Vue.set(this.user, name, value);
      Vue.set(this.payload, name, value);
    },
    handleChangeSelect(name, value) {
      Vue.set(this.user, name, value);
      let code = value ? value.id || value.code || value : null;
      this.payload = {
        ...this.payload,
        [name]: code
      };
    },
    async newUser() {
      const isValid = await this.$refs.createUser.validate();
      if (!isValid) {
        this.showToast({
          class: "bg-danger text-white",
          message: "Please fill mandatory fields!"
        });
        return;
      }
      this.payload.password = "Track@1234";
      this.createUsers(this.payload).then(() => {
        this.$emit("modalCallBack", true);
      });
    },
    cancel() {
      this.$emit("modalCallBack", false);
    }
  },
  mounted() {
    this.user = {};
  }
};
</script>
