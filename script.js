const map = L.map('map').setView([51.5, -0.13], 11);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

const markers = [];
let allData = [];

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
        allData = data;

        populateBoroughSelect(data);
        drawPoints(data);
        updateInfoForAll(data);

        document.getElementById('boroughSelect').addEventListener('change', event => {
            const selectedBorough = event.target.value;

            if (selectedBorough === 'all') {
                drawPoints(allData);
                map.setView([51.5, -0.13], 11);
                updateInfoForAll(allData);
            } else {
                const filteredData = allData.filter(point => point.borough === selectedBorough);
                drawPoints(filteredData);
                zoomToData(filteredData);
                updateBoroughInfo(selectedBorough, filteredData);
            }
        });

        document.getElementById('resetButton').addEventListener('click', () => {
            document.getElementById('boroughSelect').value = 'all';
            drawPoints(allData);
            map.setView([51.5, -0.13], 11);
            updateInfoForAll(allData);
        });
    });

function populateBoroughSelect(data) {
    const select = document.getElementById('boroughSelect');
    const boroughs = [...new Set(data.map(point => point.borough))].sort();

    boroughs.forEach(borough => {
        const option = document.createElement('option');
        option.value = borough;
        option.textContent = borough;
        select.appendChild(option);
    });
}

function drawPoints(data) {
    markers.forEach(marker => map.removeLayer(marker));
    markers.length = 0;

    data.forEach(point => {
        const colour = getColour(point.laeq);
        const radius = getRadius(point.laeq);
        const opacity = getOpacity(point.laeq);

        const halo = L.circleMarker([point.lat, point.lon], {
            radius: radius * 1.5,
            fillColor: colour,
            color: colour,
            fillOpacity: opacity * 0.1,
            opacity: 0,
            weight: 0,
            interactive: false
        }).addTo(map);

        const core = L.circleMarker([point.lat, point.lon], {
            radius: radius,
            fillColor: colour,
            color: colour,
            fillOpacity: opacity,
            opacity: 0.35,
            weight: 1
        })
        .bindPopup(`
            <span class="popup-borough">${point.borough}</span>
            <div class="popup-db">${point.laeq}<span>dB(A)</span></div>
            ${point.measure_count ? `${point.measure_count} measurements` : ''}
        `)
        .addTo(map);

        markers.push(halo, core);
    });
}

function zoomToData(data) {
    if (data.length === 0) return;

    const bounds = L.latLngBounds(data.map(point => [point.lat, point.lon]));

    map.fitBounds(bounds, {
        padding: [80, 80],
        maxZoom: 14
    });
}

function updateInfoForAll(data) {
    const avg = data.reduce((sum, point) => sum + point.laeq, 0) / data.length;

    document.getElementById('boroughInfo').innerHTML = `
        <p><strong>All London</strong></p>
        <p>${data.length} sound points</p>
        <p>Average LAeq: ${avg.toFixed(1)} dB</p>
    `;
}

function updateBoroughInfo(borough, data) {
    const avg = data.reduce((sum, point) => sum + point.laeq, 0) / data.length;

    document.getElementById('boroughInfo').innerHTML = `
        <p><strong>${borough}</strong></p>
        <p>${data.length} sound points</p>
        <p>Average LAeq: ${avg.toFixed(1)} dB</p>
    `;
}