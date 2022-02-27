<template>
  <div>
    <dashboard />
  </div>
</template>
<script>
import Dashboard from "../containers/dashboard/Dashboard.vue";
export default {
  components: { Dashboard },
  name: "DashboardPage",
  mounted() {
    document.title = "Dashboard · Track";
  }
};
</script>
