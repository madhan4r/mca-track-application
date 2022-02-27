<template>
  <CFooter class="page-footer f-bg font-small white text-white">
    <div class="ml-auto d-flex copy-right">
      <span
        class="material-icons mr-2 cursor-pointer"
        :class="darkMode ? 'light-mode' : ''"
        @click="toogleDark()"
        :style="darkMode ? 'color: white' : 'color: black'"
      >
        light_mode
      </span>
    </div>
  </CFooter>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "Thefooter",
  computed: {
    ...mapGetters(["darkMode"])
  },
  methods: {
    ...mapActions(["toggleDarkMode"]),
    toogleDark() {
      if (!this.darkMode) {
        // let duration = 6000;
        let color = "danger";
        this.$vs.notification({
          duration: 6000,
          color,
          progress: "auto",
          title: "Warning - Dark Mode Beta",
          text: `Dark Mode is under development, it may be unstable`
        });
      }
      this.toggleDarkMode();
    }
  }
};
</script>

<style lang="scss" scoped>
@media all and (max-width: 480px) {
  .copy-right {
    font-size: 9px;
  }
  .logo-adjustment {
    width: 80px !important;
    margin-right: 0px !important;
  }
  .c-footer {
    height: 35px;
  }
  .product_content {
    padding-top: 2px;
  }
}
.copy-right {
  color: #645c5c;
}
.logo-adjustment {
  width: 100px;
  margin-right: 10px;
}
.light-mode:hover {
  color: yellow !important;
}
</style>
