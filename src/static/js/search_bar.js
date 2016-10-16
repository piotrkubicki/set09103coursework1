$(document).ready(function() {
  $('#filters').select2({
    placeholder: "Select filters"
  });

  $('#search-submit').on('click', function(e) {
    e.preventDefault();
    var words = $('#search').val();
    var filters = $('#filters').select2('data');
    var link = '/search/?q=';
    
    for (var i = 0; i < words.length; i++) {
      letter = words[i];

      if (letter == '+') {
        letter = '%';
      }

      link += letter;
    }

    if (filters.length)
      link += '&filters=';

    for (var i = 0; i < filters.length; i++) {
      filter = filters[i].text;

      link += filter.toLowerCase() + ' ';
    }

    window.location.href = link;
  });
});
