<template>
  <div class="parking-lots-management">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>🅿️ Parking Lots Management</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/admin" class="text-decoration-none">Admin Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">Parking Lots</li>
          </ol>
        </nav>
      </div>
      <button class="btn btn-primary btn-lg" @click="showCreateModal = true">
        ➕ Add Parking Lot
      </button>
    </div>

    <!-- Quick Stats -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body text-center">
            <h5>Total Lots</h5>
            <h3>{{ parkingLots.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body text-center">
            <h5>Available Spots</h5>
            <h3>{{ totalAvailableSpots }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-danger text-white">
          <div class="card-body text-center">
            <h5>Occupied Spots</h5>
            <h3>{{ totalOccupiedSpots }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body text-center">
            <h5>Total Revenue</h5>
            <h3>₹{{ totalRevenue }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Parking Lots Table -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">All Parking Lots</h5>
        <div class="d-flex gap-2">
          <input 
            type="text" 
            class="form-control form-control-sm" 
            placeholder="Search lots..."
            v-model="searchQuery"
            style="width: 200px;"
          >
          <button class="btn btn-outline-secondary btn-sm" @click="refreshLots">
            🔄 Refresh
          </button>
        </div>
      </div>
      <div class="card-body">
        <div v-if="filteredLots.length === 0 && !searchQuery" class="text-center py-5">
          <div class="mb-3">
            <i class="display-1 text-muted">🅿️</i>
          </div>
          <h4 class="text-muted">No parking lots yet</h4>
          <p class="text-muted">Create your first parking lot to get started</p>
          <button class="btn btn-primary btn-lg" @click="showCreateModal = true">
            ➕ Create First Parking Lot
          </button>
        </div>

        <div v-else-if="filteredLots.length === 0 && searchQuery" class="text-center py-4">
          <p class="text-muted">No parking lots match your search "{{ searchQuery }}"</p>
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Location Name</th>
                <th>Address</th>
                <th>Pin Code</th>
                <th>Price/Hour</th>
                <th>Total Spots</th>
                <th>Available</th>
                <th>Occupied</th>
                <th>Occupancy %</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in filteredLots" :key="lot.id">
                <td>
                  <strong>{{ lot.prime_location_name }}</strong>
                </td>
                <td>
                  <small class="text-muted">{{ lot.address }}</small>
                </td>
                <td>
                  <span class="badge bg-light text-dark">{{ lot.pin_code }}</span>
                </td>
                <td>
                  <strong class="text-success">₹{{ lot.price }}</strong>
                </td>
                <td>
                  <span class="badge bg-primary">{{ lot.number_of_spots }}</span>
                </td>
                <td>
                  <span class="badge bg-success">{{ lot.available_spots }}</span>
                </td>
                <td>
                  <span class="badge bg-danger">{{ lot.occupied_spots }}</span>
                </td>
                <td>
                  <div class="progress" style="height: 20px;">
                    <div 
                      class="progress-bar" 
                      :class="getOccupancyClass(lot)"
                      :style="{ width: getOccupancyPercentage(lot) + '%' }"
                    >
                      {{ getOccupancyPercentage(lot) }}%
                    </div>
                  </div>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button 
                      class="btn btn-sm btn-outline-info"
                      @click="viewSpots(lot)"
                      title="View Spots"
                    >
                      👁️
                    </button>
                    <button 
                      class="btn btn-sm btn-outline-warning"
                      @click="editLot(lot)"
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button 
                      class="btn btn-sm btn-outline-danger"
                      @click="deleteLot(lot)"
                      :disabled="lot.occupied_spots > 0"
                      :title="lot.occupied_spots > 0 ? 'Cannot delete - has occupied spots' : 'Delete'"
                    >
                      🗑️
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div 
      class="modal fade" 
      :class="{ show: showCreateModal }" 
      :style="{ display: showCreateModal ? 'block' : 'none' }"
      tabindex="-1"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ editingLot ? '✏️ Edit Parking Lot' : '➕ Create New Parking Lot' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveLot">
              <div class="row">
                <div class="col-md-12 mb-3">
                  <label class="form-label">Location Name *</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="lotForm.prime_location_name"
                    placeholder="e.g., City Mall Parking"
                    required
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-8 mb-3">
                  <label class="form-label">Address *</label>
                  <textarea 
                    class="form-control" 
                    v-model="lotForm.address"
                    rows="3"
                    placeholder="Full address of the parking lot"
                    required
                  ></textarea>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Pin Code *</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="lotForm.pin_code"
                    placeholder="462001"
                    maxlength="6"
                    required
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Price per Hour (₹) *</label>
                  <div class="input-group">
                    <span class="input-group-text">₹</span>
                    <input 
                      type="number" 
                      step="0.01"
                      min="1"
                      class="form-control" 
                      v-model="lotForm.price"
                      placeholder="50.00"
                      required
                    >
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Number of Spots *</label>
                  <input 
                    type="number" 
                    min="1"
                    max="1000"
                    class="form-control" 
                    v-model="lotForm.number_of_spots"
                    placeholder="20"
                    required
                  >
                  <small class="text-muted">Parking spots will be auto-generated</small>
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Cancel
            </button>
            <button type="button" class="btn btn-primary" @click="saveLot" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ editingLot ? 'Update Lot' : 'Create Lot' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- View Spots Modal -->
    <div 
      class="modal fade" 
      :class="{ show: showSpotsModal }" 
      :style="{ display: showSpotsModal ? 'block' : 'none' }"
      tabindex="-1"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              🅿️ Parking Spots - {{ selectedLot?.prime_location_name }}
            </h5>
            <button type="button" class="btn-close" @click="closeSpotsModal"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingSpots" class="text-center py-4">
              <div class="spinner-border" role="status"></div>
              <p class="mt-2">Loading parking spots...</p>
            </div>
            
            <div v-else-if="parkingSpots.length > 0">
              <!-- Spots Summary -->
              <div class="row mb-4">
                <div class="col-md-4">
                  <div class="card bg-success text-white">
                    <div class="card-body text-center">
                      <h6>Available Spots</h6>
                      <h4>{{ availableSpots }}</h4>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card bg-danger text-white">
                    <div class="card-body text-center">
                      <h6>Occupied Spots</h6>
                      <h4>{{ occupiedSpots }}</h4>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="card bg-primary text-white">
                    <div class="card-body text-center">
                      <h6>Total Spots</h6>
                      <h4>{{ parkingSpots.length }}</h4>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Spots Grid -->
              <div class="row">
                <div 
                  v-for="spot in parkingSpots" 
                  :key="spot.id" 
                  class="col-xl-2 col-lg-3 col-md-4 col-sm-6 mb-3"
                >
                  <div 
                    class="card h-100 spot-card"
                    :class="spot.status === 'A' ? 'border-success' : 'border-danger'"
                  >
                    <div class="card-body text-center p-2">
                      <h6 class="card-title mb-1">
                        #{{ spot.spot_number }}
                      </h6>
                      <span 
                        :class="spot.status === 'A' ? 'badge bg-success' : 'badge bg-danger'"
                        class="badge mb-2"
                      >
                        {{ spot.status === 'A' ? 'Free' : 'Occupied' }}
                      </span>
                      
                      <!-- Occupied spot details -->
                      <div v-if="spot.status === 'O' && spot.reservation" class="mt-2">
                        <small class="text-muted">
                          <strong>{{ spot.reservation.username }}</strong><br>
                          {{ formatTime(spot.reservation.parking_timestamp) }}
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-4">
              <p class="text-muted">No parking spots found.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeSpotsModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop -->
    <div 
      v-if="showCreateModal || showSpotsModal" 
      class="modal-backdrop fade show"
      @click="closeModal"
    ></div>
  </div>
</template>

<script>
import { reactive, computed, onMounted, ref } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'
import { parkingAPI } from '@/services/api'

export default {
  name: 'ParkingLotsManagement',
  setup() {
    const store = useStore()
    const toast = useToast()

    const showCreateModal = ref(false)
    const showSpotsModal = ref(false)
    const editingLot = ref(null)
    const selectedLot = ref(null)
    const parkingSpots = ref([])
    const loadingSpots = ref(false)
    const searchQuery = ref('')

    const lotForm = reactive({
      prime_location_name: '',
      address: '',
      pin_code: '',
      price: '',
      number_of_spots: ''
    })

    const parkingLots = computed(() => store.state.parkingLots)
    const loading = computed(() => store.state.loading)
    
    const filteredLots = computed(() => {
      if (!searchQuery.value) return parkingLots.value
      
      const query = searchQuery.value.toLowerCase()
      return parkingLots.value.filter(lot =>
        lot.prime_location_name.toLowerCase().includes(query) ||
        lot.address.toLowerCase().includes(query) ||
        lot.pin_code.includes(query)
      )
    })
    
    const totalAvailableSpots = computed(() => 
      parkingLots.value.reduce((sum, lot) => sum + lot.available_spots, 0)
    )
    
    const totalOccupiedSpots = computed(() => 
      parkingLots.value.reduce((sum, lot) => sum + lot.occupied_spots, 0)
    )

    const totalRevenue = computed(() => 
      parkingLots.value.reduce((sum, lot) => sum + (lot.occupied_spots * lot.price), 0)
    )

    const availableSpots = computed(() => 
      parkingSpots.value.filter(spot => spot.status === 'A').length
    )
    
    const occupiedSpots = computed(() => 
      parkingSpots.value.filter(spot => spot.status === 'O').length
    )

    const getOccupancyPercentage = (lot) => {
      if (lot.number_of_spots === 0) return 0
      return Math.round((lot.occupied_spots / lot.number_of_spots) * 100)
    }

    const getOccupancyClass = (lot) => {
      const percentage = getOccupancyPercentage(lot)
      if (percentage >= 80) return 'bg-danger'
      if (percentage >= 50) return 'bg-warning'
      return 'bg-success'
    }

    const resetForm = () => {
      lotForm.prime_location_name = ''
      lotForm.address = ''
      lotForm.pin_code = ''
      lotForm.price = ''
      lotForm.number_of_spots = ''
      editingLot.value = null
    }

    const closeModal = () => {
      showCreateModal.value = false
      resetForm()
    }

    const closeSpotsModal = () => {
      showSpotsModal.value = false
      selectedLot.value = null
      parkingSpots.value = []
    }

    const editLot = (lot) => {
      editingLot.value = lot
      lotForm.prime_location_name = lot.prime_location_name
      lotForm.address = lot.address
      lotForm.pin_code = lot.pin_code
      lotForm.price = lot.price
      lotForm.number_of_spots = lot.number_of_spots
      showCreateModal.value = true
    }

    // FIXED saveLot method with proper error handling
    const saveLot = async () => {
      try {
        // Validate form data
        if (!lotForm.prime_location_name.trim()) {
          toast.error('Location name is required')
          return
        }
        if (!lotForm.address.trim()) {
          toast.error('Address is required')
          return
        }
        if (!lotForm.pin_code.trim() || lotForm.pin_code.length !== 6) {
          toast.error('Valid 6-digit pin code is required')
          return
        }
        if (!lotForm.price || parseFloat(lotForm.price) <= 0) {
          toast.error('Valid price is required')
          return
        }
        if (!lotForm.number_of_spots || parseInt(lotForm.number_of_spots) <= 0) {
          toast.error('Valid number of spots is required')
          return
        }

        const lotData = {
          prime_location_name: lotForm.prime_location_name.trim(),
          address: lotForm.address.trim(),
          pin_code: lotForm.pin_code.trim(),
          price: parseFloat(lotForm.price),
          number_of_spots: parseInt(lotForm.number_of_spots)
        }

        console.log('Component: Saving lot data:', lotData)
        console.log('Component: Editing lot:', editingLot.value)

        let result
        if (editingLot.value) {
          console.log('Component: Updating lot with ID:', editingLot.value.id)
          result = await store.dispatch('updateParkingLot', {
            lotId: editingLot.value.id,
            lotData
          })
        } else {
          console.log('Component: Creating new lot')
          result = await store.dispatch('createParkingLot', lotData)
        }

        console.log('Component: Action result:', result)

        if (result && result.success) {
          toast.success(
            editingLot.value 
              ? 'Parking lot updated successfully!' 
              : 'Parking lot created successfully!'
          )
          closeModal()
        } else {
          const errorMessage = result?.error || 'Operation failed'
          toast.error(errorMessage)
          console.error('Component: Save operation failed:', result)
        }
      } catch (error) {
        console.error('Component: Error in saveLot:', error)
        toast.error('An unexpected error occurred: ' + error.message)
      }
    }

    // FIXED deleteLot method with proper error handling
    const deleteLot = async (lot) => {
      try {
        if (lot.occupied_spots > 0) {
          toast.error('Cannot delete parking lot with occupied spots')
          return
        }

        const confirmed = confirm(
          `Are you sure you want to delete "${lot.prime_location_name}"?\n\n` +
          `This will permanently remove:\n` +
          `- The parking lot\n` +
          `- All ${lot.number_of_spots} parking spots\n` +
          `- All associated data\n\n` +
          `This action cannot be undone.`
        )

        if (confirmed) {
          console.log('Component: Deleting lot with ID:', lot.id)
          
          const result = await store.dispatch('deleteParkingLot', lot.id)
          
          console.log('Component: Delete result:', result)

          if (result && result.success) {
            toast.success('Parking lot deleted successfully!')
          } else {
            const errorMessage = result?.error || 'Delete operation failed'
            toast.error(errorMessage)
            console.error('Component: Delete operation failed:', result)
          }
        }
      } catch (error) {
        console.error('Component: Error in deleteLot:', error)
        toast.error('An unexpected error occurred: ' + error.message)
      }
    }

    const viewSpots = async (lot) => {
      selectedLot.value = lot
      showSpotsModal.value = true
      loadingSpots.value = true
      
      try {
        const response = await parkingAPI.getSpots(lot.id)
        parkingSpots.value = response.data.spots
      } catch (error) {
        toast.error('Failed to load parking spots')
        console.error('Error loading spots:', error)
      } finally {
        loadingSpots.value = false
      }
    }

    const refreshLots = () => {
      console.log('Component: Refreshing parking lots...')
      store.dispatch('fetchParkingLots')
      toast.info('Parking lots refreshed!')
    }

    const formatTime = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleTimeString()
    }

    onMounted(() => {
      console.log('Component: Mounted, fetching parking lots...')
      store.dispatch('fetchParkingLots')
    })

    return {
      showCreateModal,
      showSpotsModal,
      editingLot,
      selectedLot,
      parkingSpots,
      loadingSpots,
      searchQuery,
      lotForm,
      parkingLots,
      filteredLots,
      loading,
      totalAvailableSpots,
      totalOccupiedSpots,
      totalRevenue,
      availableSpots,
      occupiedSpots,
      getOccupancyPercentage,
      getOccupancyClass,
      closeModal,
      closeSpotsModal,
      editLot,
      saveLot,
      deleteLot,
      viewSpots,
      refreshLots,
      formatTime
    }
  }
}
</script>

<style scoped>
.parking-lots-management {
  max-width: 1400px;
  margin: 0 auto;
}

.spot-card {
  min-height: 100px;
  transition: transform 0.2s;
}

.spot-card:hover {
  transform: scale(1.05);
}

.progress {
  border-radius: 10px;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.modal.show {
  display: block !important;
}

.table th {
  border-top: none;
  font-weight: 600;
}
</style>