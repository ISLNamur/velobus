import StudentForm from "../components/StudentForm.vue";
import ResponsibleForm from "../components/ResponsibleForm.vue";
import SubscriberList from "../components/SubscriberList.vue";

// eslint-disable-next-line import/prefer-default-export
export const routes = [
    { path: "/", component: StudentForm },
    { path: "/list/", component: SubscriberList },
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
    {
        path: "/responsible/:step/:uuid",
        component: ResponsibleForm,
        props: (route) => ({ step: parseInt(route.params.step), uuid: route.params.uuid }),
    },
    {
        path: "/responsible/:step/",
        component: ResponsibleForm,
        props: (route) => ({ step: parseInt(route.params.step) }),
    },
];
