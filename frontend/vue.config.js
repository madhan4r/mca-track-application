module.exports = {
  lintOnSave: true,
  runtimeCompiler: true,
  css: {
    loaderOptions: {
      sass: {
        prependData: `@import "@/assets/scss/themes/ticket.scss";`
      }
    }
  }
};
