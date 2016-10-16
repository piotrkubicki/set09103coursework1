$(document).ready(function() {

  var rated = false;

  $('#rating-container i').on('mouseover', function(e) {
    var star = $(this)
    var prevStars = star.prevAll('i');
    var nextStars = star.nextAll('i');

    nextStars.each(function() {      
      $(this).removeClass('fa-star');
      $(this).addClass('fa-star-o');
    });

    prevStars.each(function() {
      $(this).removeClass('fa-star-o');
      $(this).addClass('fa-star');
    });
    star.removeClass('fa-star-o');
    star.addClass('fa-star');
  });

  $('#rating-container i').on('mouseleave', function(e) {
    var star = $(this)
    var stars = star.siblings('i');

    if (rated == false) {
      stars.each(function() { 
        $(this).removeClass('fa-star');
        $(this).addClass('fa-star-o');
      });
      
      star.removeClass('fa-star');
      star.addClass('fa-star-o');
    } else {
      rated = false;
    }
  });

  $('#rating-container i').on('click', function(e) {
    rated = true; 
  });

  $('#rate').on('click', function(e) {
    e.preventDefault();
    self = $(this);
    self.html('<div class="spinner"></div>');

    var position = $('#rating-container').position();

    $('<div id="comment-overlay"></div>').css({  
      position: 'absolute',
      width: $('#rating-container').width(),
      height: $('#rating-container').innerHeight(),
      top: position.top,
      left: position.left,
      background: '#FFFFFF',
      opacity: '0.5',
      zIndex: 9999
    }).appendTo('body');

    var  comment = {
      username : $('#username').val(),
      rating : $('#rating-container').find('.fa-star').length,
      text : $('#comment-box').val()
    }
  
    pathname = window.location.pathname;

    $.ajax({
      type: 'POST',
      url: pathname + '/comment',
      data: JSON.stringify(comment),
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        self.html('Send');
        $('#comment-overlay').remove();
        
        if (result.error) {
          $('body').append(result.error);
          setTimeout(function() {
            $('.error').removeClass('active');
          }, 3000);
        }

        if (result.rate) $('.star-rating').html(result.rate);
       
        if (result.comments) {
          if ($('.comment').length > 0) {
            $(result.comments).insertBefore('.comment:first-child').hide().slideDown();
          } else {
            $(result.comments).appendTo('#comments-container').hide().slideDown();
          }

          $('#username').val('');
          $('#comment-box').val('');
          $('#rating-container i').trigger('mouseleave');
        }
      }
    })
  });

  $(document).on('animationend', function(e) {
    if (e.originalEvent.animationName == 'slideUp') {
      $(e.target).remove();
    }
  });
});
