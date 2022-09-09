<script setup>
import axios from "axios";
import { ref, onBeforeMount } from "vue";
import { useMapStore } from "../stores/map";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

const mapStore = useMapStore();

const dateFilter = ref(null);
const trackFilter = ref(null);
const students = ref([]);

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

const availableDates = ref([]);
function displaySub(subs) {
    return subs.reduce((pV, cV) => {
        const aDate = availableDates.value.find((aD) => aD.id === cV.subscription_date).date;
        const month = aDate.slice(5, 7);
        const day = aDate.slice(8, 11);
        return `${pV ? `${pV}, ` : ""}${day}/${month} (${cV.morning ? "M" : "-"}|${cV.afternoon ? "A" : "-"})`;
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
        label: "Inscriptions",
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

onBeforeMount(() => {
    Promise.all([
        axios.get("/subscription/api/available_date"),
    ]).then((resps) => {
        availableDates.value = resps[0].data;
        loadStudents();
    });
});

</script>

<template>
    <div class="row">
        <q-table
            title="Liste des élèves inscrits"
            :rows="students"
            :columns="columns"
            class="col-12"
        >
            <template #top="props">
                <q-space />
                <q-select
                    v-model="dateFilter"
                    label="Filtrer sur une date"
                    :options="availableDates"
                    option-value="id"
                    option-label="date"
                    style="min-width: 200px"
                    clearable
                    @update:model-value="loadStudents"
                />
                <q-select
                    v-model="trackFilter"
                    label="Filtrer sur un tracé"
                    :options="mapStore.tracks"
                    option-value="id"
                    option-label="name"
                    style="min-width: 200px;margin-left:10px"
                    clearable
                    @update:model-value="loadStudents"
                />
            </template>
        </q-table>
    </div>
</template>
