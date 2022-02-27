<template>
  <div>
    <global-issue />
  </div>
</template>
<script>
import GlobalIssue from "../containers/GlobalIssue.vue";
export default {
  name: "GlobalIssuePage",
  components: { GlobalIssue },
  mounted() {
    document.title = "Global Issues · Track";
  }
};
</script>
