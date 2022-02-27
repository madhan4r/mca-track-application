<template>
  <div class="hidden">
    <vs-sidebar
      absolute
      v-model="active"
      :open.sync="sideBar"
      style="height: 100%; position: fixed !important"
    >
      <vs-sidebar-item id="/list-project" to="/list-project">
        <template #icon>
          <em class="material-icons"> home </em>
        </template>
        Home
      </vs-sidebar-item>
      <vs-sidebar-item id="/recent-updates" to="/recent-updates">
        <template #icon>
          <em class="material-icons"> recent_actors </em>
        </template>
        Recent Issues
      </vs-sidebar-item>
      <vs-sidebar-item
        v-if="[Roles.lead, Roles.developer].includes(getUserRole)"
        id="/assigned-issues"
        :to="`/assigned-issues?status_id__in=%5B1,2,3,4,6%5D&page=%5B1%5D`"
      >
        <template #icon>
          <em class="material-icons"> style </em>
        </template>
        Assigned Issues
      </vs-sidebar-item>
      <vs-sidebar-item id="/dashboard" to="/dashboard">
        <template #icon>
          <em class="material-icons"> dashboard </em>
        </template>
        Dashboard
      </vs-sidebar-item>
      <vs-sidebar-item id="/global-issues" to="/global-issues?page=%5B1%5D">
        <template #icon>
          <em class="material-icons"> public </em>
        </template>
        Global Issues
      </vs-sidebar-item>
      <vs-sidebar-item id="/change-password" to="/change-password">
        <template #icon>
          <em class="material-icons"> pin </em>
        </template>
        Change Password
      </vs-sidebar-item>
    </vs-sidebar>
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import { Roles } from "@/helpers/helpers.js";

export default {
  data: () => ({
    active: "",
    Roles
  }),
  computed: {
    ...mapGetters(["showSideBar", "getUserRole"]),
    sideBar: {
      // getter
      get() {
        return this.showSideBar;
      },
      // setter
      set() {
        this.toggleSideBar();
      }
    }
  },
  methods: {
    ...mapActions(["toggleSideBar"])
  },
  watch: {
    "$route.path": function() {
      this.active = this.$router.currentRoute.path;
      if (this.sideBar) this.sideBar = false;
    }
  },
  mounted() {
    this.active = this.$router.currentRoute.path;
  }
};
</script>
<style lang="scss" scoped>
.vs-sidebar__item.hasIcon {
  padding: 2px;
}
</style>
