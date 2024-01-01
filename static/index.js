document.addEventListener('DOMContentLoaded', function() {
    setInterval(function() {
      changeTitleColor();
    }, 5000);

    function changeTitleColor() {
      var title = document.getElementById('title');
      var randomColor = getRandomColor();
      title.style.color = randomColor;
    }

    function getRandomColor() {
      var letters = '0123456789ABCDEF';
      var color = '#';
      for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    }
  });