<template>
  <div>
    <login />
  </div>
</template>
<script>
import Login from "../containers/Login.vue";

export default {
  name: "LoginPage",
  components: { Login },
  mounted() {
    document.title = `Login · Track`;
  }
};
</script>
