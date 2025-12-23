const ctx = document.getElementById('stats');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: label,
      datasets: [{
        label: 'Pulls per rarity',
        data: history_data,
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