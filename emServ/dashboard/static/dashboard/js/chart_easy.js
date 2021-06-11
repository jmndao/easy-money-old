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

var myBarChart = new Chart(ctx, {
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


// The Stock Depot Chart
var chart_stock_depot =  document.getElementById('chart-depot');
chart_stock_depot.height = 200;
var mychart_stock_depot = new Chart(chart_stock_depot, {
    type: 'bar',
    data: {
        labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin','Juil','Aout','Sept','Oct','Nov','Dec'],
        datasets: [{
            label: 'Stock Achat',
            data: [ 212700,120000 ,97000, 170000, 212000,147000, 120000, 212700, 100000, 212000, 312000, 97000, ],
            fill: false,
            tension: 0.2,
            borderColor: 
                'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    
    options: {
        title:{
            display:true,
            text: 'Montant Dépensé Par Mois',
            fontSize:25
        },
        legend:{
            position:'bottom',
            display:false,
        },
        layout:{
            // padding:{
            //     left: 50,
            //     right: 0
            // }
        },
        scales: {
            yAxes: [{
                
                ticks: {
                    beginAtZero: true,
                }
            }]
        }
    }
});
