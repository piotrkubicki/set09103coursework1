$(document).ready(function() {
  $('#filters').select2({
    placeholder: "Select filters"
  });

  $('#search-submit').on('click', function(e) {
    e.preventDefault();
    var current_path = window.location.pathname;
    current_path = current_path.split('/');
    console.log(current_path);
    var words = $('#search').val();
    var filters = $('#filters').select2('data');
    var link = '/search/?q=';

    if (current_path[1] == 'admin')
      link = '/admin' + link;
    
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

  $('#logout-btn').on('click', function(e) {
    e.preventDefault();
    window.location.href = '/logout/';
  });
});
