import { defineStore } from 'pinia'

const Store = defineStore('store', {
    state: () => ({
        api: "http://127.0.0.1:8000",
        is_login: (localStorage.getItem('token') === null) ? false : true,
        header: {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            },
        },

        profile: {
            avatar: '',
            fullname: '',
            email: '',
            store: '',
            type: ''
        },
        limit: {
            store: ''
        },
        
        reload: false,

        loading: false,
        toast: {
            title: '',
            content: ''
        },
        upload: null,
        lang: 'vi'
    }),
    actions: {
    }
})

export default Store