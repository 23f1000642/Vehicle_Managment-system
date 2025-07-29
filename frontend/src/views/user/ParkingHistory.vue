<template>
  <div class="parking-history">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>📊 My Parking History</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/dashboard" class="text-decoration-none">Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">Parking History</li>
          </ol>
        </nav>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-primary" @click="refreshData">
          🔄 Refresh
        </button>
        <button class="btn btn-outline-success" @click="exportData">
          📥 Export CSV
        </button>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body text-center">
            <h5>Total Bookings</h5>
            <h3>{{ userReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body text-center">
            <h5>Completed</h5>
            <h3>{{ completedReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body text-center">
            <h5>Active</h5>
            <h3>{{ activeReservations.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body text-center">
            <h5>Total Spent</h5>
            <h3>₹{{ totalSpent }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="row mb-4">
      <div class="col-md-4">
        <input 
          type="text" 
          class="form-control" 
          placeholder="🔍 Search by location..."
          v-model="searchQuery"
        >
      </div>
      <div class="col-md-3">
        <select class="form-control" v-model="statusFilter">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </div>
      <div class="col-md-3">
        <select class="form-control" v-model="timeFilter">
          <option value="">All Time</option>
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="quarter">Last 3 Months</option>
        </select>
      </div>
      <div class="col-md-2">
        <button class="btn btn-outline-secondary w-100" @click="clearFilters">
          Clear
        </button>
      </div>
    </div>

    <!-- Reservation History Table -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">Parking History Details</h5>
      </div>
      <div class="card-body">
        <div v-if="filteredReservations.length === 0 && !hasFilters" class="text-center py-4">
          <div class="mb-3">
            <i class="display-1 text-muted">📊</i>
          </div>
          <h4 class="text-muted">No parking history yet</h4>
          <p class="text-muted">Your parking reservations will appear here</p>
          <router-link to="/user/book-parking" class="btn btn-primary">
            🅿️ Book Your First Spot
          </router-link>
        </div>

        <div v-else-if="filteredReservations.length === 0 && hasFilters" class="text-center py-4">
          <p class="text-muted">No reservations match your filter criteria</p>
          <button class="btn btn-outline-secondary btn-sm" @click="clearFilters">
            Clear Filters
          </button>
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Location</th>
                <th>Spot</th>
                <th>Parked Time</th>
                <th>Released Time</th>
                <th>Duration</th>
                <th>Cost</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="reservation in filteredReservations" :key="reservation.id">
                <td>
                  <strong>{{ reservation.lot_name }}</strong>
                </td>
                <td>
                  <span class="badge bg-primary">#{{ reservation.spot_number }}</span>
                </td>
                <td>
                  <small>{{ formatDateTime(reservation.parking_timestamp) }}</small>
                </td>
                <td>
                  <small>
                    {{ reservation.leaving_timestamp 
                        ? formatDateTime(reservation.leaving_timestamp) 
                        : 'Active' 
                    }}
                  </small>
                </td>
                <td>
                  <span class="badge bg-info">
                    {{ calculateDuration(reservation.parking_timestamp, reservation.leaving_timestamp) }}
                  </span>
                </td>
                <td>
                  <strong class="text-success">₹{{ reservation.parking_cost }}</strong>
                </td>
                <td>
                  <span 
                    :class="getStatusBadgeClass(reservation.status)"
                    class="badge"
                  >
                    {{ reservation.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Results Summary -->
          <div v-if="hasFilters" class="mt-3 text-muted">
            <small>
              Showing {{ filteredReservations.length }} of {{ userReservations.length }} reservations
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'
import { parkingAPI } from '@/services/api'

export default {
  name: 'ParkingHistory',
  setup() {
    const store = useStore()
    const toast = useToast()

    const searchQuery = ref('')
    const statusFilter = ref('')
    const timeFilter = ref('')

    const user = computed(() => store.state.user)
    const userReservations = computed(() => store.state.userReservations)

    const filteredReservations = computed(() => {
      let filtered = userReservations.value

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(reservation =>
          reservation.lot_name?.toLowerCase().includes(query)
        )
      }

      // Status filter
      if (statusFilter.value) {
        filtered = filtered.filter(reservation => 
          reservation.status === statusFilter.value
        )
      }

      // Time filter
      if (timeFilter.value) {
        const now = new Date()
        filtered = filtered.filter(reservation => {
          const reservationDate = new Date(reservation.parking_timestamp)
          
          switch (timeFilter.value) {
            case 'today': {
              return reservationDate.toDateString() === now.toDateString()
            }
            case 'week': {
              const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
              return reservationDate >= weekAgo
            }
            case 'month': {
              return reservationDate.getMonth() === now.getMonth() && 
                     reservationDate.getFullYear() === now.getFullYear()
            }
            case 'quarter': {
              const threeMonthsAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000)
              return reservationDate >= threeMonthsAgo
            }
            default: {
              return true
            }
          }
        })
      }

      // Sort by most recent first
      return filtered.sort((a, b) => new Date(b.parking_timestamp) - new Date(a.parking_timestamp))
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

    const hasFilters = computed(() => 
      searchQuery.value || statusFilter.value || timeFilter.value
    )

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    }

    const calculateDuration = (start, end) => {
      if (!start) return 'N/A'
      if (!end) return 'Active'
      
      const startTime = new Date(start)
      const endTime = new Date(end)
      const diffMs = endTime - startTime
      const hours = Math.floor(diffMs / (1000 * 60 * 60))
      const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      
      return `${hours}h ${minutes}m`
    }

    const getStatusBadgeClass = (status) => {
      switch (status) {
        case 'active': return 'bg-warning'
        case 'completed': return 'bg-success'
        case 'cancelled': return 'bg-danger'
        default: return 'bg-secondary'
      }
    }

    const clearFilters = () => {
      searchQuery.value = ''
      statusFilter.value = ''
      timeFilter.value = ''
    }

    const refreshData = () => {
      store.dispatch('fetchUserReservations')
      toast.info('Data refreshed!')
    }

    const exportData = async () => {
      try {
        const response = await parkingAPI.exportCSVAsync()
        
        // Create download link for the CSV file
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `parking_history_${user.value.username}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        toast.success('CSV exported successfully!')
      } catch (error) {
        toast.error('Failed to export CSV')
        console.error('Export error:', error)
      }
    }

    onMounted(() => {
      store.dispatch('fetchUserReservations')
    })

    return {
      userReservations,
      filteredReservations,
      completedReservations,
      activeReservations,
      totalSpent,
      hasFilters,
      searchQuery,
      statusFilter,
      timeFilter,
      formatDateTime,
      calculateDuration,
      getStatusBadgeClass,
      clearFilters,
      refreshData,
      exportData
    }
  }
}
</script>

<style scoped>
.parking-history {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.table th {
  border-top: none;
  font-weight: 600;
}
</style>