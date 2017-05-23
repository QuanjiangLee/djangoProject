function check_user_login(userName, passwd, verficationCodeData, verficationCode){
    if(userName == "" || passwd == "" || verficationCodeData == "" || verficationCodeData.toUpperCase() != verficationCode.toUpperCase()){
        return false;
    }
    return true;
}


function get_current_time(){
	var date = new Date();
    var seperator1 = "-";
    var seperator2 = ":";
    var month = date.getMonth() + 1;
    var strDate = date.getDate();
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
            + " " + date.getHours() + seperator2 + date.getMinutes()
            + seperator2 + date.getSeconds();
    return currentdate;
}


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
	        		no_fun(elem_no);
	        	}
	            dialogItself.close();
	        }
	    }]
	});
}


function get_verification_code(){   //获取验证码的图片
    var data = {};
    jquery_ajax("login/indentifying_code", data, set_verifucation_code);
}


function getAbsoluteLeft(elem) {    //获取元素左边的位置
	var oLeft = elem.offsetLeft;
	while(elem.offsetParent!=null) {
		var oParent = elem.offsetParent;
		oLeft += oParent.offsetLeft;
		elem = oParent
	}
	return oLeft
}

function getAbsoluteTop(elem) { //获取元素上边的位置
	var oTop = elem.offsetTop;
	while(elem.offsetParent!=null) {
		var oParent = elem.offsetParent;
		oTop += oParent.offsetTop;
		elem = oParent;
	}
	return oTop;
}


function spanClick(func, elem){ //增加下拉框
	if($(".bottom").html() != ""){
		$(".bottom").html("");
	}else{
		var num = parseInt($("#pageCount").text());
		var div = "<div id='selectPage' style='width:80px; position:absolute; border:1px solid#aaa; border-radius:5px;'><ul>";
		for(var i=0; i< num; i++){
			div += "<li>"+String(i+1)+"</li>"
		}
		div += "</ul></div>";
		$(".bottom").html(div);
		var left = getAbsoluteLeft(elem[0]);
		var top = getAbsoluteTop(elem[0]);
		top= top + 30;
		left = left + 5;
		$('#selectPage').css("left", left);
		$('#selectPage').css("top", top);
		$('#selectPage').css("z-index", 10);
		$('#selectPage').css("max-height", "200px");
		$('#selectPage').css("overflow", "auto");
		$('#selectPage').css("background","#fff");
		$('#selectPage ul li').css("cursor","pointer");
		$('#selectPage ul li').css("margin-top","10px");
		$('#selectPage ul').css("text-align","center");
		$('#selectPage ul').css("padding","0");
		$('#selectPage ul').css("list-style", "none");
		$('#selectPage ul li').hover(function(e){
			$(this).css("background", "#edd");
		},function(){
			$(this).css("background", "#fff");
		});
		$('#selectPage ul li').click(function(){
			$("#selectPage").remove();
			var page = $(this).text();
			$("#page").text(page);
			$("#pageBelow").text($("#page").text());
			if(func != undefined){
				func(page);
			}
		})
	}
}


function get_url_data(){    //获取url参数
    var url = decodeURI(window.location.href); //获取url中"?"符后的字串
	var theRequest = new Object();
	if (url.indexOf("/") != -1) {
        var reg;
		var str = url.split("/")[4];
		var strs = str.split("&");
		for(var i = 0; i < strs.length; i ++) {
			theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
		}
	}
	else
		theRequest = "";
	return theRequest;
}

function get_html(url, func){    //获取外部html页面数据
    $.get(url,function(data) {
        if(func != undefined){
            func(data);
        }
    });
}