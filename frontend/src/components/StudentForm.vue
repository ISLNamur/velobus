<script setup>
import {
    onBeforeMount, reactive, ref, watch, defineEmits,
} from "vue";
import { useRouter } from 'vue-router'
import axios from "axios";

import { useMapStore } from "../stores/map";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };

const mapStore = useMapStore();
const router = useRouter();

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

const emit = defineEmits(["exposeTrack", "updateUuid"]);

const formData = reactive({
    track: null,
    stop: null,
    last_name: "",
    first_name: "",
    school: "",
    classe: "",
    street: "",
    postal_code: null,
    locality: "",
    student_phone: "",
    phone_number: "",
    email: "",
});

if (props.uuid) {
    formData.uuid = props.uuid;
}

defineExpose({ formData });

const schoolOptions = ref([]);
const availableDates = ref([]);
const dates = ref([]);
const trackForm = ref(null);
const stopForm = ref(null);
const lastNameForm = ref(null);
const firstNameForm = ref(null);
const schoolForm = ref(null);
const classeForm = ref(null);
const streetForm = ref(null);
const postalCodeForm = ref(null);
const localityForm = ref(null);
const studentPhoneForm = ref(null);
const phoneNumberForm = ref(null);
const emailForm = ref(null);
const acceptPolicy = ref(false);

function selectTrackFromStop(event) {
    formData.track = mapStore.tracks.find((t) => t.id === event.track);
}

function changeStep(from, to) {
    if (!checkStep(from)) {
        return;
    }

    router.push(`/student/${to}/${props.uuid}`);
}

function checkStep(step) {
    switch (step) {
        case 1:
            if (!trackForm.value.validate() || !stopForm.value.validate()) {
                return false
            } else {
                trackForm.value.resetValidation();
                stopForm.value.resetValidation();
                return true;
            }
        case 2:
            if (
                !lastNameForm.value.validate()
                || !firstNameForm.value.validate()
                || !schoolForm.value.validate()
                || !classeForm.value.validate()
                || !streetForm.value.validate()
                || !postalCodeForm.value.validate()
                || !localityForm.value.validate()
            ) {
                return false;
            } else {
                lastNameForm.value.resetValidation();
                firstNameForm.value.resetValidation();
                schoolForm.value.resetValidation();
                classeForm.value.resetValidation();
                streetForm.value.resetValidation();
                postalCodeForm.value.resetValidation();
                localityForm.value.resetValidation();
                return true;
            }
        case 3:
            if (!studentPhoneForm.value.validate() || !phoneNumberForm.value.validate() || !emailForm.value.validate()) {
                return false;
            } else {
                studentPhoneForm.value.resetValidation();
                phoneNumberForm.value.resetValidation();
                emailForm.value.resetValidation();
                return true;
            }
        case 4:
            return true;
        case 5:
            return true;
    }
}

function submitData(person) {
    if (!acceptPolicy) {
        return;
    }
    const dateSubscriptions = [];
    dates.value.forEach((d) => {
        const splitValue = d.split("_");
        const availDateId = parseInt(splitValue[0], 10);
        const existingDate = dateSubscriptions.find((dS) => dS.subscription_date === availDateId);
        if (existingDate) {
            existingDate[splitValue[1]] = true;
        } else {
            const newDate = { subscription_date: availDateId, comment: "" };
            if (splitValue[2] !== "") {
                newDate.id = parseInt(splitValue[2], 10);
            }
            newDate[splitValue[1]] = true;
            dateSubscriptions.push(newDate);
        }
    });

    console.log(dateSubscriptions);

    const putSub = dateSubscriptions.filter((dS) => "id" in dS)
        .map((dS) => axios.put(`/subscription/api/date_subscription/${dS.id}/`, dS, token));
    const postSub = dateSubscriptions.filter((dS) => !("id" in dS))
        .map((dS) => axios.post("/subscription/api/date_subscription/", dS, token));
    Promise.all(putSub.concat(postSub))
        .then((resps) => {
            const dateSubIds = resps.map((d) => d.data.id);
            formData.subscription = dateSubIds;
            const data = Object.assign({}, formData);
            data.school = data.school.id;
            data.track = data.track.id;
            data.stop = data.stop.id;
            const send = "uuid" in formData ? axios.put : axios.post;
            send(`/subscription/api/${person}/${"uuid" in formData ? formData.uuid : ""}`, data, token)
                .then((resp) => {
                    emit("updateUuid", resp.data.uuid);
                    formData.uuid = resp.data.uuid;
                    return resp;
                });
            return resps;
        });
}

onBeforeMount(() => {
    axios.get("/subscription/api/school/")
        .then((resp) => {
            schoolOptions.value = resp.data;
            return resp;
        });
    // TODO We should add date subscription id to availableDates entries when editing.
    axios.get("/subscription/api/available_date/")
        .then((resp) => {
            availableDates.value = resp.data;
            return resp;
        });

    emit("exposeTrack", {
        setTrack: (trackId) => {
            formData.track = mapStore.tracks.find((t) => t.id === trackId);
        },
    });
});

watch(() => formData.track, (newVal) => {
    if (formData.stop && formData.stop.track !== newVal.id) {
        formData.stop = null;
    }
});

</script>

<template>
    <div>
        <q-form>
            <q-stepper v-model="step" vertical color="primary" animated>
                <q-step :name="1" title="Lieu de rencontre" :done="step > 1">
                    <q-select v-model="formData.track" :options="mapStore.tracks" option-value="id" option-label="name"
                        label="Choix du tracé" :rules="[val => !!val || 'Vous devez choisir un tracé.']"
                        ref="trackForm" />
                    <q-select v-model="formData.stop" :options="mapStore.stops" option-value="id" option-label="name"
                        label="Point de départ" @update:model-value="selectTrackFromStop"
                        :rules="[val => !!val || 'Vous devez choisir un arrêt.']" ref="stopForm" />
                    <q-stepper-navigation>
                        <q-btn color="primary" label="Continuer" @click="changeStep(1, 2)" />
                    </q-stepper-navigation>
                </q-step>

                <q-step :name="2" title="Identité de l'élève" :done="step > 2">
                    <q-input v-model="formData.last_name" label="Nom de l'élève"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="lastNameForm" />
                    <q-input v-model="formData.first_name" label="Prénom de l'élève"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="firstNameForm" />
                    <q-select v-model="formData.school" :options="schoolOptions" option-label="name" option-value="id"
                        label="École de l'élève" :rules="[val => !!val || 'Vous devez choisir une école']"
                        ref="schoolForm" />
                    <q-input v-model="formData.classe" label="Classe de l'élève"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="classeForm" />
                    <q-input v-model="formData.street" label="Rue"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="streetForm" />
                    <q-input v-model="formData.postal_code" label="Code postal" type="number"
                        :rules="[val => val > 999 && val < 10000 || 'Ce champ est nécessaire.']" ref="postalCodeForm" />
                    <q-input v-model="formData.locality" label="Localité"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="localityForm" />
                    <q-stepper-navigation>
                        <q-btn color="primary" label="Continuer" @click="changeStep(2, 3)" />
                        <q-btn flat color="primary" label="Retour" class="q-ml-sm" @click="changeStep(2, 1)" />
                    </q-stepper-navigation>
                </q-step>

                <q-step :name="3" title="Moyen de contact" :done="step > 3">
                    <q-input v-model="formData.student_phone" label="GSM de l'élève" type="tel"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="studentPhoneForm">
                        <template #prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input v-model="formData.phone_number" label="GSM d'un responsable" type="tel"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']" ref="phoneNumberForm">
                        <template #prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input v-model="formData.email" label="Email de contact" type="email"
                        :rules="['email' || 'Ce champ est nécessaire.']" ref="emailForm">
                        <template #prepend>
                            <q-icon name="email" />
                        </template>
                    </q-input>
                    <q-stepper-navigation>
                        <q-btn color="primary" label="Continuer" @click="changeStep(3, 4)" />
                        <q-btn flat color="primary" label="Retour" class="q-ml-sm" @click="changeStep(3, 2)" />
                    </q-stepper-navigation>
                </q-step>
                <q-step :name="4" title="Dates des trajets" :done="step > 4">
                    <div class="q-pa-md">
                        <div v-for="date in     availableDates" :key="date" class="q-gutter-sm">
                            <strong>{{ date.date }}</strong>
                            <q-checkbox v-model="dates"
                                :val="`${date.id}_morning_${date.dateSubId ? date.dateSubId : ''}`"
                                label="Aller (matin)" />
                            <q-checkbox v-model="dates" :val="`${date.id}_afternoon_${date.dateSubId ? date.dateSubId : ''
                            }`" label="Retour (après-midi)" />
                        </div>
                    </div>
                    <q-stepper-navigation>
                        <q-btn color="primary" label="Continuer" @click="changeStep(4, 5)" />
                        <q-btn flat color="primary" label="Retour" class="q-ml-sm" @click="changeStep(4, 3)" />
                    </q-stepper-navigation>
                </q-step>
                <q-step :name="5" title="Confirmation" :done="step > 5">
                    <q-checkbox v-model="acceptPolicy">
                        <slot>
                            Je confirme avoir lu et approuvé la convention ci-dessous.
                        </slot>
                    </q-checkbox>
                    <q-btn color="primary" icon="download" label="Télécharger la convention (pdf)"
                        href="/static/convention.pdf" target="_blank" />
                    <q-stepper-navigation>
                        <q-btn color="positive" label="Valider" :disable="!acceptPolicy"
                            @click="submitData('student')" />
                        <q-btn flat color="primary" label="Retour" class="q-ml-sm" @click="changeStep(5, 4)" />
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
