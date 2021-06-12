var depotChart = document.getElementById('depotChart');

var dataDepot = {
    labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
    datasets: [{
        label: 'Depot',
        data: [120000, 212700, 100000, 212000, 312000, 97000, 212700, 120000, 97000, 170000, 212000, 147000],
        backgroundColor: 'rgb(255, 61, 0)'

    }]
};

var myBarChart = new Chart(depotChart, {
    type: 'bar',
    data: dataDepot,
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