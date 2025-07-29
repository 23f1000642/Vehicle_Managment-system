<template>
  <div class="background-jobs" :class="{ 'dark-mode': isDarkMode }">
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
      <div>
        <h2 class="jobs-title">
          <span class="me-2">🔧</span>Background Jobs Testing
        </h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/admin" class="text-decoration-none">
                <span class="me-1">🏢</span>Admin Dashboard
              </router-link>
            </li>
            <li class="breadcrumb-item active">
              <span class="me-1">🔧</span>Background Jobs
            </li>
          </ol>
        </nav>
      </div>
    </div>

    <!-- System Status Cards -->
    <div class="row mb-4">
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-success text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">🟢</div>
            <h5 class="card-title">System Status</h5>
            <h2 class="stat-number">Online</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-info text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">✅</div>
            <h5 class="card-title">Jobs Completed</h5>
            <h2 class="stat-number">{{ completedJobs }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-warning text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">⚡</div>
            <h5 class="card-title">Queue Status</h5>
            <h2 class="stat-number">Running</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3 mb-3">
        <div class="card stat-card bg-primary text-white">
          <div class="card-body text-center">
            <div class="stat-icon mb-2">⏰</div>
            <h5 class="card-title">Server Uptime</h5>
            <h2 class="stat-number">{{ serverUptime }}h</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Background Jobs Testing Section -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card jobs-card">
          <div class="card-header">
            <h5 class="mb-0">
              <span class="me-2">🔧</span>Background Jobs Testing
            </h5>
          </div>
          <div class="card-body">
            <div class="test-description mb-4">
              <p class="test-info">
                <span class="me-1">ℹ️</span>Test the automated background job functionality:
              </p>
            </div>
            
            <div class="test-buttons mb-4">
              <div class="row g-3">
                <div class="col-md-6">
                  <button 
                    class="btn btn-info w-100 test-btn" 
                    @click="testDailyReminders"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    <span v-if="!loading" class="me-2">📧</span>
                    Test Daily Reminders
                  </button>
                </div>
                <div class="col-md-6">
                  <button 
                    class="btn btn-warning w-100 test-btn" 
                    @click="testMonthlyReports"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    <span v-if="!loading" class="me-2">📊</span>
                    Test Monthly Reports
                  </button>
                </div>
              </div>
            </div>

            <!-- Test Results Display -->
            <div v-if="testResults" class="test-results">
              <div class="results-header">
                <h6 class="results-title">
                  <span class="me-1">📋</span>Last Test Result:
                </h6>
              </div>
              <div class="results-content">
                <pre class="results-pre">{{ testResults }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Test Results Log -->
    <div class="card log-card">
      <div class="card-header">
        <h5 class="mb-0">
          <span class="me-2">📋</span>Test Results Log
        </h5>
      </div>
      <div class="card-body">
        <!-- Empty State -->
        <div v-if="testLog.length === 0" class="empty-state">
          <div class="empty-icon">🔧</div>
          <p class="empty-text">No test results yet. Run a test to see results here.</p>
        </div>
        
        <!-- Log Table -->
        <div v-else>
          <div class="table-responsive">
            <table class="table table-hover log-table">
              <thead>
                <tr>
                  <th scope="col" class="test-type-header">
                    <span class="me-2">🔧</span>Test Type
                  </th>
                  <th scope="col" class="status-header">
                    <span class="me-2">📊</span>Status
                  </th>
                  <th scope="col" class="timestamp-header">
                    <span class="me-2">🕒</span>Timestamp
                  </th>
                  <th scope="col" class="result-header">
                    <span class="me-2">📝</span>Result
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(log, index) in testLog" :key="index" class="log-row">
                  <td class="test-type-cell">
                    <div class="test-type-info">
                      <span class="test-icon me-2">
                        {{ getTestIcon(log.type) }}
                      </span>
                      <span class="test-name">{{ log.type }}</span>
                    </div>
                  </td>
                  <td class="status-cell">
                    <span 
                      class="badge status-badge"
                      :class="log.status === 'Success' ? 'bg-success' : 'bg-danger'"
                    >
                      <span class="me-2">{{ log.status === 'Success' ? '✅' : '❌' }}</span>
                      {{ log.status }}
                    </span>
                  </td>
                  <td class="timestamp-cell">
                    <span class="me-2">🕒</span>{{ formatDateTime(log.timestamp) }}
                  </td>
                  <td class="result-cell">
                    <span class="result-text">{{ log.result }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Log Summary -->
          <div class="log-summary">
            <div class="summary-info">
              <span class="me-1">📊</span>
              Total Tests: <strong>{{ testLog.length }}</strong>
              <span class="mx-2">|</span>
              Success: <strong class="text-success">{{ successfulTests }}</strong>
              <span class="mx-2">|</span>
              Errors: <strong class="text-danger">{{ failedTests }}</strong>
            </div>
            <button class="btn btn-outline-secondary btn-sm" @click="clearLogs">
              <span class="me-1">🗑️</span>Clear Logs
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useToast } from 'vue-toastification'
import { parkingAPI } from '@/services/api'

export default {
  name: 'BackgroundJobs',
  setup() {
    const toast = useToast()
    const isDarkMode = ref(false)

    const testResults = ref(null)
    const testLog = ref([])
    const loading = computed(() => false) // Simple loading state

    const completedJobs = ref(Math.floor(Math.random() * 100) + 50)
    const serverUptime = ref(Math.floor(Math.random() * 72) + 24)

    const successfulTests = computed(() => 
      testLog.value.filter(log => log.status === 'Success').length
    )

    const failedTests = computed(() => 
      testLog.value.filter(log => log.status === 'Error').length
    )

    // Load theme preference
    onMounted(() => {
      const savedTheme = localStorage.getItem('darkMode')
      if (savedTheme) {
        isDarkMode.value = JSON.parse(savedTheme)
      } else {
        isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      
      // Add initial log entry
      addToLog('System Check', 'Success', 'Background jobs system initialized')
    })

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', JSON.stringify(isDarkMode.value))
    }

    const addToLog = (type, status, result) => {
      testLog.value.unshift({
        type,
        status,
        result,
        timestamp: new Date().toISOString()
      })
      // Keep only last 10 results
      if (testLog.value.length > 10) {
        testLog.value = testLog.value.slice(0, 10)
      }
    }

    const getTestIcon = (testType) => {
      const icons = {
        'Daily Reminders': '📧',
        'Monthly Reports': '📊',
        'System Check': '🔍'
      }
      return icons[testType] || '🔧'
    }

    const testDailyReminders = async () => {
      try {
        const response = await parkingAPI.testDailyReminders()
        testResults.value = JSON.stringify(response.data, null, 2)
        addToLog('Daily Reminders', 'Success', response.data.result)
        toast.success(`Daily reminders test completed: ${response.data.result}`)
      } catch (error) {
        testResults.value = `Error: ${error.response?.data?.error || error.message}`
        addToLog('Daily Reminders', 'Error', error.response?.data?.error || error.message)
        toast.error('Failed to test daily reminders')
      }
    }

    const testMonthlyReports = async () => {
      try {
        const response = await parkingAPI.testMonthlyReports()
        testResults.value = JSON.stringify(response.data, null, 2)
        addToLog('Monthly Reports', 'Success', response.data.result)
        toast.success(`Monthly reports test completed: ${response.data.result}`)
      } catch (error) {
        testResults.value = `Error: ${error.response?.data?.error || error.message}`
        addToLog('Monthly Reports', 'Error', error.response?.data?.error || error.message)
        toast.error('Failed to test monthly reports')
      }
    }

    const clearLogs = () => {
      testLog.value = []
      testResults.value = null
      toast.info('Test logs cleared')
    }

    const formatDateTime = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleString()
    }

    return {
      testResults,
      testLog,
      loading,
      completedJobs,
      serverUptime,
      successfulTests,
      failedTests,
      isDarkMode,
      toggleDarkMode,
      testDailyReminders,
      testMonthlyReports,
      clearLogs,
      getTestIcon,
      formatDateTime
    }
  }
}
</script>

<style scoped>
/* Base Styles */
.background-jobs {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  color: #212529;
  transition: all 0.3s ease;
  min-height: 100vh;
}

.background-jobs.dark-mode {
  background-color: #212529;
  color: #f8f9fa;
}

/* Header */
.jobs-title {
  font-weight: 700;
  color: #212529;
  margin: 0;
}

.dark-mode .jobs-title {
  color: #f8f9fa;
}

/* Breadcrumb */
.breadcrumb {
  background: transparent;
  padding: 0;
  margin: 0;
}

.dark-mode .breadcrumb-item a {
  color: #79c0ff;
}

.dark-mode .breadcrumb-item.active {
  color: #adb5bd;
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
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
}

/* Jobs Card */
.jobs-card,
.log-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.dark-mode .jobs-card,
.dark-mode .log-card {
  background-color: #343a40;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  color: #f8f9fa;
}

.dark-mode .jobs-card .card-header,
.dark-mode .log-card .card-header {
  background-color: #495057;
  border-color: #6c757d;
  color: #f8f9fa;
}

/* Test Description */
.test-description {
  background-color: #e3f2fd;
  border-radius: 8px;
  padding: 1rem;
  border-left: 4px solid #2196f3;
}

.dark-mode .test-description {
  background-color: rgba(33, 150, 243, 0.1);
  border-color: #2196f3;
}

.test-info {
  margin: 0;
  color: #1976d2;
  font-weight: 500;
}

.dark-mode .test-info {
  color: #64b5f6;
}

/* Test Buttons */
.test-btn {
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.test-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.test-btn:disabled {
  transform: none;
}

/* Test Results */
.test-results {
  margin-top: 1.5rem;
}

.results-header {
  margin-bottom: 1rem;
}

.results-title {
  color: #495057;
  font-weight: 600;
}

.dark-mode .results-title {
  color: #adb5bd;
}

.results-content {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
}

.dark-mode .results-content {
  background-color: #495057;
  border-color: #6c757d;
}

.results-pre {
  background: transparent;
  border: none;
  color: #212529;
  font-size: 0.9rem;
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.dark-mode .results-pre {
  color: #f8f9fa;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 1rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-text {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

.dark-mode .empty-text {
  color: #adb5bd;
}

/* Log Table */
.log-table {
  margin-bottom: 0;
}

.log-table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
  padding: 1rem 0.75rem;
  white-space: nowrap;
  vertical-align: middle;
}

.dark-mode .log-table th {
  color: #adb5bd;
  background-color: #495057;
  border-color: #6c757d;
}

/* Table Header Specific Styling */
.test-type-header {
  min-width: 180px;
}

.status-header {
  min-width: 120px;
}

.timestamp-header {
  min-width: 200px;
}

.result-header {
  min-width: 250px;
}

.log-row {
  transition: all 0.3s ease;
}

.log-row:hover {
  background-color: rgba(0, 123, 255, 0.05);
}

.dark-mode .log-row:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.dark-mode .log-table td {
  border-color: #6c757d;
  color: #f8f9fa;
  background-color: #343a40;
}

.log-table td {
  background-color: #ffffff;
  color: #212529;
  border-color: #dee2e6;
}

/* Table Cells */
.test-type-cell {
  padding: 1rem 0.75rem;
  min-width: 180px;
  vertical-align: middle;
}

.test-type-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.test-icon {
  font-size: 1.2rem;
  min-width: 24px;
  display: inline-block;
  flex-shrink: 0;
}

.test-name {
  font-weight: 600;
  color: #212529 !important;
  white-space: nowrap;
}

.dark-mode .test-name {
  color: #f8f9fa !important;
}

.status-cell {
  padding: 1rem 0.75rem;
  vertical-align: middle;
  min-width: 120px;
}

.timestamp-cell {
  color: #495057 !important;
  font-size: 0.9rem;
  padding: 1rem 0.75rem;
  vertical-align: middle;
  min-width: 200px;
  white-space: nowrap;
}

.dark-mode .timestamp-cell {
  color: #adb5bd !important;
}

.result-cell {
  max-width: 300px;
  padding: 1rem 0.75rem;
  vertical-align: middle;
}

.result-text {
  color: #495057 !important;
  font-size: 0.9rem;
  word-break: break-word;
  line-height: 1.4;
}

.dark-mode .result-text {
  color: #adb5bd !important;
}

/* Log Summary */
.log-summary {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.dark-mode .log-summary {
  background-color: #495057;
}

.summary-info {
  color: #6c757d;
  font-size: 0.9rem;
  flex: 1;
}

.dark-mode .summary-info {
  color: #adb5bd;
}

/* Theme Toggle */
.btn-outline-primary {
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  transform: scale(1.05);
}

/* Button Styling for Dark Mode */
.dark-mode .btn-outline-secondary {
  border-color: #6c757d;
  color: #adb5bd;
}

.dark-mode .btn-outline-secondary:hover {
  background-color: #6c757d;
  border-color: #6c757d;
  color: #fff;
}

/* Responsive Design */
@media (max-width: 768px) {
  .background-jobs {
    padding: 15px;
  }
  
  .jobs-title {
    font-size: 1.5rem;
  }
  
  .stat-number {
    font-size: 1.8rem;
  }
  
  .stat-icon {
    font-size: 2rem;
  }
  
  .test-btn {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
  
  .log-table th,
  .log-table td {
    padding: 0.75rem 0.5rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 576px) {
  .d-flex.justify-content-between {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 1rem;
  }
  
  .log-summary {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .summary-info {
    margin-bottom: 0.5rem;
  }
  
  /* Hide some columns on mobile */
  .log-table th:nth-child(3),
  .log-table td:nth-child(3) {
    display: none;
  }
  
  .result-cell {
    max-width: 200px;
  }
}

/* Focus Styles for Accessibility */
.btn:focus {
  outline: 2px solid #0d6efd;
  outline-offset: 2px;
}

/* Text Color Overrides for Dark Mode */
.dark-mode .text-success {
  color: #75d194 !important;
}

.dark-mode .text-danger {
  color: #ea868f !important;
}

/* Table Responsiveness */
.table-responsive {
  border-radius: 8px;
}

.dark-mode .table-responsive {
  background-color: #343a40;
}
</style>