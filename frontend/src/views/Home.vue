<template>
  <div class="home" :class="{ 'dark-mode': isDarkMode }">
    <!-- Dark Mode Toggle -->
    <div class="theme-toggle-container">
      <button 
        @click="toggleDarkMode" 
        class="theme-toggle-btn"
        :title="isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
      >
        <span class="theme-icon">{{ isDarkMode ? '☀️' : '🌙' }}</span>
      </button>
    </div>

    <!-- Hero Section -->
    <div class="hero-section text-white text-center py-5 mb-5 rounded">
      <div class="container">
        <h1 class="display-4 fw-bold hero-title">
          <span class="hero-emoji">🚗</span> 
          Vehicle Parking Management
        </h1>
        <p class="lead hero-subtitle">Efficient parking lot management for 4-wheeler vehicles</p>
        <div v-if="!isAuthenticated" class="mt-4">
          <router-link to="/login" class="btn btn-hero-primary btn-lg me-3">
            <span class="btn-icon">🔑</span> Login
          </router-link>
          <router-link to="/register" class="btn btn-hero-secondary btn-lg">
            <span class="btn-icon">📝</span> Register
          </router-link>
        </div>
        <div v-else class="mt-4">
          <router-link 
            :to="isAdmin ? '/admin' : '/dashboard'" 
            class="btn btn-hero-primary btn-lg"
          >
            <span class="btn-icon">{{ isAdmin ? '⚙️' : '📊' }}</span>
            Go to {{ isAdmin ? 'Admin' : 'User' }} Dashboard
          </router-link>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section">
      <div class="row">
        <div class="col-md-4 mb-4">
          <div class="feature-card h-100">
            <div class="card-body text-center">
              <div class="feature-icon">🏢</div>
              <h4 class="card-title">Admin Management</h4>
              <p class="card-text">
                Complete control over parking lots and spots. Create, edit, and delete parking facilities with ease.
              </p>
              <div class="feature-highlight"></div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4 mb-4">
          <div class="feature-card h-100">
            <div class="card-body text-center">
              <div class="feature-icon">🚘</div>
              <h4 class="card-title">Easy Booking</h4>
              <p class="card-text">
                Automatic spot allocation for users. Book and release parking spots with just a few clicks.
              </p>
              <div class="feature-highlight"></div>
            </div>
          </div>
        </div>
        
        <div class="col-md-4 mb-4">
          <div class="feature-card h-100">
            <div class="card-body text-center">
              <div class="feature-icon">📊</div>
              <h4 class="card-title">Real-time Tracking</h4>
              <p class="card-text">
                Monitor parking lot status, reservation history, and generate comprehensive reports.
              </p>
              <div class="feature-highlight"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Section -->
    <div v-if="parkingLots.length > 0" class="parking-lots-section mt-5">
      <div class="col-12">
        <div class="section-header">
          <h3 class="section-title">
            <span class="section-icon">🅿️</span>
            Available Parking Lots
          </h3>
          <div class="section-divider"></div>
        </div>
        <div class="row">
          <div v-for="lot in parkingLots" :key="lot.id" class="col-md-6 col-lg-4 mb-4">
            <div class="parking-lot-card">
              <div class="card-body">
                <div class="lot-header">
                  <h5 class="lot-title">{{ lot.prime_location_name }}</h5>
                  <div class="lot-price">₹{{ lot.price }}/hour</div>
                </div>
                <p class="lot-address">
                  <span class="address-icon">📍</span>
                  {{ lot.address }}
                </p>
                <div class="lot-stats">
                  <div class="stat-item available">
                    <span class="stat-icon">✅</span>
                    <span class="stat-label">Available</span>
                    <span class="stat-value">{{ lot.available_spots }}</span>
                  </div>
                  <div class="stat-item occupied">
                    <span class="stat-icon">🚗</span>
                    <span class="stat-label">Occupied</span>
                    <span class="stat-value">{{ lot.occupied_spots }}</span>
                  </div>
                </div>
              </div>
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

export default {
  name: 'Home',
  setup() {
    const store = useStore()
    const isDarkMode = ref(false)

    const isAuthenticated = computed(() => store.state.isAuthenticated)
    const isAdmin = computed(() => store.getters.isAdmin)
    const parkingLots = computed(() => store.state.parkingLots)

    // Load theme preference
    onMounted(() => {
      const savedTheme = localStorage.getItem('darkMode')
      if (savedTheme) {
        isDarkMode.value = JSON.parse(savedTheme)
      } else {
        // Check system preference
        isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      
      // Fetch parking lots for display
      store.dispatch('fetchParkingLots')
    })

    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', JSON.stringify(isDarkMode.value))
    }

    return {
      isAuthenticated,
      isAdmin,
      parkingLots,
      isDarkMode,
      toggleDarkMode
    }
  }
}
</script>

<style scoped>
/* Root Variables */
:root {
  --primary-gradient: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  --dark-primary-gradient: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  --light-bg: #ffffff;
  --light-text: #333333;
  --light-card-bg: #ffffff;
  --light-border: #e9ecef;
  --dark-bg: #0d1117;
  --dark-text: #e6edf3;
  --dark-card-bg: #161b22;
  --dark-border: #30363d;
  --shadow-light: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-dark: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Base Styles */
.home {
  background-color: var(--light-bg);
  color: var(--light-text);
  transition: var(--transition);
  min-height: 100vh;
  padding: 20px;
}

.home.dark-mode {
  background-color: var(--dark-bg);
  color: var(--dark-text);
}

/* Theme Toggle */
.theme-toggle-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
}

.theme-toggle-btn {
  background: var(--light-card-bg);
  border: 2px solid var(--light-border);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
  box-shadow: var(--shadow-light);
}

.dark-mode .theme-toggle-btn {
  background: var(--dark-card-bg);
  border-color: var(--dark-border);
  box-shadow: var(--shadow-dark);
}

.theme-toggle-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.2);
}

.theme-icon {
  font-size: 24px;
  transition: var(--transition);
}

/* Hero Section */
.hero-section {
  background: var(--primary-gradient);
  border-radius: 20px;
  box-shadow: var(--shadow-light);
  position: relative;
  overflow: hidden;
}

.dark-mode .hero-section {
  background: var(--dark-primary-gradient);
  box-shadow: var(--shadow-dark);
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.hero-title {
  position: relative;
  z-index: 1;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.hero-emoji {
  display: inline-block;
  animation: bounce 2s infinite;
  margin-right: 15px;
}

.hero-subtitle {
  position: relative;
  z-index: 1;
  opacity: 0.95;
  font-size: 1.3rem;
}

/* Hero Buttons */
.btn-hero-primary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  transition: var(--transition);
  padding: 12px 30px;
  border-radius: 50px;
  font-weight: 600;
}

.btn-hero-primary:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  color: white;
}

.btn-hero-secondary {
  background: transparent;
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
  transition: var(--transition);
  padding: 12px 30px;
  border-radius: 50px;
  font-weight: 600;
}

.btn-hero-secondary:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: white;
  transform: translateY(-2px);
  color: white;
}

.btn-icon {
  margin-right: 8px;
}

/* Features Section */
.features-section {
  margin: 60px 0;
}

.feature-card {
  background: var(--light-card-bg);
  border: 1px solid var(--light-border);
  border-radius: 16px;
  transition: var(--transition);
  box-shadow: var(--shadow-light);
  position: relative;
  overflow: hidden;
}

.dark-mode .feature-card {
  background: var(--dark-card-bg);
  border-color: var(--dark-border);
  box-shadow: var(--shadow-dark);
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.dark-mode .feature-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
  display: block;
}

.feature-highlight {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #007bff, #0056b3);
  transform: scaleX(0);
  transition: var(--transition);
}

.feature-card:hover .feature-highlight {
  transform: scaleX(1);
}

/* Parking Lots Section */
.parking-lots-section {
  margin-top: 60px;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-title {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.section-icon {
  font-size: 2.5rem;
}

.section-divider {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #007bff, #0056b3);
  margin: 0 auto;
  border-radius: 2px;
}

.parking-lot-card {
  background: var(--light-card-bg);
  border: 1px solid var(--light-border);
  border-radius: 16px;
  transition: var(--transition);
  box-shadow: var(--shadow-light);
  height: 100%;
}

.dark-mode .parking-lot-card {
  background: var(--dark-card-bg);
  border-color: var(--dark-border);
  box-shadow: var(--shadow-dark);
}

.parking-lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.15);
}

.dark-mode .parking-lot-card:hover {
  box-shadow: 0 15px 20px -5px rgba(0, 0, 0, 0.4);
}

.lot-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.lot-title {
  font-weight: 700;
  margin: 0;
  color: var(--light-text);
}

.dark-mode .lot-title {
  color: var(--dark-text);
}

.lot-price {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.lot-address {
  color: #6c757d;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dark-mode .lot-address {
  color: #8b949e;
}

.address-icon {
  font-size: 1.1rem;
}

.lot-stats {
  display: flex;
  gap: 15px;
}

.stat-item {
  flex: 1;
  padding: 12px;
  border-radius: 12px;
  text-align: center;
  transition: var(--transition);
}

.stat-item.available {
  background: rgba(40, 167, 69, 0.1);
  border: 1px solid rgba(40, 167, 69, 0.2);
}

.stat-item.occupied {
  background: rgba(220, 53, 69, 0.1);
  border: 1px solid rgba(220, 53, 69, 0.2);
}

.dark-mode .stat-item.available {
  background: rgba(40, 167, 69, 0.2);
  border-color: rgba(40, 167, 69, 0.3);
}

.dark-mode .stat-item.occupied {
  background: rgba(220, 53, 69, 0.2);
  border-color: rgba(220, 53, 69, 0.3);
}

.stat-icon {
  display: block;
  font-size: 1.2rem;
  margin-bottom: 5px;
}

.stat-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 2px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
}

/* Animations */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .home {
    padding: 10px;
  }
  
  .theme-toggle-container {
    top: 10px;
    right: 10px;
  }
  
  .theme-toggle-btn {
    width: 50px;
    height: 50px;
  }
  
  .theme-icon {
    font-size: 20px;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .lot-stats {
    flex-direction: column;
    gap: 10px;
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Focus styles for accessibility */
.theme-toggle-btn:focus,
.btn-hero-primary:focus,
.btn-hero-secondary:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}
</style>