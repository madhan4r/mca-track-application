<template>
  <div>
    <issue-detail />
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import IssueDetail from "../containers/issue/IssueDetail.vue";
export default {
  name: "IssueDetailPage",
  components: { IssueDetail },
  computed: {
    ...mapGetters(["getSelectedIssue", "getSelectedIssue"])
  },
  methods: {
    ...mapActions(["fetchIssueByID", "fetchAuditRecords"])
  },
  mounted() {
    const {
      params: { issue_id }
    } = this.$route;
    this.fetchIssueByID(issue_id).then(
      () =>
        (document.title = `${this.getSelectedIssue?.issue_title} (#${issue_id}) · Track`)
    );
    this.fetchAuditRecords(issue_id);
  }
};
</script>
