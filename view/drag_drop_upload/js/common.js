function sendFileToServer(formData,status)
{
	alert('file upload');
	return;
	
    var uploadURL ="test.com/check"; //Upload URL
    var extraData ={}; //Extra Data.
    var jqXHR=$.ajax({
            xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                    xhrobj.upload.addEventListener('progress', function(event) {
                        var percent = 0;
                        var position = event.loaded || event.position;
                        var total = event.total;
                        if (event.lengthComputable) {
                            percent = Math.ceil(position / total * 100);
                        }
                        //Set progress
                        status.setProgress(percent);
                    }, false);
                }
            return xhrobj;
        },
    url: uploadURL,
    type: "POST",
    contentType:false,
    processData: false,
        cache: false,
        data: formData,
        success: function(data){	 
            status.setProgress(100);
            $("#status1").append("File upload Done<br>");         
        }
    }); 
 
}

function createStatusbar(obj)
{
     this.statusbar = $("<div class='statusbar'></div>");
     this.progressBar = $("<div class='progressBar'><div></div></div>").appendTo(this.statusbar);
     obj.after(this.statusbar);
 
    this.setProgress = function(progress)
    {       
        var progressBarWidth =progress*this.progressBar.width()/ 100;  
        this.progressBar.find('div').animate({ width: progressBarWidth }, 10).html(progress + "% ");
        if(parseInt(progress) >= 100)
        {
            alert('complete');
        }
    }
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
	    $(this).css('border', '10px dashed #333');
	});
	obj.on('dragover', function (e) 
	{
	     e.stopPropagation();
	     e.preventDefault();
	});
	obj.on('drop', function (e) 
	{
	     $(this).css('border', '10px dashed #ccc');
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
	  obj.css('border', '10px dashed #ccc');
	});
	$(document).on('drop', function (e) 
	{
	    e.stopPropagation();
	    e.preventDefault();
	});
 
});