<template>
  <div class="text-input">
    <textarea
      :type="type"
      class="m-0 form-control"
      :value="value"
      :name="name"
      @input="$emit('input', name, $event.target.value)"
      @change="$emit('change', name, $event.target.value)"
      :class="{ 'is-danger': error }"
      :disabled="disabled"
      :maxlength="maxlength"
    />
    <small class="has-error" v-if="error">{{ error }}</small>
  </div>
</template>

<script>
export default {
  name: "text-input",
  $_veeValidate: {
    // value getter
    value() {
      return this.$el.value;
    },
    // name getter
    name() {
      return this.name;
    }
  },
  props: {
    value: {
      type: String,
      default: ""
    },
    name: {
      type: String,
      default: "textInput"
    },
    input: {
      type: Function,
      default: () => {
        console.log("Default funtion triggering in select component");
      }
    },
    type: {
      type: String,
      default: "text"
    },
    error: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    },
    maxlength: {
      type: Number,
      default: null
    }
  }
};
</script>

<style lang="scss">
.input:focus {
  border-color: $red !important;
  box-shadow: none !important;
}
.has-error {
  color: $red;
}
.is-danger {
  border-color: $red !important;
  box-shadow: none !important;
}
</style>
