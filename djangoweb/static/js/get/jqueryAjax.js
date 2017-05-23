function jquery_ajax(url, data, sucess_function){
    $.ajax({
			type: "post",
			url: url,
			dataType: "json",
			data:data,
			async:true,
			success: function (ret) {
                if(sucess_function != false){
                    sucess_function(ret);
                }
            }
		});
}

function jquery_ajax_get(url, data, sucess_function){
    $.ajax({
			type: "get",
			url: url,
			dataType: "json",
			data:data,
			async:false,
			success: function (ret) {
                if(sucess_function != false){
                    sucess_function(ret);
                }
            }
		});
}