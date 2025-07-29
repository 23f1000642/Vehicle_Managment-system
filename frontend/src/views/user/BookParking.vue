<template>
  <div class="book-parking">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>🅿️ Book Parking</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/dashboard" class="text-decoration-none">Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">Book Parking</li>
          </ol>
        </nav>
      </div>
    </div>

    <!-- Active Reservation Alert -->
    <div v-if="activeReservation" class="alert alert-warning mb-4">
      <h5 class="alert-heading">⚠️ You already have an active parking reservation</h5>
      <p class="mb-1">
        <strong>Location:</strong> {{ activeReservation.lot_name }}<br>
        <strong>Spot Number:</strong> {{ activeReservation.spot_number }}<br>
        <strong>Parked Since:</strong> {{ formatDateTime(activeReservation.parking_timestamp) }}
      </p>
      <hr>
      <p class="mb-0">Please release your current spot before booking a new one.</p>
    </div>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-md-6">
        <input 
          type="text" 
          class="form-control" 
          placeholder="🔍 Search parking lots..."
          v-model="searchQuery"
        >
      </div>
      <div class="col-md-3">
        <select class="form-control" v-model="priceFilter">
          <option value="">All Prices</option>
          <option value="low">Under ₹50/hour</option>
          <option value="medium">₹50-100/hour</option>
          <option value="high">Above ₹100/hour</option>
        </select>
      </div>
      <div class="col-md-3">
        <select class="form-control" v-model="availabilityFilter">
          <option value="">All Lots</option>
          <option value="available">Available Only</option>
          <option value="full">Full Lots</option>
        </select>
      </div>
    </div>

    <!-- Available Parking Lots -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">Available Parking Lots</h5>
      </div>
      <div class="card-body">
        <div v-if="filteredLots.length === 0 && !searchQuery" class="text-center py-4">
          <div class="mb-3">
            <i class="display-1 text-muted">🅿️</i>
          </div>
          <h4 class="text-muted">No parking lots available</h4>
          <p class="text-muted">Please check back later for available spots</p>
        </div>

        <div v-else-if="filteredLots.length === 0 && searchQuery" class="text-center py-4">
          <p class="text-muted">No parking lots match your search criteria</p>
          <button class="btn btn-outline-secondary btn-sm" @click="clearFilters">
            Clear Filters
          </button>
        </div>
        
        <div v-else class="row">
          <div v-for="lot in filteredLots" :key="lot.id" class="col-md-6 col-lg-4 mb-3">
            <div class="card h-100 parking-lot-card">
              <div class="card-body">
                <h6 class="card-title">{{ lot.prime_location_name }}</h6>
                <p class="card-text">
                  <small class="text-muted">📍 {{ lot.address }}</small><br>
                  <strong class="text-success">₹{{ lot.price }}/hour</strong>
                </p>
                
                <!-- Availability Info -->
                <div class="row mb-3">
                  <div class="col-6">
                    <span class="badge bg-success">Available: {{ lot.available_spots }}</span>
                  </div>
                  <div class="col-6">
                    <span class="badge bg-danger">Occupied: {{ lot.occupied_spots }}</span>
                  </div>
                </div>

                <!-- Occupancy Progress Bar -->
                <div class="mb-3">
                  <div class="d-flex justify-content-between mb-1">
                    <small>Occupancy</small>
                    <small>{{ getOccupancyPercentage(lot) }}%</small>
                  </div>
                  <div class="progress" style="height: 8px;">
                    <div 
                      class="progress-bar" 
                      :class="getOccupancyColor(lot)"
                      :style="{ width: getOccupancyPercentage(lot) + '%' }"
                    ></div>
                  </div>
                </div>

                <!-- Book Button -->
                <button 
                  class="btn w-100"
                  :class="lot.available_spots === 0 ? 'btn-secondary' : 'btn-primary'"
                  @click="bookSpot(lot.id)"
                  :disabled="loading || lot.available_spots === 0 || activeReservation"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ lot.available_spots === 0 ? '🚫 Full' : '🅿️ Book Spot' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Results Summary -->
        <div v-if="searchQuery || priceFilter || availabilityFilter" class="mt-3 text-muted">
          <small>
            Showing {{ filteredLots.length }} of {{ parkingLots.length }} parking lots
          </small>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'

export default {
  name: 'BookParking',
  setup() {
    const store = useStore()
    const toast = useToast()

    const searchQuery = ref('')
    const priceFilter = ref('')
    const availabilityFilter = ref('')

    const parkingLots = computed(() => store.state.parkingLots)
    const activeReservation = computed(() => store.getters.activeReservation)
    const loading = computed(() => store.state.loading)

    const filteredLots = computed(() => {
      let filtered = parkingLots.value

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(lot =>
          lot.prime_location_name.toLowerCase().includes(query) ||
          lot.address.toLowerCase().includes(query)
        )
      }

      // Price filter
      if (priceFilter.value) {
        filtered = filtered.filter(lot => {
          switch (priceFilter.value) {
            case 'low': return lot.price < 50
            case 'medium': return lot.price >= 50 && lot.price <= 100
            case 'high': return lot.price > 100
            default: return true
          }
        })
      }

      // Availability filter
      if (availabilityFilter.value) {
        filtered = filtered.filter(lot => {
          switch (availabilityFilter.value) {
            case 'available': return lot.available_spots > 0
            case 'full': return lot.available_spots === 0
            default: return true
          }
        })
      }

      return filtered
    })

    const getOccupancyPercentage = (lot) => {
      if (lot.number_of_spots === 0) return 0
      return Math.round((lot.occupied_spots / lot.number_of_spots) * 100)
    }

    const getOccupancyColor = (lot) => {
      const percentage = getOccupancyPercentage(lot)
      if (percentage >= 90) return 'bg-danger'
      if (percentage >= 70) return 'bg-warning'
      return 'bg-success'
    }

    const bookSpot = async (lotId) => {
      if (activeReservation.value) {
        toast.error('You already have an active reservation. Please release it first.')
        return
      }

      const result = await store.dispatch('bookParkingSpot', lotId)
      if (result.success) {
        toast.success('Parking spot booked successfully!')
        store.dispatch('fetchParkingLots')
        store.dispatch('fetchUserReservations')
      } else {
        toast.error(result.error)
      }
    }

    const clearFilters = () => {
      searchQuery.value = ''
      priceFilter.value = ''
      availabilityFilter.value = ''
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    }

    onMounted(() => {
      store.dispatch('fetchParkingLots')
      store.dispatch('fetchUserReservations')
    })

    return {
      parkingLots,
      filteredLots,
      activeReservation,
      loading,
      searchQuery,
      priceFilter,
      availabilityFilter,
      getOccupancyPercentage,
      getOccupancyColor,
      bookSpot,
      clearFilters,
      formatDateTime
    }
  }
}
</script>

<style scoped>
.book-parking {
  max-width: 1200px;
  margin: 0 auto;
}

.parking-lot-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.parking-lot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.progress {
  border-radius: 10px;
}
</style>