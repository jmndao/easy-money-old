var venteChart = document.getElementById('venteChart');

var dataVente = {
    labels: dataset_vente["months"],
    datasets: [{
        label: 'Vente',
        data: dataset_vente['data'],
        borderWidth: 2,
        backgroundColor: 'rgb(0, 0, 0)',
        borderColor: [
            'rgb(255, 61, 0)'
        ]
        
        
        

    }]
};

var myventeChart = new Chart(venteChart, {
    type: 'bar',
    data: dataVente,
});