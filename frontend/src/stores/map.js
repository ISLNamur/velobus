import axios from "axios";

import { defineStore } from "pinia";

// eslint-disable-next-line import/prefer-default-export
export const useMapStore = defineStore("map", {
    state: () => ({
        tracks: [],
        stops: [],
    }),
    actions: {
        async getData() {
            if (this.tracks.length === 0 || this.stops.length === 0) {
                await Promise.all([
                    axios.get("/subscription/api/track/"),
                    axios.get("/subscription/api/stop/"),
                ]).then((resps) => {
                    this.tracks = resps[0].data;
                    this.stops = resps[1].data;
                    return resps;
                });
            }
        },
    },
});
