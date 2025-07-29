import axios from 'axios'

// Create axios instance
const api = axios.create({
  baseURL: '/api', // This will proxy to localhost:5000/api
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getProfile: () => api.get('/auth/profile'),
  getAllUsers: () => api.get('/auth/users')
}

// Parking API
export const parkingAPI = {
  // Parking Lots
  getAllLots: () => api.get('/parking/lots'),
  createLot: (lotData) => api.post('/parking/lots', lotData),
  updateLot: (lotId, lotData) => api.put(`/parking/lots/${lotId}`, lotData),
  deleteLot: (lotId) => api.delete(`/parking/lots/${lotId}`),
  
  // Parking Spots
  getSpots: (lotId) => api.get(`/parking/lots/${lotId}/spots`),
  
  // Reservations
  bookSpot: (lotId) => api.post('/parking/book', { lot_id: lotId }),
  releaseSpot: (reservationId) => api.post(`/parking/release/${reservationId}`),
  getMyReservations: () => api.get('/parking/my-reservations'),
  exportCSVAsync: () => api.post('/parking/export-csv-sync', {}, { responseType: 'blob' }),
  
  // Background Jobs Testing
  testDailyReminders: () => api.post('/parking/test-daily-reminder'),
  testMonthlyReports: () => api.post('/parking/test-monthly-report')
}

export default api