import { defineStore } from 'pinia'

const Store = defineStore('store', {
    state: () => ({
        api: "http://127.0.0.1:8000",
        is_login: (localStorage.getItem('token') === null) ? false : true,
        header: {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}`},
        },

        profile: {
            avatar: '',
            fullname: '',
            email: '',
            store: ''
        },
        limit: {
            store: ''
        },

        component: {
            title: 'Drive của tôi',
            url: 'home'
        },

        loading: false,
        toast: {
            title: '',
            content: ''
        }
    }),
    actions: {
    }
})

export default Store