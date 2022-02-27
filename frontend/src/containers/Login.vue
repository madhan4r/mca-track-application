<template>
  <div class="login-style">
    <div class="container px-4 py-3 mx-auto">
      <div class="card">
        <div class="row justify-content-center my-auto">
          <div class="col-md-4 col-10 my-5">
            <div class="row justify-content-center px-3 mb-3">
              <img
                id="logo"
                style="width: 80%"
                src="/img/ticket_logo.png"
                alt="logo"
              />
            </div>
            <h6 class="msg-info text-center">Login to your account</h6>
            <CForm @submit.prevent="loginSubmit">
              <div class="form-group">
                <label class="form-control-label text-muted">Username</label>
                <input
                  name="username"
                  placeholder="Email"
                  class="form-control"
                  v-model="username"
                />
              </div>
              <div class="form-group">
                <label class="form-control-label text-muted">Password</label>
                <input
                  type="password"
                  name="password"
                  placeholder="Password"
                  class="form-control"
                  v-model="password"
                />
              </div>
              <div class="row justify-content-center my-1 px-3">
                <button type="submit" class="btn-block btn-color">Login</button>
              </div>
            </CForm>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "Login",
  data: () => ({
    username: "",
    password: ""
  }),
  computed: {
    ...mapGetters(["currentActiveUser"])
  },
  methods: {
    ...mapActions(["logIn", "showToast"]),
    loginSubmit() {
      if (this.username && this.password) {
        this.logIn({
          email: this.username.toLowerCase(),
          password: this.password
        });
      } else {
        this.showToast({
          class: "bg-danger text-white",
          message: "Please fill the credentials"
        });
      }
    }
  },
  mounted() {
    if (this.currentActiveUser) {
      this.$router.push("/list-project");
    }
  }
};
</script>
