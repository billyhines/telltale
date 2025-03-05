// Dashboard functionality for Sailing Analytics Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize any dashboard components that need JavaScript
    
    // Highlight current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-menu .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
    
    // Responsive sidebar toggle for mobile
    const toggleSidebar = () => {
        const sidebar = document.querySelector('.sidebar');
        if (window.innerWidth < 768) {
            sidebar.classList.toggle('collapsed');
        }
    };
    
    // Add event listener for window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768) {
            const sidebar = document.querySelector('.sidebar');
            sidebar.classList.remove('collapsed');
        }
    });
    
    // Future dashboard features can be added here
    // For example, chart initializations, data refreshing, etc.
});