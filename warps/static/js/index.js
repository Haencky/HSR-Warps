let chartInstance = null;

function createOrUpdateChart(labels, data, title) {
    const ctx = document.getElementById('stats');

    if (chartInstance) {
        chartInstance.data.labels = labels;
        chartInstance.data.datasets[0].data = data;
        chartInstance.data.datasets[0].label = title;
        chartInstance.update();
    } else {
        chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
        labels: labels,
        datasets: [{
            label: title,
            data: data,
            borderWidth: 1,
            fill: false,
            backgroundColor: [
                'rgba(6, 46, 206, 0.8)',
                'rgba(142, 47, 110, 0.8)',
                'rgba(255, 215, 0, 1)'
            ]
        }]
        },
        options: {
        scales: {
            y: {
            type: 'logarithmic',
            min: 1,
            ticks: {
                display: false,
            },
            }
        }
        }
    });
    }
}

$(document).ready(function() {
    $('.type-container').on('click', function() {
        const dataId = $(this).data('id');
        const url = `/api/type/${dataId}`;    
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                createOrUpdateChart(response.labels, response.data, response.title);

            },
            error: function(error) {
                console.error('Cant load data:', error);
            }
        });
    });
});