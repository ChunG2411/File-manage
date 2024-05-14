import { createRouter, createWebHistory } from 'vue-router'

import Store from '../utils/store'

import Auth from '../views/Auth.vue'
import Home from '../views/Home.vue'
import NotFound from '../views/NotFound.vue'
import Profile from '../views/Profile.vue'
import FileView from '../views/FileView.vue'

import Card from '../components/card.vue'


const routes = [
    {
        name: "login",
        path: "/login",
        component: Auth,
        meta: {
            requiresAuth: false,
            title: "Đăng nhập",
        }
    },
    {
        name: "home",
        path: "/",
        component: Home,
        children: [
            {
                name: 'card_folder',
                path: '/folder/:id',
                component: Card
            },
            {
                name: 'card',
                path: '/home',
                component: Card
            },
            {
                name: 'card_type',
                path: '/home?type=:type',
                component: Card
            }
        ],
        meta: {
            requiresAuth: true,
            title: "Của tôi",
        }
    },
    {
        name: 'file',
        path: '/file/:id',
        component: FileView,
        meta: {
            requiresAuth: true
        }
    },
    {
        name: "profile",
        path: "/profile",
        component: Profile,
        meta: {
            requiresAuth: true,
            title: "Tài khoản",
        }
    },
    {
        name: "not_found",
        path: "/:pathMatch(.*)*",
        component: NotFound,
        meta: {
            requiresAuth: false,
            title: "Không tìm thấy",
        }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to,_, next) => {
    const store = Store()
    if (to.meta.title) {
        document.title = "Drive - " + to.meta.title
    }
    else {
        document.title = "Drive"
    }

    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!store.is_login) {            
            next({ name: 'login' })
        } else {
            next()
        }
    } else {
        next()
    }
})


export default router