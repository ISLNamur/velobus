<script setup>
import { ref } from "vue";

import { useMapStore } from "./stores/map";

const halfView = "col-12 col-sm-6";
const fullView = "col-12";

const mapStore = useMapStore();
mapStore.getData();

let updateTrack = () => { };
function getTrackInterface(updateFunction) {
    updateTrack = updateFunction.setTrack;
}

function updateTrackSelection(trackId) {
    updateTrack(trackId);
}

</script>

<template>
    <q-layout view="hHh lpR fFf">
        <q-page-container>
            <q-page padding>
                <h1>Vélobus</h1>
                <div>
                    <router-view @expose-track="getTrackInterface" />
                </div>
            </q-page>
        </q-page-container>

        <q-footer
            elevated
            class="bg-grey-8 text-white"
        >
            <q-toolbar>
                <q-toolbar-title>
                    <div>Vélobus</div>
                </q-toolbar-title>
            </q-toolbar>
        </q-footer>
    </q-layout>
</template>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}
h1 {
    margin-top: 0px;
    margin-bottom: 0px;
}
</style>
