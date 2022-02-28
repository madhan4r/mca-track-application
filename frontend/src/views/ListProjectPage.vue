<template>
  <div>
    <list-project />
  </div>
</template>
<script>
import { mapActions } from "vuex";
import ListProject from "@/containers/ListProject.vue";

export default {
  name: "ListProjectPage",
  components: { ListProject },
  methods: {
    ...mapActions(["fetchProjects"])
  },
  mounted() {
    document.title = "Projects · Dashboard · Track";
    this.fetchProjects();
  }
};
</script>
