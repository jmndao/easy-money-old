var chart_achat = document.getElementById('myChart');
chart_achat.height = 300;
var myChart_achat = new Chart(chart_achat, {
    type: 'bar',
    data: {
        labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin','Juil','Aout','Sept','Oct','Nov','Dec'],
        datasets: [{
            label: 'Stock Achat',
            data: [120000, 212700, 100000, 212000, 312000, 97000, 212700,120000 ,97000, 170000, 212000,147000],
            fill: true,
            tension: 0.2,
            borderColor: 
                'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }]
    },
    options: {
        title:{
            display:true,
            text: 'Montant Total Recu Par Mois ',
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

var chart_depot = document.getElementById('myChart2');
chart_depot.height = 300;
var chart_depot = new Chart(chart_depot, {
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


// The Stock Depot Chart
var chart_stock_depot =  document.getElementById('chart-depot');
chart_stock_depot.height = 100;
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
