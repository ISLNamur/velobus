<script setup>
import { reactive } from "vue";

const formData = reactive({
    lastName: "",
    firstName: "",
    uuid: "",
    street: "",
    postalCode: null,
});

const props = defineProps({
    uuid: {
        type: String,
        default: "",
    },
});
</script>

<template>
    <div>
        Coucou
        <q-form>
            <q-input
                v-model="formData.lastName"
                label="Nom de l'élève"
            />
            <q-input
                v-model="formData.firstName"
                label="Prénom de l'élève"
            />
        </q-form>
    </div>
</template>
