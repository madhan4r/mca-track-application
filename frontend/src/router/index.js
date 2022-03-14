import Vue from "vue";
import VueRouter from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import ListProjectPage from "../views/ListProjectPage.vue";
import ListIssuePage from "../views/ListIssuePage.vue";
import NewIssuePage from "../views/NewIssuePage.vue";
import IssueDetailPage from "../views/IssueDetailPage.vue";
import ChangePasswordPage from "../views/ChangePasswordPage.vue";
import GlobalIssuePage from "../views/GlobalIssuePage.vue";
import RecentUpdatesPage from "../views/RecentUpdatesPage.vue";
import DashboardPage from "../views/DashboardPage.vue";
import AssignedIssuesPage from "../views/AssignedIssuesPage.vue";
import AdminHomePage from "../views/AdminHomePage.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "login",
    component: LoginPage
  },
  {
    path: "/list-project",
    name: "list project",
    component: ListProjectPage
  },
  {
    path: "/list-project-issue/:project_id",
    name: "list project issue",
    component: ListIssuePage
  },
  {
    path: "/new-issue/project/:project_id",
    name: "create issue",
    component: NewIssuePage
  },
  {
    path: "/issue-detailed-view/:issue_id",
    name: "issue detail page",
    component: IssueDetailPage
  },
  {
    path: "/change-password",
    name: "change password",
    component: ChangePasswordPage
  },
  {
    path: "/global-issues",
    name: "global issue",
    component: GlobalIssuePage
  },
  {
    path: "/recent-updates",
    name: "recent updates",
    component: RecentUpdatesPage
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardPage
  },
  {
    path: "/assigned-issues",
    name: "/assigned-issues",
    component: AssignedIssuesPage
  },
  {
    path: "/admin-home",
    name: "/admin-home",
    component: AdminHomePage
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  if (!localStorage.getItem("token")) {
    if (to.path.includes("/login")) {
      next();
    } else {
      next("/login");
    }
  } else {
    next();
  }
  if (to.path == "" || to.path == "/") {
    next("/login");
  } else {
    next();
  }
});

export default router;
