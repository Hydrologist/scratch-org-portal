$(document).ready(function(){
  /*$.ajax({
    url: ,
    type: "GET",
    success: function(response) {
      
    },
    error: function(xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText);
    }
  })*/
  $('#create-button').click(function() {
    let clicked_button = $(this);
  });
}) // end $(document).ready()

function create_org() {
  $('#create-button').addClass('hide');
  $('#create-spinner').removeClass('hide');
  $('#create-title').html('Creating Scratch Org...');
  $.ajax({
    url: "create/",
    type: "POST",
    success: function (result) {
      console.log(result);
      $('#create-card').after(result);

      $('#create-title').html('Scratch Org Created.');
      $('#create-button').html('Create another Scratch Org');
      $('#create-button').removeClass('hide');
      $('#create-spinner').addClass('hide');
    },
    error: function (xhr, errmsg, err) {
      $('#create-title').html('Error!');
      $('#create-spinner').addClass('hide');
      $('#create-error').html(errmsg);
      $('#create-error').removeClass('hide');
      console.log(xhr.status + ": " + xhr.responseText);
    }
  });
}