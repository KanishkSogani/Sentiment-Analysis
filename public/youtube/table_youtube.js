document.addEventListener('DOMContentLoaded', function() {
  var responseData = [];

  fetch('http://127.0.0.1:3000/youtube')
    .then(response => response.json())
    .then(data => {
      responseData = data['bert3'];
      responseData = JSON.parse(responseData);
      console.log(responseData);
      buildtable(responseData);
    })
    .catch(error => {
      console.error(error);
    });

  function buildtable(data) {
    console.log('buildtable');
    var table = document.querySelector('.myTable'); // Select the table by its class

    if (table) {
      var tbody = table.querySelector('tbody'); // Select the tbody element within the table

      for (var i = 0; i < data.length; i++) {
        var row = document.createElement('tr');
        var textCell = document.createElement('td');
        var sentimentCell = document.createElement('td');
        var emoticonCell = document.createElement('td');

        textCell.textContent = data[i].text;
        sentimentCell.textContent = data[i].sentiment;

        if(data[i].sentiment == "Positive")
        {
          emoticonCell.textContent = "😊";
        }
        else if(data[i].sentiment == "Negative")
        {
          emoticonCell.textContent = "😞";
        }
        else
        {
          emoticonCell.textContent = "😐";
        }

        emoticonCell.style.left = "35px";
        sentimentCell.style.left = "15px";

        row.appendChild(textCell);
        row.appendChild(sentimentCell);
        row.appendChild(emoticonCell);

        tbody.appendChild(row);
      }
    } else {
      console.error('Table with class "myTable" not found.');
    }
  }
});
