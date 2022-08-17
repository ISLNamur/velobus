<script setup>
import axios from "axios";

import { ref, toRaw } from "vue";
import StudentForm from "./components/StudentForm.vue";
import TrackMap from "./components/TrackMap.vue";

import { useMapStore } from "./stores/map";

const mapStore = useMapStore();
mapStore.getData();

const studentForm = ref(null);

function updateTrackSelection(trackId) {
    // console.log($refs.studentForm);
    // studentForm.value.formData.tracks = mapStore.tracks.find((t) => t.id === trackId);
}

</script>

<template>
    <q-layout view="hHh lpR fFf">
        <q-page-container>
            <q-page padding>
                <h1>Vélobus</h1>
                <div class="row">
                    <TrackMap
                        class="col-12 col-sm-6"
                        @track-selected="updateTrackSelection"
                    />
                    <router-view
                        ref="studentForm"
                        class="col-12 col-sm-6"
                    />
                </div>
            </q-page>
        </q-page-container>

        <q-footer
            elevated
            class="bg-grey-8 text-white"
        >
            <q-toolbar>
                <q-toolbar-title>
                    <div>Title</div>
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

</style>
