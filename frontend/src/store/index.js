import { createStore } from 'vuex'
import { authAPI, parkingAPI } from '@/services/api'

export default createStore({
  state: {
    // Authentication
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('access_token') || null,
    isAuthenticated: !!localStorage.getItem('access_token'),
    
    // Parking
    parkingLots: [],
    userReservations: [],
    allUsers: [],
    
    // UI
    loading: false,
    error: null
  },
  
  getters: {
    isAdmin: state => state.user?.role === 'admin',
    isUser: state => state.user?.role === 'user',
    activeReservation: state => {
      return state.userReservations.find(r => r.status === 'active')
    }
  },
  
  mutations: {
    SET_LOADING(state, status) {
      state.loading = status
    },
    
    SET_ERROR(state, error) {
      state.error = error
    },
    
    SET_AUTH(state, { user, token }) {
      state.user = user
      state.token = token
      state.isAuthenticated = !!token
      
      if (token) {
        localStorage.setItem('access_token', token)
        localStorage.setItem('user', JSON.stringify(user))
      } else {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
      }
    },
    
    LOGOUT(state) {
      state.user = null
      state.token = null
      state.isAuthenticated = false
      state.userReservations = []
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    },
    
    SET_PARKING_LOTS(state, lots) {
      state.parkingLots = lots
    },
    
    ADD_PARKING_LOT(state, lot) {
      state.parkingLots.push(lot)
    },
    
    UPDATE_PARKING_LOT(state, updatedLot) {
      const index = state.parkingLots.findIndex(lot => lot.id === updatedLot.id)
      if (index !== -1) {
        state.parkingLots.splice(index, 1, updatedLot)
      }
    },
    
    REMOVE_PARKING_LOT(state, lotId) {
      state.parkingLots = state.parkingLots.filter(lot => lot.id !== lotId)
    },
    
    SET_USER_RESERVATIONS(state, reservations) {
      state.userReservations = reservations
    },
    
    ADD_RESERVATION(state, reservation) {
      state.userReservations.unshift(reservation)
    },
    
    UPDATE_RESERVATION(state, updatedReservation) {
      const index = state.userReservations.findIndex(r => r.id === updatedReservation.id)
      if (index !== -1) {
        state.userReservations.splice(index, 1, updatedReservation)
      }
    },
    
    SET_ALL_USERS(state, users) {
      state.allUsers = users
    }
  },
  
  actions: {
    // Authentication Actions
    async login({ commit }, credentials) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await authAPI.login(credentials)
        const { user, access_token } = response.data
        
        commit('SET_AUTH', { user, token: access_token })
        return { success: true, user }
      } catch (error) {
        const message = error.response?.data?.error || 'Login failed'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async register({ commit }, userData) {
      try {
        commit('SET_LOADING', true)
        commit('SET_ERROR', null)
        
        const response = await authAPI.register(userData)
        return { success: true, data: response.data }
      } catch (error) {
        const message = error.response?.data?.error || 'Registration failed'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    logout({ commit }) {
      commit('LOGOUT')
    },
    
    // Parking Actions
    async fetchParkingLots({ commit }) {
      try {
        commit('SET_LOADING', true)
        const response = await parkingAPI.getAllLots()
        commit('SET_PARKING_LOTS', response.data.parking_lots)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.error || 'Failed to fetch parking lots')
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async createParkingLot({ commit }, lotData) {
      try {
        commit('SET_LOADING', true)
        const response = await parkingAPI.createLot(lotData)
        commit('ADD_PARKING_LOT', response.data.parking_lot)
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to create parking lot'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async updateParkingLot({ commit }, { lotId, lotData }) {
      try {
        commit('SET_LOADING', true)
        const response = await parkingAPI.updateLot(lotId, lotData)
        commit('UPDATE_PARKING_LOT', response.data.parking_lot)
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update parking lot'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },

    async deleteParkingLot({ commit }, lotId) {
      try {
        commit('SET_LOADING', true)
        await parkingAPI.deleteLot(lotId)
        commit('REMOVE_PARKING_LOT', lotId)
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to delete parking lot'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async bookParkingSpot({ commit }, lotId) {
      try {
        commit('SET_LOADING', true)
        const response = await parkingAPI.bookSpot(lotId)
        commit('ADD_RESERVATION', response.data.reservation)
        
        // Update parking lot availability
        const updatedLot = response.data.parking_lot
        commit('UPDATE_PARKING_LOT', updatedLot)
        
        return { success: true, data: response.data }
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to book parking spot'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async releaseParkingSpot({ commit }, reservationId) {
      try {
        commit('SET_LOADING', true)
        const response = await parkingAPI.releaseSpot(reservationId)
        commit('UPDATE_RESERVATION', response.data.reservation)
        return { success: true, data: response.data }
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to release parking spot'
        commit('SET_ERROR', message)
        return { success: false, error: message }
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchUserReservations({ commit }) {
      try {
        const response = await parkingAPI.getMyReservations()
        commit('SET_USER_RESERVATIONS', response.data.reservations)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.error || 'Failed to fetch reservations')
      }
    },
    
    async fetchAllUsers({ commit }) {
      try {
        const response = await authAPI.getAllUsers()
        commit('SET_ALL_USERS', response.data.users)
      } catch (error) {
        commit('SET_ERROR', error.response?.data?.error || 'Failed to fetch users')
      }
    }
  }
})