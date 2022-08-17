import StudentForm from "../components/StudentForm.vue";

export const routes = [
    { path: "/", component: StudentForm },
    {
        path: "/studentform/:step",
        component: StudentForm,
        props: (route) => ({ step: parseInt(route.params.step) }),
    },
];
