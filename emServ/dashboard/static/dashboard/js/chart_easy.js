var ctx_in = document.getElementById("myChart");

var data = {
    labels: dataset_stock["months"], // or dataset_achat["months"]
    datasets: [{
            label: 'Stock',
            data: dataset_stock["data"],
            backgroundColor: 'rgb(255, 61, 0)'

        },
        {
            label: 'Achat',
            data: dataset_achat["data"],
            backgroundColor: 'rgb(0, 0, 0)'

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


// The Stock Depot Chart

// var ctx2 = document.getElementById("chart_client").getContext("2d");
// var data2 = {
//     labels: ['Janv', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aout', 'Sept', 'Oct', 'Nov', 'Dec'],
//     datasets: [{

//             label: 'Produit',
//             borderColor: ['black'],
//             data: [3, 5, 4, 8, 1, 6, 4, 2, 7, 0, 4, 1],
//             backgroundColor: 'rgb(255, 61, 0)',

//         }],
//     options: {
//         title:{
//             display: 'true',
//             text: 'Produits Par Jour'
//         }
//     },options: {
//         plugins: {
//             title: {
//                 display: true,
//                 text: 'Custom Chart Title',
//                 padding: {
//                     top: 10,
//                     bottom: 30
//                 }
//             }
//         }
//     }
// };

// var myBarChart = new Chart(ctx_in, {
//     type: 'bar',
//     data: data2,
//     options: {
//         barValueSpacing: 0,
//         scales: {
//             yAxes: [{
//                 ticks: {
//                     min: 0,
//                 }
//             }]
//         }
//     }
// });


// // The Stock Depot Chart