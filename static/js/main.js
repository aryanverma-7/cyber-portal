// CyberShield - Main JavaScript

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeAnimations();
    initializeCharts();
    initializeForms();
});

// Animation initialization
function initializeAnimations() {
    // Add cyber glow effect to cards
    const cards = document.querySelectorAll('.cyber-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.animation = 'cyberGlow 1s ease-in-out';
        });
        card.addEventListener('mouseleave', function() {
            this.style.animation = '';
        });
    });
}

// Chart initialization
function initializeCharts() {
    // Initialize any charts on the page
    const chartElements = document.querySelectorAll('canvas[data-chart]');
    chartElements.forEach(canvas => {
        initializeChart(canvas);
    });
}

function initializeChart(canvas) {
    const chartType = canvas.dataset.chart;
    
    if (chartType === 'progress') {
        new Chart(canvas, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'In Progress'],
                datasets: [{
                    data: [canvas.dataset.completed || 0, canvas.dataset.inProgress || 0],
                    backgroundColor: ['rgba(0, 255, 136, 0.8)', 'rgba(0, 212, 255, 0.8)'],
                    borderColor: ['rgba(0, 255, 136, 1)', 'rgba(0, 212, 255, 1)'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: '#e5e7eb'
                        }
                    }
                }
            }
        });
    }
}

// Form initialization
function initializeForms() {
    // Add validation to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('border-red');
        } else {
            input.classList.remove('border-red');
        }
    });
    
    return isValid;
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.container').insertBefore(notification, document.querySelector('.container').firstChild);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard!', 'success');
    });
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Smooth scroll
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}