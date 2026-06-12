/* ============================================================
   Healthy Bites & Refreshers — main.js
   Scroll-reveal animations, auto-dismiss alerts, qty helpers
   ============================================================ */

document.addEventListener('DOMContentLoaded', () => {

    /* ---- Scroll-reveal: fade cards & sections in as they enter view ---- */
    const revealEls = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('visible');
                    io.unobserve(e.target);
                }
            });
        }, { threshold: 0.12 });
        revealEls.forEach(el => io.observe(el));
    } else {
        revealEls.forEach(el => el.classList.add('visible'));
    }

    /* ---- Auto-dismiss flash messages after 4.5s ---- */
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            try { bootstrap.Alert.getOrCreateInstance(alert).close(); } catch (e) {}
        }, 4500);
    });

    /* ---- Quantity +/- buttons on the cart page ---- */
    document.querySelectorAll('[data-qty]').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('form').querySelector('input[name="quantity"]');
            let val = parseInt(input.value || '1', 10);
            val += (btn.dataset.qty === 'up') ? 1 : -1;
            input.value = Math.max(0, val);   // 0 removes the item server-side
            btn.closest('form').submit();
        });
    });

    /* ---- Smooth-scroll for same-page anchor links ---- */
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
});
