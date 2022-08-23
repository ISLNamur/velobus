import StudentForm from "../components/StudentForm.vue";

export const routes = [
    { path: "/", component: StudentForm },
    {
        path: "/student/:step/:uuid",
        component: StudentForm,
        props: (route) => ({ step: parseInt(route.params.step), uuid: route.params.uuid }),
    },
    {
        path: "/student/:step/",
        component: StudentForm,
        props: (route) => ({ step: parseInt(route.params.step) }),
    },
];
