const setActiveDevice = (element) => {
    const deviceData = getDeviceData(element);
    updateDeviceInfo(deviceData);
    setActiveCard(element);
    initializeOrUpdateCharts(deviceData);
}

const getDeviceData = (element) => {
    return {
        // Récupérer les données du capteur à partir des attributs data-*
        name : element.getAttribute('data-name'),
        description : element.getAttribute('data-description'),
        type : element.getAttribute('data-type'),
        status : element.getAttribute('data-status'),
        altitude : parseFloat(element.getAttribute('data-altitude') || 0),
        pressure : parseFloat(element.getAttribute('data-pressure') || 0),
        temperatureLabels : JSON.parse(element.getAttribute('data-temperature-labels') || '[]'),
        temperatureValues : JSON.parse(element.getAttribute('data-temperature-values') || '[]'),
    }
};

// Mettre à jour les informations affichées dans la colonne de droite
const updateDeviceInfo = ({ name, description }) => {
    document.getElementById('device-name').textContent = name;
    document.getElementById('device-description').textContent = description;
};

// Gérer l'état actif du capteur (ajouter une classe "active")
const setActiveCard = (element) => {
    const activeCard = document.querySelector('.device-card.device-active');
    if (activeCard) {
        activeCard.classList.remove('device-active');
    }
    element.classList.add('device-active');
};

// Initialiser ou mettre à jour les graphiques
const initializeOrUpdateCharts = ({ altitude, pressure, temperatureLabels, temperatureValues }) => {
    // Initialiser les graphiques si ce n'est pas déjà fait
    if (!temperatureChart || !altitudeGauge || !pressureGauge) {
        const temperatureCtx = document.getElementById('temperatureChart').getContext('2d');
        const altitudeCtx = document.getElementById('altitudeGauge').getContext('2d');
        const pressureCtx = document.getElementById('pressureGauge').getContext('2d');

        temperatureChart = createTemperatureChart(temperatureCtx);
        altitudeGauge = createAltitudeGauge(altitudeCtx);
        pressureGauge = createPressureGauge(pressureCtx);
    }

    // Mettre à jour les graphiques
    updateAltitudeGauge(altitude);
    updatePressureGauge(pressure);
    updateTemperatureChart(temperatureLabels, temperatureValues);
};

let temperatureChart, altitudeGauge, pressureGauge;

// Fonction pour mettre à jour la gauge d'altitude
const updateAltitudeGauge = (altitude) => {
    const altitudeGauge = Chart.getChart('altitudeGauge');
    if (!altitudeGauge) {
        console.error("Le graphique d'altitude n'existe pas.");
        return;
    } else {
        // 150 représente l'altitude maximale de la gauge
        altitudeGauge.data.datasets[0].data = [altitude, 150 - altitude];
        altitudeGauge.update();
    }
};

// Fonction pour mettre à jour la gauge de pression
const updatePressureGauge = (pressure) => {
    const pressureGauge = Chart.getChart('pressureGauge');
    if (!pressureGauge) {
        console.error("Le graphique de pression n'existe pas.");
        return;
    } else {
        pressureGauge.data.datasets[0].data = [pressure, 1100 - pressure];
        pressureGauge.update();
    }
};

// Fonction pour mettre à jour le graphique de température
const updateTemperatureChart = (labels, values) => {
    const temperatureChart = Chart.getChart('temperatureChart');
    if (!temperatureChart) {
        console.error("Le graphique de température n'existe pas.");
        return;
    } else {
        temperatureChart.data.labels = labels;
        temperatureChart.data.datasets[0].data = values;
        temperatureChart.update();
    }
};

//Fonction pour créer le graphique des températures
const createTemperatureChart = (ctx) => {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // A laisser vide car MAJ auto
            datasets: [{
                label: 'Température (°C)',
                data: [], // A laisser vide car MAJ auto
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(255,255,255, 0.6)',
                borderWidth: 1,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 10
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.raw + ' °C';
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Temps',
                        color: 'rgba(255,255,255, 0.8)',
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 9,
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Température (°C)',
                        color: 'rgba(255,255,255, 0.8)',
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 9,
                        }
                    },
                    beginAtZero: true
                }
            }
        }
    });
};

// Fonction pour créer la gauge d'altitude
const createAltitudeGauge = (ctx) => {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Altitude', 'Reste'],
            datasets: [{
                data: [0, 150],
                backgroundColor: ['rgba(75, 192, 192, 0.5)', 'rgba(200, 200, 200, 0.2)'],
                borderWidth: 1
            }]
        },
        
        options: {
            rotation: -90,
            circumference: 180,
            plugins: {
                legend: {
                    display: true, 
                    labels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 10,
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw + ' m';
                        }
                    }
                }
            }
        }
    });
};

// Fonction pour créer la gauge de pression
const createPressureGauge = (ctx) => {
    return new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Pression', 'Reste'],
            datasets: [{
                data: [0, 1100],
                backgroundColor: ['rgba(255, 99, 132, 0.5)', 'rgba(200, 200, 200, 0.2)'],
                borderWidth: 1
            }]
        },
        options: {
            rotation: -90,
            circumference: 180,
            plugins: {
                legend: {
                    display: true, 
                    labels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 10,
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw + ' hPa';
                        }
                    }
                }
            }
        }
    });
};