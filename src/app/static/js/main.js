// Main JavaScript file for Sailing Analytics Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all Bootstrap tooltips
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
    
    // Initialize all Bootstrap popovers
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => new bootstrap.Popover(popover));
    
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-persistent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Custom file input handler
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const fileName = e.target.files[0].name;
            const label = input.nextElementSibling;
            label.textContent = fileName;
        });
    });
    
    // Handle responsive navbar collapse after click (for mobile)
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.getComputedStyle(navbarToggler).display !== 'none') {
                    const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                    bsCollapse.hide();
                }
            });
        });
    }
});

// Function to initialize sailing route map (to be implemented with Leaflet)
function initSailingMap(elementId, routePoints, options = {}) {
    if (!elementId || !routePoints || routePoints.length === 0) {
        console.error('Missing required parameters for map initialization');
        return null;
    }
    
    // Default options
    const defaultOptions = {
        zoom: 13,
        tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    };
    
    const mapOptions = { ...defaultOptions, ...options };
    
    // Check if Leaflet is available
    if (typeof L === 'undefined') {
        console.error('Leaflet library not loaded');
        return null;
    }
    
    // Initialize map
    const map = L.map(elementId).setView([routePoints[0].lat, routePoints[0].lon], mapOptions.zoom);
    
    // Add tile layer
    L.tileLayer(mapOptions.tileLayer, {
        attribution: mapOptions.attribution
    }).addTo(map);
    
    // Create polyline from route points
    const routeLine = L.polyline(
        routePoints.map(p => [p.lat, p.lon]), 
        { color: 'blue', weight: 3, opacity: 0.7 }
    ).addTo(map);
    
    // Fit map to route bounds
    map.fitBounds(routeLine.getBounds());
    
    // Add start and end markers
    const startPoint = routePoints[0];
    const endPoint = routePoints[routePoints.length - 1];
    
    const startIcon = L.divIcon({
        className: 'start-icon',
        html: '<i class="fas fa-play-circle" style="color: green; font-size: 24px;"></i>',
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
    
    const endIcon = L.divIcon({
        className: 'end-icon',
        html: '<i class="fas fa-flag-checkered" style="color: red; font-size: 24px;"></i>',
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
    
    L.marker([startPoint.lat, startPoint.lon], { icon: startIcon }).addTo(map);
    L.marker([endPoint.lat, endPoint.lon], { icon: endIcon }).addTo(map);
    
    return {
        map: map,
        routeLine: routeLine
    };
}

// Function to initialize speed charts (to be implemented with Chart.js)
function initSpeedChart(elementId, timestamps, speeds, options = {}) {
    if (!elementId || !timestamps || !speeds) {
        console.error('Missing required parameters for chart initialization');
        return null;
    }
    
    // Check if Chart.js is available
    if (typeof Chart === 'undefined') {
        console.error('Chart.js library not loaded');
        return null;
    }
    
    // Default options
    const defaultOptions = {
        title: 'Speed Over Time',
        xLabel: 'Time',
        yLabel: 'Speed (knots)',
        lineColor: 'rgba(13, 110, 253, 1)',
        fillColor: 'rgba(13, 110, 253, 0.1)'
    };
    
    const chartOptions = { ...defaultOptions, ...options };
    
    // Format timestamps for display
    const formattedLabels = timestamps.map(timestamp => {
        // Check if timestamp is a Date object or a string
        const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });
    
    // Get the canvas element and create chart
    const ctx = document.getElementById(elementId).getContext('2d');
    
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: formattedLabels,
            datasets: [{
                label: chartOptions.title,
                data: speeds,
                borderColor: chartOptions.lineColor,
                backgroundColor: chartOptions.fillColor,
                tension: 0.1,
                fill: true,
                pointRadius: 2,
                pointHoverRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    title: {
                        display: true,
                        text: chartOptions.xLabel
                    },
                    grid: {
                        display: false
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: chartOptions.yLabel
                    },
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Speed: ${context.parsed.y.toFixed(1)} knots`;
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
    
    return chart;
}

// Wind direction visualization helper
function initWindCompass(elementId, windDirection = 0, options = {}) {
    if (!elementId) {
        console.error('Missing element ID for wind compass');
        return null;
    }
    
    // Default options
    const defaultOptions = {
        size: 150,
        arrowColor: '#0d6efd',
        compassColor: '#333',
        backgroundColor: '#f8f9fa',
        onChange: null // Callback for when direction changes
    };
    
    const compassOptions = { ...defaultOptions, ...options };
    
    // Get the container element
    const container = document.getElementById(elementId);
    if (!container) {
        console.error(`Element with ID ${elementId} not found`);
        return null;
    }
    
    // Clear container
    container.innerHTML = '';
    
    // Create canvas
    const canvas = document.createElement('canvas');
    canvas.width = compassOptions.size;
    canvas.height = compassOptions.size;
    container.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    let currentDirection = windDirection;
    let isDragging = false;
    
    // Function to draw the compass
    const drawCompass = () => {
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = (canvas.width / 2) - 10;
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw background circle
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.fillStyle = compassOptions.backgroundColor;
        ctx.fill();
        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Draw cardinal points
        ctx.font = '14px Arial';
        ctx.fillStyle = compassOptions.compassColor;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // North
        ctx.fillText('N', centerX, centerY - radius + 15);
        // East
        ctx.fillText('E', centerX + radius - 15, centerY);
        // South
        ctx.fillText('S', centerX, centerY + radius - 15);
        // West
        ctx.fillText('W', centerX - radius + 15, centerY);
        
        // Draw wind arrow
        const radian = (currentDirection - 90) * (Math.PI / 180);
        const arrowLength = radius - 30;
        
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(
            centerX + arrowLength * Math.cos(radian),
            centerY + arrowLength * Math.sin(radian)
        );
        ctx.strokeStyle = compassOptions.arrowColor;
        ctx.lineWidth = 3;
        ctx.stroke();
        
        // Draw arrow head
        const headLength = 15;
        const headWidth = 8;
        
        const arrowEndX = centerX + arrowLength * Math.cos(radian);
        const arrowEndY = centerY + arrowLength * Math.sin(radian);
        
        ctx.beginPath();
        ctx.moveTo(arrowEndX, arrowEndY);
        ctx.lineTo(
            arrowEndX - headLength * Math.cos(radian) + headWidth * Math.cos(radian + Math.PI/2),
            arrowEndY - headLength * Math.sin(radian) + headWidth * Math.sin(radian + Math.PI/2)
        );
        ctx.lineTo(
            arrowEndX - headLength * Math.cos(radian) - headWidth * Math.cos(radian + Math.PI/2),
            arrowEndY - headLength * Math.sin(radian) - headWidth * Math.sin(radian + Math.PI/2)
        );
        ctx.closePath();
        ctx.fillStyle = compassOptions.arrowColor;
        ctx.fill();
        
        // Display current direction in degrees
        ctx.font = 'bold 16px Arial';
        ctx.fillStyle = compassOptions.compassColor;
        ctx.textAlign = 'center';
        ctx.fillText(`${Math.round(currentDirection)}°`, centerX, centerY + radius + 20);
    };
    
    // Calculate direction based on mouse position
    const calculateDirection = (x, y) => {
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        
        const deltaX = x - centerX;
        const deltaY = y - centerY;
        
        // Calculate angle in radians
        let angle = Math.atan2(deltaY, deltaX) * (180 / Math.PI);
        
        // Convert to compass degrees (0-360, clockwise from north)
        angle = (angle + 90) % 360;
        if (angle < 0) angle += 360;
        
        return angle;
    };
    
    // Add event listeners for mouse/touch interaction
    canvas.addEventListener('mousedown', (e) => {
        isDragging = true;
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        currentDirection = calculateDirection(x, y);
        drawCompass();
    });
    
    canvas.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const rect = canvas.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            currentDirection = calculateDirection(x, y);
            drawCompass();
        }
    });
    
    canvas.addEventListener('mouseup', () => {
        isDragging = false;
        if (typeof compassOptions.onChange === 'function') {
            compassOptions.onChange(Math.round(currentDirection));
        }
    });
    
    canvas.addEventListener('mouseleave', () => {
        isDragging = false;
    });
    
    // Touch events for mobile
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        isDragging = true;
        const rect = canvas.getBoundingClientRect();
        const touch = e.touches[0];
        const x = touch.clientX - rect.left;
        const y = touch.clientY - rect.top;
        currentDirection = calculateDirection(x, y);
        drawCompass();
    });
    
    canvas.addEventListener('touchmove', (e) => {
        e.preventDefault();
        if (isDragging) {
            const rect = canvas.getBoundingClientRect();
            const touch = e.touches[0];
            const x = touch.clientX - rect.left;
            const y = touch.clientY - rect.top;
            currentDirection = calculateDirection(x, y);
            drawCompass();
        }
    });
    
    canvas.addEventListener('touchend', () => {
        isDragging = false;
        if (typeof compassOptions.onChange === 'function') {
            compassOptions.onChange(Math.round(currentDirection));
        }
    });
    
    // Initial drawing
    drawCompass();
    
    // Return an object with methods to interact with the compass
    return {
        getDirection: () => Math.round(currentDirection),
        setDirection: (direction) => {
            currentDirection = direction;
            drawCompass();
        },
        redraw: drawCompass
    };
}