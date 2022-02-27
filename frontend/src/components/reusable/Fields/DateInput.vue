<template>
  <div>
    <div class="d-flex align-items-center flex-wrap dateInput">
      <v-select
        :name="`date-dropdown-date-${name}`"
        v-if="!onlyMonthAndYear"
        :value="outputDd"
        @input="inputDate"
        :label="label"
        :options="options['date']"
        :taggable="taggable"
        :multiple="multiple"
        :clearable="false"
        :disabled="disabled"
        :class="[
          { 'is-danger': error },
          onlyMonthAndYear ? 'date-field-max' : 'date-field'
        ]"
        :selectOnTab="true"
        class="mr-2"
      />
      <!-- <span v-if="!onlyMonthAndYear" class="px-1 separator">/</span> -->
      <v-select
        :name="`date-dropdown-month-${name}`"
        :value="outputMm"
        @input="inputMonth"
        :label="label"
        :options="options['month']"
        :taggable="taggable"
        :multiple="multiple"
        :clearable="false"
        :disabled="disabled"
        :class="[
          { 'is-danger': error },
          onlyMonthAndYear ? 'month-field-max' : 'month-field'
        ]"
        :selectOnTab="true"
        class="mr-2"
      />
      <!-- <span class="px-1 separator">/</span> -->
      <v-select
        v-if="futureYear"
        :name="`date-dropdown-year-${name}`"
        :value="outputYy"
        @input="inputYear"
        :label="label"
        :options="options['futureyear']"
        :taggable="taggable"
        :multiple="multiple"
        :clearable="false"
        :disabled="disabled"
        :class="[
          { 'is-danger': error },
          onlyMonthAndYear ? 'year-field-max' : 'year-field'
        ]"
        :selectOnTab="true"
      />
      <v-select
        v-else
        :name="`date-dropdown-year-${name}`"
        :value="outputYy"
        @input="inputYear"
        :label="label"
        :options="options['year']"
        :taggable="taggable"
        :multiple="multiple"
        :clearable="false"
        :disabled="disabled"
        :class="[
          { 'is-danger': error },
          onlyMonthAndYear ? 'year-field-max' : 'year-field'
        ]"
        :selectOnTab="true"
      />
    </div>
    <small class="has-error" v-if="error">{{ error }}</small>
  </div>
</template>

<script>
import m from "moment";
import { times } from "lodash";

export default {
  name: "DateInput",
  props: {
    name: {
      type: String,
      default: "DateInput"
    },
    onlyMonthAndYear: {
      type: Boolean,
      default: false
    },
    futureYear: {
      type: Boolean,
      default: false
    },
    value: {
      type: [String, Date],
      default: null
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
      outputDd: null,
      outputMm: null,
      outputYy: null
    };
  },
  computed: {
    momentDate() {
      return this.value && m(this.value) ? m(this.value) : null;
    },
    dd() {
      return this.momentDate
        ? {
            code: this.pad(this.momentDate.date(), 2),
            label: this.pad(this.momentDate.date(), 2)
          }
        : null;
    },
    mm() {
      return this.momentDate
        ? {
            code: this.pad(this.momentDate.month() + 1, 2),
            label: m.monthsShort()[this.momentDate.month()]
          }
        : null;
    },
    yy() {
      return this.momentDate
        ? { code: this.momentDate.year(), label: this.momentDate.year() }
        : null;
    },
    options() {
      const pad = this.pad;
      return {
        date: times(31, i => {
          return { code: pad(i + 1, 2), label: pad(i + 1, 2) };
        }),
        month: times(12, i => {
          return { code: pad(i + 1, 2), label: m.monthsShort()[i] };
        }),
        futureyear: times(50, i => {
          return { code: m().year() + i, label: m().year() + i };
        }),
        year: times(100, i => {
          return { code: m().year() - i, label: m().year() - i };
        })
      };
    },
    outputDate() {
      let d = null;
      if (this.onlyMonthAndYear && this.outputYy && this.outputMm) {
        d = this.outputYy && this.outputYy.code ? this.outputYy.code + "-" : "";
        d = d + (this.outputMm && this.outputMm.code ? this.outputMm.code : "");
      } else if (this.outputYy && this.outputMm && this.outputDd) {
        d = this.outputYy && this.outputYy.code ? this.outputYy.code + "-" : "";
        d =
          d +
          (this.outputMm && this.outputMm.code ? this.outputMm.code + "-" : "");
        d = d + (this.outputDd && this.outputDd.code ? this.outputDd.code : "");
      }
      return d;
    }
  },
  mounted() {
    this.DateValue();
  },
  watch: {
    value() {
      if (!this.value) {
        this.resetDate();
      } else {
        this.DateValue();
      }
    }
  },
  methods: {
    inputDate(value) {
      this.outputDd = value ? value : null;
      this.change();
    },
    inputMonth(value) {
      this.outputMm = value ? value : null;
      this.change();
    },
    inputYear(value) {
      this.outputYy = value ? value : null;
      this.change();
    },
    change() {
      if (this.outputDate) {
        this.$emit("input", this.name, this.outputDate);
        this.$emit("change", this.name, this.outputDate);
      }
    },
    pad(n, width, z) {
      z = z || "0";
      n = n + "";
      return n.length >= width
        ? n
        : new Array(width - n.length + 1).join(z) + n;
    },
    resetDate() {
      this.outputDd = null;
      this.outputMm = null;
      this.outputYy = null;
    },
    DateValue() {
      (this.outputDd = this.dd),
        (this.outputMm = this.mm),
        (this.outputYy = this.yy);
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
.dateInput {
  .date-field,
  .month-field,
  .year-field {
    min-width: 100px;
    max-width: 120px;
  }
  .date-field-max,
  .month-field-max,
  .year-field-max {
    min-width: 100px;
    max-width: 120px;
  }
}
</style>
