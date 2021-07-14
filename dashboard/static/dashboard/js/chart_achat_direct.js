var achatChart = document.getElementById('achatChart');

var dataDepot = {
    labels:dataset_achat_direct["months"],
    datasets: [{
        label: 'Achat_direct',
        data: dataset_achat_direct['data'],
        borderWidth: 2,
        backgroundColor: 'rgb(0, 0, 0)',
        borderColor: [
            'rgb(255, 61, 0)'
        ]

        
        

    }]
};

var myachatChart = new Chart(achatChart, {
    type: 'bar',
    data: dataDepot,
});