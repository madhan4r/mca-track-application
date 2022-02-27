import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import CoreuiVue from "@coreui/vue";
import { iconsSet as icons } from "./assets/icons/icons.js";
import { ValidationProvider, ValidationObserver, extend } from "vee-validate";
import moment from "moment";
import vSelect from "vue-select";
import { VueEditor } from "vue2-editor";
import {
  interceptorsSetup,
  interceptorsResponse
} from "@/helpers/interceptors";
// https://vuesax.com/docs/guide/#whats-is-vuesax
import Vuesax from "vuesax";
import "vuesax/dist/vuesax.css"; //Vuesax styles
import VueDatePicker from "@mathieustan/vue-datepicker";
import "@mathieustan/vue-datepicker/dist/vue-datepicker.min.css";

// Install components globally
Vue.use(CoreuiVue);
Vue.use(VueDatePicker);
Vue.component("ValidationObserver", ValidationObserver);
Vue.component("ValidationProvider", ValidationProvider);
Vue.component("VueEditor", VueEditor);
Vue.component("v-select", vSelect);
Vue.use(Vuesax, {
  colors: {
    primary: "#67eb1b",
    secondary: "#b8b8b8"
  }
});

Vue.config.productionTip = false;
Vue.prototype.$moment = moment;

extend("required", {
  validate(value) {
    let isValid;
    if (Array.isArray(value)) {
      isValid = value.length > 0;
    } else {
      isValid = ["", null, undefined].indexOf(value) === -1;
    }
    return {
      required: true,
      valid: isValid
    };
  },
  message: "This field is required",
  computesRequired: true
});

interceptorsSetup();
interceptorsResponse();

new Vue({
  router,
  store,
  icons,
  render: h => h(App)
}).$mount("#app");
