<template>
  <div class="admin-dashboard" :class="{ 'dark-mode': isDarkMode }">
    <!-- Theme Toggle -->
    <div class="position-fixed top-0 end-0 m-4" style="z-index: 1050;">
      <button 
        @click="toggleDarkMode" 
        class="btn btn-outline-primary rounded-pill shadow-sm"
        :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
      >
        <span class="me-1">{{ isDarkMode ? '☀️' : '🌙' }}</span>
        {{ isDarkMode ? 'Light' : 'Dark' }}
      </button>
    </div>

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="dashboard-title">
        <span class="me-2">🏢</span>Admin Dashboard
      </h2>
      <div class="welcome-badge">
        <span class="badge bg-primary fs-6 px-3 py-2">
          <span class="me-1">👋</span>Welcome, {{ user?.username }}!
        </span>
      </div>
    </div>

    <!-- Statistics Cards -->
    <div class="row mb-4">
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-primary text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">🅿️</div>
            <h5 class="card-title">Total Lots</h5>
            <h2 class="stat-number">{{ parkingLots.length }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-success text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">✅</div>
            <h5 class="card-title">Available Spots</h5>
            <h2 class="stat-number">{{ totalAvailableSpots }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-danger text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">🚗</div>
            <h5 class="card-title">Occupied Spots</h5>
            <h2 class="stat-number">{{ totalOccupiedSpots }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-info text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">👥</div>
            <h5 class="card-title">Total Users</h5>
            <h2 class="stat-number">{{ allUsers.length }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation Cards -->
    <div class="row mb-4">
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card h-100" @click="navigateTo('/admin/parking-lots')">
          <div class="card-body text-center d-flex flex-column">
            <div class="nav-icon mb-3">🅿️</div>
            <h5 class="card-title">Parking Lots</h5>
            <p class="card-text flex-grow-1">Manage parking lots, add/edit spots, and view details</p>
            <div class="mt-auto">
              <span class="badge bg-primary">{{ parkingLots.length }} Lots</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card h-100" @click="navigateTo('/admin/analytics')">
          <div class="card-body text-center d-flex flex-column">
            <div class="nav-icon mb-3">📊</div>
            <h5 class="card-title">Analytics</h5>
            <p class="card-text flex-grow-1">View detailed charts and system analytics</p>
            <div class="mt-auto">
              <span class="badge bg-success">Live Data</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card h-100" @click="navigateTo('/admin/users')">
          <div class="card-body text-center d-flex flex-column">
            <div class="nav-icon mb-3">👥</div>
            <h5 class="card-title">User Management</h5>
            <p class="card-text flex-grow-1">View and manage all registered users</p>
            <div class="mt-auto">
              <span class="badge bg-info">{{ allUsers.length }} Users</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6 col-lg-3 mb-4">
        <div class="card nav-card h-100" @click="navigateTo('/admin/jobs')">
          <div class="card-body text-center d-flex flex-column">
            <div class="nav-icon mb-3">⚙️</div>
            <h5 class="card-title">Background Jobs</h5>
            <p class="card-text flex-grow-1">Test and manage automated tasks</p>
            <div class="mt-auto">
              <span class="badge bg-warning">Testing</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="card activity-card mb-4">
      <div class="card-header">
        <h5 class="mb-0">
          <span class="me-2">🕒</span>Recent Activity
        </h5>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-6">
            <div class="activity-item">
              <h6 class="activity-title">
                <span class="me-2">📅</span>Today's Bookings
              </h6>
              <p class="activity-text">{{ todayBookings }} new reservations</p>
            </div>
          </div>
          <div class="col-md-6">
            <div class="activity-item">
              <h6 class="activity-title">
                <span class="me-2">💻</span>System Health
              </h6>
              <p class="text-success mb-0">
                <span class="me-1">✅</span>All systems operational
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Summary -->
    <div class="row">
      <div class="col-md-6 mb-4">
        <div class="card summary-card h-100">
          <div class="card-header">
            <h5 class="mb-0">
              <span class="me-2">🏆</span>Top Performing Lots
            </h5>
          </div>
          <div class="card-body">
            <div v-if="topLots.length > 0" class="top-lots-list">
              <div v-for="lot in topLots" :key="lot.id" class="lot-item">
                <div class="d-flex justify-content-between align-items-center">
                  <div class="lot-info">
                    <div class="lot-name">{{ lot.prime_location_name }}</div>
                    <small class="lot-details">
                      <span class="me-1">🚗</span>{{ lot.occupied_spots }}/{{ lot.number_of_spots }} spots
                    </small>
                  </div>
                  <div class="lot-percentage">
                    <span class="badge bg-primary">
                      {{ Math.round((lot.occupied_spots / lot.number_of_spots) * 100) }}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center empty-state">
              <div class="empty-icon">🏢</div>
              <p class="text-muted">No parking lots available</p>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6 mb-4">
        <div class="card summary-card h-100">
          <div class="card-header">
            <h5 class="mb-0">
              <span class="me-2">📈</span>Quick Stats
            </h5>
          </div>
          <div class="card-body">
            <div class="row text-center mb-3">
              <div class="col-6">
                <div class="quick-stat">
                  <div class="stat-value text-success">{{ totalAvailableSpots }}</div>
                  <div class="stat-label">
                    <span class="me-1">✅</span>Available Spots
                  </div>
                </div>
              </div>
              <div class="col-6">
                <div class="quick-stat">
                  <div class="stat-value text-danger">{{ totalOccupiedSpots }}</div>
                  <div class="stat-label">
                    <span class="me-1">🚗</span>Occupied Spots
                  </div>
                </div>
              </div>
            </div>
            <hr class="stats-divider">
            <div class="text-center revenue-section">
              <div class="revenue-title">
                <span class="me-1">💰</span><strong>Total Revenue Today</strong>
              </div>
              <div class="revenue-amount">₹{{ todayRevenue }}</div>
              <small class="revenue-note">Based on current occupancy</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AdminDashboard',
  setup() {
    const store = useStore()
    const router = useRouter()
    const isDarkMode = ref(false)

    const user = computed(() => store.state.user)
    const parkingLots = computed(() => store.state.parkingLots)
    const allUsers = computed(() => store.state.allUsers)
    
    const totalAvailableSpots = computed(() => 
      parkingLots.value.reduce((sum, lot) => sum + lot.available_spots, 0)
    )
    
    const totalOccupiedSpots = computed(() => 
      parkingLots.value.reduce((sum, lot) => sum + lot.occupied_spots, 0)
    )

    const todayBookings = computed(() => {
      // This would be calculated from actual booking data
      return Math.floor(Math.random() * 20) + 5 // Mock data for now
    })

    const topLots = computed(() => {
      return parkingLots.value
        .filter(lot => lot.number_of_spots > 0)
        .sort((a, b) => (b.occupied_spots / b.number_of_spots) - (a.occupied_spots / a.number_of_spots))
        .slice(0, 5)
    })

    const todayRevenue = computed(() => {
      return parkingLots.value.reduce((total, lot) => {
        return total + (lot.occupied_spots * lot.price)
      }, 0).toFixed(2)
    })

    const navigateTo = (route) => {
      router.push(route)
    }

    // Load theme preference
    onMounted(() => {
      const savedTheme = localStorage.getItem('darkMode')
      if (savedTheme) {
        isDarkMode.value = JSON.parse(savedTheme)
      } else {
        isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      
      store.dispatch('fetchParkingLots')
      store.dispatch('fetchAllUsers')
    })

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', JSON.stringify(isDarkMode.value))
    }

    return {
      user,
      parkingLots,
      allUsers,
      totalAvailableSpots,
      totalOccupiedSpots,
      todayBookings,
      topLots,
      todayRevenue,
      navigateTo,
      isDarkMode,
      toggleDarkMode
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  color: #212529;
  transition: all 0.3s ease;
  min-height: 100vh;
}

.admin-dashboard.dark-mode {
  background-color: #212529;
  color: #f8f9fa;
}

/* Header */
.dashboard-title {
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.dark-mode .dashboard-title {
  color: #f8f9fa;
}

.welcome-badge .badge {
  font-size: 0.9rem;
  border-radius: 25px;
}

/* Statistics Cards */
.stat-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  font-size: 2.5rem;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

/* Navigation Cards */
.nav-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #0d6efd;
}

.dark-mode .nav-card {
  background-color: #343a40;
  border-color: #495057;
  color: #f8f9fa;
}

.dark-mode .nav-card:hover {
  border-color: #0d6efd;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.nav-icon {
  font-size: 3rem;
}

/* Activity Card */
.activity-card {
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: none;
}

.dark-mode .activity-card {
  background-color: #343a40;
  color: #f8f9fa;
}

.dark-mode .activity-card .card-header {
  background-color: #495057;
  border-color: #6c757d;
  color: #f8f9fa;
}

.activity-item {
  padding: 1rem 0;
}

.activity-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #495057;
}

.dark-mode .activity-title {
  color: #adb5bd;
}

.activity-text {
  color: #6c757d;
  margin: 0;
}

.dark-mode .activity-text {
  color: #8b949e;
}

/* Summary Cards */
.summary-card {
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: none;
}

.dark-mode .summary-card {
  background-color: #343a40;
  color: #f8f9fa;
}

.dark-mode .summary-card .card-header {
  background-color: #495057;
  border-color: #6c757d;
  color: #f8f9fa;
}

/* Top Lots List */
.top-lots-list {
  max-height: 300px;
  overflow-y: auto;
}

.lot-item {
  padding: 1rem 0;
  border-bottom: 1px solid #e9ecef;
}

.dark-mode .lot-item {
  border-color: #6c757d;
}

.lot-item:last-child {
  border-bottom: none;
}

.lot-name {
  font-weight: 600;
  color: #212529;
}

.dark-mode .lot-name {
  color: #f8f9fa;
}

.lot-details {
  color: #6c757d;
}

.dark-mode .lot-details {
  color: #8b949e;
}

/* Empty State */
.empty-state {
  padding: 2rem;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

/* Quick Stats */
.quick-stat {
  padding: 1rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  color: #6c757d;
}

.dark-mode .stat-label {
  color: #8b949e;
}

.stats-divider {
  border-color: #e9ecef;
  margin: 1.5rem 0;
}

.dark-mode .stats-divider {
  border-color: #6c757d;
}

/* Revenue Section */
.revenue-section {
  padding: 1rem 0;
}

.revenue-title {
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #495057;
}

.dark-mode .revenue-title {
  color: #adb5bd;
}

.revenue-amount {
  font-size: 1.8rem;
  font-weight: 700;
  color: #198754;
  margin-bottom: 0.25rem;
}

.revenue-note {
  color: #6c757d;
  font-size: 0.85rem;
}

.dark-mode .revenue-note {
  color: #8b949e;
}

/* Theme Toggle */
.btn-outline-primary {
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  transform: scale(1.05);
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 15px;
  }
  
  .dashboard-title {
    font-size: 1.5rem;
  }
  
  .welcome-badge .badge {
    font-size: 0.8rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .nav-icon {
    font-size: 2.5rem;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
}

@media (max-width: 576px) {
  .d-flex.justify-content-between {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 1rem;
  }
  
  .welcome-badge {
    align-self: stretch;
    text-align: center;
  }
}

/* Card Hover Effects */
.card {
  transition: all 0.3s ease;
}

/* Accessibility */
.nav-card:focus {
  outline: 2px solid #0d6efd;
  outline-offset: 2px;
}

/* Scrollbar Styling for Dark Mode */
.dark-mode .top-lots-list::-webkit-scrollbar {
  width: 6px;
}

.dark-mode .top-lots-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.dark-mode .top-lots-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.dark-mode .top-lots-list::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}
</style>