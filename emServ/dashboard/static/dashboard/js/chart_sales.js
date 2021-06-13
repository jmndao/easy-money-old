var salesChart = document.getElementById('salesChart');


var dataSales = {
    labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
    datasets: [{
        label: 'Achat',
        data: [130000, 214700, 40000, 262000, 412000, 87000, 200700, 143000, 67000, 320000, 232000, 184000],
        backgroundColor: 'rgb(0, 0, 0)'
    }]
};

var mySalesChart = new Chart(salesChart, {
    type: 'bar',
    data: dataSales,
});