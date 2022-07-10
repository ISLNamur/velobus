<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
import StudentForm from "./components/StudentForm.vue";
</script>

<template>
    <q-layout view="hHh lpR fFf">
        <q-page-container>
            <q-page padding>
                <div class="row">
                    <StudentForm class="col-12 col-sm-6" />
                </div>
            </q-page>
        </q-page-container>

        <q-footer
            elevated
            class="bg-grey-8 text-white"
        >
            <q-toolbar>
                <q-toolbar-title>
                    <div>Title</div>
                </q-toolbar-title>
            </q-toolbar>
        </q-footer>
    </q-layout>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
