<template>
  <div class="admin-analytics">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>📊 Analytics & Reports</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/admin" class="text-decoration-none">Admin Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">Analytics</li>
          </ol>
        </nav>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-primary" @click="refreshData">
          🔄 Refresh Data
        </button>
        <button class="btn btn-outline-success" @click="exportReport">
          📊 Export Report
        </button>
      </div>
    </div>

    <!-- Key Metrics -->
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card bg-gradient-primary text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="text-white-50">Total Revenue</h6>
                <h3 class="mb-0">₹{{ totalRevenue.toLocaleString() }}</h3>
                <small class="text-white-50">This month</small>
              </div>
              <div class="metric-icon">💰</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card bg-gradient-success text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="text-white-50">Avg. Occupancy</h6>
                <h3 class="mb-0">{{ averageOccupancy }}%</h3>
                <small class="text-white-50">Across all lots</small>
              </div>
              <div class="metric-icon">📈</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card bg-gradient-info text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="text-white-50">Peak Hours</h6>
                <h3 class="mb-0">2-5 PM</h3>
                <small class="text-white-50">Highest usage</small>
              </div>
              <div class="metric-icon">⏰</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card bg-gradient-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="text-white-50">Active Users</h6>
                <h3 class="mb-0">{{ activeUsers }}</h3>
                <small class="text-white-50">This week</small>
              </div>
              <div class="metric-icon">👥</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="row mb-4">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">📈 Parking Lots Comparison</h5>
            <div class="btn-group" role="group">
              <input type="radio" class="btn-check" id="view-spots" v-model="comparisonView" value="spots">
              <label class="btn btn-outline-primary btn-sm" for="view-spots">Spots</label>
              
              <input type="radio" class="btn-check" id="view-revenue" v-model="comparisonView" value="revenue">
              <label class="btn btn-outline-primary btn-sm" for="view-revenue">Revenue</label>
            </div>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="comparisonChart" width="800" height="400"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">🎯 Overall Status</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="statusChart" width="400" height="400"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="row mb-4">
      <div class="col-lg-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">📊 Occupancy Rate by Location</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="occupancyChart" width="600" height="400"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">📅 Weekly Usage Trend</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="trendChart" width="600" height="400"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Table -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">📋 Parking Lot Performance</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead class="table-light">
              <tr>
                <th>Parking Lot</th>
                <th>Total Spots</th>
                <th>Occupancy Rate</th>
                <th>Daily Revenue</th>
                <th>Peak Hours</th>
                <th>Performance</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="lot in performanceData" :key="lot.id">
                <td>
                  <strong>{{ lot.prime_location_name }}</strong><br>
                  <small class="text-muted">{{ lot.address }}</small>
                </td>
                <td>
                  <span class="badge bg-primary">{{ lot.number_of_spots }}</span>
                </td>
                <td>
                  <div class="progress" style="height: 20px;">
                    <div 
                      class="progress-bar" 
                      :class="getPerformanceClass(lot.occupancy_rate)"
                      :style="{ width: lot.occupancy_rate + '%' }"
                    >
                      {{ lot.occupancy_rate }}%
                    </div>
                  </div>
                </td>
                <td>
                  <strong class="text-success">₹{{ lot.daily_revenue }}</strong>
                </td>
                <td>
                  <span class="badge bg-warning">{{ lot.peak_hours }}</span>
                </td>
                <td>
                  <span 
                    class="badge" 
                    :class="getPerformanceBadge(lot.performance_score)"
                  >
                    {{ lot.performance_status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, nextTick, watch } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'vue-toastification'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  DoughnutController,
  BarController,
  LineController,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  DoughnutController,
  BarController,
  LineController,
  Title,
  Tooltip,
  Legend
)

export default {
  name: 'AdminAnalytics',
  setup() {
    const store = useStore()
    const toast = useToast()

    // Chart refs
    const comparisonChart = ref(null)
    const statusChart = ref(null)
    const occupancyChart = ref(null)
    const trendChart = ref(null)
    
    const comparisonView = ref('spots')
    let chartsInstances = {}

    const parkingLots = computed(() => store.state.parkingLots)
    const allUsers = computed(() => store.state.allUsers)
    
    const totalRevenue = computed(() => 
      parkingLots.value.reduce((sum, lot) => sum + (lot.occupied_spots * lot.price * 8), 0) // 8 hours avg
    )
    
    const averageOccupancy = computed(() => {
      if (parkingLots.value.length === 0) return 0
      const total = parkingLots.value.reduce((sum, lot) => {
        return sum + (lot.number_of_spots > 0 ? (lot.occupied_spots / lot.number_of_spots) * 100 : 0)
      }, 0)
      return Math.round(total / parkingLots.value.length)
    })

    const activeUsers = computed(() => {
      // Mock calculation - would be based on recent activity
      return allUsers.value.filter(user => user.role === 'user').length
    })

    const performanceData = computed(() => {
      return parkingLots.value.map(lot => {
        const occupancy_rate = lot.number_of_spots > 0 
          ? Math.round((lot.occupied_spots / lot.number_of_spots) * 100) 
          : 0
        const daily_revenue = lot.occupied_spots * lot.price * 8 // 8 hours avg
        const performance_score = (occupancy_rate + (daily_revenue / 1000)) / 2

        return {
          ...lot,
          occupancy_rate,
          daily_revenue,
          peak_hours: '2-5 PM',
          performance_score,
          performance_status: performance_score > 70 ? 'Excellent' : 
                            performance_score > 50 ? 'Good' : 
                            performance_score > 30 ? 'Average' : 'Poor'
        }
      })
    })

    const getPerformanceClass = (rate) => {
      if (rate >= 80) return 'bg-danger'
      if (rate >= 60) return 'bg-warning'
      if (rate >= 40) return 'bg-info'
      return 'bg-success'
    }

    const getPerformanceBadge = (score) => {
      if (score > 70) return 'bg-success'
      if (score > 50) return 'bg-info'
      if (score > 30) return 'bg-warning'
      return 'bg-danger'
    }

    const createCharts = () => {
      if (parkingLots.value.length === 0) return

      // Destroy existing charts
      Object.values(chartsInstances).forEach(chart => {
        if (chart) chart.destroy()
      })

      nextTick(() => {
        createComparisonChart()
        createStatusChart()
        createOccupancyChart()
        createTrendChart()
      })
    }

    const createComparisonChart = () => {
      if (!comparisonChart.value) return

      const ctx = comparisonChart.value.getContext('2d')
      
      let datasets = []
      if (comparisonView.value === 'spots') {
        datasets = [
          {
            label: 'Available Spots',
            data: parkingLots.value.map(lot => lot.available_spots),
            backgroundColor: '#28a745',
            borderWidth: 1
          },
          {
            label: 'Occupied Spots',
            data: parkingLots.value.map(lot => lot.occupied_spots),
            backgroundColor: '#dc3545',
            borderWidth: 1
          }
        ]
      } else {
        datasets = [
          {
            label: 'Daily Revenue (₹)',
            data: parkingLots.value.map(lot => lot.occupied_spots * lot.price * 8),
            backgroundColor: '#007bff',
            borderWidth: 1
          }
        ]
      }

      chartsInstances.comparison = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: parkingLots.value.map(lot => lot.prime_location_name),
          datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: { y: { beginAtZero: true } },
          plugins: {
            title: { 
              display: true, 
              text: comparisonView.value === 'spots' ? 'Parking Spots Analysis' : 'Revenue Analysis'
            }
          }
        }
      })
    }

    const createStatusChart = () => {
      if (!statusChart.value) return

      const ctx = statusChart.value.getContext('2d')
      const totalAvailable = parkingLots.value.reduce((sum, lot) => sum + lot.available_spots, 0)
      const totalOccupied = parkingLots.value.reduce((sum, lot) => sum + lot.occupied_spots, 0)

      chartsInstances.status = new ChartJS(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Available', 'Occupied'],
          datasets: [{
            data: [totalAvailable, totalOccupied],
            backgroundColor: ['#28a745', '#dc3545'],
            borderWidth: 3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Overall Parking Status' }
          }
        }
      })
    }

    const createOccupancyChart = () => {
      if (!occupancyChart.value) return

      const ctx = occupancyChart.value.getContext('2d')
      const occupancyData = parkingLots.value.map(lot => {
        return lot.number_of_spots > 0 ? ((lot.occupied_spots / lot.number_of_spots) * 100).toFixed(1) : 0
      })

      chartsInstances.occupancy = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: parkingLots.value.map(lot => lot.prime_location_name),
          datasets: [{
            label: 'Occupancy Rate (%)',
            data: occupancyData,
            backgroundColor: occupancyData.map(rate => 
              rate > 80 ? '#dc3545' : 
              rate > 60 ? '#ffc107' : 
              rate > 40 ? '#17a2b8' : '#28a745'
            ),
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: { callback: value => value + '%' }
            }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Occupancy Rate by Location' }
          }
        }
      })
    }

    const createTrendChart = () => {
      if (!trendChart.value) return

      const ctx = trendChart.value.getContext('2d')
      
      // Mock weekly data
      const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      const mockData = [65, 72, 68, 78, 82, 75, 69]

      chartsInstances.trend = new ChartJS(ctx, {
        type: 'line',
        data: {
          labels: days,
          datasets: [{
            label: 'Average Occupancy (%)',
            data: mockData,
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            borderWidth: 3,
            fill: true,
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
              ticks: { callback: value => value + '%' }
            }
          },
          plugins: {
            title: { display: true, text: 'Weekly Usage Trend' }
          }
        }
      })
    }

    const refreshData = () => {
      store.dispatch('fetchParkingLots')
      store.dispatch('fetchAllUsers')
      toast.success('Data refreshed!')
      setTimeout(createCharts, 500)
    }

    const exportReport = () => {
      // Mock export functionality
      toast.info('Exporting analytics report...')
      setTimeout(() => {
        toast.success('Report exported successfully!')
      }, 2000)
    }

    onMounted(() => {
      store.dispatch('fetchParkingLots')
      store.dispatch('fetchAllUsers')
      
      setTimeout(() => {
        createCharts()
      }, 500)
    })

    watch([parkingLots, comparisonView], () => {
      createCharts()
    }, { deep: true })

    return {
      comparisonChart,
      statusChart,
      occupancyChart,
      trendChart,
      comparisonView,
      parkingLots,
      totalRevenue,
      averageOccupancy,
      activeUsers,
      performanceData,
      getPerformanceClass,
      getPerformanceBadge,
      refreshData,
      exportReport
    }
  }
}
</script>

<style scoped>
.admin-analytics {
  max-width: 1400px;
  margin: 0 auto;
}

.metric-card {
  border: none;
  background: linear-gradient(135deg, var(--bs-primary) 0%, var(--bs-info) 100%);
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}

.bg-gradient-success {
  background: linear-gradient(135deg, #28a745 0%, #1e7e34 100%);
}

.bg-gradient-info {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
}

.bg-gradient-warning {
  background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
}

.metric-icon {
  font-size: 2.5rem;
  opacity: 0.8;
}

.chart-container {
  position: relative;
  height: 400px;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: none;
}

.table th {
  border-top: none;
  font-weight: 600;
}

.btn-check:checked + .btn-outline-primary {
  background-color: #007bff;
  border-color: #007bff;
  color: white;
}
</style>