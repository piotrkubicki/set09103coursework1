$(document).ready(function() {
  $('#previous').on('click', function() {
    if ($(this).parent('li').hasClass('disabled') == false) { 
      var pageNumber = $('.pagination').find('.active').text();
      var current_path = window.location.pathname;
      current_path = current_path.split('/');
      
      if ($.inArray('admin', current_path)) {
        window.location.href = '/admin/?page=' + (parseInt(pageNumber) - parseInt(1));
      } else {
        window.location.href = '/?page=' + (parseInt(pageNumber) - parseInt(1));
      }
    }
  });

  $('#next').on('click', function() {
    if ($(this).parent('li').hasClass('disabled') == false) {
      var pageNumber = $('.pagination').find('.active').text();
      var current_path = window.location.pathname;
      current_path = current_path.split('/');
      
      if ($.inArray('admin', current_path)) {
        window.location.href = '/admin/?page=' + (parseInt(pageNumber) + parseInt(1));
      } else {
        window.location.href = "/?page=" + (parseInt(pageNumber) + parseInt(1));
      }
    }
 });
});
