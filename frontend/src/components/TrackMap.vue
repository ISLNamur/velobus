<script setup>
import {
    onMounted, ref, watch,
} from "vue";

import { useMapStore } from "../stores/map";

const mapStore = useMapStore();

const emit = defineEmits(["trackSelected"]);
const mapOsm = ref({});

onMounted(() => {
    mapOsm.value = L.map("mapid").setView([50.4658, 4.8671], 12);
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
            .bindPopup(`<strong>Lieu</strong>: ${stop.place} </ br><strong>Départ</strong>: ${stop.time_morning ? stop.time_morning.slice(0, 5) : ""} <strong>Retour</strong>: ${stop.time_afternoon ? stop.time_afternoon.slice(0, 5) : ""}`)
            .addTo(mapOsm.value);
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
