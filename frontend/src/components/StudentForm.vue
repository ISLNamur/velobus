<script setup>
import { onBeforeMount, reactive, ref } from "vue";
import axios from "axios";

const props = defineProps({
    uuid: {
        type: String,
        default: '',
    },
});

const formData = reactive({
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

const schoolOptions = ref([]);
const trackOptions = ref([]);
const meetingOptions = ref([]);

const step = ref(1);

onBeforeMount(() => {
    axios.get("/subscription/api/school/")
        .then(resp => {
            schoolOptions.value = resp.data;
        })
})

</script>

<template>
    <div>
        <q-form>
            <q-stepper v-model="step" vertical color="primary" animated>
                <q-step :name="1" title="Lieu de rencontre" :done="step > 1">
                    <q-select v-model="formData.school" :options="trackOptions" label="Choix du tracé"></q-select>
                    <q-select v-model="formData.school" :options="meetingOptions" label="Point de départ"></q-select>
                    <q-stepper-navigation>
                        <q-btn @click="step = 2" color="primary" label="Continuer" />
                    </q-stepper-navigation>
                </q-step>

                <q-step :name="2" title="Identité de l'élève" :done="step > 2">
                    <q-input v-model="formData.last_name" label="Nom de l'élève" />
                    <q-input v-model="formData.first_name" label="Prénom de l'élève" />
                    <q-select v-model="formData.school" :options="schoolOptions" label="École de l'élève"></q-select>
                    <q-input v-model="formData.classe" label="Classe de l'élève" />
                    <q-input v-model="formData.street" label="Rue" />
                    <q-input v-model="formData.postal_code" label="Code postal" type="number" />
                    <q-stepper-navigation>
                        <q-btn @click="step = 3" color="primary" label="Continuer" />
                        <q-btn flat @click="step = 1" color="primary" label="Retour" class="q-ml-sm" />
                    </q-stepper-navigation>
                </q-step>

                <q-step :name="3" title="Moyen de contact" :done="step > 3">
                    <q-input v-model="formData.student_phone" label="GSM de l'élève" type="tel">
                        <template v-slot:prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input v-model="formData.phone_number" label="GSM d'un responsable" type="tel">
                        <template v-slot:prepend>
                            <q-icon name="phone" />
                        </template>
                    </q-input>
                    <q-input v-model="formData.email" label="Email de contact" type="email">
                        <template v-slot:prepend>
                            <q-icon name="email" />
                        </template>
                    </q-input>
                    <q-stepper-navigation>
                        <q-btn @click="step = 3" color="primary" label="Continuer" />
                        <q-btn flat @click="step = 2" color="primary" label="Retour" class="q-ml-sm" />
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