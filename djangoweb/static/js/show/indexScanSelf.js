//用户自查页面
function get_querySelf(){
	get_html("/querySelf.html", set_first_html);
}
function set_first_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
		get_querySelf_data();
	}
}


function get_querySelf_data(){	//获取用户数据
		//$(".bottom").html("");
		var url_data = get_url_data();
		var page =1;
		var data = {"userAcc": url_data["userAcc"],"page":page};
		jquery_ajax("/selfcheck/get_selfcheck_data", data,set_querySelf_data);
	}

function set_querySelf_data(ret){
	if(String(ret) != "undefined") {
	var url_data = get_url_data();
	 $("#department").text(ret["selfcheck_fun_data"][0]["departmentName"]);
	 $("#city").text(ret["selfcheck_fun_data"][0]["city"]);
	 $("#province").text(ret["selfcheck_fun_data"][0]["province"]);
	 $("#userDepart").text(ret["selfcheck_fun_data"][0]["departmentName"]);
     $("#userName").text(ret["selfcheck_fun_data"][0]["userName"]);   //用户名信息
	 $("#partNum").text(ret["selfcheck_fun_data"][0]["departmentName"]);//部门信息
	 $("#jobNum").text(url_data["userAcc"]);  //工号
	 if (ret["selfcheck_fun_data"][0]["loginStatus"] == 0){
	 	$("#onlinestatus").text("未在线!");
	 	$("#onlinestatus").css("color","red");
	 }else if(ret["selfcheck_fun_data"][0]["loginStatus"] == 1){
	 	$("#onlinestatus").text("在线!");
	 	$("#onlinestatus").css("color","green");
	 }else{
	 	$("#onlinestatus").text("Unknow!");
	 } 
	 $("#macNum").text(ret["selfcheck_fun_data"][0]["hostMac"]);
	 $("#ipNum").text(ret["selfcheck_fun_data"][0]["userIp"]);
	 if (String(ret["selfcheck_fun_data"][0]["userScanStatus"]) == "0"){
	 $("#scanbutton").val("自查扫描");
	 }else if(ret["selfcheck_fun_data"][0]["loginStatus"] == 1){
	 if(String(ret["selfcheck_fun_data"][0]["userScanStatus"]) == "1"){
		$("#scanbutton").val("正在扫描...");
		$("#loadingClass").addClass("glyphicon glyphicon-refresh glyphicon-refresh-animate");
	}
}
	//alert(String(ret["selfcheck_fun_data"][0]["userScanStatus"]));
	 can_scan_file(ret);
	}
	 else{
			$(".data").html("<span style='color:red;'>用户数据有误</span>");
		}
}

function can_scan_file(ret){
	$("#scanbutton").click(function (){
	if (ret["selfcheck_fun_data"][0]["loginStatus"] == 0) {
		 dialogAlert("用户未在线，请登陆后重试！", false, []);
	}else if(ret["selfcheck_fun_data"][0]["loginStatus"] == 1){
			if (String(ret["selfcheck_fun_data"][0]["userScanStatus"]) == "0"){ 
		    scan_file(this,0);
		}else if (String(ret["selfcheck_fun_data"][0]["userScanStatus"]) == "1") {
			scan_file(this,1);
			}
		}
	});
}

function scan_file(elem, status){	//扫描用户文件
	if(status == 0){
		var url_data = get_url_data();
		var user_no = url_data["userAcc"];
		var scan_time = get_current_time();
		var data = {"user_no": user_no, "status": status, "scan_time": scan_time};
		$("#scanbutton").val("正在扫描...");
		$("#loadingClass").addClass("glyphicon glyphicon-refresh glyphicon-refresh-animate");
		jquery_ajax("/index/scan_self", data, scan_file_sucess);
	}else if(status == 1){
		dialogAlert("正在扫描用户文件请等待！", false, []);
	}
}

function scan_file_sucess(ret){
	if(ret == false){
		get_querySelf();
		dialogAlert("扫描用户文件失败， 请稍后重试！", false, []);
	}else{
		dialogAlert("扫描指令成功下达，正在扫描，请你稍等！", false, []);
        fresh_page();
	}
	
}

function fresh_page(){
	var url_data = get_url_data();
		var page =1;
		var data = {"userAcc": url_data["userAcc"],"page":page};
		jquery_ajax("/selfcheck/get_selfcheck_data", data,set_fresh_page);
}

function set_fresh_page(ret){
	setTimeout(function() {
    var status = String(ret["selfcheck_fun_data"][0]["userScanStatus"]);
	if (status =="0"){
	//dialogAlert("扫描已完成，请在报警记录中查询！", get_querySelf, []);
	confirmAlert("扫描已完成，需要在报警记录中查看吗？", get_user_query, get_querySelf,[], []);
	clearTimeout(this);
}else{
fresh_page();
}
}, 5000);
}
//添插用户查询记录列表
function get_user_query(){
	//get_html("/userQuery.html", set_query_html);
	get_html("/userQueryCount.html", set_query_count_html);
}

function set_query_count_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
		get_user_query_count_data();
	}
}

function get_user_query_count_data(){	//获取查询记录条数数据
		$("#LoadingBar").show();
		$(".bottom").html("");
		var url_data = get_url_data();
		var page = $("#page").text();
		if (page == "") {
			page = 1;
		}
		var city = $("#city").text();
		var data = {"userAcc": url_data["userAcc"], "page": page};
		jquery_ajax("/selfcheck/get_selfcheck_count_data", data, set_user_query_count_data);
}

function set_user_query_count_data(ret){
	var html = "";
	if(String(ret) != "undefined") {
		$("#countErr").text(ret["count"]);
		if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
		}
		var timeSpan = "";
		var scanTime = "";
		for (var i = 0; i < ret["selfcheck_count_data"].length; i++) {
				html += "<tr><td><input class='record_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;' id='"+ret["selfcheck_count_data"][i]["scanTime"]+"'>"+ (i + 1 + (parseInt($("#page").text()) - 1) * 20) +" </td>"; //序号
				html += "<td> "+ ret["selfcheck_count_data"][i]["scanTime"] +" </td>";
				html += "<td> "+ ret["selfcheck_count_data"][i]["scanCount"] +" </td>";
				scanTime = ret["selfcheck_count_data"][i]["scanTime"];
				timeSpan = scanTime.substr(9,10) + " " + scanTime.substr(0,8) + "|";
				html +="<td><input type='button' onclick='get_user_detail_query(this)' value='查看详情' class='btn btn-info btn-sm'>&nbsp;&nbsp;&nbsp;<input type='button' onclick='delTimeSpanQueryData(\""+timeSpan+"\")' value='删除' class='btn btn-danger btn-sm'></td></tr>";
			}
	$("#userQuery").html(html);
	$("[data-toggle='popover']").popover();
		}else{
		$("#userQuery").html("<span style='color:red;'>用户数据有误</span>");
	}
	$("#LoadingBar").css('display','none'); 
}

function delTimeSpanQueryData(elem){
	confirmAlert("您确定要对这些记录进行删除操作？", deleteTimeSpan_mulrecord_data, false, [elem, ], []);
}

function delTimeSpanMulRecord() {
	var delete_record = "";
	$(".record_check").each(function(){
		if($(this).attr("checked") == "checked"){
			var timeSpan = $(this).attr("id").substr(9,10) + " " + $(this).attr("id").substr(0,8) + "|";
			delete_record += timeSpan;
		}
	});
	if(delete_record != ""){
		confirmAlert("您确定要对这些记录进行删除操作？", deleteTimeSpan_mulrecord_data, false, [delete_record, ], []);
	}else{
		dialogAlert("您没有选中任何记录!", false, []);
	}
}

function deleteTimeSpan_mulrecord_data(elem) {
	var urlData = get_url_data();
	jquery_ajax("/selfcheck/delete_timespan_data", {"record_list": elem[0], "user_acc": urlData["userAcc"]}, delTimeSpan_query_data_sucess);
}

function delTimeSpan_query_data_sucess(ret){
	if(ret == true){
		dialogAlert("删除成功！", false, []);
		get_user_query_count_data();
	}else{
		dialogAlert("您的操作有误,请稍后重试！", false, []);
	}
}

function get_user_detail_query(elem){
	get_html("/userQuery.html", set_query_html);
	var scanTime = $(elem).parent().parent().children("td").eq(1).text();
	var date = scanTime.substr(10,10);
	var time = scanTime.substr(1,8);
	scanTime = date + " " + time;
	if(scanTime != null){
	$('#scanTime').text(scanTime);
	}
	get_user_query_data();
}

function set_query_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
		//get_user_query_data();
	}
}
function get_user_query_data(){	//获取查询记录数据
		$("#LoadingBar").show();
		$(".bottom").html("");
		var url_data = get_url_data();
		var page = $("#page").text();
		if (page == "") {
			page = 1;
		}
		var scanTime = $("#scanTime").text();
		var data = {"userAcc": url_data["userAcc"], "page": page,"scanTime":scanTime};
		jquery_ajax("/selfcheck/get_selfcheck_data", data, set_user_query_data);
}

function user_check_click(elem){
	if($(elem).attr("checked") != "checked"){
		$(elem).attr("checked", "checked");
	}else{
		$(elem).removeAttr("checked");
	}
}

function set_user_query_data(ret){
	var html = "";
	/*$("#department").text(ret["selfcheck_fun_data"][0]["departmentName"]);
	 $("#city").text(ret["selfcheck_fun_data"][0]["city"]);
	 $("#province").text(ret["selfcheck_fun_data"][0]["province"]);
	 $("#userDepart").text(ret["selfcheck_fun_data"][0]["departmentName"]);
     $("#userName").text(ret["selfcheck_fun_data"][0]["userName"]);*/
	if(String(ret) != "undefined") {
		$("#countErr").text(ret["count"]);
		if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
		}
		var usId=new Array();
		for (var i = 0; i < ret["selfcheck_data"].length; i++) {
				if($('#selectTimeLabel').text() == "1") {
					if(ret["selfcheck_data"][i]["scanTime"] != ret["selfcheck_data"][0]["scanTime"]) {
						$("#page").text(1);
						$("#pageCount").text(Math.ceil(i / 20));
						$("#countErr").text(i);
						break;
					}
				}
				var start = ret["selfcheck_data"][i]["keywords"].indexOf("-",0); 
				var end = ret["selfcheck_data"][i]["keywords"].indexOf("-",2); 
				var keyword = ret["selfcheck_data"][i]["keywords"].substr(start + 1,end - start - 1);
				var keywordDetail = "级别：" + ret["selfcheck_data"][i]["keywords"].substr(0,1) + "  关键字：" + keyword + "  重复次数：" + ret["selfcheck_data"][i]["keywords"].substr(end + 1,ret["selfcheck_data"][i]["keywords"].indexOf(" ",0) - end - 1);
				usId[i]=ret['selfcheck_data'][i]['usId'];
				html += "<tr><td><input class='record_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;' id='"+usId[i]+"'>"+ (i + 1 + (parseInt($("#page").text()) - 1) * 20) +" </td>"; //序号
				//html += "<tr><td> "+ ret["selfcheck_data"][i]["userIp"] +" </td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["selfcheck_data"][i]["fileName"]+"'>"+ret["selfcheck_data"][i]["fileName"]+"</td><td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["selfcheck_data"][i]["filePath"]+"'>"+ret["selfcheck_data"][i]["filePath"]+"</td><td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+keywordDetail+"'>"+keyword+"</td>";
				html +="<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["selfcheck_data"][i]["keyExtend"]+"'>"+getSingleKeyWord(ret["selfcheck_data"][i]["keywords"],ret["selfcheck_data"][i]["keyExtend"],2)+"</td><td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["selfcheck_data"][i]["scanTime"]+"'>"+ret["selfcheck_data"][i]["scanTime"]+"</td>";
				html +="<td><input type='button' onclick='delQueryData("+usId[i]+")' value='删除' class='btn btn-danger btn-sm'></td></tr>";
			}
	$("#userQuery").html(html);
	$("[data-toggle='popover']").popover();
		}else{
		$("#userQuery").html("<span style='color:red;'>用户数据有误</span>");
	}
	$("#LoadingBar").css('display','none'); 
}

function selectTime() {
	var selection = $('#selectTime option:selected').text();//选中的文本
		if(selection == "所有记录") {
			$('#selectTimeLabel').text(0);
		} else if(selection == "最新记录") {
			$('#selectTimeLabel').text(1);
		}
	get_user_query_data();
}

function getSingleKeyWord(keyWords,keyExtend,type) {  //keyWords为关键字原文，keyExtend为关键字上下文
	if(keyExtend == null){
		return keyExtend;
	}else{
	if(type == 1) {
		var start = keyWords.indexOf("关键字",0); 
		var end = keyWords.indexOf("重复次数",0); 
		var keyword = keyWords.substr(start + 4,end - start - 5); //得到关键字
		if(keyword != null){
		var keyPos = keyExtend.indexOf(keyword);  //关键字在关键字上下文中的位置
		}else{
			return keyExtend;
		}
		var keyLevel = keyWords.substr(keyWords.indexOf("级别") + 3,1); //关键字级别
	} else if(type == 2) {
		var start = keyWords.indexOf("-",0); 
		var end = keyWords.indexOf("-",2); 
		var keyword = keyWords.substr(start + 1,end - start - 1); //得到关键字
		
		var keyPos = keyExtend.indexOf(keyword);  //关键字在关键字上下文中的位置
		var keyLevel = keyWords.substr(0,1); //关键字级别
	}
	var first = keyExtend.substr(0,keyPos);
	if(keyLevel == "0") {
		var second = "<font color='#ff0000' style='font-weight:900' size='3px'>" + keyword + "</font>";
	} else if(keyLevel == "1") {
		var second = "<font color='#ffaa25' style='font-weight:900' size='3px'>" + keyword + "</font>";
	} else if(keyLevel == "2") {
		var second = "<font color='#41a62d' style='font-weight:900' size='3px'>" + keyword + "</font>";
	}	
	var thirdLen = keyExtend.length - first.length - keyword.length; //最后一段长度
	var third = keyExtend.substr(keyPos + keyword.length,thirdLen);
	return first + second + third;
}
}

function delMulRecord() {
	var delete_record = "";
	$(".record_check").each(function(){
		if($(this).attr("checked") == "checked"){
			delete_record += $(this).attr("id") + "|";
		}
	});
	if(delete_record != ""){
		confirmAlert("您确定要对这些记录进行删除操作？", delete_mulrecord_data, false, [delete_record, ], []);
	}else{
		dialogAlert("您没有选中任何记录!", false, []);
	}
}

function delete_mulrecord_data(elem) {
	var urlData = get_url_data();
	jquery_ajax("/selfcheck/delete_mulrecord_data", {"record_list": elem[0], "user_acc": urlData["userAcc"]}, del_query_data_sucess)
}

function delQueryData(elem){
	//alert(typeof elem);
	//confirmAlert(message, ok_fun, no_fun, elem_ok, elem_no);
	confirmAlert("确定操作吗？", ok_delQueryData, false, elem, []);
	//var urlData = get_url_data();
	
}

function ok_delQueryData(elem){
	jquery_ajax("/selfcheck/set_selfcheck_data", {"usId": elem}, del_query_data_sucess);
}

function del_query_data_sucess(ret){
	if(ret == true){
		dialogAlert("删除成功！", false, []);
		get_user_query_data();
	}else{
		dialogAlert("您的操作有误,请稍后重试！", false, []);
	}
}
function queryBefore(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		get_user_query_data();
	}
}
function queryAfter(){
	var pageCount = $("#pageCount").text();
	var page = $("#page").text();
	if(page.toString() == pageCount.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		get_user_query_data();
	}
}

function queryCountBefore(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		get_user_query_count_data();
	}
}
function queryCountAfter(){
	var pageCount = $("#pageCount").text();
	var page = $("#page").text();
	if(page.toString() == pageCount.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		get_user_query_count_data();
	}
}
function queryspanCountSelectClick(elem){
	spanClick(set_user_query_count_data, [elem, ]);
}
function querySpanClick(elem){
	spanClick(set_user_query_data, [elem, ])
}
function queryspanSelectClick(elem){	//用户报警信息页面翻页
	spanClick(set_user_query_data, [elem, ]);
}
function userspanSelectClick(elem){	//用户报警信息页面翻页
	spanClick(get_user_query_data, [elem, ]);
}

function get_passwdChange(){
	$("#LoadingBar").show();
	get_html("/passwdChange.html", set_passwd_html);
}
function set_passwd_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
	}
	$("#LoadingBar").css('display','none');
}

function oldPwd_check(){
	var url_data = get_url_data();
	var userName = url_data["userAcc"];
	var passwd = $("input[name='oldPasswd']").val();
	var data = {"userName": userName, "passwd": passwd};
			jquery_ajax("/login/user_login", data, check_oldPwd);
	}

function check_oldPwd(ret){
	if(ret == undefined){
		dialogAlert("系统验证错误!", false, []);
	}else{
		if(ret.toString() == "false"){
			dialogAlert("请输入正确的原密码!", false, []);
			get_passwdChange();
		}else{
			$("#oldPassMsg").text("已验证!");		
		}
	}
}

 function passwd_check(){
  var passbool = true;
  //var check_oldPwd = $("#oldPassMsg").text();
  //var oldPasswd = $("input[name='oldPasswd']").val();
  var newPasswd = $("input[name='newPasswd']").val();
  var newPasswdRep = $("input[name='newPasswdRep']").val(); 
  if(newPasswd =="") {
    passbool = false;
    $("#newPassMsg").text("*新密码为空，请检查后再修改");  
  } 
  if(newPasswdRep == ""){
  	passbool = false;
  	$("#newPassRepMsg").text("*新密码为空，请检查后再修改");
  }
  if(newPasswd != newPasswdRep ){
    passbool = false;
    //$("input[name='passwd']").css("border-color", "#f33");
    $("#newPassMsg").text("*两次新密码不一致!");
    $("#newPassRepMsg").text("*两次新密码不一致!");
  }
  return passbool;
}

function passwd_Sub(){
	var oldPasswd = $("input[name='oldPasswd']").val();
    ret = passwd_check();
	if(oldPasswd == "") {
		dialogAlert("请输入正确的原密码!", false, []);
	} else {
		if (ret == true) {
        //$("form".submit());
		var newPasswd = $("input[name='newPasswd']").val();
		var url_data = get_url_data();
		var userAcc =  url_data["userAcc"];
		var data = {"userAcc": userAcc, "passwd": newPasswd};
			jquery_ajax("/selfcheck/set_newpasswd", data, change_oldPwd);
    }else{
	  dialogAlert("提交表单失败!", false, []);
      //alert("提交表单失败！");
      return false;
    }
  }   
}

function change_oldPwd(ret){
	if(ret == undefined){
		dialogAlert("系统验证错误!", false, []);
	}else{
		if(ret.toString() == "false"){
			dialogAlert("密码修改错误!", false, []);
			get_passwdChange();
		}else{
			dialogAlert("修改成功!", url_to_login, []);
			
		}
	}
}

function url_to_login(){
	window.location.href = "/loginScanSelf";
}

function btnreset_ok(){
	$("#oldPassMsg").text("");
	$("#newPassMsg").text("");
    $("#newPassRepMsg").text("");
}

function aboutClick(){
	$("#LoadingBar").show();
	get_html("/about", set_about_html);	//获取about页面
}

function set_about_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
	}
	$("#LoadingBar").css('display','none'); 
}
function quit_sucess(ret){
	window.location.href = "/loginScanSelf";
}
function quit(){
	jquery_ajax('/index/quit', {}, quit_sucess);
}

function clearn_index_style(){	//清除index的样式
	$(".index div").each(function(){
		$(this).css("background-color", "rgb(12, 124, 183)");
	})
}

$(function(){
	get_querySelf();
	$(".index div").click(function(){
		clearn_index_style();
		$(this).css("background-color", "#01263a");
	});
});


function selectAll() {
	if(document.getElementById("selectAll").checked == true) {
		$("input[type='checkbox']").prop("checked",true);
		$("input[type='checkBox']").attr("checked","true"); 
		
		$("input[disabled='disabled']").prop("checked", false);
		$("input[disabled='disabled']").removeAttr("checked");
	} else {
		$("input[type='checkbox']").prop("checked", false);
		$("input[type='checkBox']").removeAttr("checked");
	}
}