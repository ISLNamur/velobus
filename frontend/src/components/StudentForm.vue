<script setup>
import {
    onBeforeMount, reactive, ref, watch, defineEmits,
} from "vue";
import { useRouter } from "vue-router";
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

const loading = ref(false);
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
const successModal = ref(null);
const acceptPolicy = ref(false);

function selectTrackFromStop(event) {
    formData.track = mapStore.tracks.find((t) => t.id === event.track);
}

function checkStep(step) {
    switch (step) {
    case 1:
        if (!trackForm.value.validate() || !stopForm.value.validate()) {
            return false;
        }
        trackForm.value.resetValidation();
        stopForm.value.resetValidation();
        return true;

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
        }
        lastNameForm.value.resetValidation();
        firstNameForm.value.resetValidation();
        schoolForm.value.resetValidation();
        classeForm.value.resetValidation();
        streetForm.value.resetValidation();
        postalCodeForm.value.resetValidation();
        localityForm.value.resetValidation();
        return true;

    case 3:
        if (
            !studentPhoneForm.value.validate()
            || !phoneNumberForm.value.validate()
            || !emailForm.value.validate()
        ) {
            return false;
        }
        studentPhoneForm.value.resetValidation();
        phoneNumberForm.value.resetValidation();
        emailForm.value.resetValidation();
        return true;

    case 4:
        return true;
    case 5:
        return true;
    default:
        return true;
    }
}

function changeStep(from, to) {
    if (!checkStep(from)) {
        return;
    }

    router.push(`/student/${to}/${props.uuid}`);
}

function submitData(person) {
    if (!acceptPolicy.value) {
        return;
    }
    loading.value = true;
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

    const putSub = dateSubscriptions.filter((dS) => "id" in dS)
        .map((dS) => axios.put(`/subscription/api/date_subscription/${dS.id}/`, dS, token));
    const postSub = dateSubscriptions.filter((dS) => !("id" in dS))
        .map((dS) => axios.post("/subscription/api/date_subscription/", dS, token));
    Promise.all(putSub.concat(postSub))
        .then((resps) => {
            const dateSubIds = resps.map((d) => d.data.id);
            formData.subscription = dateSubIds;
            const data = { ...formData };
            data.school = data.school.id;
            data.track = data.track.id;
            data.stop = data.stop.id;
            resps.forEach((dS) => {
                const availDate = availableDates.value.find(
                    (aD) => aD.id === dS.data.subscription_date,
                );
                availDate.dateSubId = dS.data.id;
            });
            const send = "uuid" in formData ? axios.put : axios.post;
            send(`/subscription/api/${person}/${"uuid" in formData ? `${formData.uuid}/` : ""}`, data, token)
                .then((resp) => {
                    formData.uuid = resp.data.uuid;
                    successModal.value.show();
                    return resp;
                })
                .catch(() => {
                    // eslint-disable-next-line no-alert
                    alert("Une erreur s'est produite pendant l'envoi des données, merci de réessayer.");
                    loading.value = false;
                });
            return resps;
        })
        .catch(() => {
            // eslint-disable-next-line no-alert
            alert("Une erreur s'est produite pendant l'envoi des données, merci de réessayer.");
            loading.value = false;
        });
}

function reloadPage() {
    router.push("/")
        .then(() => {
            window.location.reload();
        });
}

onBeforeMount(() => {
    Promise.all([
        axios.get("/subscription/api/school/"),
        axios.get("/subscription/api/available_date/"),
    ]).then((resps) => {
        schoolOptions.value = resps[0].data;
        availableDates.value = resps[1].data;

        if (props.uuid) {
            axios.get(`/subscription/api/student/${props.uuid}`)
                .then((resp) => {
                    formData.track = mapStore.tracks.find((t) => t.id === resp.data.track);
                    formData.stop = mapStore.stops.find((s) => s.id === resp.data.stop);
                    formData.last_name = resp.data.last_name;
                    formData.first_name = resp.data.first_name;
                    formData.school = schoolOptions.value.find((s) => s.id === resp.data.school);
                    formData.classe = resp.data.classe;
                    formData.street = resp.data.street;
                    formData.postal_code = resp.data.postal_code;
                    formData.locality = resp.data.locality;
                    formData.phone_number = resp.data.phone_number;
                    formData.student_phone = resp.data.student_phone;
                    formData.email = resp.data.email;

                    acceptPolicy.value = true;

                    Promise.all(resp.data.subscription.map((s) => axios.get(`/subscription/api/date_subscription/${s}`)))
                        .then((respsDates) => {
                            respsDates.forEach((r) => {
                                const availDate = availableDates.value.find(
                                    (aD) => aD.id === r.data.subscription_date,
                                );
                                availDate.dateSubId = r.data.id;
                                if (r.data.morning) {
                                    dates.value.push(`${r.data.subscription_date}_morning_${r.data.id}`);
                                }
                                if (r.data.afternoon) {
                                    dates.value.push(`${r.data.subscription_date}_afternoon_${r.data.id}`);
                                }
                            });
                        });
                });
        }
        return resps;
    });

    emit("exposeTrack", {
        setTrack: (trackId) => {
            if (props.step === 1) {
                formData.track = mapStore.tracks.find((t) => t.id === trackId);
            }
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
        <q-dialog
            ref="successModal"
            persistent
            transition-show="scale"
            transition-hide="scale"
            @hide="reloadPage"
        >
            <q-card>
                <q-card-section>
                    <div class="text-h6">
                        Merci
                    </div>
                </q-card-section>

                <q-card-section class="q-pt-none">
                    Les données ont été envoyées avec succes !
                    <span v-if="!$route.params.uuid">
                        Un courriel de confirmation reprenant les données
                        de l'inscription a été envoyé.
                    </span>
                </q-card-section>

                <q-card-actions align="right">
                    <q-btn
                        v-close-popup
                        flat
                        label="OK"
                        color="primary"
                    />
                </q-card-actions>
            </q-card>
        </q-dialog>
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
                        ref="trackForm"
                        v-model="formData.track"
                        :options="mapStore.tracks"
                        option-value="id"
                        option-label="name"
                        label="Choix du tracé"
                        :rules="[val => !!val || 'Vous devez choisir un tracé.']"
                    />
                    <q-select
                        ref="stopForm"
                        v-model="formData.stop"
                        :options="mapStore.stops"
                        option-value="id"
                        option-label="name"
                        label="Point de départ"
                        :rules="[val => !!val || 'Vous devez choisir un arrêt.']"
                        @update:model-value="selectTrackFromStop"
                    />
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="changeStep(1, 2)"
                        />
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="2"
                    title="Identité de l'élève"
                    :done="step > 2"
                >
                    <q-input
                        ref="lastNameForm"
                        v-model="formData.last_name"
                        label="Nom de l'élève"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    />
                    <q-input
                        ref="firstNameForm"
                        v-model="formData.first_name"
                        label="Prénom de l'élève"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    />
                    <q-select
                        ref="schoolForm"
                        v-model="formData.school"
                        :options="schoolOptions"
                        option-label="name"
                        option-value="id"
                        label="École de l'élève"
                        :rules="[val => !!val || 'Vous devez choisir une école']"
                    />
                    <q-input
                        ref="classeForm"
                        v-model="formData.classe"
                        label="Classe de l'élève"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    />
                    <q-input
                        ref="streetForm"
                        v-model="formData.street"
                        label="Rue"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    />
                    <q-input
                        ref="postalCodeForm"
                        v-model="formData.postal_code"
                        label="Code postal"
                        type="number"
                        :rules="[val => val > 999 && val < 10000 || 'Ce champ est nécessaire.']"
                    />
                    <q-input
                        ref="localityForm"
                        v-model="formData.locality"
                        label="Localité"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    />
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="changeStep(2, 3)"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="changeStep(2, 1)"
                        />
                    </q-stepper-navigation>
                </q-step>

                <q-step
                    :name="3"
                    title="Moyen de contact"
                    :done="step > 3"
                >
                    <q-input
                        ref="studentPhoneForm"
                        v-model="formData.student_phone"
                        label="GSM de l'élève"
                        type="tel"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    >
                        <template #prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input
                        ref="phoneNumberForm"
                        v-model="formData.phone_number"
                        label="GSM d'un responsable"
                        type="tel"
                        :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                    >
                        <template #prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input
                        ref="emailForm"
                        v-model="formData.email"
                        label="Email de contact"
                        type="email"
                        :rules="['email' || 'Ce champ est nécessaire.']"
                    >
                        <template #prepend>
                            <q-icon name="email" />
                        </template>
                    </q-input>
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="changeStep(3, 4)"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="changeStep(3, 2)"
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
                                :val="`${date.id}_morning_${date.dateSubId ? date.dateSubId : ''}`"
                                label="Aller (matin)"
                            />
                            <q-checkbox
                                v-model="dates"
                                :val="`${date.id}_afternoon_${date.dateSubId ? date.dateSubId : ''
                                }`"
                                label="Retour (après-midi)"
                            />
                        </div>
                    </div>
                    <q-stepper-navigation>
                        <q-btn
                            color="primary"
                            label="Continuer"
                            @click="changeStep(4, 5)"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="changeStep(4, 3)"
                        />
                    </q-stepper-navigation>
                </q-step>
                <q-step
                    :name="5"
                    title="Confirmation"
                    :done="step > 5"
                >
                    <q-checkbox v-model="acceptPolicy">
                        <slot>
                            Je confirme avoir lu et approuvé la convention ci-dessous.
                        </slot>
                    </q-checkbox>
                    <q-btn
                        color="primary"
                        icon="download"
                        label="Télécharger la convention (pdf)"
                        href="/static/convention.pdf"
                        target="_blank"
                    />
                    <q-stepper-navigation>
                        <q-btn
                            color="positive"
                            label="Valider"
                            :disable="!acceptPolicy"
                            :loading="loading"
                            @click="submitData('student')"
                        />
                        <q-btn
                            flat
                            color="primary"
                            label="Retour"
                            class="q-ml-sm"
                            @click="changeStep(5, 4)"
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
