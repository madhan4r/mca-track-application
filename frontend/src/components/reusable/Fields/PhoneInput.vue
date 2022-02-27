<template>
  <div>
    <div class="d-flex align-items-center">
      <v-select
        :name="`phone-code-${name}`"
        :value="dialCode"
        @input="inputDialCode"
        :label="label"
        :options="options"
        :taggable="taggable"
        :multiple="multiple"
        :clearable="false"
        :disabled="disabled"
        :class="{ 'is-danger': error }"
        :style="{ minWidth: '120px' }"
        :selectOnTab="true"
      />
      <span class="px-1 separator"> - </span>
      <input
        :name="`phone-number-${name}`"
        class="m-0 form-control"
        :value="phone"
        :disabled="disabled"
        :style="{ minWidth: '80px' }"
        @change="inputPhone"
        :class="{ 'is-danger': error }"
      />
    </div>
    <small class="has-error" v-if="error">{{ error }}</small>
  </div>
</template>

<script>
export default {
  name: "PhoneInput",
  props: {
    name: {
      type: String,
      default: "SelectBox"
    },
    value: {
      type: String,
      default: ""
    },
    options: {
      type: Array,
      default: () => []
    },
    label: {
      type: String,
      default: undefined
    },
    taggable: {
      type: Boolean,
      default: false
    },
    multiple: {
      type: Boolean,
      default: false
    },
    clearable: {
      type: Boolean,
      default: true
    },
    error: {
      type: String,
      default: ""
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dialCode: null,
      phone: null
    };
  },
  mounted() {
    if (this.value) {
      const val = this.value.split("^");
      this.dialCode = val[0];
      this.phone = val[1];
    }
  },
  watch: {
    value() {
      if (!this.value) {
        this.resetPhoneno();
      }
    }
  },
  methods: {
    inputDialCode(value) {
      this.dialCode = value || null;
      this.input();
    },
    inputPhone(e) {
      const { value } = e.target;
      this.phone = value || "";
      this.input();
    },
    input() {
      if (this.dialCode && this.dialCode.code && this.phone) {
        this.$emit(
          "change",
          this.name,
          this.dialCode[this.label] + "^" + this.phone
        );
        this.$emit(
          "input",
          this.name,
          this.dialCode[this.label] + "^" + this.phone
        );
      } else if (this.dialCode && this.dialCode.dialing_code && this.phone) {
        this.$emit(
          "change",
          this.name,
          this.dialCode.dialing_code + "^" + this.phone
        );
        this.$emit(
          "input",
          this.name,
          this.dialCode.dialing_code + "^" + this.phone
        );
      } else if (this.dialCode && this.phone) {
        this.$emit("change", this.name, this.dialCode + "^" + this.phone);
        this.$emit("input", this.name, this.dialCode + "^" + this.phone);
      } else {
        this.$emit("change", this.name, "");
        this.$emit("input", this.name, "");
      }
    },
    resetPhoneno() {
      this.dialCode = null;
      this.phone = null;
    }
  }
};
</script>
<style lang="scss">
.has-error {
  color: $red;
}
.is-danger {
  .vs__dropdown-toggle {
    border-color: $red;
    box-shadow: none;
    outline: none;
  }
}

.separator {
  opacity: 0.5;
}
</style>
