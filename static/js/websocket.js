// ─── Khalvian Tech Hub WebSocket Client ───────────────────

// ─── Notification WebSocket ───────────────────────────────
class NotificationSocket {
    constructor() {
        this.socket = null;
        this.reconnectDelay = 3000;
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const url = `${protocol}//${window.location.host}/ws/notifications/`;

        this.socket = new WebSocket(url);

        this.socket.onopen = () => {
            console.log('Notification socket connected');
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = () => {
            console.log('Notification socket disconnected. Reconnecting...');
            setTimeout(() => this.connect(), this.reconnectDelay);
        };

        this.socket.onerror = (error) => {
            console.error('Notification socket error:', error);
        };
    }

    handleMessage(data) {
        if (data.type === 'connection') {
            this.updateBadge(data.unread_count);
        } else if (data.type === 'new_notification') {
            this.showToast(data.message, data.notification_type);
            this.incrementBadge();
        } else if (data.type === 'marked_read') {
            this.updateBadge(0);
        }
    }

    updateBadge(count) {
        const badge = document.getElementById('notification-badge');
        if (badge) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'inline' : 'none';
        }
    }

    incrementBadge() {
        const badge = document.getElementById('notification-badge');
        if (badge) {
            const current = parseInt(badge.textContent) || 0;
            badge.textContent = current + 1;
            badge.style.display = 'inline';
        }
    }

    showToast(message, type) {
        const toastContainer = document.getElementById('toast-container');
        if (!toastContainer) return;

        const bgClass = {
            'success': 'bg-success',
            'warning': 'bg-warning',
            'error': 'bg-danger',
            'info': 'bg-primary'
        }[type] || 'bg-primary';

        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white ${bgClass} border-0 show`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" 
                        data-bs-dismiss="toast"></button>
            </div>
        `;
        toastContainer.appendChild(toast);

        setTimeout(() => toast.remove(), 5000);
    }

    markAllRead() {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ action: 'mark_read' }));
        }
    }
}


// ─── Device WebSocket ─────────────────────────────────────
class DeviceSocket {
    constructor(deviceId) {
        this.deviceId = deviceId;
        this.socket = null;
        this.reconnectDelay = 3000;
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const url = `${protocol}//${window.location.host}/ws/devices/${this.deviceId}/`;

        this.socket = new WebSocket(url);

        this.socket.onopen = () => {
            console.log(`Device socket connected: ${this.deviceId}`);
            this.updateStatusIndicator('connecting');
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = () => {
            console.log('Device socket disconnected. Reconnecting...');
            this.updateStatusIndicator('offline');
            setTimeout(() => this.connect(), this.reconnectDelay);
        };

        this.socket.onerror = (error) => {
            console.error('Device socket error:', error);
        };
    }

    handleMessage(data) {
        if (data.type === 'status_update') {
            this.updateStatusIndicator(data.status);
            this.updateLastSeen(data.timestamp);
        }
    }

    updateStatusIndicator(status) {
        const indicator = document.getElementById('device-status');
        if (!indicator) return;

        const classes = {
            'online': 'badge bg-success',
            'offline': 'badge bg-danger',
            'idle': 'badge bg-warning',
            'connecting': 'badge bg-secondary'
        };

        indicator.className = classes[status] || 'badge bg-secondary';
        indicator.textContent = status.charAt(0).toUpperCase() + status.slice(1);
    }

    updateLastSeen(timestamp) {
        const el = document.getElementById('device-last-seen');
        if (el) {
            el.textContent = new Date(timestamp).toLocaleString();
        }
    }

    sendStatus(status) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({ status: status }));
        }
    }
}


// ─── Initialize on page load ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    // Start notification socket if user is logged in
    const isAuthenticated = document.body.dataset.authenticated === 'true';
    if (isAuthenticated) {
        window.notificationSocket = new NotificationSocket();
    }

    // Start device socket if on device detail page
    const deviceId = document.body.dataset.deviceId;
    if (deviceId) {
        window.deviceSocket = new DeviceSocket(deviceId);
    }
});