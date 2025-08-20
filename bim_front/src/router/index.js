import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/Home.vue';
import BIMReview from '@/components/BIMReview.vue';
import ReviewResults from '@/views/ReviewResults.vue';
import UserLogin from '@/views/UserLogin.vue';
import UserRegister from '@/views/Register.vue';
import History from '@/views/History.vue';
import ifcView from '@/components/ifcView.vue';
import TestVue from "@/components/TestVue.vue";
import TestVue2 from "@/components/TestVue2.vue";

const routes = [
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/login',
        name: 'login',
        component: UserLogin,
    },
    {
        path: '/register',
        name: 'UserRegister',
        component: UserRegister,
    },
    {
        path: '/home',
        name: 'home',
        component: Home,
    },
    {
        path: '/upload',
        name: 'upload',
        component: BIMReview,
    },
    {
        path: '/results',
        name: 'results',
        component: ReviewResults,
        props: route => ({ results: route.params.results }),
    },
    {
        path: '/review-result',
        name: 'ReviewResult',
        component: ReviewResults,
    },
    {
        path: '/history',
        name: 'History',
        component: History,
    },
    {
        path: '/ifcView',
        name: 'ifcView',
        component: ifcView,
    },
    {
        path: '/test',
        name: 'test',
        component: TestVue
    },
    {
        path: '/test2',
        name: 'test2',
        component: TestVue2
    },

];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;