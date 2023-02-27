<!--
Velobus
Copyright (C) 2023  Manuel Tondeur

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
-->

<script setup>
import {
    onMounted, ref, watch,
} from "vue";

import { useMapStore } from "../stores/map";

const mapStore = useMapStore();
const mapZoomData = mapZoom;
const mapCenterData = mapCenter;

const emit = defineEmits(["trackSelected"]);
const mapOsm = ref({});

onMounted(() => {
    mapOsm.value = L.map("mapid").setView(mapCenterData, mapZoomData);
    const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 19,
        attribution: "&copy; <a href=\"https://www.openstreetmap.org/copyright\">OpenStreetMap</a>",
    });

    osm.addTo(mapOsm.value);
});

watch([() => mapStore.tracks, () => mapStore.stops], ([newTracks, newStops]) => {
    newTracks.forEach((track) => {
        const trackGeoJson = track.track_coordinates;
        L.geoJSON(trackGeoJson, {
            style() {
                return {
                    color: track.color,
                    weight: 6,
                };
            },
        }).on("click", () => {
            emit("trackSelected", track.id);
        }).addTo(mapOsm.value);
    });

    newStops.forEach((stop) => {
        L.marker([stop.coordinates[1], stop.coordinates[0]])
            .bindPopup(
                `<strong>Lieu</strong>: ${stop.place} </ br><strong>Départ</strong>: ${stop.time_morning ? stop.time_morning.slice(0, 5) : ""} ${stop.time_afternoon ? "<strong>Retour</strong>:" : ""} ${stop.time_afternoon ? stop.time_afternoon.slice(0, 5) : ""}`,
            ).addTo(mapOsm.value);
    });
});

</script>

<template>
    <div id="mapid" />
</template>

<style>
#mapid {
    min-height: 500px;
}

</style>
