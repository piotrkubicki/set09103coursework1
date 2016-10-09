$(document).ready(function() {
  $('#filters').select2({
    placeholder: "Select filters"
  });

  $('#previous').on('click', function() {
    if ($(this).parent('li').hasClass('disabled') == false) { 
      var pageNumber = $('.pagination').find('.active').text();
      window.location.href = "/?page=" + (parseInt(pageNumber) - parseInt(1));
    }
  });

  $('#next').on('click', function() {
    if ($(this).parent('li').hasClass('disabled') == false) {
      var pageNumber = $('.pagination').find('.active').text();
      window.location.href = "/?page=" + (parseInt(pageNumber) + parseInt(1));
    }
 });
});
