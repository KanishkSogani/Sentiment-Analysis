// Function to fetch data and create the bar chart
function createChart() {
  fetch("http://127.0.0.1:3000/youtube")
    .then((response) => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then((data) => {
      // Extract data from the response
      const percent = data.percentage3;

      // Replace single quotes with double quotes in the data strings to make them valid JSON
      const validJSONData_labels = percent.replace(/'/g, '"');

      // Parse the data as JSON
      const dataArray = JSON.parse(validJSONData_labels);
      console.log(dataArray);
      // Create the bar chart
      const ctx = document.getElementById('doughnut');
      new Chart(ctx, {
        type: 'doughnut',
        data: {
        labels: ['Neutral', 'Positive', 'Negative',],
        datasets: [{
          label: '# of Votes',
          data: dataArray,
          backgroundColor: [
          'rgba(177,72,210,0.5)',
          'rgba(231,154,255,0.5)',
          'rgba(243,204,255,0.5)',

          ],
        borderColor: [
          'rgb(153, 102, 255)',
          'rgb(153, 102, 255)',
          'rgb(153, 102, 255)',
        ],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            display: false
          },
          grid: {
            display: false,
            drawTicks: false,
          }
        }
      }
    }
  });
    })
    .catch((error) => {
      console.error('There was a problem with the fetch operation:', error);
    });
}

// Call the function to create the chart when the DOM is loaded
document.addEventListener('DOMContentLoaded', ()=>{
  createChart();
});
