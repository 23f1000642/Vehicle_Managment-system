<template>
  <div class="user-dashboard">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>🚘 My Dashboard</h2>
      <span class="badge bg-primary">Welcome, {{ user?.username }}!</span>
    </div>

    <!-- Active Reservation Alert -->
    <div v-if="activeReservation" class="alert alert-info mb-4">
      <h5 class="alert-heading">🅿️ Active Parking</h5>
      <p class="mb-1">
        <strong>Location:</strong> {{ activeReservation.lot_name }}<br>
        <strong>Spot Number:</strong> {{ activeReservation.spot_number }}<br>
        <strong>Parked Since:</strong> {{ formatDateTime(activeReservation.parking_timestamp) }}<br>
        <strong>Current Cost:</strong> ₹{{ activeReservation.parking_cost }}
      </p>
      <hr>
      <button 
        class="btn btn-warning"
        @click="releaseSpot(activeReservation.id)"
        :disabled="loading"
      >
        🚪 Release Parking Spot
      </button>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Total Bookings</h5>
            <h3>{{ userReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Completed</h5>
            <h3>{{ completedReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">Total Spent</h5>
            <h3>₹{{ totalSpent }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5 class="card-title">Active</h5>
            <h3>{{ activeReservation ? 1 : 0 }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Cards -->
    <div class="row mb-4">
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card" @click="navigateTo('/user/book-parking')">
          <div class="card-body text-center">
            <div class="nav-icon">🅿️</div>
            <h5 class="card-title">Book Parking</h5>
            <p class="card-text">Find and book available parking spots</p>
            <span class="badge bg-primary">{{ availableLots.length }} Available Lots</span>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card" @click="navigateTo('/user/parking-history')">
          <div class="card-body text-center">
            <div class="nav-icon">📊</div>
            <h5 class="card-title">Parking History</h5>
            <p class="card-text">View your complete parking history and details</p>
            <span class="badge bg-success">{{ userReservations.length }} Records</span>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card" @click="navigateTo('/user/profile')">
          <div class="card-body text-center">
            <div class="nav-icon">👤</div>
            <h5 class="card-title">My Profile</h5>
            <p class="card-text">Manage your account and preferences</p>
            <span class="badge bg-warning">Settings</span>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card" @click="navigateTo('/user/analytics')">
          <div class="card-body text-center">
            <div class="nav-icon">📈</div>
            <h5 class="card-title">My Analytics</h5>
            <p class="card-text">View charts and spending analytics</p>
            <span class="badge bg-info">Live Data</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Summary -->
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">🏆 Recent Activity</h5>
          </div>
          <div class="card-body">
            <div v-if="recentReservations.length > 0">
              <div v-for="reservation in recentReservations" :key="reservation.id" class="d-flex justify-content-between align-items-center mb-2">
                <div>
                  <strong>{{ reservation.lot_name }}</strong>
                  <small class="d-block text-muted">{{ formatDate(reservation.parking_timestamp) }}</small>
                </div>
                <div class="text-end">
                  <span 
                    :class="getStatusBadgeClass(reservation.status)"
                    class="badge"
                  >
                    {{ reservation.status }}
                  </span>
                </div>
              </div>
            </div>
            <div v-else class="text-center text-muted">
              <p>No recent activity</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">🎯 Quick Stats</h5>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-6">
                <div class="stat-item">
                  <h4 class="text-success">{{ availableLots.length }}</h4>
                  <small class="text-muted">Available Lots</small>
                </div>
              </div>
              <div class="col-6">
                <div class="stat-item">
                  <h4 class="text-primary">{{ favoriteLocation }}</h4>
                  <small class="text-muted">Favorite Location</small>
                </div>
              </div>
            </div>
            <hr>
            <div class="text-center">
              <p class="mb-1">
                <strong>This Month Spent:</strong>
                <span class="text-success">₹{{ thisMonthSpent }}</span>
              </p>
              <small class="text-muted">Based on completed bookings</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

export default {
  name: 'UserDashboard',
  setup() {
    const store = useStore()
    const router = useRouter()
    const toast = useToast()

    const user = computed(() => store.state.user)
    const parkingLots = computed(() => store.state.parkingLots)
    const userReservations = computed(() => store.state.userReservations)
    const activeReservation = computed(() => store.getters.activeReservation)
    const loading = computed(() => store.state.loading)

    const availableLots = computed(() => 
      parkingLots.value.filter(lot => lot.available_spots > 0)
    )

    const completedReservations = computed(() => 
      userReservations.value.filter(r => r.status === 'completed')
    )

    const totalSpent = computed(() => 
      userReservations.value.reduce((sum, r) => sum + (r.parking_cost || 0), 0)
    )

    // Fixed: Use spread operator to avoid mutating original array
    const recentReservations = computed(() => 
      [...userReservations.value]
        .sort((a, b) => new Date(b.parking_timestamp) - new Date(a.parking_timestamp))
        .slice(0, 5)
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

    const thisMonthSpent = computed(() => {
      const now = new Date()
      const thisMonth = userReservations.value.filter(r => {
        const reservationDate = new Date(r.parking_timestamp)
        return reservationDate.getMonth() === now.getMonth() && 
               reservationDate.getFullYear() === now.getFullYear()
      })
      return thisMonth.reduce((sum, r) => sum + (r.parking_cost || 0), 0)
    })

    const navigateTo = (route) => {
      router.push(route)
    }

    const releaseSpot = async (reservationId) => {
      if (confirm('Are you sure you want to release this parking spot?')) {
        const result = await store.dispatch('releaseParkingSpot', reservationId)
        if (result.success) {
          toast.success(`Parking spot released! Final cost: ₹${result.data.final_cost}`)
          store.dispatch('fetchParkingLots')
          store.dispatch('fetchUserReservations')
        } else {
          toast.error(result.error)
        }
      }
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    }

    const getStatusBadgeClass = (status) => {
      switch (status) {
        case 'active': return 'bg-warning'
        case 'completed': return 'bg-success'
        case 'cancelled': return 'bg-danger'
        default: return 'bg-secondary'
      }
    }

    onMounted(() => {
      store.dispatch('fetchParkingLots')
      store.dispatch('fetchUserReservations')
    })

    return {
      user,
      parkingLots,
      userReservations,
      activeReservation,
      availableLots,
      completedReservations,
      totalSpent,
      recentReservations,
      favoriteLocation,
      thisMonthSpent,
      loading,
      navigateTo,
      releaseSpot,
      formatDateTime,
      formatDate,
      getStatusBadgeClass
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.nav-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 2px solid transparent;
}

.nav-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  border-color: #007bff;
}

.nav-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.card {
  margin-bottom: 1rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.stat-item {
  padding: 0.5rem;
}
</style>