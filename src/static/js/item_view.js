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
    $('<div></div>').css({  
      position: 'absolute',
      width: '100%',
      height: '100%',
      top: 0,
      left: 0,
      background: '#ccc',
      opacity: '0.5'
    }).appendTo($(this).closest('div').closest('div').closest('div'));

    var  comment = {
      username : $('#username').val(),
      rating : $('#rating-container').find('.fa-star').length,
      comment : $('#comment-box').val()
    }

    $.ajax({
      type: 'POST',
      url: '/books/1/comment',
      data: JSON.stringify(comment),
      contentType: 'application/json;charset=UTF-8',
      success: function(result) {
        console.log(result);
        //self.html('Send');
      }
    })
  });

});
