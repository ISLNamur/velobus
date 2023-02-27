// Velobus
// Copyright (C) 2023  Manuel Tondeur

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.

// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
