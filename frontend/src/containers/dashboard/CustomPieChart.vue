<template>
  <CRow class="row d-flex justify-content-start align-items-top">
    <CCol
      class="p-0 d-flex justify-content-center align-items-top"
      lg="4"
      md="4"
      sm="12"
    >
      <Pie :PieChartData="PieChartData" :useRandomColors="useRandomColors" />
    </CCol>
    <CCol
      class="p-0 d-flex flex-column justify-content-center"
      lg="8"
      md="8"
      sm="12"
    >
      <PieChartCustomLegend
        :data="PieChartLegendData"
        :useRandomColors="useRandomColors"
      />
    </CCol>
  </CRow>
</template>

<script>
import Pie from "@/components/reusable/Charts/Pie";
import PieChartCustomLegend from "@/components/reusable/Charts/PieChartCustomLegend";
export default {
  components: {
    Pie,
    PieChartCustomLegend
  },
  props: {
    PieChartLegendData: {
      type: Array,
      default: () => []
    },
    PieChartData: {
      type: Array,
      default: () => []
    },
    useRandomColors: {
      type: Boolean,
      default: false
    }
  }
};
</script>
