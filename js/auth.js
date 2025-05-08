// Константы для API
const API_URL = 'http://localhost:8000/api/v1';
const AUTH_ENDPOINT = `${API_URL}/auth`;

// DOM элементы
const loginBtn = document.getElementById('loginBtn');
const registerBtn = document.getElementById('registerBtn');
const startBtn = document.getElementById('startBtn');
const languageBtns = document.querySelectorAll('.language-btn');

const loginModal = document.getElementById('loginModal');
const registerModal = document.getElementById('registerModal');
const modalCloseButtons = document.querySelectorAll('.modal__close');

const showRegisterModalLink = document.getElementById('showRegisterModal');
const showLoginModalLink = document.getElementById('showLoginModal');

const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

const loginError = document.getElementById('loginError');
const registerError = document.getElementById('registerError');

// Функции для работы с токеном
function saveToken(token) {
    localStorage.setItem('authToken', token);
}

function getToken() {
    return localStorage.getItem('authToken');
}

function removeToken() {
    localStorage.removeItem('authToken');
}

function isLoggedIn() {
    return !!getToken();
}

// Функции для работы с модальными окнами
function openModal(modal) {
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.classList.remove('show');
    document.body.style.overflow = '';
}

function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => closeModal(modal));
}

// API функции
async function registerUser(userData) {
    try {
        const response = await fetch(`${AUTH_ENDPOINT}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка при регистрации');
        }

        return data;
    } catch (error) {
        throw error;
    }
}

async function loginUser(username, password) {
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${AUTH_ENDPOINT}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка при входе');
        }

        return data;
    } catch (error) {
        throw error;
    }
}

async function getUserProfile() {
    try {
        const token = getToken();
        if (!token) throw new Error('Не авторизован');

        const response = await fetch(`${API_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Ошибка при получении профиля');
        }

        return data;
    } catch (error) {
        throw error;
    }
}

// Обработчики событий
loginBtn.addEventListener('click', () => openModal(loginModal));
registerBtn.addEventListener('click', () => openModal(registerModal));
startBtn.addEventListener('click', () => {
    if (isLoggedIn()) {
        window.location.href = '/lessons.html';
    } else {
        openModal(registerModal);
    }
});

languageBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const lang = btn.getAttribute('data-lang');
        if (isLoggedIn()) {
            window.location.href = `/lessons.html?lang=${lang}`;
        } else {
            openModal(registerModal);
        }
    });
});

modalCloseButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        closeAllModals();
    });
});

// Закрытие модального окна при клике вне его
window.addEventListener('click', (event) => {
    if (event.target === loginModal || event.target === registerModal) {
        closeAllModals();
    }
});

// Переключение между модальными окнами
showRegisterModalLink.addEventListener('click', (e) => {
    e.preventDefault();
    closeModal(loginModal);
    openModal(registerModal);
});

showLoginModalLink.addEventListener('click', (e) => {
    e.preventDefault();
    closeModal(registerModal);
    openModal(loginModal);
});

// Обработка формы регистрации
registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('registerEmail').value;
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    
    registerError.textContent = '';
    
    try {
        const userData = { email, username, password };
        const user = await registerUser(userData);
        
        // После успешной регистрации автоматически входим
        const authData = await loginUser(username, password);
        saveToken(authData.access_token);
        
        closeAllModals();
        
        // Обновляем UI для авторизованного пользователя
        updateUIForLoggedInUser();
        
        // Перенаправляем на страницу уроков
        setTimeout(() => {
            window.location.href = '/lessons.html';
        }, 1000);
        
    } catch (error) {
        registerError.textContent = error.message;
    }
});

// Обработка формы входа
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    loginError.textContent = '';
    
    try {
        const authData = await loginUser(username, password);
        saveToken(authData.access_token);
        
        closeAllModals();
        
        // Обновляем UI для авторизованного пользователя
        updateUIForLoggedInUser();
        
        // Перенаправляем на страницу уроков
        setTimeout(() => {
            window.location.href = '/lessons.html';
        }, 1000);
        
    } catch (error) {
        loginError.textContent = error.message;
    }
});

// Функция для обновления UI после авторизации
async function updateUIForLoggedInUser() {
    try {
        const user = await getUserProfile();
        
        // Меняем кнопки в шапке
        const headerAuth = document.querySelector('.header__auth');
        headerAuth.innerHTML = `
            <span class="user-greeting">Привет, ${user.username}!</span>
            <button class="btn btn--primary" id="dashboardBtn">Мой прогресс</button>
            <button class="btn btn--login" id="logoutBtn">Выйти</button>
        `;
        
        // Добавляем обработчик для кнопки выхода
        document.getElementById('logoutBtn').addEventListener('click', () => {
            removeToken();
            window.location.reload();
        });
        
        // Добавляем обработчик для кнопки дашборда
        document.getElementById('dashboardBtn').addEventListener('click', () => {
            window.location.href = '/dashboard.html';
        });
        
    } catch (error) {
        console.error('Ошибка при обновлении UI:', error);
    }
}

// Проверяем авторизацию при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    if (isLoggedIn()) {
        try {
            await updateUIForLoggedInUser();
        } catch (error) {
            // Если токен недействителен, удаляем его
            if (error.message === 'Не авторизован') {
                removeToken();
            }
        }
    }
});