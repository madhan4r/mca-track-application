<template>
  <div :class="$options.name">
    <div
      v-for="option in adaptedOptions"
      :key="option.id"
      :class="`${$options.name}__option`"
    >
      <label>
        <input
          :class="`${$options.name}__input`"
          :value="option.id"
          v-model="selected"
          type="checkbox"
          @change="updateValue"
        />
        {{ option.label }}
      </label>
    </div>
    <small class="has-error" v-if="error">{{ error }}</small>
  </div>
</template>

<script>
export default {
  model: {
    // By default, `v-model` reacts to the `input`
    // event for updating the value, we change this
    // to `change` for similar behavior as the
    // native `<select>` element.
    event: "change"
  },
  props: {
    // The option adapter is responsible for
    // transforming the values and options,
    // provided in a certain format, to valid
    // option objects. You can pass your own
    // `optionAdapter()` as property to make the
    // component work with your custom data
    // structure
    optionAdapter: {
      type: Function,
      default: value => ({
        id: value,
        label: value,
        value
      })
    },
    options: {
      type: Array,
      default: () => []
    },
    value: {
      type: [Array, String, Number, Object],
      default: null
    },
    error: {
      type: String
    }
  },
  data() {
    return {
      // A computed property can't be used
      // because `data` is evaluated first.
      selected: Array.isArray(this.value)
        ? this.value.map(x => this.optionAdapter(x).id)
        : this.value && this.optionAdapter(this.value).id
    };
  },
  computed: {
    adaptedOptions() {
      return this.options.map(x => this.optionAdapter(x));
    },
    multiple() {
      return Array.isArray(this.value);
    }
  },
  methods: {
    updateValue() {
      const newValue = this.multiple
        ? this.selected.map(
            id => this.adaptedOptions.find(x => x.id === id).value
          )
        : this.adaptedOptions.find(x => x.id === this.selected).value;

      // Emitting a `change` event with the new
      // value of the `<select>` field, updates
      // all values bound with `v-model`.
      this.$emit("change", newValue);
    }
  }
};
</script>
<style lang="scss">
.has-error {
  color: $red;
}
</style>
