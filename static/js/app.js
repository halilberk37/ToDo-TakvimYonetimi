// TodoCalendar Frontend Application - Simplified Version

class TodoCalendarApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.authToken = localStorage.getItem('authToken');
        this.currentUser = null;
        this.todos = [];
        this.events = [];
        
        console.log('TodoCalendarApp constructor called');
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    init() {
        console.log('TodoCalendarApp init called');
        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // Login Form
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }

        // Register Form
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister();
            });
        }

        // Add Todo Form
        const addTodoForm = document.getElementById('addTodoForm');
        if (addTodoForm) {
            addTodoForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAddTodo();
            });
        }

        // Add Event Form
        const addEventForm = document.getElementById('addEventForm');
        if (addEventForm) {
            addEventForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleAddEvent();
            });
        }
    }

    async checkAuthStatus() {
        if (this.authToken) {
            try {
                const response = await this.apiCall('/auth/profile/', 'GET');
                if (response.ok) {
                    this.currentUser = await response.json();
                    this.showDashboard();
                    this.loadData();
                } else {
                    this.logout();
                }
            } catch (error) {
                console.error('Auth check failed:', error);
                this.logout();
            }
        } else {
            this.showAuthButtons();
        }
    }

    async loadData() {
        await Promise.all([
            this.loadTodos(),
            this.loadEvents()
        ]);
        this.updateStatistics();
    }

    async handleLogin() {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (!email || !password) {
            this.showAlert('E-posta ve şifre alanları zorunludur!', 'danger');
            return;
        }

        try {
            const response = await this.apiCall('/auth/login/', 'POST', {
                email: email,
                password: password
            });

            if (response.ok) {
                const data = await response.json();
                this.authToken = data.access;
                localStorage.setItem('authToken', this.authToken);
                this.currentUser = data.user;
                
                this.showDashboard();
                this.hideModal('loginModal');
                this.showAlert('Başarıyla giriş yaptınız!', 'success');
                
                // Load data after login
                this.loadData();
                
                // Clear form
                document.getElementById('email').value = '';
                document.getElementById('password').value = '';
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Giriş başarısız!', 'danger');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showAlert('Bir hata oluştu!', 'danger');
        }
    }

    async handleRegister() {
        const formData = {
            email: document.getElementById('regEmail').value,
            username: document.getElementById('regUsername').value,
            first_name: document.getElementById('regFirstName').value,
            last_name: document.getElementById('regLastName').value,
            password: document.getElementById('regPassword').value,
            password_confirm: document.getElementById('regPasswordConfirm').value
        };

        if (formData.password !== formData.password_confirm) {
            this.showAlert('Şifreler eşleşmiyor!', 'danger');
            return;
        }

        try {
            const response = await this.apiCall('/auth/register/', 'POST', formData);

            if (response.ok) {
                const data = await response.json();
                this.authToken = data.access;
                localStorage.setItem('authToken', this.authToken);
                
                this.currentUser = {
                    email: formData.email,
                    first_name: formData.first_name,
                    last_name: formData.last_name
                };
                
                this.showDashboard();
                this.hideModal('registerModal');
                this.showAlert('Başarıyla kayıt oldunuz!', 'success');
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Kayıt başarısız!', 'danger');
            }
        } catch (error) {
            console.error('Register error:', error);
            this.showAlert('Bir hata oluştu!', 'danger');
        }
    }

    async handleAddTodo() {
        const formData = {
            title: document.getElementById('todoTitle').value,
            description: document.getElementById('todoDescription').value,
            priority: document.getElementById('todoPriority').value,
            due_date: document.getElementById('todoDueDate').value,
            is_important: document.getElementById('todoImportant').checked
        };

        try {
            const response = await this.apiCall('/todos/', 'POST', formData);

            if (response.ok) {
                const newTodo = await response.json();
                this.todos.push(newTodo);
                this.renderTodos();
                this.updateStatistics();
                this.hideModal('addTodoModal');
                this.showAlert('Todo başarıyla eklendi!', 'success');
                document.getElementById('addTodoForm').reset();
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Todo eklenemedi!', 'danger');
            }
        } catch (error) {
            console.error('Add todo error:', error);
            this.showAlert('Bir hata oluştu!', 'danger');
        }
    }

    async handleAddEvent() {
        const formData = {
            title: document.getElementById('eventTitle').value,
            description: document.getElementById('eventDescription').value,
            start_time: document.getElementById('eventStartDate').value,
            end_time: document.getElementById('eventEndDate').value,
            location: document.getElementById('eventLocation').value
        };

        try {
            const response = await this.apiCall('/calendar/events/', 'POST', formData);

            if (response.ok) {
                const newEvent = await response.json();
                this.events.push(newEvent);
                this.renderEvents();
                this.updateStatistics();
                this.hideModal('addEventModal');
                this.showAlert('Etkinlik başarıyla eklendi!', 'success');
                document.getElementById('addEventForm').reset();
            } else {
                const error = await response.json();
                this.showAlert(error.detail || 'Etkinlik eklenemedi!', 'danger');
            }
        } catch (error) {
            console.error('Add event error:', error);
            this.showAlert('Bir hata oluştu!', 'danger');
        }
    }

    async loadTodos() {
        try {
            const response = await this.apiCall('/todos/', 'GET');
            if (response.ok) {
                this.todos = await response.json();
                this.renderTodos();
            }
        } catch (error) {
            console.error('Load todos error:', error);
        }
    }

    async loadEvents() {
        try {
            const response = await this.apiCall('/calendar/events/', 'GET');
            if (response.ok) {
                this.events = await response.json();
                this.renderEvents();
            }
        } catch (error) {
            console.error('Load events error:', error);
        }
    }

    renderTodos() {
        const todoList = document.getElementById('todoList');
        if (!todoList) return;
        
        if (this.todos.length === 0) {
            todoList.innerHTML = `
                <div class="text-center text-muted py-3">
                    <i class="fas fa-tasks fa-2x mb-2"></i>
                    <p>Henüz todo eklenmemiş</p>
                </div>
            `;
            return;
        }

        todoList.innerHTML = '';
        this.todos.forEach(todo => {
            const todoElement = this.createTodoElement(todo);
            todoList.appendChild(todoElement);
        });
    }

    renderEvents() {
        const eventsList = document.getElementById('eventsList');
        if (!eventsList) return;
        
        if (this.events.length === 0) {
            eventsList.innerHTML = `
                <div class="text-center text-muted py-3">
                    <i class="fas fa-calendar fa-2x mb-2"></i>
                    <p>Henüz etkinlik eklenmemiş</p>
                </div>
            `;
            return;
        }

        eventsList.innerHTML = '';
        this.events.forEach(event => {
            const eventElement = this.createEventElement(event);
            eventsList.appendChild(eventElement);
        });
    }

    createTodoElement(todo) {
        const div = document.createElement('div');
        div.className = `list-group-item list-group-item-action`;
        
        const priorityClass = {
            'low': 'text-success',
            'medium': 'text-warning',
            'high': 'text-danger'
        }[todo.priority] || 'text-secondary';

        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <div class="d-flex align-items-center mb-1">
                        <input type="checkbox" class="form-check-input me-2" ${todo.is_completed ? 'checked' : ''} 
                               onchange="app.toggleTodo(${todo.id})">
                        <h6 class="mb-0 ${todo.is_completed ? 'text-decoration-line-through text-muted' : ''}">${todo.title}</h6>
                        ${todo.is_important ? '<i class="fas fa-star text-warning ms-2"></i>' : ''}
                    </div>
                    ${todo.description ? `<p class="mb-1 text-muted small">${todo.description}</p>` : ''}
                    <div class="d-flex align-items-center">
                        <span class="badge bg-secondary me-2">${this.getPriorityText(todo.priority)}</span>
                        ${todo.due_date ? `<small class="text-muted"><i class="fas fa-calendar me-1"></i>${this.formatDate(todo.due_date)}</small>` : ''}
                    </div>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="app.deleteTodo(${todo.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return div;
    }

    createEventElement(event) {
        const div = document.createElement('div');
        div.className = 'list-group-item list-group-item-action';
        
        const startDate = new Date(event.start_time);
        const endDate = new Date(event.end_time);

        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
                <div class="flex-grow-1">
                    <h6 class="mb-1">${event.title}</h6>
                    ${event.description ? `<p class="mb-1 text-muted small">${event.description}</p>` : ''}
                    <div class="d-flex align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-calendar me-1"></i>
                            ${this.formatDateTime(startDate)} - ${this.formatDateTime(endDate)}
                        </small>
                        ${event.location ? `<small class="text-muted ms-3"><i class="fas fa-map-marker-alt me-1"></i>${event.location}</small>` : ''}
                    </div>
                </div>
                <button class="btn btn-sm btn-outline-danger" onclick="app.deleteEvent(${event.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;

        return div;
    }

    async toggleTodo(todoId) {
        try {
            const todo = this.todos.find(t => t.id === todoId);
            const response = await this.apiCall(`/todos/${todoId}/toggle/`, 'POST');

            if (response.ok) {
                todo.is_completed = !todo.is_completed;
                this.renderTodos();
                this.updateStatistics();
            }
        } catch (error) {
            console.error('Toggle todo error:', error);
        }
    }

    async deleteTodo(todoId) {
        if (confirm('Bu todo\'yu silmek istediğinizden emin misiniz?')) {
            try {
                const response = await this.apiCall(`/todos/${todoId}/`, 'DELETE');

                if (response.ok) {
                    this.todos = this.todos.filter(t => t.id !== todoId);
                    this.renderTodos();
                    this.updateStatistics();
                    this.showAlert('Todo silindi!', 'success');
                }
            } catch (error) {
                console.error('Delete todo error:', error);
            }
        }
    }

    async deleteEvent(eventId) {
        if (confirm('Bu etkinliği silmek istediğinizden emin misiniz?')) {
            try {
                const response = await this.apiCall(`/calendar/events/${eventId}/`, 'DELETE');

                if (response.ok) {
                    this.events = this.events.filter(e => e.id !== eventId);
                    this.renderEvents();
                    this.updateStatistics();
                    this.showAlert('Etkinlik silindi!', 'success');
                }
            } catch (error) {
                console.error('Delete event error:', error);
            }
        }
    }

    updateStatistics() {
        const totalTodos = this.todos.length;
        const completedTodos = this.todos.filter(t => t.is_completed).length;
        const pendingTodos = totalTodos - completedTodos;
        const totalEvents = this.events.length;

        document.getElementById('totalTodos').textContent = totalTodos;
        document.getElementById('completedTodos').textContent = completedTodos;
        document.getElementById('pendingTodos').textContent = pendingTodos;
        document.getElementById('totalEvents').textContent = totalEvents;
    }

    async apiCall(endpoint, method = 'GET', data = null) {
        const url = this.apiBaseUrl + endpoint;
        
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (this.authToken) {
            options.headers['Authorization'] = `Bearer ${this.authToken}`;
        }

        if (data) {
            options.body = JSON.stringify(data);
        }

        return fetch(url, options);
    }

    showDashboard() {
        const authButtons = document.getElementById('authButtons');
        const dashboard = document.getElementById('dashboard');
        const userName = document.getElementById('userName');
        
        if (authButtons) authButtons.classList.add('d-none');
        if (dashboard) dashboard.classList.remove('d-none');
        if (userName && this.currentUser) {
            userName.textContent = `${this.currentUser.first_name} ${this.currentUser.last_name}`;
        }
    }

    showAuthButtons() {
        const authButtons = document.getElementById('authButtons');
        const dashboard = document.getElementById('dashboard');
        
        if (authButtons) authButtons.classList.remove('d-none');
        if (dashboard) dashboard.classList.add('d-none');
    }

    showModal(modalId) {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }

    hideModal(modalId) {
        const modalElement = document.getElementById(modalId);
        if (modalElement) {
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) {
                modal.hide();
            }
        }
    }

    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }

    logout() {
        this.authToken = null;
        this.currentUser = null;
        localStorage.removeItem('authToken');
        this.showAuthButtons();
        this.showAlert('Başarıyla çıkış yaptınız!', 'info');
    }

    getPriorityText(priority) {
        const priorities = {
            'low': 'Düşük',
            'medium': 'Orta',
            'high': 'Yüksek'
        };
        return priorities[priority] || priority;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('tr-TR');
    }

    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('tr-TR');
    }
}

// Global functions
function showLogin() {
    if (window.app) {
        window.app.showModal('loginModal');
    }
}

function showRegister() {
    if (window.app) {
        window.app.showModal('registerModal');
    }
}

function showAddTodoModal() {
    if (window.app) {
        document.getElementById('addTodoForm').reset();
        window.app.showModal('addTodoModal');
    }
}

function showAddEventModal() {
    if (window.app) {
        document.getElementById('addEventForm').reset();
        window.app.showModal('addEventModal');
    }
}

function logout() {
    if (window.app) {
        window.app.logout();
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TodoCalendarApp();
});