import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/',
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle 401 errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token is invalid or expired
            console.log('Session expired or unauthorized, logging out...');

            // Clear local storage
            localStorage.removeItem('token');
            localStorage.removeItem('user');

            // Dispatch custom event to notify AuthContext
            window.dispatchEvent(new CustomEvent('auth:logout', {
                detail: { reason: 'session_expired' }
            }));

            // Redirect to login page
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;
