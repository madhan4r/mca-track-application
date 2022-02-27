<template>
  <div>
    <new-issue />
  </div>
</template>
<script>
import { mapActions } from "vuex";
import NewIssue from "../containers/issue/NewIssue.vue";
export default {
  components: { NewIssue },
  methods: {
    ...mapActions(["fetchProjectByID", "fetchInitialOptionForIssue"])
  },
  mounted() {
    const {
      params: { project_id }
    } = this.$route;
    this.fetchProjectByID(project_id);
    this.fetchInitialOptionForIssue(project_id);
  }
};
</script>
<style lang=""></style>
