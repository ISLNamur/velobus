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
import axios from "axios";
import { ref, onBeforeMount } from "vue";
import { useQuasar } from "quasar";
import { useMapStore } from "../stores/map";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

const mapStore = useMapStore();

const dateFilter = ref(null);
const trackFilter = ref(null);
const students = ref([]);
const responsibles = ref([]);

const $q = useQuasar();

function objName(obj) {
    if (!obj) return "";

    return obj.name;
}

function loadStudents() {
    axios.get(`/subscription/api/student_list/?${
        dateFilter.value ? `subscription__subscription_date=${dateFilter.value.id}&` : ""
    }${
        trackFilter.value ? `track=${trackFilter.value.id}&` : ""
    }`)
        .then((resp) => {
            students.value = resp.data;
        });
}

function loadResponsibles() {
    axios.get(`/subscription/api/responsible_list/?${
        dateFilter.value ? `subscription__subscription_date=${dateFilter.value.id}&` : ""
    }${
        trackFilter.value ? `track=${trackFilter.value.id}&` : ""
    }`)
        .then((resp) => {
            responsibles.value = resp.data;
        })
        .catch((err) => {
            if (err.response.status === 403) {
                window.location.assign("/accounts/login");
            }
        });
}

function validate(responsibleId) {
    $q.dialog({
        title: "Valider la personne",
        message: "La personne n'est pas encore validée et ne peut donc pas accéder à la liste des inscriptions (ainsi que toutes les données personnelles !). Si vous reconnaissez cette personne, vous pouvez la valider en cliquant sur «Valider».",
        cancel: "Annuler",
        ok: {
            color: "primary",
            label: "Valider",
        },
    }).onOk(() => {
        axios.post(`/subscription/api/validate/${responsibleId}/`, { validated: true }, token)
            .then(() => {
                const validatedResp = responsibles.value.find((r) => r.uuid === responsibleId);
                validatedResp.validated = true;
            });
    });
}

const availableDates = ref([]);
function displaySub(subs) {
    const subsWithDates = subs.map((s) => {
        const aDate = availableDates.value.find((aD) => aD.id === s.subscription_date);
        return { morning: s.morning, afternoon: s.afternoon, subscription_date: aDate.date };
    }).sort((s1, s2) => s1.subscription_date > s2.subscription_date);

    return subsWithDates.reduce((pV, cV) => {
        const aDate = cV.subscription_date;
        const month = aDate.slice(5, 7);
        const day = aDate.slice(8, 11);
        return `${pV ? `${pV}, ` : ""}${day}/${month} (${cV.morning ? "A" : "-"}|${cV.afternoon ? "R" : "-"})`;
    }, "");
}

const columns = [
    {
        name: "last_name",
        field: "last_name",
        label: "Nom",
    },
    {
        name: "first_name",
        field: "first_name",
        label: "Prénom",
    },
    {
        name: "track",
        field: "track",
        label: "Tracé",
        format: (t) => objName(t),
    },
    {
        name: "stop",
        field: "stop",
        label: "Arrêt",
        format: (s) => objName(s),
    },
    {
        name: "subscription",
        field: "subscription",
        label: "Inscriptions (Aller/Retour)",
        format: (s) => displaySub(s),
    },
];

const columns_resp = [
    {
        name: "last_name",
        field: "last_name",
        label: "Nom",
    },
    {
        name: "first_name",
        field: "first_name",
        label: "Prénom",
    },
    {
        name: "track",
        field: "track",
        label: "Tracé",
        format: (t) => objName(t),
    },
    {
        name: "stop",
        field: "stop",
        label: "Arrêt",
        format: (s) => objName(s),
    },
    {
        name: "subscription",
        field: "subscription",
        label: "Inscriptions (Aller/Retour)",
        format: (s) => displaySub(s),
    },
    {
        name: "phone_number",
        field: "phone_number",
        label: "Tél. responsable",
    },
    {
        name: "validated",
        field: "validated",
        label: "Validé",
    },
];

onBeforeMount(() => {
    Promise.all([
        axios.get("/subscription/api/available_date"),
    ]).then((resps) => {
        availableDates.value = resps[0].data;
        loadStudents();
        loadResponsibles();
    });
});

</script>

<template>
    <div class="row">
        <q-table
            title="Liste des élèves inscrits"
            :rows="students"
            :columns="columns"
            :pagination="{rowsPerPage: 10}"
            class="col-12"
            row-key="uuid"
        >
            <template #top="props">
                <h3 class="gt-xs">
                    Élèves
                </h3>
                <q-space />
                <q-select
                    v-model="dateFilter"
                    label="Filtrer date"
                    :options="availableDates"
                    option-value="id"
                    option-label="date"
                    style="min-width: 160px"
                    clearable
                    @update:model-value="loadStudents();loadResponsibles()"
                />
                <q-select
                    v-model="trackFilter"
                    label="Filtrer tracé"
                    :options="mapStore.tracks"
                    option-value="id"
                    option-label="name"
                    style="min-width: 160px;margin-left:10px"
                    clearable
                    @update:model-value="loadStudents();loadResponsibles()"
                />
            </template>
            <template #header="props">
                <q-tr :props="props">
                    <q-th auto-width />
                    <q-th
                        v-for="col in props.cols"
                        :key="col.name"
                        :props="props"
                    >
                        {{ col.label }}
                    </q-th>
                </q-tr>
            </template>
            <template #body="props">
                <q-tr :props="props">
                    <q-td auto-width>
                        <q-btn
                            size="sm"
                            color="accent"
                            round
                            dense
                            :icon="props.expand ? 'remove' : 'add'"
                            @click="props.expand = !props.expand"
                        />
                    </q-td>
                    <q-td
                        v-for="col in props.cols"
                        :key="col.name"
                        :props="props"
                    >
                        {{ col.value }}
                    </q-td>
                </q-tr>
                <q-tr
                    v-show="props.expand"
                    :props="props"
                >
                    <q-td colspan="100%">
                        <div class="text-left">
                            Tél. étudiant: {{ props.row.student_phone }} <br>
                            Tél. responsable: {{ props.row.phone_number }} <br>
                            École: {{ props.row.school.name }} <br>
                            Classe: {{ props.row.classe }}<br>
                            Adresse: {{ props.row.street }} –
                            {{ props.row.postal_code }} {{ props.row.locality }}
                        </div>
                    </q-td>
                </q-tr>
            </template>
        </q-table>
        <q-table
            title="Liste des responsables inscrits"
            :rows="responsibles"
            :columns="columns_resp"
            :pagination="{rowsPerPage: 10}"
            class="col-12 q-mt-sm"
        >
            <template #top="props">
                <h3 class="gt-xs">
                    Responsables
                </h3>
                <q-space />
                <q-select
                    v-model="dateFilter"
                    label="Filtrer date"
                    :options="availableDates"
                    option-value="id"
                    option-label="date"
                    style="min-width: 160px"
                    clearable
                    @update:model-value="loadStudents();loadResponsibles()"
                />
                <q-select
                    v-model="trackFilter"
                    label="Filtrer tracé"
                    :options="mapStore.tracks"
                    option-value="id"
                    option-label="name"
                    style="min-width: 160px;margin-left:10px"
                    clearable
                    @update:model-value="loadResponsibles();loadStudents();"
                />
            </template>
            <template #body-cell-validated="props">
                <q-td>
                    <span v-if="props.row.validated">
                        <q-icon
                            name="check"
                            color="positive"
                        />
                    </span>
                    <span v-else>
                        <q-btn
                            size="sm"
                            color="primary"
                            icon="check"
                            @click="validate(props.row.uuid)"
                        >
                            Valider
                        </q-btn>
                    </span>
                </q-td>
            </template>
        </q-table>
    </div>
</template>
