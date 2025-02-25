/**
 * Main JavaScript file for Sailing Analytics Platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Handle form delete confirmations
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // GPX file upload preview
    const gpxFileInput = document.getElementById('gpx_file');
    const gpxFileName = document.getElementById('gpx_file_name');
    
    if (gpxFileInput && gpxFileName) {
        gpxFileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                gpxFileName.textContent = this.files[0].name;
            } else {
                gpxFileName.textContent = 'No file selected';
            }
        });
    }
});

/**
 * Function to render charts on the analytics page
 */
function renderCharts() {
    // Monthly distance chart
    const monthlyCtx = document.getElementById('monthlyChart');
    if (monthlyCtx) {
        const monthlyData = JSON.parse(monthlyCtx.dataset.chartData);
        new Chart(monthlyCtx, {
            type: 'bar',
            data: {
                labels: monthlyData.labels,
                datasets: [{
                    label: 'Distance (NM)',
                    data: monthlyData.values,
                    backgroundColor: 'rgba(13, 110, 253, 0.7)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Distance (Nautical Miles)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    }
                }
            }
        });
    }
    
    // Boat performance chart
    const boatCtx = document.getElementById('boatPerformanceChart');
    if (boatCtx) {
        const boatData = JSON.parse(boatCtx.dataset.chartData);
        new Chart(boatCtx, {
            type: 'radar',
            data: {
                labels: boatData.labels,
                datasets: [{
                    label: 'Average Speed (knots)',
                    data: boatData.speeds,
                    backgroundColor: 'rgba(13, 110, 253, 0.2)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(13, 110, 253, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

/**
 * Function to initialize map for session detail page
 */
function initSessionMap(gpxUrl) {
    const mapContainer = document.getElementById('session-map');
    if (!mapContainer) return;
    
    // Here you would initialize a map with the GPX track
    // This is a placeholder - implementation would depend on your chosen map library
    console.log('Would initialize map with GPX from:', gpxUrl);
    
    // Example with Leaflet (add appropriate script tags to the page):
    /*
    const map = L.map('session-map').setView([0, 0], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Load the GPX track
    new L.GPX(gpxUrl, {
        async: true,
        marker_options: {
            startIconUrl: '/static/images/pin-icon-start.png',
            endIconUrl: '/static/images/pin-icon-end.png',
            shadowUrl: '/static/images/pin-shadow.png'
        }
    }).on('loaded', function(e) {
        map.fitBounds(e.target.getBounds());
    }).addTo(map);
    */
}