
$(document).ready( () => {
  //Everything here is going to be loaded after the DOM is load
  console.log("Everything is ready.");
  //Ajax method to submit a POST-request entry
  $('#submit-btn').click( function(e){
    titleEntry = $('#id_title_entry').val();
    contentPage = $('#id_content').val();
    //This is to obtain the csfrtoken in order to make the request
    var csrftoken = Cookies.get('csrftoken');
    $.ajax({
      type : 'POST',
      url: 'newentry',
      dataType: 'json',
      headers:{
        "X-CSRFToken": csrftoken
      },
      contentType: 'application/json',
      data : { title : 'TITLE', content : 'contenido' },
      success: function (){
        alert('Entry saved!!');
        }
    }); //end ajaxPost
      e.preventDefault();
  });

  //Add a with href to edit page
  pageTitle = document.title;
  firstParagraph = $('p').first();
  editBtn = document.createElement('a');
  editBtn.innerHTML = 'Edit page';
  editBtn.className = 'btn btn-info float-right mr-3';
  editBtn.id = 'editBtn'
  $(editBtn).attr("href", '/wiki/editentry/'+pageTitle)
  $(editBtn).insertBefore(firstParagraph);

  //change style to message error in editEntry
  $('.alert-danger').css('display', 'inline-block');
  $('.alert-danger').css('font-size', '18px')
});
