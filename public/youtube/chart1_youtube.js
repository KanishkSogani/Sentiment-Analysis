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
      const bar_labels = data.barGraph3;
      const graph_data = data.countGraph3;

      // Replace single quotes with double quotes in the data strings to make them valid JSON
      const validJSONData_labels = bar_labels.replace(/'/g, '"');
      const validJSONData_data = graph_data.replace(/'/g, '"');

      // Parse the data as JSON
      const dataArray = JSON.parse(validJSONData_labels);
      const graphArray = JSON.parse(validJSONData_data);

      // Create the bar chart
      const ctx = document.getElementById('bar');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: dataArray,
          datasets: [{
            label: '# of Votes',
            data: graphArray,
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgb(153, 102, 255)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            x: {
              grid: {
                display: false,
                drawTicks: false
              }
            },
            y: {
              beginAtZero: true,
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
document.addEventListener('DOMContentLoaded', createChart);
