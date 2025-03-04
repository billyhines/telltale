// Main JavaScript file for Sailing Analytics Platform

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Enable tooltips everywhere
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Enable popovers everywhere
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    
    // File input customization
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0].name;
            const label = e.target.nextElementSibling;
            label.textContent = fileName;
        });
    });
});

// Function to initialize sailing route map (to be implemented with a mapping library)
function initSailingMap(elementId, routePoints) {
    if (!elementId || !routePoints || routePoints.length === 0) {
        console.error('Missing required parameters for map initialization');
        return;
    }
    
    // This is a placeholder for map initialization
    // To be implemented with Leaflet, MapBox, or Google Maps
    console.log('Map would be initialized with', routePoints.length, 'points');
    
    // Example implementation with Leaflet would go here
    // const map = L.map(elementId).setView([routePoints[0].lat, routePoints[0].lon], 13);
    // L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    // const routeLine = L.polyline(routePoints.map(p => [p.lat, p.lon])).addTo(map);
    // map.fitBounds(routeLine.getBounds());
}

// Function to initialize speed charts (to be implemented with a charting library)
function initSpeedChart(elementId, timestamps, speeds) {
    if (!elementId || !timestamps || !speeds) {
        console.error('Missing required parameters for chart initialization');
        return;
    }
    
    // This is a placeholder for chart initialization
    // To be implemented with Chart.js, D3.js, or another library
    console.log('Chart would be initialized with', speeds.length, 'data points');
    
    // Example implementation with Chart.js would go here
    // const ctx = document.getElementById(elementId).getContext('2d');
    // new Chart(ctx, {
    //     type: 'line',
    //     data: {
    //         labels: timestamps,
    //         datasets: [{
    //             label: 'Speed (knots)',
    //             data: speeds,
    //             borderColor: 'rgba(75, 192, 192, 1)',
    //             tension: 0.1
    //         }]
    //     }
    // });
}