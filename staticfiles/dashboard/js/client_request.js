var ctx = document.getElementById('chart_client').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
        datasets: [{
            label: 'frequence des cliens en fonction du temps',
            data: [12, 9, 13, 15, 12, 13, 9, 15, 14, 13, 14, 14],
            borderColor: [
                'rgba(255,61,0,1)',
            ],
            borderPointColor: 'rgba(0,0,0,0)',
            borderWidth: 1,
            fill: false,
            tension: 0.1
        }]
    },
    options: {
        barValueSpacing: 0,
        scales: {
            yAxes: [{
                ticks: {
                    min: 0,
                }
            }]
        }
    }
});