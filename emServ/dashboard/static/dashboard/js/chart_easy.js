var ctx_in = document.getElementById("myChart");

var data = {
    labels: dataset_achat["months"], // or dataset_achat["months"]
    datasets: [{
            label: 'Vente',
            data: dataset_vente["data"],
            borderWidth: 2,
            backgroundColor: 'rgb(255, 61, 0)',
            borderColor: [
                'rgb(0, 0, 0)',
            ]

        },
        {
            label: 'Achat Direct',
            data: dataset_achat["data"],
            borderWidth: 2,
            backgroundColor: 'rgb(0, 0, 0)',
            borderColor: [
                'rgb(255, 61, 0)',
            ]

        },
        {
            label: 'Depot',
            data: dataset_depot["data"],
            borderWidth: 2,
            backgroundColor: 'rgb(218, 223, 225)',
            borderColor: [
                'rgb(255, 61, 0)',
            ]

        }
    ]
};

var myBarChart = new Chart(ctx_in, {
    type: 'bar',
    data: data,
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


