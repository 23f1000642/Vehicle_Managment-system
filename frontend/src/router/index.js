import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

// Views
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import UserDashboard from '@/views/UserDashboard.vue'

// Admin Pages
import ParkingLotsManagement from '@/views/admin/ParkingLotsManagement.vue'
import AdminAnalytics from '@/views/admin/AdminAnalytics.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import BackgroundJobs from '@/views/admin/BackgroundJobs.vue'

// User Pages (Create these files to uncomment)
import BookParking from '@/views/user/BookParking.vue'
import ParkingHistory from '@/views/user/ParkingHistory.vue'
import UserAnalytics from '@/views/user/UserAnalytics.vue'
import UserProfile from '@/views/user/UserProfile.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresGuest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresGuest: true }
  },
  
  // Admin Routes
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/parking-lots',
    name: 'ParkingLotsManagement',
    component: ParkingLotsManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/analytics',
    name: 'AdminAnalytics',
    component: AdminAnalytics,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/jobs',
    name: 'BackgroundJobs',
    component: BackgroundJobs,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  
  // User Routes (All files created and ready!)
  {
    path: '/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, requiresUser: true }
  },
  {
    path: '/user/book-parking',
    name: 'BookParking',
    component: BookParking,
    meta: { requiresAuth: true, requiresUser: true }
  },
  {
    path: '/user/parking-history',
    name: 'ParkingHistory',
    component: ParkingHistory,
    meta: { requiresAuth: true, requiresUser: true }
  },
  {
    path: '/user/analytics',
    name: 'UserAnalytics',
    component: UserAnalytics,
    meta: { requiresAuth: true, requiresUser: true }
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true, requiresUser: true }
  },
  
  // Catch all route
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.state.isAuthenticated
  const user = store.state.user
  
  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // Check if route requires guest (not logged in)
  if (to.meta.requiresGuest && isAuthenticated) {
    if (user?.role === 'admin') {
      next('/admin')
    } else {
      next('/dashboard')
    }
    return
  }
  
  // Check if route requires admin
  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    next('/dashboard')
    return
  }
  
  // Check if route requires user role
  if (to.meta.requiresUser && user?.role !== 'user') {
    next('/admin')
    return
  }
  
  next()
})

export default router