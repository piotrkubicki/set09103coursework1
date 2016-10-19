$(document).ready(function() {
  $(document).on('click', '.header', function() {
    header = $(this);
    sublist = header.next('ul');
    arrow = header.find('.arrow');
    
    if (sublist.hasClass('active') == false) {
      sublist.css('display', 'block');
      $('.arrow').removeClass('active');
      $('ul').removeClass('active');
      sublist.toggleClass('active');
      arrow.addClass('active');
    } else {
      sublist.removeClass('active');
      arrow.removeClass('active');
    }
  });

  $(document).on('animationend', '.sublist',  function(e) {
    if (e.originalEvent.animationName == 'slideUp')
      $(this).css('display', 'none');
  });

  $(document).on('animationend', '.arrow', function(e) {
    arrow = $(this);
    
    if (e.originalEvent.animationName == 'turnDown') {
      arrow.removeClass('fa-chevron-circle-right');
      arrow.addClass('fa-chevron-circle-down');
    } else { 
      arrow.removeClass('fa-chevron-circle-down');
      arrow.addClass('fa-chevron-circle-right');
    }
  });

  $(document).on('click', '#send-genre-form', function(e) {
    e.preventDefault();

    var genre = {
      name : $('#genre-name').val()
    }

    $.ajax({
      type: 'POST',
      url: '/admin/genre/',
      data: JSON.stringify(genre),
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        console.log('success');
        $('#sidebar-menu').html(result);
      }
    });
  });

  if (document.location.pathname.indexOf('/genres/') == 0) {
    $('#genres').trigger('click');
  } else if (document.location.pathname.indexOf('/authors/') == 0) {
    $('#authors').trigger('click');
  }
});
