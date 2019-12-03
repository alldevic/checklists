import Vue from 'vue'
import Router from 'vue-router'
import store from './store/store'

import Login from './views/Login.vue'
import Checklists from './views/Checklists.vue'
import Checklist from './views/Checklist.vue'
import Report from './views/Report.vue'
import Reports from './views/Reports.vue'
import Profile from './views/Profile.vue'
import FilledChecklists from '@/views/FilledChecklists.vue'
import FilledChecklist from '@/views/FilledChecklist.vue'
import PageNotFound from '@/views/PageNotFound.vue'

Vue.use(Router);

let router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      name: 'checklists',
      component: Checklists,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/checklist/:id',
      name: 'checklist',
      component: Checklist,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/reports',
      name: 'reports',
      component: Reports,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/report/:id',
      name: 'report',
      component: Report,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/responses',
      name: 'responses',
      component: FilledChecklists,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/response/:id',
      name: 'response',
      component: FilledChecklist,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '*',
      component: PageNotFound,
    },
  ]
});

router.beforeEach((to, from, next) => {
  if(to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters.isLoggedIn) {
      next();
      return
    }
    next('/login')
  } else {
    next()
  }
});

export default router
