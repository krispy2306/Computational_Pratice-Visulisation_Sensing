const map = L.map('map').setView([51.5, -0.13], 11);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

function getRadius(laeq) {
    return Math.max(3, Math.min(13, (laeq - 50) / 3.2));
}

function getColour(laeq) {
    if (laeq >= 85) {
        return '#ec3d69'; // very loud 
    } else if (laeq >= 79) {
        return '#de7220'; // medium loud
    } else if (laeq >= 70) {
        return '#cfe141'; // moderate
    } else if (laeq >= 60) {
        return '#73dca4'; // quiet
    } else {
        return '#6585ac'; // quietest 
    }
}

function getOpacity(laeq) {
    return Math.max(0.25, Math.min(0.75, (laeq - 45) / 50));
}

fetch('data/london_noise.json')
    .then(response => response.json())
    .then(data => {
        data.forEach(point => {
            const colour = getColour(point.laeq);
            const radius = getRadius(point.laeq);
            const opacity = getOpacity(point.laeq);

            L.circleMarker([point.lat, point.lon], {
                radius: radius * 1.8,
                fillColor: colour,
                color: colour,
                fillOpacity: opacity * 0.16,
                opacity: 0,
                weight: 0,
                interactive: false
            }).addTo(map);

            L.circleMarker([point.lat, point.lon], {
                radius: radius,
                fillColor: colour,
                color: colour,
                fillOpacity: Math.min(opacity + 0.18, 0.95),
                opacity: 0.65,
                weight: 1
            })
            
            .bindPopup(`
                <strong>${point.borough}</strong><br>
                LAeq: ${point.laeq} dB<br>
                Measurements: ${point.measure_count}
            `)
            .addTo(map);
        });
    });