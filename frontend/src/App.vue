<template>
  <div id="app" :style="`min-height: ${getScreenSize.height - 130}px`">
    <the-header />
    <collapse-bar />
    <router-view class="class-components" />
    <toaster />
    <loader v-if="isLoading" />
    <the-footer />
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import CollapseBar from "./components/reusable/CollapseBar.vue";
import Toaster from "./components/reusable/Toaster.vue";
import TheFooter from "./containers/TheFooter.vue";
import TheHeader from "./containers/TheHeader.vue";
import Loader from "./Loader.vue";
export default {
  components: { Toaster, Loader, TheHeader, TheFooter, CollapseBar },
  name: "App",
  computed: {
    ...mapGetters(["isLoading", "darkMode"]),
    getScreenSize() {
      return {
        width: screen.availWidth,
        height: screen.availHeight
      };
    }
  },
  methods: {
    ...mapActions(["toggleDarkMode"])
  },
  mounted() {
    // set page title
    document.title = "Ticket";

    // set 'app-background' class to body tag
    let bodyElement = document.body;
    bodyElement.classList.add("app-background");

    // check for active theme
    let htmlElement = document.documentElement;
    let theme = localStorage.getItem("ticket_theme");

    if (theme === "dark") {
      htmlElement.setAttribute("theme", "dark");
      this.toggleDarkMode();
    }
  },
  watch: {
    darkMode() {
      // add/remove class to/from html tag
      let htmlElement = document.documentElement;

      if (this.darkMode) {
        localStorage.setItem("ticket_theme", "dark");
        htmlElement.setAttribute("theme", "dark");
      } else {
        localStorage.setItem("ticket_theme", "light");
        htmlElement.setAttribute("theme", "light");
      }
    }
  }
};
</script>

<style lang="scss">
// Import Main styles for this application
@import "assets/scss/custom";
#app {
  font-family: "Roboto", sans-serif;
}
.app-background {
  #app {
    background-color: var(--primary-background-color) !important;
    color: var(--dynamic-title-color);
  }
}
.dynamic-title {
  color: var(--dynamic-title-color) !important;
}

.dynamic-subtitle {
  color: var(--dynamic-subtitle-color);
  padding-top: 10px;
}

.class-components {
  margin-top: 56px;
  padding-top: 10px;
}
</style>
