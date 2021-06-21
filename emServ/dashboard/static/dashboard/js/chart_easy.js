var ctx_in = document.getElementById("myChart");

var data = {
    labels: dataset_stock["months"], // or dataset_achat["months"]
    datasets: [{
            label: 'Stock',
            data: dataset_stock["data"],
            borderWidth: 2,
            backgroundColor: 'rgb(255, 61, 0)',
            borderColor: [
                'rgb(0, 0, 0)',
            ]

        },
        {
            label: 'Achat',
            data: dataset_achat["data"],
            borderWidth: 2,
            backgroundColor: 'rgb(0, 0, 0)',
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


