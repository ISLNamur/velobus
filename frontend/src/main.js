import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHashHistory } from "vue-router";
import { Quasar, Dialog } from "quasar";
import "@quasar/extras/material-icons/material-icons.css";
import "quasar/dist/quasar.css";

import App from "./App.vue";
import { routes } from "./routers/router";

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

const myApp = createApp(App);

myApp.use(Quasar, {
    plugins: {
        Dialog,
    },
    extras: [
    ],
});

myApp.use(createPinia());
myApp.use(router);

myApp.mount("#app");
