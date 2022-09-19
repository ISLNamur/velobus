<script setup>
import axios from "axios";
import { ref, onBeforeMount } from "vue";
import { useMapStore } from "../stores/map";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

const mapStore = useMapStore();

const dateFilter = ref(null);
const trackFilter = ref(null);
const students = ref([]);
const responsibles = ref([]);

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
        .catch(err => {
            if (err.response.status === 403) {
                window.location.assign("/accounts/login");
            } 
        })
}

const availableDates = ref([]);
function displaySub(subs) {
    return subs.reduce((pV, cV) => {
        const aDate = availableDates.value.find((aD) => aD.id === cV.subscription_date).date;
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
    {
        name: "student_phone",
        field: "student_phone",
        label: "Tél. étudiant",
    },
    {
        name: "phone_number",
        field: "phone_number",
        label: "Tél. responsable",
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
        label: "Inscriptions",
        format: (s) => displaySub(s),
    },
    {
        name: "phone_number",
        field: "phone_number",
        label: "Tél. responsable",
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
        >
            <template #top="props">
                <h3 class="gt-xs">Élèves</h3>
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
        </q-table>
        <q-table
            title="Liste des responsables inscrits"
            :rows="responsibles"
            :columns="columns_resp"
            :pagination="{rowsPerPage: 10}"
            class="col-12 q-mt-sm"
        >
            <template #top="props">
                <h3 class="gt-xs">Responsables</h3>
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
        </q-table>
    </div>
</template>
