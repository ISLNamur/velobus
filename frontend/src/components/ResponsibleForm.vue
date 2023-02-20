<script setup>
import {
    onBeforeMount, reactive, ref, watch, defineEmits, computed,
} from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

import { useMapStore } from "../stores/map";
import TrackMap from "./TrackMap.vue";

const token = { xsrfCookieName: "csrftoken", xsrfHeaderName: "X-CSRFToken" };
// eslint-disable-next-line no-undef
const scheduleCommentText = scheduleComment;

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

const emit = defineEmits(["exposeTrack", "updateId"]);

const formData = reactive({
    track: null,
    stop: null,
    last_name: "",
    school: null,
    first_name: "",
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
const pointOfContact = ref([]);
const dates = ref([]);
const trackForm = ref(null);
const stopForm = ref(null);
const lastNameForm = ref(null);
const firstNameForm = ref(null);
const schoolForm = ref(null);
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
        ) {
            return false;
        }
        lastNameForm.value.resetValidation();
        firstNameForm.value.resetValidation();
        return true;

    case 3:
        if (!phoneNumberForm.value.validate() || !emailForm.value.validate()
        ) {
            return false;
        }
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

    router.push(`/responsible/${to}/${props.uuid}`);
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
                    loading.value = false;
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
    router.push("/responsible/1")
        .then(() => {
            window.location.reload();
        });
}

const getPointOfContact = computed(
    () => (formData.track ? pointOfContact.value.find((pOC) => pOC.track === formData.track.id) : ""),
);

const stopsFromTrack = computed(
    () => {
        if (!formData.track) return mapStore.stops;

        return mapStore.stops.filter((s) => s.track === formData.track.id);
    },
);

onBeforeMount(() => {
    Promise.all([
        axios.get("/subscription/api/school/"),
        axios.get("/subscription/api/available_date/"),
        axios.get("/subscription/api/point_of_contact/"),
    ]).then((resps) => {
        schoolOptions.value = resps[0].data;
        availableDates.value = resps[1].data;
        pointOfContact.value = resps[2].data;

        if (props.uuid) {
            axios.get(`/subscription/api/responsible/${props.uuid}`)
                .then((resp) => {
                    mapStore.getData();
                    formData.track = mapStore.tracks.find((t) => t.id === resp.data.track);
                    formData.stop = mapStore.stops.find((s) => s.id === resp.data.stop);
                    formData.last_name = resp.data.last_name;
                    formData.first_name = resp.data.first_name;
                    formData.school = schoolOptions.value.find((s) => s.id === resp.data.school);
                    formData.phone_number = resp.data.phone_number;
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
        <div class="row">
            <q-form class="col-12 col-sm-6">
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
                            :options="stopsFromTrack"
                            option-value="id"
                            option-label="name"
                            label="Point de départ"
                            :rules="[val => !!val || 'Vous devez choisir un arrêt.']"
                            @update:model-value="selectTrackFromStop"
                        />
                        <p v-if="scheduleCommentText">
                            {{ scheduleCommentText }}
                        </p>
                        <p v-if="formData.stop">
                            <span v-if="formData.stop.time_morning">
                                Heure de départ vers l'école :
                                <strong>
                                    {{ formData.stop.time_morning.slice(0, 5).replace(":", "h") }}
                                </strong><br>
                            </span>
                            <span v-if="formData.stop.time_afternoon">
                                Heure de retour :
                                <strong>
                                    {{ formData.stop.time_afternoon.slice(0, 5).replace(":", "h") }}
                                </strong>
                            </span>
                        </p>
                        <p v-if="getPointOfContact">
                            <strong>Référent du tracé</strong>:
                            {{ getPointOfContact.last_name }} {{ getPointOfContact.first_name }}
                            ({{ getPointOfContact.phone_number }})
                        </p>
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
                        title="Identité"
                        :done="step > 2"
                    >
                        <q-input
                            ref="lastNameForm"
                            v-model="formData.last_name"
                            label="Nom"
                            :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                        />
                        <q-input
                            ref="firstNameForm"
                            v-model="formData.first_name"
                            label="Prénom"
                            :rules="[val => val.trim().length > 0 || 'Ce champ est nécessaire.']"
                        />
                        <q-select
                            ref="schoolForm"
                            v-model="formData.school"
                            :options="schoolOptions"
                            option-label="name"
                            option-value="id"
                            label="École"
                            :rules="[val => !!val || 'Vous devez choisir une école']"
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
                            ref="phoneNumberForm"
                            v-model="formData.phone_number"
                            label="GSM"
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
                        <p v-if="formData.school">
                            <strong>{{ formData.school.comment }}</strong>
                        </p>
                        <div class="q-pa-md">
                            <div
                                v-for="date in availableDates"
                                :key="date"
                                class="q-gutter-sm"
                            >
                                <p class="datelabel">
                                    {{ date.date.slice(8, 10) }}/{{ date.date.slice(5, 7) }}
                                </p>
                                <q-checkbox
                                    v-model="dates"
                                    :val="`${date.id}_morning_${
                                        date.dateSubId ? date.dateSubId : ''
                                    }`"
                                    label="Aller (matin)"
                                    dense
                                />
                                <q-checkbox
                                    v-model="dates"
                                    :val="`${date.id}_afternoon_${
                                        date.dateSubId ? date.dateSubId : ''
                                    }`"
                                    label="Retour (après-midi)"
                                    dense
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
                                @click="submitData('responsible')"
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
            <TrackMap class="col-12 col-sm-6" />
        </div>
    </div>
</template>

<style>
h3 {
    font-size: 2rem;
}
</style>
