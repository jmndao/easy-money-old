var depotChart = document.getElementById('depotChart');

var dataDepot = {
    labels:dataset_depot["months"],
    datasets: [{
        label: 'Depot',
        data: dataset_depot['data'],
        borderWidth: 2,
        backgroundColor: 'rgb(0, 0, 0)',
        borderColor: [
            'rgb(255, 61, 0)'
        ]
    }]
};

var myDepotChart = new Chart(depotChart, {
    type: 'bar',
    data: dataDepot,
});