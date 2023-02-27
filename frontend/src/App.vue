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
import { ref } from "vue";

import { useMapStore } from "./stores/map";

const halfView = "col-12 col-sm-6";
const fullView = "col-12";
// eslint-disable-next-line no-undef
const formTitleText = formTitle;

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
                <h1>{{ formTitleText }}</h1>
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
                    <div>
                        <a href="https://github.com/ISLNamur/velobus">Vélobus</a> est un logiciel libre sous licence
                        <a href="https://www.gnu.org/licenses/agpl-3.0.html">AGPL 3.0</a>.
                    </div>
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
