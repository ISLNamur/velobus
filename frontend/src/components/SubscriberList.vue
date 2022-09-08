<script setup>
import axios from "axios";
import { ref, onBeforeMount } from "vue";
import { useMapStore } from "../stores/map";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

const mapStore = useMapStore();

function objName(obj) {
    if (!obj) return "";

    return obj.name;
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

const students = ref([]);
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
        axios.get("/subscription/api/student_list"),
        axios.get("/subscription/api/available_date"),
    ]).then((resps) => {
        students.value = resps[0].data;
        availableDates.value = resps[1].data;
    });
});

</script>

<template>
    <div>
        <q-table
            title="Liste des élèves inscrits"
            :rows="students"
            :columns="columns"
        />
    </div>
</template>
