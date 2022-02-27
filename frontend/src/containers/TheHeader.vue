<template>
  <div>
    <CHeader
      class="bg-sidebar-color sticky-top header"
      id="header"
      fixed
      with-subheader
      light
    >
      <div class="d-flex w-100">
        <div
          class="ml-2"
          style="margin-top: auto; margin-bottom: auto"
          v-if="currentActiveUser"
        >
          <vs-button @click="toggleSideBar()">
            <i class="material-icons" style="color: black"> menu </i>
          </vs-button>
        </div>
        <div style="margin-top: auto; margin-bottom: auto">
          <div class="col-12 p-0 logo">
            <img
              class="p-1 d-inline-block mw-100 cursor-pointer"
              src="/img/ticket_logo.png"
              style="max-height: 50px; width: 120px"
              alt="logo"
              @click="NavigateTo('/dashboard')"
            />
          </div>
        </div>
        <div
          class="d-flex justify-content-end user_name w-100 pr-2"
          v-if="currentActiveUser"
        >
          <div class="d-flex flex-column justify-content-center">
            <span
              class="material-icons mr-2 cursor-pointer"
              v-c-tooltip="'Recent Issues'"
              @click="NavigateTo('/recent-updates')"
            >
              forum
            </span>
          </div>
          <div class="d-flex flex-column justify-content-center">
            <span>Welcome {{ getUserName }} [{{ getOrganizationName }}]</span>
          </div>
          <div class="d-flex flex-column justify-content-center">
            <CDropdown
              inNav
              class="c-header-nav-items"
              placement="bottom-end"
              add-menu-classes="pt-0"
              ref="profile"
              @mouseover.native="show()"
              @mouseleave.native="hide()"
            >
              <template #toggler>
                <CHeaderNavLink id="user-settings-dropdown">
                  <div class="c-avatar text">
                    <img
                      class="avatar rounded-circle"
                      alt="profile"
                      src="/img/default_user_pic.png"
                    />
                  </div>
                </CHeaderNavLink>
              </template>
              <CDropdownHeader tag="div" class="text-center" color="light">
                <strong>Profile</strong>
              </CDropdownHeader>
              <a
                class="dropdown-item cursor-pointer"
                @click="navigateToChangePassword()"
              >
                <i class="material-icons mr-2"> pin </i>Change Password
              </a>
              <a class="dropdown-item cursor-pointer" @click="logoutSession()">
                <i class="material-icons mr-2"> logout </i>Sign out
              </a>
            </CDropdown>
          </div>
        </div>
      </div>
    </CHeader>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "TheHeader",
  data: () => ({
    collapsed: false,
    page: ""
  }),
  computed: {
    ...mapGetters(["getUserName", "currentActiveUser", "getOrganizationName"])
  },
  methods: {
    ...mapActions(["fetchUser", "logout", "toggleSideBar"]),
    logoutSession() {
      this.logout();
    },
    show() {
      this.$refs.profile._data.visible = true;
    },
    hide() {
      this.$refs.profile._data.visible = false;
    },
    navigateToChangePassword() {
      this.$router.push("/change-password");
    },
    NavigateTo(path) {
      this.$router.push({
        path: path
      });
    }
  },
  watch: {
    "$route.name"() {
      this.collapsed = false;
    },
    "$route.path": function() {
      this.page = this.$router.currentRoute.path;
    },
    currentActiveUser() {
      if (this.currentActiveUser) {
        this.fetchUser();
      }
    }
  },
  created() {
    if (this.currentActiveUser) {
      this.fetchUser();
    }
    this.page = this.$router.currentRoute.path;
  }
};
</script>

<style lang="scss" scoped>
.avatar {
  padding-top: 10px;
  width: 45px;
}
@media all and (max-width: 620px) {
  .user_name {
    font-size: 9px;
  }
  .avatar {
    padding-top: 0px;
    width: 35px;
  }
}
::marker {
  color: var(--main-background-color);
}
</style>
