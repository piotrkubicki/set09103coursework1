$(document).ready(function() {
  $('#filters').select2({
    placeholder: "Select filters"
  });

  $('#search-submit').on('click', function(e) {
    e.preventDefault();
    var words = $('#search').val();
    var filters = $('#filters').text();
    var processed_words = ''
    
    for (var i = 0; i < words.length; i++) {
      letter = words[i];

      if (letter == '+') {
        letter = '%';
      }

      processed_words += letter;
    }

    window.location.href = '/search/?q=' + processed_words + '&filters=' + filters; 
  });
});
