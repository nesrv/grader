document.addEventListener('DOMContentLoaded', function() {
    // Анимация появления элементов при скролле
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.language-card, .feature-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                element.classList.add('animate');
            }
        });
    };
    
    // Добавляем класс для анимации при скролле
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Запускаем один раз при загрузке страницы
    
    // Мобильное меню
    const createMobileMenu = () => {
        const header = document.querySelector('.header');
        
        // Создаем кнопку мобильного меню
        const mobileMenuBtn = document.createElement('button');
        mobileMenuBtn.classList.add('mobile-menu-btn');
        mobileMenuBtn.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        
        // Добавляем кнопку в шапку для мобильных устройств
        if (window.innerWidth <= 992) {
            header.querySelector('.header__container').appendChild(mobileMenuBtn);
            
            // Обработчик клика по кнопке мобильного меню
            mobileMenuBtn.addEventListener('click', function() {
                this.classList.toggle('active');
                document.querySelector('.header__nav').classList.toggle('active');
                document.querySelector('.header__auth').classList.toggle('active');
            });
        }
    };
    
    // Вызываем функцию создания мобильного меню
    createMobileMenu();
    
    // Обработка изменения размера окна
    window.addEventListener('resize', function() {
        const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
        
        if (window.innerWidth <= 992) {
            if (!mobileMenuBtn) {
                createMobileMenu();
            }
        } else {
            if (mobileMenuBtn) {
                mobileMenuBtn.remove();
                document.querySelector('.header__nav').classList.remove('active');
                document.querySelector('.header__auth').classList.remove('active');
            }
        }
    });
    
    // Имитация выбора языка
    const languageCards = document.querySelectorAll('.language-card');
    
    languageCards.forEach(card => {
        card.addEventListener('click', function() {
            // Здесь можно добавить логику выбора языка
            const languageName = this.querySelector('.language-card__name').textContent;
            alert(`Вы выбрали ${languageName}! Скоро начнем обучение.`);
        });
    });
    
    // Плавный скролл для навигации
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Здесь можно добавить логику для плавного скролла к разделам
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            
            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
});