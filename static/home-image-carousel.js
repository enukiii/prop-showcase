(() => {
    const carousel = document.querySelector('[data-home-carousel]');
    if (!carousel) return;

    const slides = [...carousel.querySelectorAll('[data-home-slide]')];
    const dots = [...carousel.querySelectorAll('[data-home-dot]')];
    const previous = carousel.querySelector('[data-home-prev]');
    const next = carousel.querySelector('[data-home-next]');
    if (slides.length < 2) return;

    let currentIndex = Math.max(0, slides.findIndex(slide => slide.classList.contains('is-active')));
    let timer;
    let hovered = false;
    let focused = false;
    let touchStartX = null;

    const stop = () => window.clearInterval(timer);
    const start = () => {
        stop();
        if (!hovered && !focused && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            timer = window.setInterval(() => show(currentIndex + 1), 4000);
        }
    };

    const show = index => {
        currentIndex = (index + slides.length) % slides.length;
        slides.forEach((slide, i) => {
            const active = i === currentIndex;
            slide.classList.toggle('is-active', active);
            slide.setAttribute('aria-hidden', String(!active));
            slide.tabIndex = active ? 0 : -1;
        });
        dots.forEach((dot, i) => {
            const active = i === currentIndex;
            dot.classList.toggle('is-active', active);
            if (active) dot.setAttribute('aria-current', 'true');
            else dot.removeAttribute('aria-current');
        });
    };

    previous?.addEventListener('click', () => { show(currentIndex - 1); start(); });
    next?.addEventListener('click', () => { show(currentIndex + 1); start(); });
    dots.forEach((dot, i) => dot.addEventListener('click', () => { show(i); start(); }));

    carousel.addEventListener('mouseenter', () => { hovered = true; stop(); });
    carousel.addEventListener('mouseleave', () => { hovered = false; start(); });
    carousel.addEventListener('focusin', () => { focused = true; stop(); });
    carousel.addEventListener('focusout', event => {
        if (!carousel.contains(event.relatedTarget)) { focused = false; start(); }
    });
    carousel.addEventListener('keydown', event => {
        if (event.key === 'ArrowLeft') { show(currentIndex - 1); start(); }
        if (event.key === 'ArrowRight') { show(currentIndex + 1); start(); }
    });
    carousel.addEventListener('touchstart', event => { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
    carousel.addEventListener('touchend', event => {
        if (touchStartX === null) return;
        const distance = event.changedTouches[0].clientX - touchStartX;
        touchStartX = null;
        if (Math.abs(distance) > 45) { show(currentIndex + (distance < 0 ? 1 : -1)); start(); }
    }, { passive: true });
    document.addEventListener('visibilitychange', start);

    show(currentIndex);
    start();
})();
