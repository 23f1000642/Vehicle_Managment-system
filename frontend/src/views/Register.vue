<template>
  <div class="register">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-5">
        <div class="card">
          <div class="card-body">
            <h3 class="card-title text-center mb-4">Register</h3>
            
            <form @submit.prevent="handleRegister">
              <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input
                  id="username"
                  type="text"
                  class="form-control"
                  v-model="form.username"
                  required
                  :class="{ 'is-invalid': errors.username }"
                >
                <div v-if="errors.username" class="invalid-feedback">
                  {{ errors.username }}
                </div>
              </div>
              
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  id="email"
                  type="email"
                  class="form-control"
                  v-model="form.email"
                  required
                  :class="{ 'is-invalid': errors.email }"
                >
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
              </div>
              
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input
                  id="password"
                  type="password"
                  class="form-control"
                  v-model="form.password"
                  required
                  :class="{ 'is-invalid': errors.password }"
                >
                <div v-if="errors.password" class="invalid-feedback">
                  {{ errors.password }}
                </div>
              </div>
              
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm Password</label>
                <input
                  id="confirmPassword"
                  type="password"
                  class="form-control"
                  v-model="form.confirmPassword"
                  required
                  :class="{ 'is-invalid': errors.confirmPassword }"
                >
                <div v-if="errors.confirmPassword" class="invalid-feedback">
                  {{ errors.confirmPassword }}
                </div>
              </div>
              
              <div v-if="error" class="alert alert-danger">
                {{ error }}
              </div>
              
              <button 
                type="submit" 
                class="btn btn-primary w-100"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Register
              </button>
            </form>
            
            <div class="text-center mt-3">
              <p class="mb-0">
                Already have an account? 
                <router-link to="/login" class="text-decoration-none">Login here</router-link>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'Register',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()

    const form = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const errors = reactive({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })

    const loading = computed(() => store.state.loading)
    const error = computed(() => store.state.error)

    const validateForm = () => {
      // Reset errors
      Object.keys(errors).forEach(key => errors[key] = '')

      let isValid = true

      if (!form.username.trim()) {
        errors.username = 'Username is required'
        isValid = false
      } else if (form.username.trim().length < 3) {
        errors.username = 'Username must be at least 3 characters'
        isValid = false
      }

      if (!form.email.trim()) {
        errors.email = 'Email is required'
        isValid = false
      } else if (!/\S+@\S+\.\S+/.test(form.email)) {
        errors.email = 'Email is invalid'
        isValid = false
      }

      if (!form.password) {
        errors.password = 'Password is required'
        isValid = false
      } else if (form.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
        isValid = false
      }

      if (!form.confirmPassword) {
        errors.confirmPassword = 'Please confirm your password'
        isValid = false
      } else if (form.password !== form.confirmPassword) {
        errors.confirmPassword = 'Passwords do not match'
        isValid = false
      }

      return isValid
    }

    const handleRegister = async () => {
      if (!validateForm()) return

      const result = await store.dispatch('register', {
        username: form.username.trim(),
        email: form.email.trim().toLowerCase(),
        password: form.password
      })

      if (result.success) {
        toast.success('Registration successful! Please login.')
        router.push('/login')
      } else {
        toast.error(result.error)
      }
    }

    return {
      form,
      errors,
      loading,
      error,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register {
  margin-top: 2rem;
}

.card {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>