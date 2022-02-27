<template>
  <div>
    <change-password />
  </div>
</template>
<script>
import ChangePassword from "../containers/ChangePassword.vue";
export default {
  components: { ChangePassword },
  name: "ChangePasswordPage",
  mounted() {
    document.title = "Change Password · Track";
  }
};
</script>
