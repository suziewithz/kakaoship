function sendFileToServer(formData,status)
{
	startProgress();
    var uploadURL ="/upload"; //Upload URL
    var extraData ={}; //Extra Data.
    var jqXHR=$.ajax({
	    url: uploadURL,
	    type: "POST",
	    contentType:false,
	    processData: false,
	    cache: false,
	    data: formData,
	    success: function(data){
	        location.href = "/chart/" + data;
	    },
	    failure: function(data) { 
	        alert('Got an error dude');
	    }
    }); 
 
}

function handleFileUpload(files,obj)
{        var fd = new FormData();
        fd.append('file', files);
        sendFileToServer(fd,status);
}
$(document).ready(function()
{
	var obj = $("#holder");
	obj.on('dragenter', function (e) 
	{
	    e.stopPropagation();
	    e.preventDefault();
	    setCircleLine('on');
	});
	obj.on('dragover', function (e) 
	{
	     e.stopPropagation();
	     e.preventDefault();
	});
	obj.on('drop', function (e) 
	{
		setCircleLine('off');
	     e.preventDefault();
	     var files = e.originalEvent.dataTransfer.files[0];
	 
	     //We need to send dropped files to Server
	     handleFileUpload(files,obj);
	});
	$(document).on('dragenter', function (e) 
	{
	    e.stopPropagation();
	    e.preventDefault();
	});
	$(document).on('dragover', function (e) 
	{
	  e.stopPropagation();
	  e.preventDefault();
	  setCircleLine('on');
	});
	$(document).on('drop', function (e) 
	{
	    e.stopPropagation();
	    e.preventDefault();
	});
 
});
function setCircleLine(str){
	if(str == "on"){
		$('.circle').css("background-color","#444F5C");
	}else{
		$('.circle').css("background-color","#E5E5E5");
	}
}