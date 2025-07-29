<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg" :class="navbarClass">
      <div class="container">
        <!-- Brand -->
        <router-link class="navbar-brand d-flex align-items-center" to="/">
          <span class="me-2">🚗</span>
          <span>Vehicle Parking Management</span>
        </router-link>
        
        <!-- Mobile Toggle -->
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <!-- Navigation Items -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <span class="me-1">🏠</span>Home
              </router-link>
            </li>
          </ul>

          <ul class="navbar-nav">
            <!-- Theme Toggle -->
            <li class="nav-item">
              <button 
                @click="toggleDarkMode" 
                class="btn btn-outline-light btn-sm me-2"
                :class="{ 'btn-outline-dark': isDarkMode }"
              >
                <span class="me-1">{{ isDarkMode ? '☀️' : '🌙' }}</span>
                {{ isDarkMode ? 'Light' : 'Dark' }}
              </button>
            </li>

            <!-- Unauthenticated Links -->
            <template v-if="!isAuthenticated">
              <li class="nav-item">
                <router-link class="nav-link" to="/login">
                  <span class="me-1">🔑</span>Login
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" to="/register">
                  <span class="me-1">📝</span>Register
                </router-link>
              </li>
            </template>
            
            <!-- Authenticated Links -->
            <template v-if="isAuthenticated">
              <li v-if="isAdmin" class="nav-item">
                <router-link class="nav-link" to="/admin">
                  <span class="me-1">⚙️</span>Admin Dashboard
                </router-link>
              </li>
              <li v-if="isUser" class="nav-item">
                <router-link class="nav-link" to="/dashboard">
                  <span class="me-1">📊</span>My Dashboard
                </router-link>
              </li>
              
              <!-- User Dropdown -->
              <li class="nav-item dropdown">
                <a 
                  class="nav-link dropdown-toggle d-flex align-items-center" 
                  href="#" 
                  id="navbarDropdown" 
                  role="button" 
                  data-bs-toggle="dropdown"
                >
                  <span class="me-1">👤</span>{{ user?.username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li>
                    <div class="dropdown-header">
                      <div class="d-flex align-items-center">
                        <span class="me-2">👤</span>
                        <div>
                          <div class="fw-bold">{{ user?.username }}</div>
                          <small class="text-muted">{{ user?.role }}</small>
                        </div>
                      </div>
                    </div>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item" href="#" @click="logout">
                      <span class="me-2">🚪</span>Logout
                    </a>
                  </li>
                </ul>
              </li>
            </template>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="container mt-4">
      <router-view />
    </main>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="text-center text-white">
        <div class="spinner-border mb-3" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <div>Loading...</div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'App',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()
    
    const isDarkMode = ref(false)

    const isAuthenticated = computed(() => store.state.isAuthenticated)
    const user = computed(() => store.state.user)
    const loading = computed(() => store.state.loading)
    const isAdmin = computed(() => store.getters.isAdmin)
    const isUser = computed(() => store.getters.isUser)

    const navbarClass = computed(() => ({
      'navbar-dark bg-primary': !isDarkMode.value,
      'navbar-dark bg-dark': isDarkMode.value
    }))

    // Load theme preference
    onMounted(() => {
      const savedTheme = localStorage.getItem('darkMode')
      if (savedTheme) {
        isDarkMode.value = JSON.parse(savedTheme)
      } else {
        isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
    })

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', JSON.stringify(isDarkMode.value))
    }

    const logout = () => {
      store.dispatch('logout')
      toast.success('Logged out successfully')
      router.push('/')
    }

    return {
      isAuthenticated,
      user,
      loading,
      isAdmin,
      isUser,
      isDarkMode,
      navbarClass,
      toggleDarkMode,
      logout
    }
  }
}
</script>

<style>
/* Base App Styles */
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  background-color: #f8f9fa;
  color: #212529;
  transition: background-color 0.3s ease, color 0.3s ease;
}

#app.dark-mode {
  background-color: #212529;
  color: #f8f9fa;
}

/* Navbar Styles */
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dark-mode .navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.3rem;
  text-decoration: none;
}

.nav-link {
  font-weight: 500;
  display: flex;
  align-items: center;
}

.nav-link.router-link-active {
  font-weight: 600;
}

/* Theme Toggle Button */
.btn-outline-light {
  color: #fff;
  border-color: rgba(255, 255, 255, 0.5);
}

.btn-outline-light:hover {
  color: #212529;
  background-color: #f8f9fa;
  border-color: #f8f9fa;
}

.btn-outline-dark {
  color: #212529;
  border-color: rgba(33, 37, 41, 0.5);
}

.btn-outline-dark:hover {
  color: #fff;
  background-color: #212529;
  border-color: #212529;
}

/* Dropdown Styles */
.dropdown-menu {
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-mode .dropdown-menu {
  background-color: #343a40;
  border-color: rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.dark-mode .dropdown-item {
  color: #f8f9fa;
}

.dark-mode .dropdown-item:hover {
  background-color: #495057;
  color: #f8f9fa;
}

.dark-mode .dropdown-header {
  color: #adb5bd;
}

.dark-mode .dropdown-divider {
  border-color: rgba(255, 255, 255, 0.1);
}

/* Main Content */
.container {
  transition: all 0.3s ease;
}

/* Loading Overlay */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* Global Card Styles */
.card {
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.dark-mode .card {
  background-color: #343a40;
  border-color: rgba(255, 255, 255, 0.1);
  color: #f8f9fa;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark-mode .card-header {
  background-color: #495057;
  border-color: rgba(255, 255, 255, 0.1);
  color: #f8f9fa;
}

.dark-mode .card-footer {
  background-color: #495057;
  border-color: rgba(255, 255, 255, 0.1);
  color: #f8f9fa;
}

/* Global Button Styles */
.btn {
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

/* Form Controls */
.dark-mode .form-control {
  background-color: #495057;
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.dark-mode .form-control:focus {
  background-color: #495057;
  border-color: #0d6efd;
  color: #f8f9fa;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.dark-mode .form-control::placeholder {
  color: rgba(248, 249, 250, 0.6);
}

/* Input Groups */
.dark-mode .input-group-text {
  background-color: #495057;
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

/* Alerts */
.dark-mode .alert-danger {
  background-color: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.3);
  color: #f8d7da;
}

.dark-mode .alert-success {
  background-color: rgba(25, 135, 84, 0.2);
  border-color: rgba(25, 135, 84, 0.3);
  color: #d1e7dd;
}

.dark-mode .alert-warning {
  background-color: rgba(255, 193, 7, 0.2);
  border-color: rgba(255, 193, 7, 0.3);
  color: #fff3cd;
}

.dark-mode .alert-info {
  background-color: rgba(13, 202, 240, 0.2);
  border-color: rgba(13, 202, 240, 0.3);
  color: #cff4fc;
}

/* Links */
.dark-mode a {
  color: #79c0ff;
}

.dark-mode a:hover {
  color: #a5d6ff;
}

/* Text Colors */
.dark-mode .text-muted {
  color: #adb5bd !important;
}

/* Responsive Design */
@media (max-width: 991.98px) {
  .navbar-collapse {
    margin-top: 1rem;
    padding: 1rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 0.5rem;
  }
  
  .dark-mode .navbar-collapse {
    background-color: rgba(0, 0, 0, 0.2);
  }
  
  .nav-item {
    margin: 0.25rem 0;
  }
}

@media (max-width: 575.98px) {
  .navbar-brand span:last-child {
    display: none;
  }
  
  .container {
    padding: 0 15px;
  }
}

/* Focus styles for accessibility */
.btn:focus,
.nav-link:focus,
.dropdown-toggle:focus {
  outline: 2px solid #0d6efd;
  outline-offset: 2px;
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}
</style>