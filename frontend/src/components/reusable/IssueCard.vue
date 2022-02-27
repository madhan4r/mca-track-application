<template>
  <li class="d-flex no-block card-body">
    <em class="material-icons w-30px mt-2 mr-2">
      {{ getIconBasedOnType(item.type_) }}
    </em>
    <div>
      <h5>
        <a
          @click="navigateToIssueDetail(item)"
          class="m-b-0 font-weight-bold p-0 cursor-pointer pr-3 issue-title dynamic-title"
        >
          {{ item.issue_title }}
          <CBadge
            :color="getBadgeColor(item.type_)"
            class="ml-2"
            v-c-tooltip="'Issue Type'"
            >{{ item.type_ }}
          </CBadge>
        </a>
      </h5>
      <span
        v-if="show_project_name"
        @click="navigateToIssue(item)"
        class="cursor-pointer text-muted font-weight-bold"
        >{{ item.project_ }} ·
      </span>
      <span class="text-muted">
        <strong>#{{ item.issue_id }} </strong>
      </span>
      <span class="text-muted issue-data">
        created {{ showTimeDiff(item.created_on) }} ago by
        <strong>{{ item.created_user_ }}</strong>
      </span>
    </div>
    <div class="ml-auto">
      <div class="text-right">
        <h5 class="text-muted m-b-0"></h5>
        <span class="text-muted font-16" v-c-tooltip="'Issue Status'">
          <strong>{{ item.status_ }}</strong>
        </span>
      </div>
    </div>
  </li>
</template>
<script>
import m from "moment";

export default {
  name: "IssueCard",
  props: {
    item: {
      type: Object,
      default: () => ({})
    },
    show_project_name: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    showTimeDiff(date) {
      return m
        .utc(date)
        .local()
        .fromNow(true);
    },
    navigateToIssueDetail(item) {
      this.$router.push({
        path: `/issue-detailed-view/${item?.issue_id}`
      });
    },
    navigateToIssue(item) {
      this.$router.push({
        path: `/list-project-issue/${item?.project_id}?page=%5B1%5D`
      });
    },
    getIconBasedOnType(key) {
      switch (key) {
        case "New Requirement":
          return "maps_ugc";
        case "Issue":
          return "bug_report";
        case "Change Request":
          return "change_circle";
        case "Support Request":
          return "manage_accounts";

        default:
          return "bug_report";
      }
    },
    getBadgeColor(key) {
      switch (key) {
        case "New Requirement":
        case "WIP":
          return "primary";
        case "Issue":
        case "Re-Open":
          return "danger";
        case "Change Request":
        case "Closed":
          return "amber";
        case "Support Request":
        case "Completed":
          return "medium-blue";
        case "Open":
          return "grey";

        default:
          return "primary";
      }
    }
  }
};
</script>
