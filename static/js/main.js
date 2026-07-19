// Event Registration System - Client-side Interactive Logic

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Setup close button click event
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissAlert(alert);
            });
        }

        // Auto timeout
        setTimeout(() => {
            dismissAlert(alert);
        }, 5000);
    });

    // Helper to fade/slide out alert
    function dismissAlert(alert) {
        alert.style.transition = 'opacity 0.5s ease, transform 0.5s ease, margin-bottom 0.5s ease, height 0.5s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-15px)';
        
        setTimeout(() => {
            alert.style.height = '0';
            alert.style.padding = '0';
            alert.style.marginBottom = '0';
            alert.style.border = 'none';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 300);
    }

    // 2. Interactivity on Event Cards (Subtle parallax rotation based on cursor)
    const cards = document.querySelectorAll('.event-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x coordinate within card
            const y = e.clientY - rect.top;  // y coordinate within card
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (centerY - y) / 12; // tilt angle
            const rotateY = (x - centerX) / 12; // tilt angle
            
            card.style.transform = `perspective(1000px) translateY(-5px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) translateY(0) rotateX(0deg) rotateY(0deg)';
        });
    });

    // 3. Confirmation modal for registration cancellation
    const cancelForms = document.querySelectorAll('.cancel-registration-form');
    cancelForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const eventTitle = form.getAttribute('data-event-title') || 'this event';
            const confirmed = confirm(`Are you sure you want to cancel your registration for "${eventTitle}"?`);
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });
});
