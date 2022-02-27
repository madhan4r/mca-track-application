<template>
  <div class="pl-2">
    <label class="mr-2" :key="index" v-for="(item, index) in options">
      <input
        :checked="value === item.id || value === item"
        type="radio"
        :value="item.id || item"
        :name="name"
        :disabled="disabled || false"
        @input="$emit('change', name, item.id || item)"
      />
      <span class="ml-2">{{ item.label }}</span>
    </label>
    <small class="has-error" v-if="error">{{ error }}</small>
  </div>
</template>
<script>
export default {
  props: ["name", "value", "options", "error", "disabled"]
};
</script>
<style lang="scss">
.has-error {
  color: $red;
}
</style>
