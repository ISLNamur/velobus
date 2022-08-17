<script setup>
import {
    onBeforeMount, reactive, ref, watch,
} from "vue";
import axios from "axios";

import { useMapStore } from "../stores/map";

const mapStore = useMapStore();

const props = defineProps({
    uuid: {
        type: String,
        default: "",
    },
    step: {
        type: Number,
        default: 1,
    },
});

const formData = reactive({
    tracks: null,
    stops: null,
    last_name: "",
    first_name: "",
    uuid: "",
    school: "",
    classe: "",
    street: "",
    postal_code: null,
    locality: "",
    student_phone: "",
    phone_number: "",
    email: "",
});

defineExpose({ formData });

const schoolOptions = ref([]);
const availableDates = ref([]);
const dates = ref([]);

onBeforeMount(() => {
    axios.get("/subscription/api/school/")
        .then((resp) => {
            schoolOptions.value = resp.data;
        });
    axios.get("/subscription/api/available_date/")
        .then((resp) => {
            availableDates.value = resp.data;
        });
});

function selectTrackFromStop(event) {
    formData.tracks = mapStore.tracks.find((t) => t.id === event.track);
}

watch(() => formData.tracks, (newVal) => {
    if (formData.stops && formData.stops.track !== newVal.id) {
        formData.stops = null;
    }
});

</script>

<template>
    <div>
        <q-form>
            <q-stepper
                v-model="step"
                vertical
                color="primary"
                animated
            >
                <q-step
                    :name="1"
                    title="Lieu de rencontre"
                    :done="step > 1"
                >
                    <q-select
                        v-model="formData.tracks"
                        :options="mapStore.tracks"
                        option-value="id"
                        option-label="name"
                        label="Choix du tracé"
                    />
                    <q-select
                        v-model="formData.stops"
                        :options="mapStore.stops"
                        option-value="id"
                        option-label="name"
                        label="Point de départ"
                        @update:model-value="selectTrackFromStop"
                    />
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="$router.push('/studentform/2')"
                        />
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="2"
                    title="Identité de l'élève"
                    :done="step > 2"
                >
                    <q-input
                        v-model="formData.last_name"
                        label="Nom de l'élève"
                    />
                    <q-input
                        v-model="formData.first_name"
                        label="Prénom de l'élève"
                    />
                    <q-select
                        v-model="formData.school"
                        :options="schoolOptions"
                        option-label="name"
                        option-value="id"
                        label="École de l'élève"
                    />
                    <q-input
                        v-model="formData.classe"
                        label="Classe de l'élève"
                    />
                    <q-input
                        v-model="formData.street"
                        label="Rue"
                    />
                    <q-input
                        v-model="formData.postal_code"
                        label="Code postal"
                        type="number"
                    />
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="$router.push('/studentform/3')"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="$router.push('/studentform/1')"
                        />
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="3"
                    title="Moyen de contact"
                    :done="step > 3"
                >
                    <q-input
                        v-model="formData.student_phone"
                        label="GSM de l'élève"
                        type="tel"
                    >
                        <template #prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input
                        v-model="formData.phone_number"
                        label="GSM d'un responsable"
                        type="tel"
                    >
                        <template #prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input
                        v-model="formData.email"
                        label="Email de contact"
                        type="email"
                    >
                        <template #prepend>
                            <q-icon name="email" />
                        </template>
                    </q-input>
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="$router.push('/studentform/4')"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="$router.push('/studentform/2')"
                        />
                    </q-stepper-navigation>
                </q-step>
                <q-step
                    :name="4"
                    title="Dates des trajets"
                    :done="step > 4"
                >
                    <div class="q-pa-md">
                        <div
                            v-for="date in availableDates"
                            :key="date"
                            class="q-gutter-sm"
                        >
                            <strong>{{ date.date }}</strong>
                            <q-checkbox
                                v-model="dates"
                                :val="`${date.date}-morning`"
                                label="Aller (matin)"
                            />
                            <q-checkbox
                                v-model="dates"
                                :val="`${date.date}-afternoon`"
                                label="Retour (après-midi)"
                            />
                        </div>
                    </div>
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="$router.push('/studentform/5')"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="$router.push('/studentform/3')"
                        />
                    </q-stepper-navigation>
                </q-step>
                <q-step
                    :name="5"
                    title="Confirmation"
                    :done="step > 5"
                >
                    <q-stepper-navigation>
                        <q-btn
                            color="positive"
                            label="Valider"
                            @click=""
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="$router.push('/studentform/4')"
                        />
                    </q-stepper-navigation>
                </q-step>
            </q-stepper>
        </q-form>
    </div>
</template>

<style>
h3 {
    font-size: 2rem;
}
</style>
