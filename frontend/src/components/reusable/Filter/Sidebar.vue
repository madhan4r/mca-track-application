<template>
  <div class="sidebar">
    <div class="sidebar-backdrop" @click="toggleSideBar" v-if="show"></div>
    <transition name="slide">
      <div v-if="show" class="sidebar-panel">
        <slot name="container">
          <div class="sidebar-pannel-container">
            <slot name="header-wrapper">
              <header class="sidebar-panel-header">
                <slot name="header">
                  <p>header</p>
                </slot>
              </header>
            </slot>
            <slot name="body-wrapper">
              <div class="sidebar-panel-body">
                <slot></slot>
              </div>
            </slot>
          </div>
        </slot>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
  props: ["show", "toggleSideBar"],
  data: function() {
    return {
      formattedSelectedFilters: {}
    };
  },
  watch: {
    show(val) {
      if (val == true) {
        document.getElementsByTagName("body")[0].style.overflow = "hidden";
      } else {
        document.getElementsByTagName("body")[0].style.overflow = "";
      }
    }
  }
};
</script>
