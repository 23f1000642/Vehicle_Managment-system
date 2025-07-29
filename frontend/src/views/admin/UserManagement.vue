<template>
  <div class="user-management">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h2>👥 User Management</h2>
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            <li class="breadcrumb-item">
              <router-link to="/admin" class="text-decoration-none">Admin Dashboard</router-link>
            </li>
            <li class="breadcrumb-item active">User Management</li>
          </ol>
        </nav>
      </div>
    </div>

    <!-- User Statistics -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5 class="card-title">Total Users</h5>
            <h3>{{ allUsers.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5 class="card-title">Regular Users</h5>
            <h3>{{ regularUsers.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5 class="card-title">Admin Users</h5>
            <h3>{{ adminUsers.length }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5 class="card-title">New This Month</h5>
            <h3>{{ newUsersThisMonth }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Users List -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">Registered Users</h5>
        <div class="d-flex gap-2">
          <input 
            type="text" 
            class="form-control form-control-sm" 
            placeholder="🔍 Search users..."
            v-model="searchQuery"
            style="width: 250px;"
          >
          <select class="form-select form-select-sm" v-model="roleFilter" style="width: 120px;">
            <option value="">All Roles</option>
            <option value="admin">Admin</option>
            <option value="user">User</option>
          </select>
        </div>
      </div>
      <div class="card-body">
        <div v-if="filteredUsers.length === 0 && !searchQuery && !roleFilter" class="text-center py-4">
          <p class="text-muted">No users found.</p>
        </div>

        <div v-else-if="filteredUsers.length === 0 && (searchQuery || roleFilter)" class="text-center py-4">
          <p class="text-muted">
            No users match your search criteria
            <span v-if="searchQuery">"{{ searchQuery }}"</span>
            <span v-if="roleFilter">for role "{{ roleFilter }}"</span>
          </p>
          <button class="btn btn-outline-secondary btn-sm" @click="clearFilters">
            Clear Filters
          </button>
        </div>
        
        <div v-else class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Created Date</th>
                <th>Last Login</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span 
                    :class="user.role === 'admin' ? 'badge bg-warning' : 'badge bg-primary'"
                  >
                    {{ user.role }}
                  </span>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>{{ user.last_login ? formatDate(user.last_login) : 'Never' }}</td>
                <td>
                  <span class="badge bg-success">Active</span>
                </td>
              </tr>
            </tbody>
          </table>

          <!-- Search Results Summary -->
          <div v-if="searchQuery || roleFilter" class="mt-3 text-muted">
            <small>
              Showing {{ filteredUsers.length }} of {{ allUsers.length }} users
              <span v-if="searchQuery">matching "{{ searchQuery }}"</span>
              <span v-if="roleFilter">with role "{{ roleFilter }}"</span>
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

export default {
  name: 'UserManagement',
  setup() {
    const store = useStore()

    // Search and filter states
    const searchQuery = ref('')
    const roleFilter = ref('')

    const allUsers = computed(() => store.state.allUsers)
    
    // Filtered users based on search and role filter
    const filteredUsers = computed(() => {
      let filtered = allUsers.value

      // Search filter
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(user =>
          user.username.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        )
      }

      // Role filter
      if (roleFilter.value) {
        filtered = filtered.filter(user => user.role === roleFilter.value)
      }

      return filtered
    })
    
    const regularUsers = computed(() => 
      allUsers.value.filter(user => user.role === 'user')
    )
    
    const adminUsers = computed(() => 
      allUsers.value.filter(user => user.role === 'admin')
    )

    const newUsersThisMonth = computed(() => {
      const thisMonth = new Date().getMonth()
      const thisYear = new Date().getFullYear()
      return allUsers.value.filter(user => {
        const createdDate = new Date(user.created_at)
        return createdDate.getMonth() === thisMonth && createdDate.getFullYear() === thisYear
      }).length
    })

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A'
      return new Date(dateString).toLocaleDateString()
    }

    const clearFilters = () => {
      searchQuery.value = ''
      roleFilter.value = ''
    }

    onMounted(() => {
      store.dispatch('fetchAllUsers')
    })

    return {
      allUsers,
      filteredUsers,
      regularUsers,
      adminUsers,
      newUsersThisMonth,
      searchQuery,
      roleFilter,
      formatDate,
      clearFilters
    }
  }
}
</script>

<style scoped>
.user-management {
  max-width: 1200px;
  margin: 0 auto;
}

.card {
  margin-bottom: 1rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.table th {
  border-top: none;
  font-weight: 600;
}
</style>