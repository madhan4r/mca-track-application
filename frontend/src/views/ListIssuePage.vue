<template>
  <div>
    <list-issue />
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import ListIssue from "../containers/ListIssue.vue";
export default {
  name: "ListIssuePage",
  components: { ListIssue },
  computed: {
    ...mapGetters(["getOrganizationProjects", "getSelectedProject"])
  },
  methods: {
    ...mapActions(["fetchProjectByID"])
  },
  mounted() {
    document.title = "Issues · Track";
    const {
      params: { project_id }
    } = this.$route;
    if (this.getSelectedProject?.project_id != project_id) {
      this.fetchProjectByID(project_id).then(
        () =>
          (document.title = `${this.getSelectedProject?.project_name} · Issues · Track`)
      );
    } else {
      document.title = `${this.getSelectedProject?.project_name} · Issues · Track`;
    }
  }
};
</script>
