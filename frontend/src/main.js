import "vite/modulepreload-polyfill";

import { createApp } from "vue";
import { Quasar } from "quasar";
import "@quasar/extras/material-icons/material-icons.css";
import "quasar/dist/quasar.css";

import App from "./App.vue";

const myApp = createApp(App);

myApp.use(Quasar, {
    plugins: {}, // import Quasar plugins and add here
    extras: [
    ]
});

myApp.mount("#app");
