<template>
  <div>
    <list-project />
  </div>
</template>
<script>
import { mapActions, mapGetters } from "vuex";
import ListProject from "@/containers/ListProject.vue";

export default {
  name: "ListProjectPage",
  components: { ListProject },
  computed: {
    ...mapGetters(["getOrganizationId"])
  },
  methods: {
    ...mapActions(["fetchOrganizationProject"])
  },
  mounted() {
    document.title = "Projects · Dashboard · Track";
    this.fetchOrganizationProject(this.getOrganizationId);
  }
};
</script>
