// API Configuration
// Для локальной разработки используем localhost
// Для production используем переменную окружения или задайте свой URL
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000/api'
    : 'https://your-backend-url.onrender.com/api'; // ЗАМЕНИТЕ НА ВАШ URL БЭКЕНДА!

// API Client
class APIClient {
    constructor() {
        this.token = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
    }

    // Headers
    getHeaders(includeAuth = true) {
        const headers = {
            'Content-Type': 'application/json',
        };
        if (includeAuth && this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // Request wrapper
    async request(url, options = {}) {
        const config = {
            ...options,
            headers: this.getHeaders(options.auth !== false),
        };

        try {
            const response = await fetch(`${API_BASE_URL}${url}`, config);
            
            // Handle 401 Unauthorized
            if (response.status === 401) {
                this.logout();
                throw new Error('Необходима авторизация');
            }

            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                throw new Error(data.message || data.detail || 'Ошибка запроса');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Authentication
    async register(username, password, passwordConfirm, email = '', firstName = '', lastName = '') {
        const data = await this.request('/auth/register/', {
            method: 'POST',
            auth: false,
            body: JSON.stringify({
                username,
                password,
                password_confirm: passwordConfirm,
                email,
                first_name: firstName,
                last_name: lastName,
            }),
        });
        return data;
    }

    async login(username, password) {
        const data = await this.request('/auth/login/', {
            method: 'POST',
            auth: false,
            body: JSON.stringify({ username, password }),
        });

        if (data.access_token) {
            this.token = data.access_token;
            this.refreshToken = data.refresh_token;
            this.user = data.user;
            
            localStorage.setItem('access_token', this.token);
            localStorage.setItem('refresh_token', this.refreshToken);
            localStorage.setItem('user', JSON.stringify(this.user));
        }

        return data;
    }

    async logout() {
        try {
            await this.request('/auth/logout/', { method: 'POST' });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            this.token = null;
            this.refreshToken = null;
            this.user = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
        }
    }

    async getCurrentUser() {
        const data = await this.request('/auth/me/');
        this.user = data;
        localStorage.setItem('user', JSON.stringify(this.user));
        return data;
    }

    isAuthenticated() {
        return !!this.token && !!this.user;
    }

    isSuperAdmin() {
        return this.user && this.user.is_super_admin;
    }

    // Users (Admin only)
    async getUsers(status = null) {
        const url = status ? `/users/?status=${status}` : '/users/';
        return await this.request(url);
    }

    async getUser(id) {
        return await this.request(`/users/${id}/`);
    }

    async updateUser(id, data) {
        return await this.request(`/users/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteUser(id) {
        return await this.request(`/users/${id}/`, { method: 'DELETE' });
    }

    async approveUser(id) {
        return await this.request(`/users/${id}/approve/`, { method: 'POST' });
    }

    async suspendUser(id) {
        return await this.request(`/users/${id}/suspend/`, { method: 'POST' });
    }

    async unsuspendUser(id) {
        return await this.request(`/users/${id}/unsuspend/`, { method: 'POST' });
    }

    async setAccessPeriod(id, accessUntil) {
        return await this.request(`/users/${id}/set_access_period/`, {
            method: 'POST',
            body: JSON.stringify({ access_until: accessUntil }),
        });
    }

    // Admin Stats
    async getAdminStats() {
        return await this.request('/admin/stats/');
    }

    // Rooms
    async getRooms() {
        return await this.request('/rooms/');
    }

    async createRoom(data) {
        return await this.request('/rooms/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateRoom(id, data) {
        return await this.request(`/rooms/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteRoom(id) {
        return await this.request(`/rooms/${id}/`, { method: 'DELETE' });
    }

    // Beds
    async getBeds(roomId = null) {
        const url = roomId ? `/beds/?room=${roomId}` : '/beds/';
        return await this.request(url);
    }

    async createBed(data) {
        return await this.request('/beds/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateBed(id, data) {
        return await this.request(`/beds/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteBed(id) {
        return await this.request(`/beds/${id}/`, { method: 'DELETE' });
    }

    // Residents
    async getResidents(roomId = null, currentOnly = false) {
        let url = '/residents/';
        const params = [];
        if (roomId) params.push(`room=${roomId}`);
        if (currentOnly) params.push('current=true');
        if (params.length > 0) url += '?' + params.join('&');
        return await this.request(url);
    }

    async createResident(data) {
        return await this.request('/residents/', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    }

    async updateResident(id, data) {
        return await this.request(`/residents/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    }

    async deleteResident(id) {
        return await this.request(`/residents/${id}/`, { method: 'DELETE' });
    }

    // Audit Logs (Admin only)
    async getAuditLogs(userId = null, action = null) {
        let url = '/audit-logs/';
        const params = [];
        if (userId) params.push(`user=${userId}`);
        if (action) params.push(`action=${action}`);
        if (params.length > 0) url += '?' + params.join('&');
        return await this.request(url);
    }
}

// Create global instance
const apiClient = new APIClient();
