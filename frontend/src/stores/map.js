// Velobus
// Copyright (C) 2023  Manuel Tondeur

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
