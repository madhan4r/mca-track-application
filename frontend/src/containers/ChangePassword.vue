<template>
  <div class="change-password">
    <CContainer class="d-flex align-items-center justify-content-center mt-5">
      <CRow class="justify-content-center">
        <CCol md="8" lg="12">
          <CCardGroup class="has-loading-overlay">
            <CCard class="p-4">
              <h4 class="font-weight-bold mb-3 ml-3">Change Password</h4>
              <CCardBody>
                <ValidationObserver ref="reset" v-slot="{ handleSubmit }">
                  <CForm @submit.prevent="handleSubmit(onSubmit)">
                    <CRow class="row mb-3">
                      <label class="required col-lg-4 col-md-12"
                        >New Password</label
                      >
                      <div class="col-lg-6 col-md-6 col-sm-12">
                        <ValidationProvider
                          name="password"
                          :rules="{
                            required: true,
                            password_length: 8,
                            password_strength: /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})/
                          }"
                          v-slot="{ errors }"
                        >
                          <TextInput
                            name="password"
                            type="password"
                            :value="userDetail.password"
                            @input="handleInput"
                            :error="errors[0]"
                          />
                          <small class="hint"
                            >Password format: 8 characters - containing upper &
                            lower case letters, numbers and a special character.
                            No words.</small
                          >
                        </ValidationProvider>
                      </div>
                    </CRow>
                    <CRow class="row mb-3">
                      <label class="required col-lg-4 col-md-12"
                        >Confirm Password</label
                      >
                      <div class="col-lg-6 col-md-6 col-sm-12">
                        <ValidationProvider
                          rules="required|confirmed:password"
                          v-slot="{ errors }"
                        >
                          <TextInput
                            name="confirmPassword"
                            :value="confirmPassword"
                            @input="handleConfirmPassword"
                            type="password"
                            :error="errors[0]"
                          />
                        </ValidationProvider>
                      </div>
                    </CRow>
                    <CRow>
                      <CCol class="col-10" style="text-align: end">
                        <CButton
                          type="button"
                          color="secondary"
                          class="px-4 mr-3"
                          @click="redirectToPrevPage"
                          >{{ "Cancel" }}</CButton
                        >
                        <CButton type="submit" color="primary" class="px-4">{{
                          "Submit"
                        }}</CButton></CCol
                      >
                    </CRow>
                  </CForm>
                </ValidationObserver>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>
<script>
import Vue from "vue";
import { extend } from "vee-validate";
import { required, confirmed, regex, min } from "vee-validate/dist/rules";
extend("required", { ...required, message: "This field is required" });
extend("password_length", {
  ...min,
  message: "Password be atleast 8 characters"
});
extend("password_strength", {
  ...regex,
  message: "Password must have capitals, numbers and special characters"
});
extend("confirmed", {
  ...confirmed,
  message: "This field should match password"
});

import TextInput from "@/components/reusable/Fields/TextInput";
import { mapActions } from "vuex";
export default {
  name: "ChangePassword",
  components: {
    TextInput
  },
  data() {
    return {
      userDetail: {
        username: "",
        password: ""
      },
      confirmPassword: ""
    };
  },
  methods: {
    ...mapActions(["updateUser", "showToast"]),
    handleConfirmPassword(name, value) {
      this.confirmPassword = value;
    },
    handleInput(name, value) {
      Vue.set(this.userDetail, name, value);
    },
    async onSubmit() {
      const isValid = await this.$refs.reset.validate();
      if (!isValid) {
        this.showToast({
          class: "bg-danger text-white",
          message: "passwords does not match criteria"
        });
        return;
      }
      let finalPayload = {
        password: this.userDetail?.password
      };
      this.updateUser(finalPayload).then(() => {
        this.$router.go(-1);
      });
    },
    redirectToPrevPage() {
      this.$router.go(-1);
    }
  }
};
</script>
