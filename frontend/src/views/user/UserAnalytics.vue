<template>
  <div class="user-analytics">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>📈 My Analytics</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/dashboard" class="text-decoration-none">Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">Analytics</li>
          </ol>
        </nav>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-outline-primary" @click="refreshData">
          🔄 Refresh Data
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
                <h6 class="text-white-50">Total Spent</h6>
                <h3 class="mb-0">₹{{ totalSpent.toLocaleString() }}</h3>
                <small class="text-white-50">All time</small>
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
                <h6 class="text-white-50">Total Bookings</h6>
                <h3 class="mb-0">{{ userReservations.length }}</h3>
                <small class="text-white-50">Completed trips</small>
              </div>
              <div class="metric-icon">🅿️</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card bg-gradient-info text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="text-white-50">Avg. Duration</h6>
                <h3 class="mb-0">{{ averageDuration }}</h3>
                <small class="text-white-50">Per session</small>
              </div>
              <div class="metric-icon">⏱️</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="card metric-card bg-gradient-warning text-white">
          <div class="card-body">
            <div class="d-flex justify-content-between">
              <div>
                <h6 class="text-white-50">Favorite Spot</h6>
                <h3 class="mb-0" style="font-size: 1.5rem;">{{ favoriteLocation }}</h3>
                <small class="text-white-50">Most visited</small>
              </div>
              <div class="metric-icon">🏆</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">📊 My Parking Summary</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="userSummaryChart" width="400" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">💰 Monthly Spending</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="spendingChart" width="400" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">🏢 Most Used Parking Lots</h5>
          </div>
          <div class="card-body">
            <div class="chart-container" style="height: 400px;">
              <canvas ref="usageChart" width="800" height="400"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Usage Patterns -->
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">🕒 Parking Hours Pattern</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="hoursChart" width="400" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="mb-0">📅 Weekly Usage Pattern</h5>
          </div>
          <div class="card-body">
            <div class="chart-container">
              <canvas ref="weeklyChart" width="400" height="300"></canvas>
            </div>
          </div>
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
  name: 'UserAnalytics',
  setup() {
    const store = useStore()
    const toast = useToast()

    // Chart refs
    const userSummaryChart = ref(null)
    const spendingChart = ref(null)
    const usageChart = ref(null)
    const hoursChart = ref(null)
    const weeklyChart = ref(null)
    let chartsInstances = {}

    const userReservations = computed(() => store.state.userReservations)

    const totalSpent = computed(() => 
      userReservations.value.reduce((sum, r) => sum + (r.parking_cost || 0), 0)
    )

    const averageDuration = computed(() => {
      const completedReservations = userReservations.value.filter(r => 
        r.status === 'completed' && r.parking_timestamp && r.leaving_timestamp
      )
      
      if (completedReservations.length === 0) return '0h 0m'
      
      const totalDuration = completedReservations.reduce((sum, r) => {
        const start = new Date(r.parking_timestamp)
        const end = new Date(r.leaving_timestamp)
        return sum + (end - start)
      }, 0)
      
      const avgMs = totalDuration / completedReservations.length
      const hours = Math.floor(avgMs / (1000 * 60 * 60))
      const minutes = Math.floor((avgMs % (1000 * 60 * 60)) / (1000 * 60))
      
      return `${hours}h ${minutes}m`
    })

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

    const createCharts = () => {
      if (userReservations.value.length === 0) return

      // Destroy existing charts
      Object.values(chartsInstances).forEach(chart => {
        if (chart) chart.destroy()
      })

      nextTick(() => {
        createSummaryChart()
        createSpendingChart()
        createUsageChart()
        createHoursChart()
        createWeeklyChart()
      })
    }

    const createSummaryChart = () => {
      if (!userSummaryChart.value) return

      const ctx = userSummaryChart.value.getContext('2d')
      const activeCount = userReservations.value.filter(r => r.status === 'active').length
      const completedCount = userReservations.value.filter(r => r.status === 'completed').length
      const cancelledCount = userReservations.value.filter(r => r.status === 'cancelled').length

      chartsInstances.summary = new ChartJS(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Active', 'Completed', 'Cancelled'],
          datasets: [{
            data: [activeCount, completedCount, cancelledCount],
            backgroundColor: ['#ffc107', '#28a745', '#dc3545'],
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' },
            title: { display: true, text: 'Reservation Status Distribution' }
          }
        }
      })
    }

    const createSpendingChart = () => {
      if (!spendingChart.value) return

      const ctx = spendingChart.value.getContext('2d')
      
      // Group spending by month
      const monthlySpending = {}
      userReservations.value.forEach(reservation => {
        if (reservation.parking_cost && reservation.parking_timestamp) {
          const date = new Date(reservation.parking_timestamp)
          const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
          monthlySpending[monthKey] = (monthlySpending[monthKey] || 0) + reservation.parking_cost
        }
      })

      const sortedMonths = Object.keys(monthlySpending).sort()
      const spendingData = sortedMonths.map(month => monthlySpending[month])

      chartsInstances.spending = new ChartJS(ctx, {
        type: 'line',
        data: {
          labels: sortedMonths.map(month => {
            const [year, monthNum] = month.split('-')
            return new Date(year, monthNum - 1).toLocaleDateString('en', { month: 'short', year: 'numeric' })
          }),
          datasets: [{
            label: 'Amount Spent (₹)',
            data: spendingData,
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            borderWidth: 2,
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
              ticks: { callback: value => '₹' + value }
            }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Spending Trend Over Time' }
          }
        }
      })
    }

    const createUsageChart = () => {
      if (!usageChart.value) return

      const ctx = usageChart.value.getContext('2d')
      
      // Count usage by parking lot
      const lotUsage = {}
      userReservations.value.forEach(reservation => {
        if (reservation.lot_name) {
          lotUsage[reservation.lot_name] = (lotUsage[reservation.lot_name] || 0) + 1
        }
      })

      const sortedLots = Object.entries(lotUsage)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 10) // Top 10 most used lots

      chartsInstances.usage = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: sortedLots.map(([name]) => name),
          datasets: [{
            label: 'Number of Visits',
            data: sortedLots.map(([, count]) => count),
            backgroundColor: [
              '#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1',
              '#20c997', '#fd7e14', '#e83e8c', '#6c757d', '#17a2b8'
            ],
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 }
            }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Most Frequently Used Parking Lots' }
          }
        }
      })
    }

    const createHoursChart = () => {
      if (!hoursChart.value) return

      const ctx = hoursChart.value.getContext('2d')
      
      // Count usage by hour of day
      const hourlyUsage = Array(24).fill(0)
      userReservations.value.forEach(reservation => {
        if (reservation.parking_timestamp) {
          const hour = new Date(reservation.parking_timestamp).getHours()
          hourlyUsage[hour]++
        }
      })

      chartsInstances.hours = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: Array.from({length: 24}, (_, i) => `${i}:00`),
          datasets: [{
            label: 'Bookings',
            data: hourlyUsage,
            backgroundColor: '#17a2b8',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 }
            }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Parking Preferences by Hour' }
          }
        }
      })
    }

    const createWeeklyChart = () => {
      if (!weeklyChart.value) return

      const ctx = weeklyChart.value.getContext('2d')
      
      // Count usage by day of week
      const weeklyUsage = Array(7).fill(0)
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
      
      userReservations.value.forEach(reservation => {
        if (reservation.parking_timestamp) {
          const day = new Date(reservation.parking_timestamp).getDay()
          weeklyUsage[day]++
        }
      })

      chartsInstances.weekly = new ChartJS(ctx, {
        type: 'bar',
        data: {
          labels: dayNames,
          datasets: [{
            label: 'Bookings',
            data: weeklyUsage,
            backgroundColor: '#28a745',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { stepSize: 1 }
            }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Parking Preferences by Day' }
          }
        }
      })
    }

    const refreshData = () => {
      store.dispatch('fetchUserReservations')
      toast.success('Data refreshed!')
      setTimeout(createCharts, 500)
    }

    onMounted(() => {
      store.dispatch('fetchUserReservations')
      setTimeout(() => {
        createCharts()
      }, 500)
    })

    watch(userReservations, () => {
      createCharts()
    }, { deep: true })

    return {
      userReservations,
      totalSpent,
      averageDuration,
      favoriteLocation,
      userSummaryChart,
      spendingChart,
      usageChart,
      hoursChart,
      weeklyChart,
      refreshData
    }
  }
}
</script>

<style scoped>
.user-analytics {
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
  height: 300px;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border: none;
}
</style>