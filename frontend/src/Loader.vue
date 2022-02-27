<template>
  <div>
    <div ref="loader" class="box-loading"></div>
  </div>
</template>
<script>
export default {
  name: "Loader",
  data: () => ({
    loading: null
  }),
  beforeDestroy() {
    this.loading.close();
  },
  mounted() {
    let types = [
      "default",
      // "waves",
      "corners",
      // "border",
      "points",
      "square",
      // "gradient",
      // "rectangle",
      "circles",
      // "square-rotate",
      "scale"
    ];
    const random = Math.floor(Math.random() * types.length);
    let type = types[random];
    // https://vuesax.com/docs/components/Loading.html
    this.loading = this.$vs.loading({
      target: this.$refs.loader[0],
      text: "Loading...",
      type
    });
  }
};
</script>
