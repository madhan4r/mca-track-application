<template>
  <div class="pie-legend">
    <div
      class="legend"
      v-for="(legend, index) in data"
      :key="legend.name"
      style="cursor: pointer"
      @click="$router.push(`/global-issues?${legend.urlToGlobalIssues}`)"
    >
      <p
        v-if="useRandomColors"
        class="legend-count m-0"
        :style="`color: ${getRandomColor(index)}`"
      >
        {{ legend.count }}
      </p>
      <p
        v-else
        class="legend-count m-0"
        :style="`color: ${getColor(legend.name)}`"
      >
        {{ legend.count }}
      </p>
      <p class="label">{{ legend.displayName }}</p>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  props: {
    data: {
      type: Array,
      default: () => []
    },
    isFromJobStatus: {
      type: Boolean,
      default: false
    },
    useRandomColors: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapGetters(["getColor", "getRandomColor"])
  }
};
</script>
<style lang="scss" scoped>
.pie-legend {
  display: flex;
  flex-flow: row wrap;
  .legend {
    width: 25%;
    display: flex;
    align-items: center;
    flex-direction: column;
    padding: 5px 0;
    .legend-count {
      font-weight: 600;
      font-size: 16px;
    }
    .label {
      margin: 0;
      white-space: nowrap;
      font-size: 11px;
    }
  }
  @media only screen and (max-width: 320px) {
    .pie-legend {
      .legend {
        width: 33%;
      }
    }
  }
}
</style>
