// JavaScript Document
function keyupgo(){
		 $(document).keyup(function(e){
			if (e.keyCode == 13) 
			{
				if(document.activeElement.id == "userName") {
						$("#userName").blur();
						$("#passwd").focus();
						return;
					}
					if(document.activeElement.id == "passwd") {
						$("#passwd").blur();
						$("#verficationCodeData").focus();
						return;
					}
					if(document.activeElement.id == "verficationCodeData") {
						$("#verficationCodeData").blur();
						$("#input").focus();
						$("#input").click();
						return;
					}
    } 
	return;

})
}
function inp_reset(){	//页面重置
	$("#userName").val("");
	$("#passwd").val("");
	$("#verficationCodeData").val("");
	get_verification_code();
}

function user_login(ret){	//用户登陆跳转
	if(ret == undefined){
		dialogAlert("请输入正确的用户名或密码!", inp_reset, []);
	}else{
		if(ret.toString() == "false"){
			dialogAlert("请输入正确的用户名或密码!", inp_reset, []);
		}else if(ret.toString() == "-1"){
			dialogAlert("您输入的用户没有登陆的权限， 如有问题请联系超级管理员！", inp_reset, []);
		}else{
			window.location.href = "/index/userAcc=" + $(".userName").val()
		}
	}
}

function set_verifucation_code(ret){	//设置验证码
	if(ret != undefined){
		$("#verficationCode").attr("src", ret["img"]);
		$("#verficationCode").attr("code", ret["value"]);
	}

}



$(function(){
	get_verification_code();

	$("#input").click(function(){
		var userName = $("#userName").val();
		var passwd = $("#passwd").val();
		var verficationCodeData = $("#verficationCodeData").val();
		var verficationCode = $("#verficationCode").attr("code");
		/*var check_result = check_user_login(userName, passwd, verficationCodeData, verficationCode);
		if(check_result ==false){
			dialogAlert("请输入正确的用户名或密码!", inp_reset, []);
		}else{
			var data = {"userName": userName, "passwd": passwd};
			jquery_ajax("/login/user_login", data, user_login);
		}*/
		if(userName == "" ) {
			dialogAlert("请输入用户名", inp_reset, []);
		} else if(passwd == "") {
			dialogAlert("请输入密码", inp_reset, []);
		} else if(verficationCodeData == "") {
			dialogAlert("请输入验证码", false, []);
		} else if(verficationCodeData.toUpperCase() != verficationCode.toUpperCase()) {
			dialogAlert("验证码输入错误", false, []);
			$("#verficationCodeData").val("");
			get_verification_code();
		} else {
			var data = {"userName": userName, "passwd": passwd};
			jquery_ajax("/login/user_login", data, user_login);
		}
	});
	keyupgo();
});