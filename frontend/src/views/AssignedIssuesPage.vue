<template>
  <div>
    <assigned-issues />
  </div>
</template>
<script>
import AssignedIssues from "../containers/AssignedIssues.vue";
export default {
  name: "AssignedIssuesPage",
  components: { AssignedIssues },
  mounted() {
    document.title = "Assigned · Issues";
  }
};
</script>
