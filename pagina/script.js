// Variables globales
let isLoggedIn = false;
let currentUser = null;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    console.log('Iniciando aplicación...');
    
    // Inicializar componentes
    initNavigation();
    initFAQ();
    initAuth();
    checkUserSession();
    initGallery();
    
    console.log('Aplicación iniciada');
});

// Verificar sesión del usuario
async function checkUserSession() {
    try {
        const response = await fetch('conexion.php');
        const data = await response.json();
        
        if (data.logged_in) {
            isLoggedIn = true;
            currentUser = data.username;
            showUserInfo(data.username);
        } else {
            isLoggedIn = false;
            currentUser = null;
            showAuthButtons();
        }
    } catch (error) {
        console.error('Error checking session:', error);
        showAuthButtons();
    }
}

// Mostrar información del usuario
function showUserInfo(username) {
    const authButtons = document.getElementById('auth-buttons');
    const userInfo = document.getElementById('user-info');
    const usernameDisplay = document.getElementById('username-display');
    
    if (authButtons) authButtons.style.display = 'none';
    if (userInfo) userInfo.style.display = 'flex';
    if (usernameDisplay) usernameDisplay.textContent = `¡Hola, ${username}!`;
    
    // Mostrar sección de usuario en sugerencias
    const authRequired = document.getElementById('authRequired');
    const userLogged = document.getElementById('userLogged');
    
    if (authRequired) authRequired.style.display = 'none';
    if (userLogged) userLogged.style.display = 'block';
}

// Mostrar botones de autenticación
function showAuthButtons() {
    const authButtons = document.getElementById('auth-buttons');
    const userInfo = document.getElementById('user-info');
    
    if (authButtons) authButtons.style.display = 'flex';
    if (userInfo) userInfo.style.display = 'none';
    
    // Mostrar sección de autenticación en sugerencias
    const authRequired = document.getElementById('authRequired');
    const userLogged = document.getElementById('userLogged');
    
    if (authRequired) authRequired.style.display = 'block';
    if (userLogged) userLogged.style.display = 'none';
}

// Inicializar autenticación
function initAuth() {
    console.log('Inicializando autenticación');
    
    // Botones de registro
    const registerBtn = document.getElementById('register-btn');
    const showRegisterBtn = document.getElementById('show-register-btn');
    
    if (registerBtn) {
        console.log('Configurando botón header');
        registerBtn.onclick = function(e) {
            e.preventDefault();
            console.log('Click en registrarse (header)');
            showAuthModal('register');
        };
    }
    
    if (showRegisterBtn) {
        console.log('Configurando botón sugerencias');
        showRegisterBtn.onclick = function(e) {
            e.preventDefault();
            console.log('Click en registrarse (sugerencias)');
            showAuthModal('register');
        };
    }
    
    // Configurar dropdown y otros botones
    initDropdown();
    initSuggestionForm();
    initStars();
}

// Mostrar modal de autenticación
function showAuthModal(type) {
    console.log('Abriendo modal:', type);
    
    const modal = document.getElementById('modal');
    const modalTitle = document.getElementById('modal-title');
    const modalBody = document.getElementById('modal-body');
    
    if (!modal) {
        console.error('Modal no encontrado');
        return;
    }
    
    const isRegister = type === 'register';
    modalTitle.textContent = isRegister ? 'Registrarse' : 'Iniciar Sesión';
    
    modalBody.innerHTML = `
        <form id="auth-form">
            <div class="form-group">
                <label for="username">Usuario:</label>
                <input type="text" id="username" name="username" required>
            </div>
            ${isRegister ? `
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            ` : ''}
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">
                ${isRegister ? 'Registrarse' : 'Iniciar Sesión'}
            </button>
        </form>
        <p class="auth-switch">
            ${isRegister 
                ? '¿Ya tienes cuenta? <a href="#" onclick="showAuthModal(\'login\')">Inicia sesión aquí</a>'
                : '¿No tienes cuenta? <a href="#" onclick="showAuthModal(\'register\')">Regístrate aquí</a>'
            }
        </p>
    `;
    
    modal.style.display = 'block';
    
    // Configurar formulario
    const authForm = document.getElementById('auth-form');
    authForm.onsubmit = async function(e) {
        e.preventDefault();
        console.log('Enviando formulario');
        
        // Obtener datos del formulario
        const formData = new FormData(e.target);
        const data = {};
        
        // Convertir FormData a objeto
        for (let [key, value] of formData.entries()) {
            data[key] = value.trim();
        }
        
        console.log('Datos del formulario:', data);
        
        // Validar campos en el frontend
        if (!data.username || !data.password) {
            alert('Por favor, completa todos los campos requeridos');
            return;
        }
        
        if (isRegister && !data.email) {
            alert('Por favor, ingresa un email válido');
            return;
        }
        
        if (isRegister && data.password.length < 6) {
            alert('La contraseña debe tener al menos 6 caracteres');
            return;
        }
        
        console.log('Datos a enviar:', data);
        
        const endpoint = isRegister ? 'registrar.php' : 'iniciar_sesion.php';
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                alert(result.message);
                closeModal();
                showUserInfo(result.username);
            } else {
                alert(result.error || 'Error en la autenticación');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión');
        }
    };
}

// Cerrar modal
function closeModal() {
    const modal = document.getElementById('modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Inicializar dropdown
function initDropdown() {
    const dropdownBtn = document.getElementById('dropdown-btn');
    const dropdownMenu = document.querySelector('.dropdown-menu');
    
    if (dropdownBtn && dropdownMenu) {
        dropdownBtn.onclick = function(e) {
            e.stopPropagation();
            dropdownMenu.classList.toggle('show');
        };
        
        document.onclick = function() {
            dropdownMenu.classList.remove('show');
        };
    }
    
    // Botones de gestión de cuenta
    const deleteBtn = document.getElementById('delete-btn');
    const logoutBtn = document.getElementById('logout-btn');
    
    if (deleteBtn) deleteBtn.onclick = deleteAccount;
    if (logoutBtn) logoutBtn.onclick = logout;
    if (logoutBtn) logoutBtn.onclick = logout;
}

// Cerrar sesión
async function logout() {
    try {
        await fetch('conexion.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: 'action=logout'
        });
        
        showAuthButtons();
        alert('Sesión cerrada exitosamente');
    } catch (error) {
        console.error('Error:', error);
        showAuthButtons();
    }
}

// Eliminar cuenta
async function deleteAccount() {
    if (confirm('¿Estás seguro de que quieres ELIMINAR PERMANENTEMENTE tu cuenta? Esta acción no se puede deshacer.')) {
        if (confirm('¡ATENCIÓN! Esto eliminará tu cuenta y todos tus datos para siempre. ¿Continuar?')) {
            try {
                const response = await fetch('eliminar.php', { method: 'POST' });
                const data = await response.json();
                
                if (data.success) {
                    alert(data.message);
                    showAuthButtons();
                } else {
                    alert(data.error || 'Error al eliminar cuenta');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al eliminar cuenta');
            }
        }
    }
}

// Inicializar formulario de sugerencias
function initSuggestionForm() {
    const suggestionForm = document.getElementById('suggestionForm');
    if (suggestionForm) {
        suggestionForm.onsubmit = async function(e) {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            formData.append('action', 'enviar');
            
            try {
                const response = await fetch('sugerencias.php', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    alert('¡Sugerencia enviada exitosamente! Gracias por tu feedback.');
                    e.target.reset();
                    initStars(); // Resetear estrellas
                } else {
                    alert(data.error || 'Error al enviar la sugerencia');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error de conexión');
            }
        };
    }
}

// Inicializar funciones de sugerencias
function initStars() {
    // Contador de caracteres
    const textarea = document.getElementById('suggestion-text');
    const charCount = document.getElementById('charCount');
    
    if (textarea && charCount) {
        textarea.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count;
            
            if (count > 450) {
                charCount.style.color = '#ff6b6b';
            } else if (count > 400) {
                charCount.style.color = '#ffa726';
            } else {
                charCount.style.color = 'var(--color-text-muted)';
            }
        });
    }
}

// Inicializar navegación
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.onclick = function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        };
        
        // Cerrar menú al hacer clic en un enlace
        document.querySelectorAll('.nav-link').forEach(link => {
            link.onclick = function() {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            };
        });
    }
}

// Inicializar FAQ
function initFAQ() {
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        if (question) {
            question.onclick = function() {
                const isActive = item.classList.contains('active');
                
                // Cerrar todos los FAQs
                faqItems.forEach(faq => faq.classList.remove('active'));
                
                // Abrir el clickeado si no estaba activo
                if (!isActive) {
                    item.classList.add('active');
                }
            };
        }
    });
}

// Variables para el carrusel
let currentSlideIndex = 0;
let autoSlideInterval;
const autoSlideDelay = 4000; // 4 segundos

// Inicializar galería
function initGallery() {
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        console.log('Inicializando carrusel automático');
        
        // Iniciar carrusel automático
        startAutoSlide();
        
        // Pausar cuando el mouse está sobre el carrusel
        carouselContainer.addEventListener('mouseenter', stopAutoSlide);
        carouselContainer.addEventListener('mouseleave', startAutoSlide);
    }
}

// Iniciar carrusel automático
function startAutoSlide() {
    stopAutoSlide(); // Limpiar cualquier intervalo existente
    autoSlideInterval = setInterval(() => {
        changeSlide(1);
    }, autoSlideDelay);
}

// Detener carrusel automático
function stopAutoSlide() {
    if (autoSlideInterval) {
        clearInterval(autoSlideInterval);
        autoSlideInterval = null;
    }
}

// Cambiar slide
function changeSlide(direction) {
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    const carousel = document.getElementById('gameCarousel');
    
    if (!slides.length) return;
    
    // Remover clase active del slide actual
    slides[currentSlideIndex].classList.remove('active');
    indicators[currentSlideIndex].classList.remove('active');
    
    // Calcular nuevo índice
    currentSlideIndex += direction;
    
    // Manejar loop infinito
    if (currentSlideIndex >= slides.length) {
        currentSlideIndex = 0;
    } else if (currentSlideIndex < 0) {
        currentSlideIndex = slides.length - 1;
    }
    
    // Aplicar transformación
    const translateX = -currentSlideIndex * 100;
    carousel.style.transform = `translateX(${translateX}%)`;
    
    // Agregar clase active al nuevo slide
    slides[currentSlideIndex].classList.add('active');
    indicators[currentSlideIndex].classList.add('active');
    
    console.log('Slide cambiado a:', currentSlideIndex);
}

// Ir a slide específico
function currentSlide(slideIndex) {
    const direction = slideIndex - 1 - currentSlideIndex;
    changeSlide(direction);
    
    // Reiniciar temporizador automático
    startAutoSlide();
}

console.log('Script cargado correctamente');