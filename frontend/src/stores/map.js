import axios from "axios";

import { defineStore } from "pinia";

export const useMapStore = defineStore("map", {
    state: () => ({
        tracks: [],
        stops: [],
    }),
    actions: {
        getData() {
            axios.get("/subscription/api/track/")
                .then((resp) => {
                    this.tracks = resp.data;
                });
            axios.get("/subscription/api/stop/")
                .then((resp) => {
                    this.stops = resp.data;
                });
        },
    },
});
