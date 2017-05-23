//提示框模板函数
function dialogAlert(message, fun, elem){
	var dialogInstance = BootstrapDialog.show({
		title: '互联网终端保密监管平台',
		message: message,
		type: BootstrapDialog.TYPE_WARNING,
		buttons: [
		{
			label: '关闭',
			cssClass: 'btn-warning',
			action: function(dialogItself){
                if(fun != false){
                    fun(elem)
                }
				dialogItself.close();
			}
		  }
		]
	});
}

//确认框提示函数
function confirmAlert(message, ok_fun, no_fun, elem_ok, elem_no){
	BootstrapDialog.show({
	    title: "互联网终端保密监管平台",//'确认框'
	    message: message,//'确认删除吗？'
	    buttons: [{
	        label: "确认",//'确认'
	        // no title as it is optional
	        cssClass: 'btn-primary',
	        action: function(dialogItself){
	        	if(ok_fun != false){
	        		ok_fun(elem_ok)
	        	}
	            dialogItself.close();
	        }
	    }, {
	        label: "取消", //'取消'
	        cssClass: 'btn-warning',
	        action: function(dialogItself){
	        	if(no_fun != false){
	        		no_fun();
	        	}
	            dialogItself.close();
	        }
	    }]
	});
}
