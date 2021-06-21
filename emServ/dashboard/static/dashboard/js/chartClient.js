var clientChart = document.getElementById('chart_client');

var dataClient = {
    labels: dataset_client["months"],
    datasets: [{
        label: 'Vente',
        data: dataset_client['data'],
        borderWidth: 2,
        backgroundColor: 'rgb(0, 0, 0)',
        borderColor: [
            'rgb(255, 61, 0)'
        ]
        

    }]
};

var myclientChart = new Chart(clientChart, {
    type: 'line',
    data: dataClient,
});