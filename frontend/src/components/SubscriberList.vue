<script setup>
import axios from "axios";
import { ref, onBeforeMount } from "vue";
import { useMapStore } from "../stores/map";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

const mapStore = useMapStore();

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
];
onBeforeMount(() => {
    Promise.all([
        axios.get("/subscription/api/student_list"),
    ]).then((resps) => {
        students.value = resps[0].data;
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
