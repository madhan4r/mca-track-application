<template>
  <div class="donut">
    <div class="donut-inner">
      <b>{{ sumOfTotal }}</b>
      <Br />
      <small>
        <!-- <router-link to="/job-list">Total List</router-link> -->
        Total
      </small>
    </div>
    <CChartDoughnut
      :datasets="defaultDatasets"
      :labels="labels"
      :options="options"
    />
  </div>
</template>

<script>
import { CChartDoughnut } from "@coreui/vue-chartjs";
import { mapGetters } from "vuex";

export default {
  name: "Pie",
  components: { CChartDoughnut },
  props: {
    PieChartData: {
      type: Array,
      default: () => []
    },
    useRandomColors: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      labels: this.getlabels,
      options: {
        circumference: 2 * Math.PI,
        maintainAspectRatio: false,
        cutoutPercentage: 80,
        legend: {
          display: false
        },
        title: {
          display: false,
          text: " Pie Chart "
        }
      }
    };
  },
  computed: {
    ...mapGetters(["getColor", "getRandomColor"]),
    getlabels() {
      return this.PieChartData.map(val => val.label);
    },
    backgroundColor() {
      return this.PieChartData.map((val, index) =>
        val.color
          ? val.color
          : this.useRandomColors
          ? this.getRandomColor(index)
          : this.getColor(val.name)
      );
    },
    data() {
      return this.PieChartData.map(val => val.value);
    },
    sumOfTotal() {
      return this.data.reduce((a, b) => a + b, 0);
    },
    defaultDatasets() {
      return [
        {
          backgroundColor: this.backgroundColor,
          data: this.data
        }
      ];
    }
  }
};
</script>

<style lang="scss" scoped>
.donut {
  width: auto;
  position: relative;
  .donut-inner {
    width: 100%;
    top: 7em;
    position: relative;
    left: 0;
    margin-top: -20px;
    line-height: 19px;
    text-align: center;
    z-index: 9;
    b {
      font-size: 25px;
    }
  }
}
</style>
