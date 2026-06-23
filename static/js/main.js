// Main JavaScript for Employee Training System

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips, popovers, or other components
    initializeComponents();
});

// Initialize UI components
function initializeComponents() {
    // Add any initialization code here
    console.log('Employee Training System loaded');
}

// API Helper Functions
const API = {
    get: async (url) => {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return await response.json();
    },
    
    post: async (url, data) => {
        const response = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return await response.json();
    },
    
    put: async (url, data) => {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return await response.json();
    },
    
    delete: async (url) => {
        const response = await fetch(url, {method: 'DELETE'});
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return await response.json();
    }
};

// Utility Functions
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    document.body.insertBefore(alert, document.body.firstChild);
    setTimeout(() => alert.remove(), 5000);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(datetime) {
    return new Date(datetime).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password && password.length >= 6;
}

// Local Storage Helper
const Storage = {
    set: (key, value) => localStorage.setItem(key, JSON.stringify(value)),
    get: (key) => {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    },
    remove: (key) => localStorage.removeItem(key),
    clear: () => localStorage.clear()
};

// Export function for CSV
function exportToCSV(data, filename) {
    const csv = convertArrayToCSV(data);
    downloadCSV(csv, filename);
}

function convertArrayToCSV(data) {
    if (!data || data.length === 0) return '';
    
    const keys = Object.keys(data[0]);
    let csv = keys.join(',') + '\n';
    
    data.forEach(row => {
        const values = keys.map(key => {
            const value = row[key];
            return typeof value === 'string' ? `"${value}"` : value;
        });
        csv += values.join(',') + '\n';
    });
    
    return csv;
}

function downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
}

// Notification System
class Notification {
    static success(message) {
        showAlert(message, 'success');
    }
    
    static error(message) {
        showAlert(message, 'error');
    }
    
    static info(message) {
        showAlert(message, 'info');
    }
}

// Page-specific initialization
if (document.body.classList.contains('login-page')) {
    // Login page scripts
}

if (document.body.classList.contains('dashboard')) {
    // Dashboard scripts
}

// Export for use in other scripts
window.API = API;
window.Storage = Storage;
window.Notification = Notification;
