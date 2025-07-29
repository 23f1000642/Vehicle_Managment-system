<template>
  <div class="login" :class="{ 'dark-mode': isDarkMode }">
    <!-- Theme Toggle -->
    <div class="position-fixed top-0 end-0 m-4" style="z-index: 1050;">
      <button 
        @click="toggleDarkMode" 
        class="btn btn-outline-primary rounded-pill shadow-sm"
        :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
      >
        <i class="theme-icon">{{ isDarkMode ? '☀️' : '🌙' }}</i>
      </button>
    </div>

    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-4">
          <!-- Login Card -->
          <div class="card border-0 shadow-lg login-card">
            <div class="card-header bg-transparent border-0 text-center py-4">
              <div class="mb-3">
                <div class="bg-primary bg-gradient rounded-circle d-inline-flex align-items-center justify-content-center login-icon">
                  <i class="text-white fs-2">🔐</i>
                </div>
              </div>
              <h2 class="card-title mb-2 fw-bold">Sign In</h2>
              <p class="text-muted mb-0">Welcome back! Please sign in to your account</p>
            </div>

            <div class="card-body px-4 pb-4">
              <form @submit.prevent="handleLogin">
                <!-- Username Field -->
                <div class="mb-4">
                  <label for="username" class="form-label fw-semibold">
                    <i class="me-2">👤</i>Username
                  </label>
                  <div class="input-group">
                    <span class="input-group-text border-end-0 bg-transparent">
                      <i>👤</i>
                    </span>
                    <input
                      id="username"
                      type="text"
                      class="form-control border-start-0 ps-0"
                      v-model="form.username"
                      required
                      :class="{ 
                        'is-invalid': errors.username, 
                        'is-valid': form.username && !errors.username && form.username.length > 0 
                      }"
                      placeholder="Enter your username"
                      autocomplete="username"
                    >
                  </div>
                  <div v-if="errors.username" class="invalid-feedback d-block">
                    <i class="me-1">⚠️</i>{{ errors.username }}
                  </div>
                </div>

                <!-- Password Field -->
                <div class="mb-4">
                  <label for="password" class="form-label fw-semibold">
                    <i class="me-2">🔒</i>Password
                  </label>
                  <div class="input-group">
                    <span class="input-group-text border-end-0 bg-transparent">
                      <i>🔒</i>
                    </span>
                    <input
                      id="password"
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control border-start-0 border-end-0 ps-0"
                      v-model="form.password"
                      required
                      :class="{ 
                        'is-invalid': errors.password, 
                        'is-valid': form.password && !errors.password && form.password.length >= 6 
                      }"
                      placeholder="Enter your password"
                      autocomplete="current-password"
                    >
                    <button 
                      class="btn btn-outline-secondary border-start-0" 
                      type="button"
                      @click="showPassword = !showPassword"
                      :title="showPassword ? 'Hide password' : 'Show password'"
                    >
                      <i>{{ showPassword ? '🙈' : '👁️' }}</i>
                    </button>
                  </div>
                  <div v-if="errors.password" class="invalid-feedback d-block">
                    <i class="me-1">⚠️</i>{{ errors.password }}
                  </div>
                </div>

                <!-- Global Error Alert -->
                <div v-if="error" class="alert alert-danger d-flex align-items-center mb-4" role="alert">
                  <i class="me-2">❌</i>
                  <div>{{ error }}</div>
                </div>

                

                <!-- Login Button -->
                <div class="d-grid mb-4">
                  <button 
                    type="submit" 
                    class="btn btn-primary btn-lg fw-semibold py-3"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <i v-if="!loading" class="me-2">🚀</i>
                    {{ loading ? 'Signing In...' : 'Sign In' }}
                  </button>
                </div>

                
              </form>
            </div>

            <!-- Card Footer -->
            <div class="card-footer bg-transparent border-0 text-center py-4">
              <p class="mb-3 text-muted">
                Don't have an account? 
                <router-link to="/register" class="text-decoration-none fw-semibold">
                  <i class="me-1">📝</i>Create Account
                </router-link>
              </p>
              <router-link to="/" class="text-muted text-decoration-none small">
                <i class="me-1">🏠</i>Back to Home
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed, ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Login',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()
    
    const isDarkMode = ref(false)
    const showPassword = ref(false)

    const form = reactive({
      username: '',
      password: ''
    })

    const errors = reactive({
      username: '',
      password: ''
    })

    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)

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

    const validateForm = () => {
      errors.username = ''
      errors.password = ''

      if (!form.username.trim()) {
        errors.username = 'Username is required'
        return false
      }

      if (!form.password) {
        errors.password = 'Password is required'
        return false
      }

      if (form.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
        return false
      }

      return true
    }

    const handleLogin = async () => {
      if (!validateForm()) return

      const result = await store.dispatch('login', {
        username: form.username.trim(),
        password: form.password
      })

      if (result.success) {
        toast.success(`Welcome back, ${result.user.username}!`)
        
        if (result.user.role === 'admin') {
          router.push('/admin')
        } else {
          router.push('/dashboard')
        }
      } else {
        toast.error(result.error)
      }
    }

    return {
      form,
      errors,
      loading,
      error,
      handleLogin,
      isDarkMode,
      toggleDarkMode,
      showPassword
    }
  }
}
</script>

<style scoped>
/* Base container */
.login {
  background-color: #f8f9fa;
  color: #212529;
  transition: all 0.3s ease;
  min-height: 100vh;
}

.login.dark-mode {
  background-color: #212529;
  color: #f8f9fa;
}

/* Login Card */
.login-card {
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dark-mode .login-card {
  background-color: rgba(33, 37, 41, 0.95) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.login-icon {
  width: 70px;
  height: 70px;
  animation: pulse 2s infinite;
}

/* Dark mode card content */
.dark-mode .card-body,
.dark-mode .card-header,
.dark-mode .card-footer {
  color: #f8f9fa;
}

/* Form Inputs */
.input-group-text {
  transition: all 0.3s ease;
}

.dark-mode .input-group-text {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.dark-mode .form-control {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8f9fa;
}

.dark-mode .form-control:focus {
  background-color: rgba(255, 255, 255, 0.15);
  border-color: #0d6efd;
  color: #f8f9fa;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.dark-mode .form-control::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

/* Buttons */
.btn-primary {
  background: linear-gradient(135deg, #0d6efd, #0056b3);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(13, 110, 253, 0.4);
}

.dark-mode .btn-outline-dark {
  border-color: rgba(255, 255, 255, 0.3);
  color: #f8f9fa;
}

.dark-mode .btn-outline-dark:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.5);
  color: #f8f9fa;
}

/* Theme toggle button */
.btn-outline-primary {
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  transform: scale(1.1);
}

.theme-icon {
  font-size: 1.2rem;
}

/* Alerts */
.dark-mode .alert-danger {
  background-color: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.3);
  color: #f8d7da;
}

/* Links */
.dark-mode a {
  color: #79c0ff;
}

.dark-mode a:hover {
  color: #a5d6ff;
}

/* Form feedback */
.dark-mode .invalid-feedback {
  color: #ea868f;
}

.dark-mode .valid-feedback {
  color: #75d194;
}

/* HR separator */
.dark-mode hr {
  border-color: rgba(255, 255, 255, 0.2);
}

.dark-mode .bg-white {
  background-color: #212529 !important;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

/* Responsive adjustments */
@media (max-width: 575.98px) {
  .card-body {
    padding: 1.5rem;
  }
  
  .login-icon {
    width: 60px;
    height: 60px;
  }
}

/* Focus styles for accessibility */
.btn:focus,
.form-control:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

/* Custom scrollbar for dark mode */
.dark-mode ::-webkit-scrollbar {
  width: 8px;
}

.dark-mode ::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
}

.dark-mode ::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.dark-mode ::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>