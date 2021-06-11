var ctx = document.getElementById("myChart").getContext("2d");

var data = {
    labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
    datasets: [{
            label: 'Depot',
            data: [120000, 212700, 100000, 212000, 312000, 97000, 212700, 120000, 97000, 170000, 212000, 147000],
            backgroundColor: 'rgb(255, 61, 0)'

        },
        {
            label: 'Achat',
            data: [130000, 214700, 40000, 262000, 412000, 87000, 200700, 143000, 67000, 320000, 232000, 184000],
            backgroundColor: 'rgb(0, 0, 0)'

        }
    ]
};


// The Stock Depot Chart
