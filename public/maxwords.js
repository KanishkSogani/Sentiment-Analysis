//For adjusting maxwords in table data!
var maxWords = 30; 

  var tableCells = document.querySelectorAll('td');
  tableCells.forEach(function (cell) {
    var text = cell.textContent.trim().split(' ');
    if (text.length > maxWords) {
      cell.textContent = text.slice(0, maxWords).join(' ') + '...';
    }
  });