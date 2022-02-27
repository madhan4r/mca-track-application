<template>
  <div class="text-input">
    <div class="input-group">
      <input
        :type="isPasswordType ? 'password' : 'text'"
        min="0"
        class="m-0 form-control"
        :value="value"
        :name="name"
        v-on:keyup.enter="$emit('onEnter', $event.target.value)"
        :disabled="disabled"
        @input="$emit('input', name, $event.target.value)"
        @change="$emit('change', name, $event.target.value)"
        :class="{ 'is-danger': error }"
        :autocomplete="autocomplete"
      />
      <span class="input-group-append">
        <button
          class="btn btn-outline-secondary"
          tabindex="-1"
          :class="{ 'is-danger': error }"
          type="button"
          v-if="isPasswordType"
          @click="isPasswordType = false"
        >
          <i class="fas fa-eye"></i>
        </button>
        <button
          class="btn btn-outline-secondary"
          tabindex="-1"
          :class="{ 'is-danger': error }"
          type="button"
          v-else
          @click="isPasswordType = true"
        >
          <i class="fas fa-eye-slash"></i>
        </button>
      </span>
    </div>
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
      type: [String, Number],
      default: ""
    },
    name: {
      type: String,
      default: "textInput"
    },
    onEnter: {
      type: Function,
      default: () => {
        console.log("Default function triggering in TextInput component");
      }
    },
    input: {
      type: Function,
      default: () => {
        console.log("Default funtion triggering in select component");
      }
    },
    error: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    },
    autocomplete: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      isPasswordType: true
    };
  },
  methods: {
    inputPassword(e) {
      console.log(e);
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
.input-group-append {
  height: calc(1.5em + 0.75rem + 2px);
}
</style>
