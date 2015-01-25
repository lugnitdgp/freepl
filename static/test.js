$(document).ready(function() {
$("#button").click(function() {
var name_string = $("#name").val();
var password_string = $("#password").val();
$.ajax({
url : "/ajaxexample_json",
type : "POST",
dataType: "json",
data : {
name : name_string,
passwd : password_string,
csrfmiddlewaretoken: '{{ csrf_token }}'
},
success : function(hill) {location.href="/qwe";
//$('#result').append( 'Server Response: ' + hill.server_response);
//var form=$('#limit').val('My Submit');
$(form).submit();
},
error : function(xhr,errmsg,err) {
alert(xhr.status + ": " + xhr.responseText);
}
});
return false;
});
});
