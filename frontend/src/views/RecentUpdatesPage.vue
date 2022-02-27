<template>
  <div>
    <recent-updates />
  </div>
</template>
<script>
import RecentUpdates from "../containers/RecentUpdates.vue";
export default {
  name: "RecentUpdatesPage",
  components: { RecentUpdates },
  mounted() {
    document.title = `Recent Updates · Track`;
  }
};
</script>
