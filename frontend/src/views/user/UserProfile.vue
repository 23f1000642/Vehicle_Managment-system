<template>
  <div class="user-profile">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>👤 My Profile</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/dashboard" class="text-decoration-none">Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">Profile</li>
          </ol>
        </nav>
      </div>
    </div>

    <div class="row">
      <!-- Profile Information -->
      <div class="col-md-8">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Profile Information</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateProfile">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Username *</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="profileForm.username"
                    required
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Email *</label>
                  <input 
                    type="email" 
                    class="form-control" 
                    v-model="profileForm.email"
                    required
                  >
                </div>
              </div>
              
              

              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  Update Profile
                </button>
                <button type="button" class="btn btn-outline-secondary" @click="resetForm">
                  Reset
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Change Password -->
        <div class="card mt-4">
          <div class="card-header">
            <h5 class="mb-0">Change Password</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="changePassword">
              <div class="mb-3">
                <label class="form-label">Current Password *</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="passwordForm.currentPassword"
                  required
                >
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">New Password *</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    v-model="passwordForm.newPassword"
                    required
                    minlength="6"
                  >
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Confirm New Password *</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    v-model="passwordForm.confirmPassword"
                    required
                    minlength="6"
                  >
                </div>
              </div>

              <button type="submit" class="btn btn-warning" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                Change Password
              </button>
            </form>
          </div>
        </div>
      </div>

      <!-- Profile Summary -->
      <div class="col-md-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">Profile Summary</h5>
          </div>
          <div class="card-body text-center">
            <div class="profile-avatar mb-3">
              {{ user?.username?.charAt(0).toUpperCase() }}
            </div>
            <h5>{{ user?.username }}</h5>
            <p class="text-muted">{{ user?.email }}</p>
            <p class="text-muted">
              <strong>Role:</strong> 
              <span class="badge bg-primary">{{ user?.role }}</span>
            </p>
            <p class="text-muted">
              <strong>Member Since:</strong><br>
              {{ formatDate(user?.created_at) }}
            </p>
          </div>
        </div>

        <!-- Account Statistics -->
        <div class="card mt-4">
          <div class="card-header">
            <h5 class="mb-0">Account Statistics</h5>
          </div>
          <div class="card-body">
            <div class="stat-item mb-3">
              <div class="d-flex justify-content-between">
                <span>Total Bookings</span>
                <strong>{{ userReservations.length }}</strong>
              </div>
            </div>
            
            <div class="stat-item mb-3">
              <div class="d-flex justify-content-between">
                <span>Completed Trips</span>
                <strong>{{ completedReservations.length }}</strong>
              </div>
            </div>
            
            <div class="stat-item mb-3">
              <div class="d-flex justify-content-between">
                <span>Total Spent</span>
                <strong class="text-success">₹{{ totalSpent }}</strong>
              </div>
            </div>
            
            <div class="stat-item mb-3">
              <div class="d-flex justify-content-between">
                <span>Active Reservations</span>
                <strong class="text-warning">{{ activeReservations.length }}</strong>
              </div>
            </div>

            <hr>

            <div class="stat-item">
              <div class="d-flex justify-content-between">
                <span>Favorite Location</span>
                <strong>{{ favoriteLocation }}</strong>
              </div>
            </div>
          </div>
        </div>

        <!-- Account Actions -->
        <div class="card mt-4">
          <div class="card-header">
            <h5 class="mb-0">Account Actions</h5>
          </div>
          <div class="card-body">
            <div class="d-grid gap-2">
              <button class="btn btn-outline-primary" @click="exportUserData">
                📥 Export My Data
              </button>
              <router-link to="/user/parking-history" class="btn btn-outline-info">
                📊 View History
              </router-link>
              <button class="btn btn-outline-danger" @click="logout">
                🚪 Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { parkingAPI } from '@/services/api'

export default {
  name: 'UserProfile',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()

    const user = computed(() => store.state.user)
    const userReservations = computed(() => store.state.userReservations)
    const loading = computed(() => store.state.loading)

    const profileForm = reactive({
      username: '',
      email: '',
      fullName: '',
      phone: '',
      address: ''
    })

    const passwordForm = reactive({
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    })

    const completedReservations = computed(() => 
      userReservations.value.filter(r => r.status === 'completed')
    )

    const activeReservations = computed(() => 
      userReservations.value.filter(r => r.status === 'active')
    )

    const totalSpent = computed(() => 
      userReservations.value.reduce((sum, r) => sum + (r.parking_cost || 0), 0)
    )

    const favoriteLocation = computed(() => {
      const locationCounts = {}
      userReservations.value.forEach(r => {
        if (r.lot_name) {
          locationCounts[r.lot_name] = (locationCounts[r.lot_name] || 0) + 1
        }
      })
      
      const topLocation = Object.entries(locationCounts)
        .sort(([,a], [,b]) => b - a)[0]
      
      return topLocation ? topLocation[0] : 'None'
    })

    const initializeForm = () => {
      if (user.value) {
        profileForm.username = user.value.username || ''
        profileForm.email = user.value.email || ''
        profileForm.fullName = user.value.full_name || ''
        profileForm.phone = user.value.phone || ''
        profileForm.address = user.value.address || ''
      }
    }

    const resetForm = () => {
      initializeForm()
    }

    const updateProfile = async () => {
      try {
        toast.info('Profile update functionality needs to be implemented')
      } catch (error) {
        toast.error('Failed to update profile')
        console.error('Profile update error:', error)
      }
    }

    const changePassword = async () => {
      if (passwordForm.newPassword !== passwordForm.confirmPassword) {
        toast.error('New passwords do not match')
        return
      }

      if (passwordForm.newPassword.length < 6) {
        toast.error('Password must be at least 6 characters long')
        return
      }

      try {
        toast.info('Password change functionality needs to be implemented')
        
        // Clear form
        passwordForm.currentPassword = ''
        passwordForm.newPassword = ''
        passwordForm.confirmPassword = ''
      } catch (error) {
        toast.error('Failed to change password')
        console.error('Password change error:', error)
      }
    }

    const exportUserData = async () => {
      try {
        const response = await parkingAPI.exportCSVAsync()
        
        // Create download link for the CSV file
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `user_data_${user.value.username}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        toast.success('User data exported successfully!')
      } catch (error) {
        toast.error('Failed to export user data')
        console.error('Export error:', error)
      }
    }

    const logout = async () => {
      if (confirm('Are you sure you want to logout?')) {
        await store.dispatch('logout')
        toast.success('Logged out successfully!')
        router.push('/login')
      }
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    }

    onMounted(() => {
      store.dispatch('fetchUserReservations')
      initializeForm()
    })

    return {
      user,
      userReservations,
      completedReservations,
      activeReservations,
      totalSpent,
      favoriteLocation,
      loading,
      profileForm,
      passwordForm,
      resetForm,
      updateProfile,
      changePassword,
      exportUserData,
      logout,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-profile {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #007bff, #6f42c1);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin: 0 auto;
}

.stat-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f8f9fa;
}

.stat-item:last-child {
  border-bottom: none;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>