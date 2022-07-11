<script setup>
import { onMounted, ref } from "vue";

import axios from "axios";

const zoom = ref(12);
const iconWidth = ref(25);
const iconHeight = ref(40);

const geojson = ref({});
onMounted(() => {
    const mymap = L.map('mapid').setView([50.4658, 4.8671], 12);
    var osm_malnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    osm_malnik.addTo(mymap);
    var marker = new L.Marker([50.4658, 4.8671]);
    marker.addTo(mymap);


    function popUp(f, l) {
        var out = [];
        image = '';
        if (f.properties && f.geometry.type === 'Point') {
            for (key in f.properties) {
                // ignore marker for now;
                if (key.startsWith("marker")) continue;
                // Add image
                if (key === 'image') {
                    image = f.properties[key];
                    continue;
                }

                out.push("<strong>" + key + "</strong>: " + f.properties[key]);
            }

            // Prepend image
            out.unshift("<img src='" + image + "'/>");

            l.bindPopup(out.join("<br />"));

            colorMap = { "#ff0000": 'red', '#0000ff': 'blue', '#ffff00': 'orange', '#00ff00': 'green', '#804040': 'darkpurple', '#ff00ff': 'pink' }
            markerMap = { 'bicycle': 'bicycle', 'school': 'users' }

            // Set icon
            var marker = L.AwesomeMarkers.icon({
                prefix: 'fa',
                icon: markerMap[f.properties['marker-symbol']],
                markerColor: colorMap[f.properties['marker-color']]
            });
            l.setIcon(marker);

            return;
        }

        if (f.geometry && f.geometry.type === 'LineString') {
            if (f.properties) {
                l.options.weight = f.properties['stroke-width'] + 3;
                l.options.color = f.properties['stroke'];
                l.options.opacity = f.properties['stroke-opacity'];
            }
            if (f.properties.trackId) {
                l.on('click', function () {
                    // Do on track
                    $("option[value='" + f.properties.trackId[0] + "']").prop('selected', true);
                });
            }
        }
    }

    var jsonTest = new L.GeoJSON.AJAX(["/static/velobus.geojson"], { onEachFeature: popUp }).addTo(mymap);
});

</script>

<template>
    <div id="mapid">
    </div>
</template>