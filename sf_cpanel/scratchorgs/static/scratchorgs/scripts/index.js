$(document).ready(function(){
  $('#create-form').on('submit', create_org);
  $('.generate-password-button').click(function() {
    generate_password($(this).attr('data-userid'));
  })
  $('.user-login-button').click(function() {
    user_login($(this).attr('data-userid'), $(this).attr('data-username'));
  })
  $('.delete-button').click(function () {
    let clicked_button = $(this);
    open_delete_modal(clicked_button.attr('data-orgid'));
  });
  $('#delete-modal-agree-button').click(function () {
    delete_org($(this).attr('data-orgid'));
  });
}) // end $(document).ready()

function create_org(event) {
  event.preventDefault();

  const csrftoken = Cookies.get('csrftoken');
  $('#create-form-wrapper').addClass('hide');
  $('#create-form-loader').removeClass('hide');

  modal = M.Modal.getInstance($('#create-modal').get(0));

  $.ajax({
    url: 'create/',
    type: 'POST',
    data: jQuery.param({ 'alias': $('#create-form-alias').val() }),
    headers: {'X-CSRFToken': csrftoken},
    success: function (result) {
      $('#create-button-wrapper').after(result);

      $('#create-form-wrapper').removeClass('hide');
      $('#create-form-loader').addClass('hide');
      
      reset_modal();
      modal.close();
    },
    error: function (xhr, errmsg, err) {
      $('#create-form-loader').addClass('hide');

      $('create-form-error-details').html(xhr.status + ": " + xhr.responseText);
      $('#create-form-error').removeClass('hide');
    },
    complete: function() {
      $('#create-form-alias').val('');
    }
  });

  function reset_modal() {
    $('#create-form-error').addClass('hide');
    $('#create-form-loader').addClass('hide');
    $('#create-form-wrapper').removeClass('hide');

    $('#create-form-alias').val('');
  }
}

function generate_password(user_id) {
  const csrftoken = Cookies.get('csrftoken');

  $('#generate-password-button-' + user_id).addClass('hide');
  $('#generate-password-spinner-' + user_id).removeClass('hide');

  $.ajax({
    url: 'users/' + user_id + '/generate/',
    type: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    success: function (result) {
      $('#user-password-' + user_id).html(result);
    },
    error: function (xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText);
    },
    complete: function () {
      $('#generate-password-spinner-' + user_id).addClass('hide');
    }
  });
}

function user_login(user_id) {
  $('#user-login-button-' + user_id).addClass('hide');
  $('#user-login-spinner-' + user_id).removeClass('hide');

  $.ajax({
    url: 'users/' + user_id + '/login/',
    type: 'GET',
    success: function (result) {
      window.open(result, '_blank');
    },
    error: function (xhr, errmsg, err) {
      console.log(xhr.status + ": " + xhr.responseText);
    },
    complete: function () {
      $('#user-login-button-' + user_id).removeClass('hide');
      $('#user-login-spinner-' + user_id).addClass('hide');
    }
  });
}

function open_delete_modal(org_id) {
  $('#delete-modal-agree-button').attr('data-orgid', org_id);
  $('#delete-modal-title').html('Are you sure?');
  $('#delete-modal-text').html('Do you want to delete this scratch org?');
  $('#delete-modal-agree-button').removeClass('hide');
  $('#delete-modal-disagree-button').removeClass('hide');
  $('#delete-modal-close-button').addClass('hide');
  $('#delete-modal-spinner').addClass('hide');
}

function delete_org(org_id) {
  $('#delete-modal-agree-button').addClass('hide');
  $('#delete-modal-disagree-button').addClass('hide');
  $('#delete-modal-spinner').removeClass('hide');
  $.ajax({
    url: org_id + '/delete/',
    type: "POST",
    success: function (response) {
      $('#delete-modal-title').html('Success!');
      $('#delete-modal-text').html('The page will now refresh.');
      setTimeout(function() {
        document.location.reload();
      }, 2000)
    },
    error: function (xhr, errmsg, err) {
      $('#modal-title').html('Error!');
      $('#modal-text').html(errmsg);
      console.log(xhr.status + ": " + xhr.responseText);
    },
    complete: function(){
      $('#delete-modal-spinner').addClass('hide');
      $('#delete-modal-close-button').removeClass('hide');
    }
  });
}