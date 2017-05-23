function set_first_html(ret){	//设置首页数据
	$(".bottom").html("");
    if(ret != undefined){
        $("#body").html(ret);
         $("#wPage").text(0);
		get_dep_user_err_Count();
		//setTimeout("get_dep_user_err_Count()","200");
    }   
}

function get_info_data(){	//获取用户数据
		//$(".bottom").html("");
		var url_data = get_url_data();
		var page =1;
		var data = {"userAcc": url_data["userAcc"],"page":page};
		jquery_ajax("/selfcheck/get_selfcheck_data", data,set_info_data);
	}

function set_info_data(ret){
	if(String(ret) != "undefined") {
	var url_data = get_url_data();
	if(ret["selfcheck_fun_data"][0]["province"] == "一级部门") {  //部门信息
		$("#userDep").text("超高级管理员");
	 } else if(ret["selfcheck_fun_data"][0]["city"] == "二级部门") {
		$("#userDep").text(ret["selfcheck_fun_data"][0]["province"]);  
	 } else if(ret["selfcheck_fun_data"][0]["departmentName"] == "三级部门") {
		$("#userDep").text(ret["selfcheck_fun_data"][0]["city"]);  
	 } else{
		$("#userDep").text(ret["selfcheck_fun_data"][0]["departmentName"]);  
	 }
     $("#userManager").text(ret["selfcheck_fun_data"][0]["userName"]);   //用户名信息
	 //$("#userCity").text(ret["selfcheck_fun_data"][0]["city"]);   //市信息
	 $("#province").text(ret["selfcheck_fun_data"][0]["province"]);  //设置默省
	 //if(ret["selfcheck_fun_data"][0]["city"] == "")
	  if($("#isAdmin").text() == "2"){
		 $("#city").text("二级部门");
	 } else {
		 $("#city").text(ret["selfcheck_fun_data"][0]["city"]);  //设置默认市
	 }
	 //if(ret["selfcheck_fun_data"][0]["departmentName"] == "") 
		 $("#department").text("三级部门");
	}else{
		dialogAlert("获取数据有误,请稍后重试！", false, []);
	}
}

function userErrspanClick(elem){	//用户报警信息页面翻页
	spanClick(get_user_error_data, [elem, ]);
}


function get_user_error_data(){	//获取用户异常数据
	var department = $("#department").text();
	if(department == "--请选择--"){
		dialogAlert("请选择部门!", false, []);
	}else {
		$("#LoadingBar").show();
		$(".bottom").html("");
		var url_data = get_url_data();
		var status = 0;
		var page = $("#page").text();

		if ($("#errorStatus").text() == "未处理文件") {
			status = 0;
		} else if ($("#errorStatus").text() == "涉密文件") {
			status = 1;
		} else if ($("#errorStatus").text() == "非涉密文件") {
			status = 2;
		}
		if (page == "") {
			page = 1;
		}
		var province = $("#province").text();
		var city = $("#city").text();
		var startTime = $("#startTime").val();
		var endTime = $("#endTime").val();
		var personName = $("#select_data").val();
		var keyclass = "所有";
		var temp = $("#selectLevel").val();
		if(typeof(temp) != "undefined") {
			keyclass = temp;
		}
		if($("#timeSearch").val() == "1") {
			var data = {"keyclass":keyclass,"startTime":startTime,"endTime":endTime,"userAcc": url_data["userAcc"], "page": page, "status": status, "province":province, "city":city, "department":department};
			jquery_ajax("/index/get_user_error_bytime", data, set_user_error);
		} else if($("#personSearch").val() == "1") {
			var data = {"keyclass":keyclass,"personName":personName,"userAcc": url_data["userAcc"], "page": page, "status": status, "province":province, "city":city, "department":department};
			jquery_ajax("/index/get_user_error_byperson", data, set_user_error);
		} else {
			var data = {"keyclass":keyclass,"userAcc": url_data["userAcc"], "page": page, "status": status, "province":province, "city":city, "department":department};
			jquery_ajax("/index/get_user_error", data, set_user_error);
		}
		$("#selectAll").removeAttr("checked");
	}
}

function target_sucess(ret){
	if(ret == true){
		dialogAlert("操作成功！", false, []);
		get_user_error_data();
	}else{
		dialogAlert("您的操作有误,请稍后重试！", false, []);
	}
}

function targetSecret(){
	var secretId = "";
	$(".err_check").each(function(){
		if($(this).attr("checked") == "checked"){
			secretId += $(this).attr("id")+"|";
		}
	});
	if(secretId == ""){
		dialogAlert("您尚未选中任何报警信息,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}else{
		jquery_ajax("/index/user_error", {"secretId":secretId, "status":1}, target_sucess);
		get_user_error_data()
	}
}


function targetNotSecret(){
	var secretId = "";
	$(".err_check").each(function(){
		if($(this).attr("checked") == "checked"){
			secretId += $(this).attr("id")+"|";
		}
	});
	if(secretId == ""){
		dialogAlert("您尚未选中任何报警信息,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}else{
		jquery_ajax("/index/user_error", {"secretId":secretId, "status":2}, target_sucess);
		get_user_error_data()
	}
}

function delRecord() {
	var secretId = "";
	$(".err_check").each(function(){
		if($(this).attr("checked") == "checked"){
			secretId += $(this).attr("id")+"|";
		}
	});
	if(secretId == ""){
		dialogAlert("您尚未选中任何报警信息,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}else{
		confirmAlert("您确定要对这些记录进行删除操作？", delRecord_data, false, [secretId, ], []);
	}
}

function delRecord_data(elem){
	jquery_ajax("/index/del_user_error", {"secretId":elem[0]}, target_sucess);
	get_user_error_data();
}

function errorMoreClick(){	//首页"报警统计"中"更多"的点击事件
	if($("#errData tr").length == 0){
		dialogAlert("今天没有报警信息 ^_^", false, []);
	}else{
		userErrorCount();
	}
}

/*
function get_dep_user_err_Count(userAcc){	//获取部门人员违规统计的情况
	var data={"userAcc": userAcc};
	jquery_ajax("/index/get_dep_user_count", data, set_dep_user_err_Count);
}
*/

function selectStatus() {
	if($("#selectStatus").val() == "未处理") {
		$("#errStatus").text("0");  //未处理
	} else {
		$("#errStatus").text("1");  //涉密
	}
	if($("#areaLabel").text() != "") { 
		getPage_sec_dep_user_err_Count();
	} else {
		get_dep_user_err_Count();
	}
}

function get_dep_user_err_Count(){	//获取部门人员违规统计的情况
	var department = $("#department").text();
	if(department == ""){
		dialogAlert("请选择部门!", false, []);
	}else{ 
		$("#LoadingBar").show();
		$(".bottom").html("");
		var province = $("#province").text();
		var city = $("#city").text();
		var url_data = get_url_data();
		var page = $("#page").text();
		if (page == "") {
			page = 1;
		}
		var errStatus = 1;
		if($("#errStatus").text() == "0") {
			errStatus = 0;
			$("#selectStatus").val("未处理");
		}
		if(city == "二级部门") {
			$("#platformExplainBody2").show();
			$("#platformExplainBody1").remove();
			var data = {"province":province,"page":page,"errStatus":errStatus }
			jquery_ajax("/index/get_dep_count", data, set_dep_err_Count);
		} else {
			var data = {"userAcc": url_data["userAcc"],"province":province,"city":city,"department":department,"page":page,"errStatus":errStatus }
			jquery_ajax("/index/get_dep_user_count", data, set_dep_user_err_Count);
		}

		
}
}

function set_dep_err_Count(ret){	//设置部门违规统计数据
	var html = "";
	if(ret != undefined){
		if($("#areaLabel").text() != "") { 
			$("#returnBtn").show();
		}
		if($("#wPage").text() == 0){
			//alert(ret["error_data"]);
			if(ret["error_data"].length < 5 ){
			for(var i=0; i<ret["error_data"].length % 5; i++){
				html += "<tr><td>"+ret["error_data"][i]["province"]+"</td>";
				html += "<td>"+ret["error_data"][i]["city"]+"</td>";
				html += "<td valign='middle'><span style='color:red;'>"+ret["error_data"][i]["count"]+"</span></td>";
				html += "<td><button onclick='get_sec_dep_user_err_Count(this)' type='button' class='btn btn-link' style='padding:0;'>查看详情</button></td></tr>";
				}
					}else{
						for(var i=0; i<5; i++){
							html += "<tr><td>"+ret["error_data"][i]["province"]+"</td>";
							html += "<td>"+ret["error_data"][i]["city"]+"</td>";
							html += "<td valign='middle'><span style='color:red;'>"+ret["error_data"][i]["count"]+"</span></td>";
							html += "<td><button onclick='get_sec_dep_user_err_Count(this)' type='button' class='btn btn-link' style='padding:0;'>查看详情</button></td></tr>";
					}
				}
		$("#errData").html(html);
		$("table").css("width", "100%");
	    $("#errData tr td span").popover();
		}else{
			if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
		}
		for(var i=0; i<ret["error_data"].length; i++){
			html += "<tr><td>"+ret["error_data"][i]["province"]+"</td>";
			html += "<td>"+ret["error_data"][i]["city"]+"</td>";
			html += "<td valign='middle'><span style='color:red;'>"+ret["error_data"][i]["count"]+"</span></td>";
			html += "<td><button onclick='get_sec_dep_user_err_Count(this)' type='button' class='btn btn-link' style='padding:0;'>查看详情</button></td></tr>";
		}
	$("#geterrData").html(html);
	$("#countCount").text(ret["count"]);
	$("table").css("width", "100%");
	$("#geterrData tr td span").popover();
	}
	$("#LoadingBar").css('display','none'); 
	}

}

function depErrorCount(){
	get_html("/userErrorCount.html",set_dep_Error_count);
	$("#wPage").text(8);
}
function set_dep_Error_count(ret){	//设置报警统计数据
	$(".bottom").html("");
    if(ret != undefined){
        $("#body").html(ret);
    }
}

function get_sec_dep_user_err_Count(elem){	//获取部门人员违规统计的情况
	depErrorCount();
	if($("#wPage").text() == "8"){
	$("#LoadingBar").show();
	$(".bottom").html("");
	var province = $(elem).parent().parent().children().eq(0).text();
	var city = $(elem).parent().parent().children().eq(1).text();
	var url_data = get_url_data();
	var page = $("#page").text();
	if (page == "") {
		page = 1;
	}
	var errStatus = 1;
	if($("#errStatus").text() == "0") {
		errStatus = 0;
	}
	//$("#selectStatus").hide();
	var data = {"userAcc": url_data["userAcc"],"province":province,"city":city,"department":"三级部门","page":page,"errStatus":errStatus }
	jquery_ajax("/index/get_dep_user_count", data, set_dep_user_err_Count);
}
}
function set_dep_user_err_Count(ret){	//设置部门用户违规统计数据
	var html = "";
	if(ret != undefined){
		if(ret["error_data"].length > 0) {
			$("#areaLabel").text("(" + ret["error_data"][0]["province"] + ")");
		}
		if($("#areaLabel").text() != "") { 
			$("#returnBtn").show();
		}
		if($("#errStatus").text() == "0") {
			$("#selectStatus").val("未处理");
		}
		if($("#wPage").text() == 0){
			//alert(ret["error_data"]);
			if(ret["error_data"].length < 5 ){
			for(var i=0; i<ret["error_data"].length % 5; i++){
				html += "<tr userno='"+ret["error_data"][i]["userNo"]+"'><td>"+ret["error_data"][i]["city"]+"</td>";
				html += "<td>"+ret["error_data"][i]["department"]+"</td>";
				html += "<td>"+ret["error_data"][i]["userName"]+"</td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][i]["hostMAC"].substring(0,ret["error_data"][i]["hostMAC"].length-1)+"'>"+ret["error_data"][i]["hostMAC"].substring(0,17)+"</span></td>";
				html += "<td>"+ret["error_data"][i]["ip"]+"</td>";
				html += "<td valign='middle'><span class='btn btn-link' onclick='error_more_html(this)' style='color:red;'>"+ret["error_data"][i]["count"]+"</span></td></tr>"
				}
					}else{
						for(var i=0; i<5; i++){
							html += "<tr userno='"+ret["error_data"][i]["userNo"]+"'><td>"+ret["error_data"][i]["city"]+"</td>";
							html += "<td>"+ret["error_data"][i]["department"]+"</td>";
							html += "<td>"+ret["error_data"][i]["userName"]+"</td>";
							html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][i]["hostMAC"].substring(0,ret["error_data"][i]["hostMAC"].length-1)+"'>"+ret["error_data"][i]["hostMAC"].substring(0,17)+"</span></td>";
							html += "<td>"+ret["error_data"][i]["ip"]+"</td>";
							html += "<td valign='middle' ><span class='btn btn-link' onclick='error_more_html(this)' style='color:red;'>"+ret["error_data"][i]["count"]+"</span></td></tr>"
					}
				}
		$("#errData").html(html);
		$("table").css("width", "100%");
	    $("#errData tr td span").popover();
		}else{
			if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
		}
		for(var i=0; i<ret["error_data"].length; i++){
			html += "<tr userno='"+ret["error_data"][i]["userNo"]+"'><td>"+ret["error_data"][i]["city"]+"</td>";
			html += "<td>"+ret["error_data"][i]["department"]+"</td>";
			html += "<td>"+ret["error_data"][i]["userName"]+"</td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][i]["hostMAC"].substring(0,ret["error_data"][i]["hostMAC"].length-1)+"'>"+ret["error_data"][i]["hostMAC"].substring(0,17)+"</span></td>";
			html += "<td>"+ret["error_data"][i]["ip"]+"</td>";
			html += "<td valign='middle' ><span class='btn btn-link' onclick='error_more_html(this)' style='color:red;'>"+ret["error_data"][i]["count"]+"</span></td></tr>";
			//html += "<td>"+ret["error_data"][i]["time"]+"</td></tr>"
		}
	$("#geterrData").html(html);
	$("#countCount").text(ret["count"]);
	$("table").css("width", "100%");
	$("#geterrData tr td span").popover();
	}
	$("#LoadingBar").css('display','none'); 
	}

}


function error_more_html(elem){	//查看报警人员详细条数   
   get_html("/errorDataMore.html", set_error_more_html);
	$("#wPage").text(9);
	var errorName = $(elem).parent().parent().children().eq(2).text();
	if(errorName != null){
	$("#errorName").text(errorName);
}
	get_error_data_more();
}

function set_error_more_html(ret){
	$(".bottom").html("");
    if(ret != undefined){
        $("#body").html(ret);
		if($("#errStatus").text() == "0") {
		$("#statusLabel").text("(未处理)");
	}
    }
}   

function get_error_data_more(){
	var status = 1;
	if($("#errStatus").text() == "0") {
		status = 0;
	}
	var errorName = $("#errorName").text();
	var province = $("#province").text();
	var city = $("#city").text();
	var url_data = get_url_data();
	var page = $("#page").text();
		if (page == "") {
			page = 1;
		}
	var department = $("#department").text();
	var data = {"personName":errorName,"userAcc": url_data["userAcc"], "page": page, "status": status, "province":province, "city":city, "department":department};
	jquery_ajax("/index/get_user_error_detail", data, set_user_error);
}

function userspanErrorMoreClick(elem){	//用户报警信息页面翻页
	spanClick(get_error_data_more, [elem, ]);
}


function after_errormore_page(){	//下一页
	var page = $("#page").text();
	var end_page = $("#pageCount").text();
	if(page.toString() == end_page.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		get_error_data_more();
	}
	$("#pageBelow").text($("#page").text());
}

function before_errormore_page(){	//下一页
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		get_error_data_more();
	}
	$("#pageBelow").text($("#page").text());
}

function getErrorAfter(){
	var pageCount = $("#pageCount").text();
	var page = $("#page").text();
	if(page.toString() == pageCount.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		if($("#platformExplainBody2").css("display") == "none") {
			getPage_sec_dep_user_err_Count();
		} else {
			get_dep_user_err_Count();
		}
	}
	$("#pageBelow").text($("#page").text());
}
function getErrorBefore(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		if($("#platformExplainBody2").css("display") == "none") {
			getPage_sec_dep_user_err_Count();
		} else {
			get_dep_user_err_Count();
		}
}
	$("#pageBelow").text($("#page").text());
}

function getPage_sec_dep_user_err_Count(){	//获取部门人员违规统计的情况
	depErrorCount();
	if($("#wPage").text() == "8"){
	$("#LoadingBar").show();
	$(".bottom").html("");
	var province = $("#areaLabel").text().substr(1,$("#areaLabel").text().length - 2);
	var city = $("#geterrData").children("tr").eq(0).children("td").eq(0).text();
	var url_data = get_url_data();
	var page = $("#page").text();
	if (page == "") {
		page = 1;
	}
	var errStatus = 1;
	if($("#errStatus").text() == "0") {
		errStatus = 0;
	}
	var data = {"userAcc": url_data["userAcc"],"province":province,"city":city,"department":"三级部门","page":page,"errStatus":errStatus }
	jquery_ajax("/index/get_dep_user_count", data, set_dep_user_err_Count);
}
}

function errorSpanClick(elem){
	if($("#platformExplainBody2").css("display") == "none") {
			spanClick(getPage_sec_dep_user_err_Count, [elem, ]);
		} else {
			spanClick(get_dep_user_err_Count, [elem, ]);
		}
}


function userErrorCount(){
	get_html("/userErrorCount.html",set_Error_count);
	$("#wPage").text(8);
}
function set_Error_count(ret){	//设置报警统计数据
	$(".bottom").html("");
    if(ret != undefined){
        $("#body").html(ret);
		get_dep_user_err_Count();
    }
}

function set_user_err_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
		if($("#isAdmin").text() == "1") {
			$("#delRecord").remove();
		}
	}
}
function clearn_index_style(){	//清除index的样式
	$(".index div").each(function(){
		$(this).css("background-color", "rgb(12, 124, 183)");
	})
}


function btnSelectClick(){
	if($("#select_data").val() == "") {
		dialogAlert("请输入数据", false, []);
	} else {
	$("#timeSearch").val("0");
	$("#page").text(1);
	$("#personSearch").val("1");
	get_user_error_data();
	$("#select_data").focus(function(){
					$("#personSearch").val("0");
					get_user_error_data();
				});
	}
	/*var select_data = $("#select_data").val();
	var re = new RegExp(select_data);
	if(select_data != ""){
		$("tbody tr").each(function(){
			if(!re.test($(this).children("td").eq(1).text()) && !re.test($(this).children("td").eq(2).children("span").text())){
				$(this).hide();
			}
		});
	}else{
		//dialogAlert("请输入数据", false, []);
		getUserErr();
	}
	$("#select_data").focus(function(){
					$("tbody tr").each(function(){
					$(this).show();	
				});
				})*/
}

function insert_alert(elem){
	var right = getAbsoluteLeft(elem) - 610;
	var top = getAbsoluteTop(elem) -200 ;
	var html = '<div class="show" style="padding:40px 20px; width:500px;border:1px solid#aaa; left:'+right+'px; top:'+top+'px; position:absolute;z-index:100; background:#fff; min-height:200px; max-height:500px;">';
	html += '</div>';
	return html;
}

function set_user_error_data(data, elem){
	if($(".show").html() == undefined) {
		$(".bottom").append(insert_alert(elem));
	}
	if(data != undefined){
		var table="<table>";
		table += "<tr><td style='width:120px;'>用户编号：</td><td>" +data["userNo"]+ "</td></tr>";
		table += "<tr><td style='width:120px;'>用户名：</td><td>" +data["userName"]+ "</td></tr>";
		table += "<tr><td style='width:120px;'>部门：</td><td>" +data["department"]+ "</td></tr>";
		table += "<tr><td style='width:120px;'>mac地址：</td><td>" +data["hostMac"]+ "</td></tr>";
		table += "<tr><td style='width:120px;'>ip地址：</td><td>" +data["ipAddr"]+ "</td></tr>";
		table += "<tr><td style='width:120px;'>报警文件名：</td><td>" +data["fileName"] + "</td></tr>";
		//table += "<tr><td style='width:120px;'>文件哈希：</td><td>" +data["fileHash"] + "</td></tr>";
		var fileSizeKB = (parseInt(data["fileSize"]) / 1024).toFixed(1);
		if(fileSizeKB < 1) {
			table += "<tr><td style='width:120px;'>文件大小</td><td>" + data["fileSize"] +"B" + "</td></tr>"; 
		} else {
			var fileSizeMB = (fileSizeKB / 1024).toFixed(1);
			if(fileSizeMB < 1) {
				table += "<tr><td style='width:120px;'>文件大小</td><td>" + fileSizeKB +"KB" + "</td></tr>";
			} else {
				table += "<tr><td style='width:120px;'>文件大小</td><td>" + fileSizeMB +"MB" + "</td></tr>";
			}				
		}
		//table += "<tr><td style='width:120px;'>文件大小</td><td>" + data["fileSize"] +"KB" + "</td></tr>";
		table += "<tr><td style='width:120px;'>关键字：</td><td>" +data["keyWords"]+ "</td></tr>";
		table += "<tr><td style='width:120px;'>关键字前后文：</td><td>" +getSingleKeyWord(data["keyWords"],data["keyExtend"],1)+ "</td></tr>";
		table += "<tr><td style='width:120px;'>报警时间：</td><td>" +data["errTime"]+ "</td></tr>";
		table +="</table>";
		$(".show").html(table);
		$(".show table td").css("height", "30px");
	}else{
		$(".show").html("<span style='color:red;'>用户数据有误</span>")
	}
}

function singletargetSecret(elem){  //单个标为涉密
	var secretId = $(elem).parent().parent().children("td").eq(0).children("input").attr("id")+"|";
	jquery_ajax("/index/user_error", {"secretId":secretId, "status":1}, target_sucess);
	get_user_error_data()
}

function singletargetNotSecret(elem){  //单个标为非涉密
	var secretId = $(elem).parent().parent().children("td").eq(0).children("input").attr("id")+"|";
	jquery_ajax("/index/user_error", {"secretId":secretId, "status":2}, target_sucess);
	get_user_error_data();
}

function set_user_error(ret) {	//设置部门用户异常数据
	if(ret != false){
		var html = "";
		if (ret != undefined) {
			for (var index = 0; index < ret["error_data"].length; index++) {
				html += "<tr><td><input class='err_check' type='checkBox' style='margin-right:10px;' id='" + ret["error_data"][index]["errId"] + "'/>" + ret["error_data"][index]["city"] + "</td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][index]["department"]+"'>" + ret["error_data"][index]["department"] + "</span></td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][index]["userName"]+"'>" + ret["error_data"][index]["userName"] + "</span></td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][index]["fileName"]+"'>" + ret["error_data"][index]["fileName"] + "</span></td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][index]["hostMac"].substring(0,ret["error_data"][index]["hostMac"].length-1)+"'>" + ret["error_data"][index]["hostMac"].substring(0,17) + "</span></td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][index]["ipAddr"]+"'>" + ret["error_data"][index]["ipAddr"] + "</span></td>";
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["error_data"][index]["errTime"]+"'>" + ret["error_data"][index]["errTime"] + "</span></td>";
				html += "<td><div><button type='button' class='user_data btn btn-link' style='padding:0;'>详细信息</button></div></td>";
				html += "<td><a target='_blank' href='/index/download_file?errId="+ret["error_data"][index]["errId"]+"&&file_name="+ret["error_data"][index]["fileName"]+"'>下载</a></td>";
				html += "<td class='operatethis'><a onclick='singletargetSecret(this)'  style='cursor:pointer'>标为涉密</a>&nbsp;&nbsp;<a  onclick='singletargetNotSecret(this)' style='cursor:pointer'>标为非涉密</a></td></tr>";

			}
			$("#errorCount").text(parseInt(ret["count"]));
		}
		$("tbody").html(html);
		if($("#wPage").text() == 9){
					$(".err_check").hide();
					$(".operatethis").hide();
					$("#errorTotal").text(ret["count"].toString());
				}
		if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
		}
		$("#pageCountBelow").text($("#pageCount").text());
		$("[data-toggle='popover']").popover();
		$(".err_check").click(function(){
			if($(this).attr("checked") == undefined){
				$(this).attr("checked", "checked");
			}else{
				$(this).removeAttr("checked");
			}
		});
		$("table tr td .user_data").hover(function(){
			for (var index = 0; index < ret["error_data"].length; index++) {
				if(ret["error_data"][index]["errId"] == $(this).parent().parent().parent().children("td").eq(0).children("input").attr("id")){
					set_user_error_data(ret["error_data"][index], this);
				}
			}
		}, function(){
			$(".show").remove();
		})
		/*if($("#selectLevel").val() == "严重") {
			for (var index = 0; index < ret["error_data"].length; index++) {
				if(ret["error_data"][index]["errId"] == $("tr").children("td").eq(0).children("input").attr("id")){
					var keyLevel = ret["error_data"][index]["keyWords"].substr(ret["error_data"][index]["keyWords"] + 3,1); //关键字级别
					if(keyLevel != "2") {
						$('#'+ret["error_data"][index]["errId"]).parent().parent().hide();
					}
				}
			}
		}*/
	}else{
		window.location.href = "/login";
	}
	
	$("#LoadingBar").css('display','none'); 
	
}


//查找用户信息
function btnPeoSelectClick(){
	var province = $("#province").text();
	var city = $("#city").text();
	var page = $("#page").text();
	var department = $("#department").text();
	var select_data = $("#select_data").val();
	var urlData = get_url_data();
	if(select_data != ""){
		//select:1表示按姓名查找
		jquery_ajax("/index/get_user_data_select", {"select_data": select_data, "user_acc": urlData["userAcc"], "province": province, "city": city, "department": department,"page":page}, set_user_data);
	}else{
		//dialogAlert("请输入数据", false, []);
		userManage();
	}
}

function btnKeySelectClick(){
	var province = $("#province").text();
	var city = $("#city").text();
	var page = $("#page").text();
	var department = $("#department").text();
	var select_data = $("#key_select_data").val();
	var url_data = get_url_data();
	var userAcc = url_data["userAcc"];
	var data = {"select_data":select_data,"user_acc":userAcc,"province":province,"city":city,"department":department,"page":page};
	if(select_data !=""){
		jquery_ajax("/index/get_user_key_select",data,set_key_data);
	}else{
		get_key_data();
	}
}

function changeErrorStatus(elem){
	var errorStatus = $("#errorStatus").text();
	$("#errorStatus").text($(elem).children("a").text());
	$(elem).children("a").text(errorStatus);
	$("#page").text(1);
	get_user_error_data();
}


function user_check_click(elem){
	if($(elem).attr("checked") != "checked"){
		$(elem).attr("checked", "checked");
	}else{
		$(elem).removeAttr("checked");
	}
}


function reset_user_sucess(ret){
	if(ret == true){
		dialogAlert("账号重置成功！", false, []);
		get_user_data();
	}else{
		dialogAlert("账号重置失败请稍后重试！", false, []);
	}
}


function reset_user_ok(elem){
	jquery_ajax("/index/reset_user", {"userNo": elem[0]}, reset_user_sucess)
}

function reset_user(elem){	//账号重置
	var userName = $(elem).parent().parent().children("td").eq(1).text();
	var userNo = $(elem).parent().parent().children("td").eq(0).text();
	var alert_text = "确定重置<span style='font-weight:700; color:red;'>"+ userName +"</span>的账号:<span style='font-weight:700; color:red;'>" + userNo+"</span>";
	alert_text += "<br>注意:<span style='color:red;'>重置后该用户的密码将为初始密码</span>";
	confirmAlert(alert_text, reset_user_ok, false, [userNo, ], []);
}


function set_user_data(ret){
	var html = "";
	var url_data = get_url_data();
	var userAcc = url_data["userAcc"];
	if(ret != undefined && ret != false){
		var user_count = parseInt(ret["user_count"]);
		if(parseInt(ret["user_count"]) == 0 || isNaN(parseInt(ret["user_count"]))){
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["user_count"])/20));
		}
		$("#pageCountBelow").text($("#pageCount").text());

		for(var index=0; index<ret["user_data"].length; index ++){
			if($("#isAdmin").text() == "1" && ret["user_data"][index]["userPosition"] == 2) {
				continue;
			} else {
				if(ret["user_data"][index]["userNo"] == userAcc){
					user_count--;
				  $("#userCount").text(user_count);
					continue;
				}
				html += '<tr><td><input class="user_check" onclick="user_check_click(this)" type="checkBox" style="margin-right:10px;">'+ret["user_data"][index]["userNo"]+'</td>';
				html += '<td>'+ret["user_data"][index]["userName"]+'</td>';
				if(ret["user_data"][index]["userPosition"] == 0){
					html += '<td>一般人员</td>';
				}else if(ret["user_data"][index]["userPosition"] == 1){
					html += '<td>普通管理员</td>';
				}else if(ret["user_data"][index]["userPosition"] == 2){
					html += '<td>超级管理员</td>';
				}
				if(String(ret["user_data"][index]["macAddr"]) != "null"){
					html += "<td><div style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["user_data"][index]["macAddr"].substring(0,ret["user_data"][index]["macAddr"].length-1)+"'>" + ret["user_data"][index]["macAddr"].substring(0,17) + "</div></td>";
				}else{
					html += "<td>"+ret["user_data"][index]["macAddr"]+"</td>";
				}

				html += '<td>'+ret["user_data"][index]["ipAddr"]+'</td>';
				//html += '<td><button onclick="update_user(this)" type="button" class="btn btn-link" style="padding:0;">修改</button>';
				html +=  '<td><button onclick="reset_user(this)" type="button" class="btn btn-link" style="padding:0; margin-left:10px;">账号重置</button></td>';
				html += '</tr>';
			}
		}
	}
	$("#userInf").html(html);
	if($("#userCount").text() == ""){
		$("#userCount").text(user_count);
	}
	$("[data-toggle='popover']").popover();
	$("#LoadingBar").css('display','none'); 
}


function userBefore(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		if($("#select_data").val() != ""){
			btnPeoSelectClick();
		}else{
		get_user_data();
	}
}
	$("#pageBelow").text($("#page").text());
}


function userAfter(){
	var pageCount = $("#pageCount").text();
	var page = $("#page").text();
	if(page.toString() == pageCount.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		if($("#select_data").val() != ""){
			btnPeoSelectClick();
		}else{
		get_user_data();
	}
	}
	$("#pageBelow").text($("#page").text());
}
function connBefore(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		//get_user_conn_data();
		if($("#online").val() == "1") {
			get_user_online_data();
		}
		if($("#offline").val() == "1") {
			get_user_offline_data();
		}
	}
	$("#pageBelow").text($("#page").text());
}


function connAfter(){
	var pageCount = $("#pageCount").text();
	var page = $("#page").text();
	if(page.toString() == pageCount.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		//get_user_conn_data();
		if($("#online").val() == "1") {
			get_user_online_data();
		}
		if($("#offline").val() == "1") {
			get_user_offline_data();
		}
	}
	$("#pageBelow").text($("#page").text());
}


/*function connSpanClick(elem){
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
			if($("#online").val() == "1") {
				get_user_online_data();
			}
			if($("#offline").val() == "1") {
				get_user_offline_data();
			}
		})
	}
}*/

function connSpanClick(elem){	//用户报警信息页面翻页
	if($("#online").val() == "1") {
		spanClick(get_user_online_data, [elem, ]);
	}
	if($("#offline").val() == "1") {
		spanClick(get_user_offline_data, [elem, ]);
	}
}

function set_user_conn_data(ret){
	var html = "";
	if(String(ret) != "undefined") {
		if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
		}
		var onlinePerson = 0;
		var offlinePerson = 0;
		for (var i = 0; i < ret["user_data"].length; i++) {
			if($("#online").val() == "1") {  //选择在线
				if (+ret["user_data"][i]["loginStatus"] != 0) {
				html += "<tr><td><input class='user_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;'>" + ret["user_data"][i]["userNo"] + "</td><td>" + ret["user_data"][i]["userName"] + "</td><td>" +  ret["user_data"][i]["ipAddr"];
				html += "</td><td><div style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["user_data"][i]["macAddr"].substring(0,ret["user_data"][i]["macAddr"].length-1)+"'>" + ret["user_data"][i]["macAddr"].substring(0,17) + "</div></td>";
				html += "<td style='color:green;'>" + "在线" + "</td>";
				/*if (String(ret["user_data"][i]["userNetStatus"]) == "0") {
					html += "<td><button type='button' style='margin-top: 0px; height:20px; padding: 0 5px;' class='btn btn-link close_net' onclick='clost_net(this, 0)'>断开网络</button>";
				} else {
					html += "<td><button type='button' style='margin-top: 0px; height:20px; padding: 0 5px;' class='btn btn-link close_net' onclick='clost_net(this, 1)'>打开网络</button>"
				}*/
				if (String(ret["user_data"][i]["userScanStatus"]) == "0") {
					html += "<td><button type='button' class='btn btn-link scanFile' style='margin-top: 0px;margin-left: 0px; height:20px; padding:0 5px;' onclick='scan_file(this, 0)'>扫描用户文件<span id='loadingClass' class=''></span></button>"
				} else if (String(ret["user_data"][i]["userScanStatus"]) == "1") {
					html += "<td><button type='button' class='btn btn-link scanFile' style='margin-top: 0px;margin-left: 0px; height:20px; padding:0 5px;' onclick='scan_file(this, 1)'>正在扫描文件<span id='loadingClass' class='glyphicon glyphicon-refresh glyphicon-refresh-animate'></span></button>"
				}
				if($("#isAdmin").text() == "2") {
					html += "<button type='button' class='btn btn-link unInstallClient' style='margin-top: 0px;margin-left: 0px; height:20px; padding:0 5px;' onclick='unInstallClient(this)'>卸载客户端</button>"
				}
				html += "</td><tr>";
				}
				onlinePerson++;
			}
			if($("#offline").val() == "1") {//选择离线
				if (+ret["user_data"][i]["loginStatus"] == 0) {
				html += "<tr><td><input class='user_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;' disabled='disabled'>" + ret["user_data"][i]["userNo"] + "</td><td>" + ret["user_data"][i]["userName"] + "</td><td>" + ret["user_data"][i]["ipAddr"];
				html += "</td><td><div style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["user_data"][i]["macAddr"].substring(0,ret["user_data"][i]["macAddr"].length-1)+"'>" + ret["user_data"][i]["macAddr"].substring(0,17) + "</div></td>";
				html += "<td style='color:red;'>" + "离线" + "</td>";
				html += "<td><button type='button' class='btn btn-link' style='margin-top: 0px; height:27px; padding:0 5px;' disabled='disabled'>断开网络</button>";
				html += "<button type='button' class='btn btn-link' style='margin-top: 0px; height:27px; padding:0 5px;' disabled='disabled'>扫描用户文件</button></td><tr>"
				}
				offlinePerson++;
			}
		}
			if(onlinePerson == 0 && $("#online").val() == "1" && $("#offline").val() == "0") {
				dialogAlert("暂无在线人员!", false, []);
				$("#page").text(1);
				$("#pageCount").text(1);
			}
			if(offlinePerson == 0 && $("#online").val() == "0" && $("#offline").val() == "1") {
				dialogAlert("暂无离线人员!", false, []);
				$("#page").text(1);
				$("#pageCount").text(1);
			}
			$("#pageCountBelow").text($("#pageCount").text());
	}
	$("#userConn").html(html);
	$("#connCount").text(ret["count"]);
	$("[data-toggle='popover']").popover();
	frash_user_conn();
	$("#LoadingBar").css('display','none'); 
}


function clost_net_sucess(ret){
	if(ret == false){
		dialogAlert("操作失败,请稍后重试!");
	}
	//get_user_conn_data();
	if($("#online").val() == "1") {
		get_user_online_data();
	}
	if($("#offline").val() == "1") {
		get_user_offline_data();
	}
}

function unInstallClient(elem){
		var receive_no = $(elem).parent().parent().children("td").eq(0).text();
		var url_data = get_url_data();
		var send_no = url_data["userAcc"];
		var send_time = get_current_time();
		var data = {"receive_no": receive_no, "send_no":send_no, "send_time":send_time};
		$(elem).text("正在卸载客户端");
		$(elem).attr("disabled", "true");
		jquery_ajax("/index/remove_self", data, remove_self_sucess);

}

function remove_self_sucess(ret){
	if(ret == false){
		dialogAlert("卸载客户端失败， 请稍后重试！", false, [])
	}else{
		dialogAlert("卸载客户端命令已成功发送！", false, [])
	}
	if($("#online").val() == "1") {
		get_user_online_data();
	}
	if($("#offline").val() == "1") {
		get_user_offline_data();
	}
}

function mul_clost_net(elem, status){	//多选关闭网络
	var secretId = "";
	$(".user_check").each(function(){
		if($(this).attr("checked") == "checked"){
			secretId += $(this).attr("id")+"|";
			clost_net(this,0);
		}
	});
	if(secretId == ""){
		dialogAlert("您尚未选中任何人员,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}
}

function clost_net(elem, status){	//关闭网络
	var receive_no = $(elem).parent().parent().children("td").eq(0).text();
	var url_data = get_url_data();
	var send_no = url_data["userAcc"];
	var send_time = get_current_time();
	var data= {"receive_no":receive_no+"|", "status": status, "send_no":send_no, "send_time":send_time};
	jquery_ajax("/index/close_net", data, clost_net_sucess);
}


function scan_file_sucess(ret){
	if(ret == false){
		dialogAlert("扫描用户文件失败， 请稍后重试！", false, [])
		get_user_online_data();
	}else{
		dialogAlert("扫描命令已成功发送，请您耐心等待扫描结果！", false, []);
	}
	if($("#online").val() == "1") {
		get_user_online_data();
	}
	if($("#offline").val() == "1") {
		get_user_offline_data();
	}
	//fresh_scan_status();
}

/* 扫描结果反馈
function fresh_scan_status(){
	var department = $("#department").text();
	if(department == "--请选择--"){
		dialogAlert("请选择部门!", false, []);
	}else{
		$("#LoadingBar").show();
		var province = $("#province").text();
		var city = $("#city").text();
		var urlData = get_url_data();
		var page = $("#page").text();
		var data = {"province":province, "city": city, "department": department, "userAcc": urlData["userAcc"], "page": page, "status":1};//status=1表示在线
		jquery_ajax("/index/get_user_conn_data", data, set_fresh_status);
		$("#selectAll").removeAttr("checked");
	}
}

function set_fresh_status(ret){
	setTimeout(function() {
    var status = String(ret["user_data"][0]["userScanStatus"]);
	if (status =="0"){
	dialogAlert("扫描已完成，请在报警记录中查询！", false, []);
	clearTimeout(this);
}else{
fresh_scan_status();
}
}, 5000);
}*/

function queryBefore(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		get_scan_file_data();
	}
	$("#pageBelow").text($("#page").text());
}

function queryAfter(){
	var page = $("#page").text();
	var end_page = $("#pageCount").text();
	if(page.toString() == end_page.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		get_scan_file_data();
	}
	$("#pageBelow").text($("#page").text());
}

function set_scan_data(ret){
	var html = "";
	if(ret != undefined && ret["file"].length >0){
		for(var i=0; i< ret["file"].length; i++) {
			var start = ret["file"][i]["keywords"].indexOf("-",0); 
			var end = ret["file"][i]["keywords"].indexOf("-",2); 
			var keyword = ret["file"][i]["keywords"].substr(start + 1,end - start - 1);
			var keywordDetail = "级别：" + ret["file"][i]["keywords"].substr(0,1) + " 关键字：" + keyword + " 重复次数：" + ret["file"][i]["keywords"].substr(end + 1,ret["file"][i]["keywords"].indexOf(" ",0) - end - 1);
			html += "<tr>";
			html += "<td>" + ret["file"][i]["city"] + "</td>"
			html += "<td>" + ret["file"][i]["departmentName"] + "</td>"
			html += "<td>" + ret["file"][i]["userNo"] + "</td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["userName"]+"'>" + ret["file"][i]["userName"] + "</td>";
			//html += "<td>" + ret["file"][i]["fileName"] + "</td>";
			//html += "<td>" + ret["file"][i]["filePath"] + "</td>";
			//html += "<td>" + ret["file"][i]["keywords"] + "</td>";
			//html += "<td>" + ret["file"][i]["keyExtend"] + "</td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["fileName"]+"'>" + ret["file"][i]["fileName"] + "</span></td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["filePath"]+"'>" + ret["file"][i]["filePath"] + "</span></td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+keywordDetail+"'>" + keyword + "</span></td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["keyExtend"]+"'>" + getSingleKeyWord(ret["file"][i]["keywords"],ret["file"][i]["keyExtend"],2) + "</span></td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["scanTime"]+"'>" + ret["file"][i]["scanTime"] + "</span></td>";
			//html += "<td>" + ret["file"][i]["scanTime"] + "</td>";
			//html += "<td><button type='button' style='margin-top: 0px; height:27px; padding: 0 5px;' class='btn btn-link close_net'>下载该文件</button></td>";
			html += "</tr>";
		}
		if(parseInt(ret["key_count"]) == 0){  //总页数
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"])/20));  //key_count为当前页有几条
		}
	}
	$("#userQuery").html(html);
	$("#scanCount").text(parseInt(ret["count"]));
	$("[data-toggle='popover']").popover();
	$("#LoadingBar").css('display','none');
}

function set_user_scan_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
	}
}


function show_scanFile(){
	get_html("/userScan.html", set_user_scan_html);
	$("#wPage").text(7);
}

function show_file(ret){
	if(ret != false){
		set_scan_data(ret);
	}

}


function frash(){
	//get_user_conn_data();
	if($("#online").val() == "1") {
		get_user_online_data();
	}
	if($("#offline").val() == "1") {
		get_user_offline_data();
	}
}


function get_scan_file_data(){
	$("#LoadingBar").show();
	$("#title").text("扫描结果");
	if($("#scanUserAcc").text() == "") {
		$("#table1").show();
		$("#table2").remove();
		var province = $("#province").text();
		var city = $("#city").text();
		var department = $("#department").text();
		var urlData = get_url_data();
		var page = $("#page").text();
		var data = {"province":province, "city": city, "department": department, "userAcc": urlData["userAcc"], "page": page};
		jquery_ajax("/index/get_scan_file_bytime", data, show_file_bytime);
		$("#selectAll").removeAttr("checked");
	} else {
		$("#table2").show();
		$("#table1").remove();
		var province = $("#province").text();
		var city = $("#city").text();
		var department = $("#department").text();
		var scanTime = $("#scanTime").text();
		var scanUserAcc = $("#scanUserAcc").text();
		var page = $("#page").text();
		var data = {"scanTime":scanTime,"province":province, "city": city, "department": department, "userAcc": scanUserAcc, "page": page};
		jquery_ajax("/index/get_scan_file", data, show_file);
		$("#selectAll").removeAttr("checked");
	}
}

function show_file_bytime(ret){
	if(ret != false){
		set_scan_data_bytime(ret);
	}
}

function set_scan_data_bytime(ret){
	var html = "";
	if(ret != undefined && ret["file"].length >0){
		for(var i=0; i< ret["file"].length; i++) {
			html += "<tr>";
			html += "<td>" + ret["file"][i]["city"] + "</td>"
			html += "<td>" + ret["file"][i]["departmentName"] + "</td>"
			html += "<td>" + ret["file"][i]["userNo"] + "</td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["userName"]+"'>" + ret["file"][i]["userName"] + "</td>";
			html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["file"][i]["scanTime"]+"'>" + ret["file"][i]["scanTime"] + "</span></td>";
			html += "<td>" + ret["file"][i]["timecount"] + "</td>";
			html += "<td><button onclick='get_scan_detail_file(this)' type='button' class='btn btn-link' style='padding:0;'>查看详情</button></td>";
			html += "</tr>";
		}
		if(parseInt(ret["key_count"]) == 0){  //总页数
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["count"])/20));  //key_count为当前页有几条
		}
	}
	$("#userQuery").html(html);
	$("#scanCount").text(parseInt(ret["count"]));
	$("[data-toggle='popover']").popover();
	$("#LoadingBar").css('display','none');
}

function get_scan_detail_file(elem) {
	var userAcc = $(elem).parent().parent().children().eq(2).text();
	var scanTime = $(elem).parent().parent().children().eq(4).text();
	$("#scanUserAcc").text(userAcc);
	$("#scanTime").text(scanTime);
	get_scan_file_data();
}

function get_scan_file(){
	show_scanFile();
	get_scan_file_data();
}


function scan_file(elem, status){	//扫描用户文件
	if(status == 0){
		var receive_no = $(elem).parent().parent().children("td").eq(0).text();
		var send_time = get_current_time();
		var url_data = get_url_data();
		var send_no = url_data["userAcc"];
		var data = {"receive_no": receive_no, "status": status, "send_time": send_time, "send_no": send_no};
		$(elem).text("正在扫描文件");
		$(elem).attr("disabled", "true");
		$("#loadingClass").addClass("glyphicon glyphicon-refresh glyphicon-refresh-animate");
		jquery_ajax("/index/scan_file", data, scan_file_sucess);
	}else if(status == 1){
		dialogAlert("正在扫描用户文件请等待！", false, []);
	}
}

function mul_scan_file(elem, status){	//多选扫描用户文件
	var secretId = "";
	$(".user_check").each(function(){
		if($(this).attr("checked") == "checked"){
			secretId += $(this).attr("id")+"|";
			scan_file(this,0);
		}
	});
	if(secretId == ""){
		dialogAlert("您尚未选中任何人员,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}
}
//获取在线用户信息
function get_user_online_data(){
	var department = $("#department").text();
	if(department == "--请选择--"){
		dialogAlert("请选择部门!", false, []);
	}else{
		$("#LoadingBar").show();
		var province = $("#province").text();
		var city = $("#city").text();
		var urlData = get_url_data();
		var page = $("#page").text();
		var data = {"province":province, "city": city, "department": department, "userAcc": urlData["userAcc"], "page": page, "status":1};//status=1表示在线
		jquery_ajax("/index/get_user_conn_data", data, set_user_conn_data);
		$("#selectAll").removeAttr("checked");
	}
}
//获取离线用户信息
function get_user_offline_data(){
	var department = $("#department").text();
	if(department == "--请选择--"){
		dialogAlert("请选择部门!", false, []);
	}else{
		$("#LoadingBar").show();
		var province = $("#province").text();
		var city = $("#city").text();
		var urlData = get_url_data();
		var page = $("#page").text();
		var data = {"province":province, "city": city, "department": department, "userAcc": urlData["userAcc"], "page": page, "status":0};//status=0表示离线
		jquery_ajax("/index/get_user_conn_data", data, set_user_conn_data)
		$("#selectAll").removeAttr("checked");
	}
}

function frash_user_conn(){
	var frash = false;
	$("tbody tr").each(function(){
		if($(this).children("tr").eq(5).children("button").eq(1).text() == "正在扫描用户文件"){
			frash = true;
		}
	});
	if(frash == true){
		if($("#online").val() == "1") {
			setInt = window.setInterval("get_user_online_data()", 60*1000);
		}
		if($("#offline").val() == "1") {
			setInt = window.setInterval("get_user_offline_data()", 60*1000);
		}
		//setInt = window.setInterval("get_user_conn_data()", 60*1000);
	}else{
		try{
			window.clearInterval(setInt);
		}catch(e){

		}
	}
}

function set_user_conn_html(ret){
	if(ret != undefined){
		$("#body").html(ret);
		get_user_online_data();
	}
}

function connClick(){
	if($("#scanUserAcc").text() == "") {
		get_html("/userConn.html", set_user_conn_html);
		$("#wPage").text(3);
	} else {
		$("#scanUserAcc").text("");
		get_scan_file();
	}
	
}

function get_user_data(){
	var department = $("#department").text();
	if(department == "无"){
		dialogAlert("请选择省市部门信息!", false, []);
	} else{
		$("#LoadingBar").show();
		var province = $("#province").text();
		var city = $("#city").text();
		var urlData = get_url_data();
		var page = $("#page").text();
		var data = {"userAcc": urlData["userAcc"], "province": province, "city": city, "department": department, "page": page};
		jquery_ajax("/index/get_user_data", data, set_user_data);
		$("#selectAll").removeAttr("checked");
	}
}


function set_user_manage(ret){	//设置用户数据
	$("#body").html(ret);
	get_user_data();
}


function userspanSelectClick(elem){	//用户报警信息页面翻页
	spanClick(get_scan_file_data, [elem, ]);
}


function userManage(){	//获取普通人员管理页面
	get_html("/userManage.html", set_user_manage);	//获取首页数据
	$("#wPage").text(2);
}
function set_about(ret){
	ret=ret.slice(ret.indexOf('<body>')+6,ret.indexOf('</body>'));
	$("#body").html(ret);
}
function aboutClick(){
	get_html("/about", set_about);	//获取首页数据
	$("#wPage").text(6);
}

function update_user(elem){	//修改用户信息
	if($("tbody tr").eq($("tbody tr").length -1).attr("increase") != undefined){
		dialogAlert("请提交后再添加!", false, []);
	}else {
		$(elem).parent().parent().attr("update", "true");
		var user_name = $(elem).parent().parent().children("td").eq(1).text();
		$(elem).parent().parent().children("td").eq(1).html("<div style='background:#eee;' contenteditable='true'>"+user_name+"</div>");
		//$(elem).parent().parent().children("td").eq(2).html("<select><option value=2>超级管理员</option><option value=1>普通管理员</option><option value=0>一般人员</option></select>");
		if($("#isAdmin").text() == "1") {
			if($(elem).parent().parent().children("td").eq(2).text()!="超级管理员") {
				$(elem).parent().parent().children("td").eq(2).html("<select><option value=1>普通管理员</option><option value=0>一般人员</option></select>");
			}
		} else/* if($("#isAdmin").text() == "2" && $("#province").text() == "所有省" && $("#city").text() == "所有市") */{
			$(elem).parent().parent().children("td").eq(2).html("<select><option value=2>超级管理员</option><option value=1>普通管理员</option><option value=0>一般人员</option></select>");
		}/*else {
			if($(elem).parent().parent().children("td").eq(2).text()!="超级管理员") {
			    $(elem).parent().parent().children("td").eq(2).html("<select><option value=1>普通管理员</option><option value=0>一般人员</option></select>");				
			}*/ 
		$(elem).parent().parent().children("td").eq(1).children("div").focus();
	}
}

function drop_column(elem){
	$(elem).parent().parent().remove();
}


function increase_user(){	//增加用户
	if($("tbody tr").eq($("tbody tr").length -1).attr("increase") != undefined){
		dialogAlert("请提交后再添加!", false, []);
	}else if($("#isAdmin").text() == "1" && $("#department").text() == "三级部门") {
		dialogAlert("请选择一个存在的三级部门添加一般人员!", false, []);
	}else if($("#province").text() == "一级部门" ){
		dialogAlert("请选择一个存在的部门添加人员，例如选择一个存在的一级部门添加超管人员!", false, []);
	}else if($("#isAdmin").text() == "2" && $("#userDep").text() != "超高级管理员" && $("#city").text() == "二级部门"){
		dialogAlert("请选择一个存在的部门添加人员，例如选择一个存在的二级部门添加普管人员!", false, []);
	}else{
		var html = '<tr increase="true"><td><div contenteditable="true" style="background:#eee;"></div></td>';
		html += '<td><div contenteditable="true" style="background:#eee;"></div></td>';
		//html += '<td><select><option value=2>超级管理员</option><option value=1>普通管理员</option><option value=0>一般人员</option></select></td>';
		if($("#isAdmin").text() == "1") {
			html += '<td><select><option value=0>一般人员</option></select></td>';
		}else if($("#isAdmin").text() == "2" ) {
			if($("#userDep").text() == "超高级管理员" ){
				if ($("#city").text() == "二级部门"){
                       html += '<td><select><option value=2>超级管理员</option></select></td>';
               }else if($("#department").text() == "三级部门"){
                       html += '<td><select><option value=2>超级管理员</option><option value=1>普通管理员</option></select></td>';
			}else{
				html += '<td><select><option value=2>超级管理员</option><option value=1>普通管理员</option><option value=0>一般人员</option></select></td>';
			}		
		}else {
			if ($("#department").text() == "三级部门"){
			html += '<td><select><option value=1>普通管理员</option></select></td>';	
		}else{
			html += '<td><select><option value=1>普通管理员</option><option value=0>一般人员</option></select></td>';
		}
	}
		}  
		html += '<td></td><td></td>';
		html += '<td><button onclick="drop_column(this)" type="button" class="btn btn-link" style="padding:0;">取消</button></td></tr>';
		if($("table tbody tr").length != 0){
			$("table tbody tr").eq(0).before(html);
		}else{
			$("table tbody").html(html);
		}

		$("tbody tr").eq($("tbody tr").length -1).children("td").eq(0).children("div").focus();
	}
}

function import_excel(){
	var province = $("#province").text();
	var xlsx_name = $("#choosefile").val().substr($("#choosefile").val().length - 4,4);
	var xls_name = $("#choosefile").val().substr($("#choosefile").val().length - 3,3);
	if(xlsx_name != "xlsx" && xls_name != "xls"){
		dialogAlert("请选择一个excel格式文件!", false, []);
		return;
	}
	if (province == "一级部门"){
		dialogAlert("请选择一个可导入人员的部门!", false, []);
	} else{
		$.ajaxFileUpload({
		url: '/index/import_excel', //用于文件上传的服务器端请求地址
        secureuri: false, //是否需要安全协议，一般设置为false
        fileElementId: 'choosefile', //文件上传域的ID
        dataType: 'json', //返回值类型 一般设置为json
        data: {"province": province},
        success: function (ret)  //服务器成功响应处理函数
        {
            if(ret == 1){
            	dialogAlert("人员导入成功！",false,[]);
            }else{
            	dialogAlert("导入人员失败,请检查插入数据!",false,[]);
            }
        },
        error: function (ret, status, e)//服务器响应失败处理函数
        {
            dialogAlert("服务器响应失败!",false,[]);
        }
	})
	}
}

/*
function import_sucess(ret){
	if(ret == true){
		dialogAlert("导入人员成功!", false, []);
	}else{
		dialogAlert("导入人员失败,请检查插入数据!", false, []);

	}
}*/

function delete_sucess(ret){
	if(ret == true){
		dialogAlert("删除成功！", false, []);
		userManage();
	}else{
		dialogAlert("您的操作有误,请稍后重试！", false, []);
	}

}

function delete_user_data(elem){
	jquery_ajax("/index/delete_user_data", {"user_list": elem[0],}, delete_sucess)
}


function delete_user(){	//删除用户
	var update_user = false;
	var url_data = get_url_data();
	var delUser = url_data["userAcc"];
	$("tbody tr").each(function(){
		if($(this).attr("update") != undefined){
			update_user = true;
		}
	});
	if($("tbody tr").eq($("tbody tr").length -1).attr("increase") != undefined || update_user == true){
		dialogAlert("请提交后再做删除动作!", false, []);
	}else{
		var delete_user = "";
		var breaktag = false;
		$(".user_check").each(function(){
			if($(this).attr("checked") == "checked"){
				var delete_id = $(this).parent().parent().children("td").eq(0).text();
				if (delete_id == delUser){
					dialogAlert("您不能删除自己，否则账户无法使用!", false, []);
					breaktag = true;
					return;
		 		}
				delete_user += $(this).parent().parent().children("td").eq(0).text() + "|";
			}
		});
		if(breaktag == true) {
			return;
		}
		if(delete_user != ""){
			confirmAlert("您确定要对这些用户进行删除操作？", delete_user_data, false, [delete_user, ], []);
		}else{
			dialogAlert("您没有选中任何用户,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
		}
	}
}


function input_sucess(ret){
	if(ret == true){
		dialogAlert("提交成功!", false, []);
		userManage();
	}else{
		dialogAlert("您填写的数据有问题，或选择的部门无法添加用户（如所有部门）,请仔细检查后在作提交!", false, []);
	}
}


function input_user_data(elem){
	var province = $("#province").text();
	var city = $("#city").text();
	var department = $("#department").text();
	var urlData = get_url_data();
	jquery_ajax("/index/input_user_data", {"user_data": elem[0], "userAcc": urlData["userAcc"], "province": province, "city":city, "department":department}, input_sucess)
}


function input_user(){	//提交用户修改
	var user_update = false;
	var defaule = false;
	var user_data = "";
	var breaktag = false;
	$("tbody tr").each(function(){
		if($(this).attr("update") != undefined){
			if($(this).children("td").eq(1).text() != ""){
				user_update = true;
				user_data += $(this).children("td").eq(0).text() +"&"+$(this).children("td").eq(1).text()+"&"+$(this).children("td").eq(2).children("select").val()+ ",update|"
			}else{
				defaule = true;
			}
		}
		if($(this).attr("increase") != undefined){
			if($(this).children("td").eq(0).children("div").text() != "" && $(this).children("td").eq(1).children("div").text() != ""){
				user_update = true;
				user_data += $(this).children("td").eq(0).children("div").text()+"&"+ $(this).children("td").eq(1).text() + "&"+$(this).children("td").eq(2).children("select").val() + ",increase|"
				var addUserNo = $(this).children("td").eq(0).children("div").text();
				var reg = new RegExp("[\\u4E00-\\u9FFF]+","g");
　　			if(reg.test(addUserNo)) { 
					dialogAlert("用户编号中不能有汉字!", false, []);
					breaktag = true;
					return;
				}
			}else{
				defaule = true;
			}
		}
	});
	if(breaktag == true) {
		return;
	}
	var userManage = $("tbody tr").children("td").eq(2).children("select").val();
	if($("#userDep").text() == "超高级管理员" && userManage == 1 && $("#city").text() == "二级部门"){
		dialogAlert("添加普管人员需选择存在的二级部门，请仔细检查后在作提交!", false, []);
	}else if(userManage == 0 && $("#department").text() == "三级部门"){
		dialogAlert("添加一般人员需选择存在的三级部门，请仔细检查后在作提交!", false, []);
	}else{
	if(user_update == true && defaule != true){
		var firstDep = $("#province").text();
		var secondDep = $("#city").text();
		var thirdDep = $("#department").text();
		if(secondDep == "二级部门"){
		confirmAlert("您当前所在的部门是:"+firstDep+"，您确定您所做的操作吗？", input_user_data, false, [user_data, ], []);
	}else if(thirdDep == "三级部门"){
		confirmAlert("您当前所在的部门是: "+firstDep+">"+secondDep+"，您确定您所做的操作吗？", input_user_data, false, [user_data, ], []);
	}else{
		confirmAlert("您当前所在的部门是: "+firstDep+">"+secondDep+">"+thirdDep+"，您确定您所做的操作吗？", input_user_data, false, [user_data, ], []);
	}
	}

	if(user_update == true && defaule == true){
		dialogAlert("您填写的数据有问题，请仔细检查后在作提交!", false, []);
	}
	if(user_update == false && defaule == true){
		dialogAlert("您填写的数据有问题，请仔细检查后在作提交!", false, []);
	}
	if(user_update == false && defaule == false){
		dialogAlert("您没有修改或增加任何用户,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}
}
}



function before_page(){	//上一页
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		get_user_error_data();
	}
	$("#pageBelow").text($("#page").text());
}


function after_page(){	//下一页
	var page = $("#page").text();
	var end_page = $("#pageCount").text();
	if(page.toString() == end_page.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		get_user_error_data();
	}
	$("#pageBelow").text($("#page").text());
}

function getUserErr(){	//获取用户异常数据
	get_html("/userError.html", set_user_err_html);
	$("table th").css("width", "10%");
	$("#page").text(1);
	get_user_error_data();
	$("#wPage").text(1);
}


function firstClick(){	//点击首页
    get_html("/first.html", set_first_html);
	$("#wPage").text(0);

}


function absPos(node){
    var x=y=0;
    do{
        x= parseInt(x) +parseInt(node.offsetLeft);
        y= parseInt(y) +parseInt(node.offsetTop);
    }while(node=node.offsetParent);
    return{
        'x':x,
        'y':y
    };
}

function get_dep_data(){	//获取部门信息
	var url_data = get_url_data();
	var city = "none";
	var province = $("#province").text();
	//var city = $("#city").text();
	if($("#province").attr("get") != "false"){
		province = $("#province").text();
	}
	if($("#city").attr("get") != "false"){
		city = $("#city").text();
	}
	var userAcc = url_data["userAcc"];
	var data = {"userAcc": userAcc, "province": province, "city":city};
	jquery_ajax("/index/get_dpt_data", data, set_dpt_data)
	return true;
}


function set_dpt_data(ret){	//设置部门信息
	if(ret == false || ret == undefined){
		//window.location.href = "/login";
		dialogAlert("部门加载错误，请重试！",false,[]);
	}else{
		$("body").append("<div id='get_dpt' style='display:none;'></div>");
		var province="";
		var city="";
		var department = '';
		if($("#province").attr("get").toString() == "false") {
			for (var i = 0; i < ret["province"].length; i++) {
				province += '<li role="presentation"><a role="menuitem" tabindex="-1">' + ret["province"][i] + '</a></ul>';
			}
		}
		if($("#city").attr("get").toString() == "false") {
			if($("#isAdmin").text() == "2") {
				//$("#city").text(ret["city"][0]);
				city += '<li role="presentation"><a role="menuitem" tabindex="-1">二级部门</a></ul>';
				for (var i = 0; i < ret["city"].length; i++) {
					if(ret["city"][i] != "二级部门") {
						city += '<li role="presentation"><a role="menuitem" tabindex="-1">' + ret["city"][i] + '</a></ul>';
					}
				}
				
			} else {
				//$("#city").text($("#userCity").text());
				$("#city").attr("get", "true");
				get_dep_data();
				city += '<li role="presentation"><a role="menuitem" tabindex="-1">' + $("#city").text() + '</a></ul>';
				$(".title .dropdown").eq(1).children(".dropdown-menu").html(city);
				setTimeout("reloadPage()","100");
			}
			
		}
		/*if($("#isAdmin").text() == "1") {
			department += '<li class="dep" hasTow=false role="presentation" ><a role="menuitem" tabindex="-1">'+$("#department").text()+'</a></ul>';
		} else {
			for(var i in ret["department"]){
			if(ret["department"][i].length == 1){
				department += '<li class="dep" hasTow=false role="presentation" ><a role="menuitem" tabindex="-1">'+i+'</a></ul>';
			}else{
				department += '<li class="dep" hasTow=true role="presentation"><a role="menuitem" tabindex="-1">'+i+'<img src="../static/images/leftPoint.png" width="15" height="15" style="float:right;"></a></ul>';
			}
			}
		}*/
		department += '<li class="dep" hasTow=false role="presentation" ><a role="menuitem" tabindex="-1">三级部门</a></ul>';
		for(var i in ret["department"]){
			if(i != "三级部门") {
				department += '<li class="dep" hasTow=false role="presentation" ><a role="menuitem" tabindex="-1">'+i+'</a></ul>';
			  }
		}
		if($("#province").attr("get").toString() == "false"){
			$(".title .dropdown").eq(2).children(".dropdown-menu").html(province);
		}
		if($("#city").attr("get").toString() == "false"){
			$(".title .dropdown").eq(1).children(".dropdown-menu").html(city);
		}
		$(".title .dropdown").eq(0).children(".dropdown-menu").html(department);
		if($("#province").text() == ""){
			$("#province").html($(".title .dropdown").eq(2).children(".dropdown-menu").children("li").eq(0).children("a").text());
		}if($("#city").text() == ""){
			$("#city").html($(".title .dropdown").eq(1).children(".dropdown-menu").children("li").eq(0).children("a").text());
		}
		$(".title .dropdown").eq(2).children("ul").children("li").click(function(){
			var province = $("#province").text();
			$("#province").text($(this).children("a").text());
			$("#province").attr("get", "true");
			var urlData = get_url_data();
			if(province != $(this).children("a").text()){
				if($("#isAdmin").text() == "2"){
					$("#city").text("二级部门");
				}
				$("#department").text("三级部门");
				$("#city").attr("get", "false");
				get_dep_data();
				setTimeout("reloadPage()","100");//刷新页面延迟			
			}
		}); 
		$(".title .dropdown").eq(1).children("ul").children("li").click(function(){
			var city = $("#city").text();
			var urlData = get_url_data();
			$("#city").text($(this).children("a").text());
			$("#city").attr("get", "true");
			if(city != $(this).children("a").text()){
				get_dep_data();
				setTimeout("reloadPage()","100");//刷新页面
			}
			
		});
		$(".title .dropdown").eq(0).children("ul").children("li").click(function(){
			var department = $("#department").text();
			$("#department").text($(this).children("a").text());
			setTimeout("reloadPage()","100");//刷新页面
		});
		$(".dep").hover(function(){
			$("#get_dpt").text($(this).children("a").text());
			if(String($(this).attr("hasTow")) == "true"){
				if($("#dpt_2").text() != ""){
					$("#dpt_2").remove();
				}
				var dpt_2="";
				for(var i in ret["department"]){
					if($(this).text() == i){
						dpt_2 = get_dpt_2_html(ret["department"][i]);
					}
				}
				$("body").append(dpt_2);
				$("#dpt_2").css("top", getTop(this)+document.body.scrollTop);
				$("#dpt_2").css("left",getLeft(this)+$("#depul").width());
			}
			$("#dpt_2 ul li").click(function(){
				if($("#dpt_2").text() != undefined){
					$("#get_dpt").text($(this).text());
					$("#dpt_2").remove();
					$("#department").text($("#get_dpt").text())
					setTimeout("reloadPage()","100");//刷新页面
				}
			});
			$("#dpt_2").hover(function(){}, function(){
				$("#dpt_2").remove();
			})
			
			$("#dpt_2 ul li").hover(function(){  //变灰
				$(this).css("background-color","#F5F5F5");
				},function(){
				$(this).css("background-color","white");
			});
			
		},function(){
			//$("#dpt_2").remove();
		})
		if($("ul:eq(0) li:first").text() != "") {
			$("#department").html($("ul:eq(0) li:first").text());
		}
	}
	if($("#wPage").text() == 0){
	firstClick();
}
}

//获取元素的纵坐标
function getTop(e){
  var offset=e.offsetTop;
  if(e.offsetParent!=null) offset+=getTop(e.offsetParent);
  offset-=e.scrollTop;
  return offset;
}
//获取元素的横坐标
function getLeft(e){
  var offset=e.offsetLeft;
  if(e.offsetParent!=null) offset+=getLeft(e.offsetParent);
  return offset;
}

function get_dpt_2_html(data){
	html = "<div id='dpt_2' style='position:absolute;min-width:100px; max-width:200px; border:2px solid #ccc; background:#fff;max-height:500px;overflow:auto;z-index:100;'><ul style='padding:5px 10px;'>";
	for(var i in data){
		html += "<li style='list-style-type:none; cursor:pointer;'>"+data[i]+"</li>";
	}
	html += "</ul></div>";

	return html;
}



function set_key_data(ret){
	var html = "";
	if(ret != undefined && ret != false){
		
		if(parseInt(ret["key_count"]) == 0){  //总页数
			$("#pageCount").text(1);
		}else{
			$("#pageCount").text(Math.ceil(parseInt(ret["key_count"])/20));  //key_count为当前页有几条
		}
		$("#pageCountBelow").text($("#pageCount").text());
		
		for(var i=0; i < ret["key_data"].length; i++){
			if($("#isAdmin").text().toString() == "1"){
				if(ret["key_data"][i]["isUpdate"].toString() == "1"){
					html += "<tr id='"+ret["key_data"][i]["keyId"]+"'><td> <input class='key_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;'>"+ret["key_data"][i]["keyword"]+"</td>";
				}else{
					html += "<tr id='"+ret["key_data"][i]["keyId"]+"'><td> <input disabled='disabled' class='key_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;'>"+ret["key_data"][i]["keyword"]+"</td>";
				}
			}else{
				html += "<tr id='"+ret["key_data"][i]["keyId"]+"'><td> <input class='key_check' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;'>"+ret["key_data"][i]["keyword"]+"</td>";
			}

			if(ret["key_data"][i]["keyLever"] == 0){
				html += "<td align='center' style=''><span style='color:white;background-color:red;padding:3px 3px 3px 3px; border-radius: 5px;'>严重</span></td>";
			}else if(ret["key_data"][i]["keyLever"] == 1){
				html += "<td align='center' style=''><span style='color:white;background-color:#ff9933;padding:3px 3px 3px 3px; border-radius: 5px;'>重要</span></td>";
			}else{
				html += "<td align='center' style=''><span style='color:white;background-color:#009900;padding:3px 3px 3px 3px; border-radius: 5px;'>一般</span></td>";
			}
			if($("#isAdmin").text().toString() == "1"){
				if(ret["key_data"][i]["isUpdate"].toString() == "1"){
					html += "<td align='center'><button onclick='update_key(this)' type='button' class='btn btn-link' style='padding:0;'>修改</button></td>";
				}else{
					html += "<td align='center'><button disabled='disabled' onclick='update_key(this)' type='button' class='btn btn-link' style='padding:0;'>修改</button></td>";
				}
			}else{
				html += "<td align='center'><button onclick='update_key(this)' type='button' class='btn btn-link' style='padding:0;'>修改</button></td>";
			}

			html += "</tr>"
		}
	}
	$("#key_data").html(html);
	$("#keyCount").text(parseInt(ret["key_count"]));
	$("tbody td").css("width", "20%");
	$("#LoadingBar").css('display','none'); 
}


function quit_sucess(ret){
	window.location.href = "/login";
}


function quit(){
	jquery_ajax('/index/quit', {}, quit_sucess);
}


function delete_key_sucess(ret){
	if(ret == true){
		dialogAlert("删除成功！", false, []);
		get_key_data();
	}else{
		dialogAlert("您的操作有误,请稍后重试！", false, []);
	}
}


function delete_key_data(elem){//删除关键字
	var urlData = get_url_data();
	jquery_ajax("/index/delete_key_data", {"key_list": elem[0], "user_acc": urlData["userAcc"]}, delete_key_sucess)
}


function delete_key(){	//删除关键字
	var update_key = false;
	$("tbody tr").each(function(){
		if($(this).attr("update") != undefined){
			update_key = true;
		}
	});
	if($("tbody tr").eq($("tbody tr").length -1).attr("increase") != undefined || update_key == true){
		dialogAlert("请提交后再做删除动作!", false, []);
	}else{
		var delete_key = "";
		$(".key_check").each(function(){
			if($(this).attr("checked") == "checked"){
				delete_key += $(this).parent().parent().attr("id") + "|";
			}
		});
		if(delete_key != ""){
			confirmAlert("您确定要对这些关键字进行删除操作？", delete_key_data, false, [delete_key, ], []);
		}else{
			dialogAlert("您没有选中任何关键字,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
		}
	}
}


function input_key_sucess(ret){
	if(ret == true){
		dialogAlert("提交成功!", false, []);
		get_key_data();
	}else{
		dialogAlert("您填写的数据有问题(如关键字重复等问题),请仔细检查后在作提交!", false, []);
		get_key_data();
	}
}


function input_key_data(elem){
	var province = $("#province").text();
	var city = $("#city").text();
	var department = $("#department").text();
	var urlData = get_url_data();
	jquery_ajax("/index/input_key_data", {"key_data": elem[0], "userAcc": urlData["userAcc"], "province": province, "city":city, "department":department}, input_key_sucess)
}


function input_key(){	//提交用户修改
	var key_update = false;
	var defaule = false;
	var key_data = "";
	var breaktag = false;
	$("tbody tr").each(function(){
		if($(this).attr("update") != undefined){
			if($(this).children("td").eq(1).text() != ""){
				key_update = true;
				key_data += $(this).attr("id") +"&"+$(this).children("td").eq(0).text() +"&"+$(this).children("td").eq(1).children("select").val()+ ",update|"
			}else{
				defaule = true;
			}
		}
		if($(this).attr("increase") != undefined){
			if($(this).children("td").eq(0).children("div").text() != ""){
				if($(this).children("td").eq(0).children("div").text().indexOf("|") >= 0) {
					dialogAlert("关键字中不能含有'|'！", false, []);
					breaktag = true;
					return;
				}
				key_update = true;
				key_data += $(this).children("td").eq(0).children("div").text()+"&"+ $(this).children("td").eq(1).children("select").val() + ",increase|"
			}else{
				defaule = true;
			}
		}
	});
	if(breaktag == true) {
		return;
	}
	if(key_update == true && defaule != true){
		confirmAlert("您确定要对这些写数据进行修改？", input_key_data, false, [key_data, ], []);
	}
	if(key_update == true && defaule == true){
		dialogAlert("您填写的数据有问题，请仔细检查后在作提交!", false, []);
		get_key_data();
	}
	if(key_update == false && defaule == true){
		dialogAlert("您填写的数据有问题，请仔细检查后在作提交!", false, []);
		get_key_data();
	}
	if(key_update == false && defaule == false){
		dialogAlert("您没有修改或增加任何用户,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}

}


function update_key(elem){
	if($("tbody tr").eq($("tbody tr").length -1).attr("increase") != undefined){
		dialogAlert("请提交后再添加!", false, []);
	}else {
		var key = $(elem).parent().parent().children("td").eq(0).text();
		$(elem).parent().parent().attr("update", true);
		$(elem).parent().parent().children("td").eq(0).html("<div style='background:#eee;' contenteditable='true'>"+key+"</div>");
		var select = "<select><option value=2>一般</option><option value=1>重要</option><option value=0>严重</option></select>";
		$(elem).parent().parent().children("td").eq(1).html(select);
		$(elem).parent().parent().children("td").eq(0).children("div").focus();
	}
}

function increase_key(){
	if($("tbody tr").eq(0).attr("increase") != undefined){
		dialogAlert("请提交后再添加!", false, []);
	}else{
		var html = '<tr increase="true"><td><div contenteditable="true" style="background:#eee;"></div></td>';
		html += '<td><select><option value=2>一般</option><option value=1>重要</option><option value=0>严重</option></select></td>';
		html += '<td><button onclick="drop_column(this)" type="button" class="btn btn-link" style="padding:0;">取消</button></td></tr>';
		if($("table tbody tr").length != 0){
			$("table tbody tr").eq(0).before(html);
		}else{
			$("table tbody").html(html);
		}
		$("tbody tr").eq(0).children("td").eq(0).children("div").focus();
	}
}


function get_key_data(){
	var department = $("#department").text();
	if(department == "--请选择--"){
		dialogAlert("请选择部门!", false, []);
	}else {
		$("#LoadingBar").show();
		var urlData = get_url_data();
		var province = $("#province").text();
		var city = $("#city").text();
		var page = $("#page").text();
		var data = {"user_acc": urlData["userAcc"], "province": province, "city": city, "department": department, "page": page};
		jquery_ajax("/index/get_key_data", data, set_key_data)
		$("#selectAll").removeAttr("checked");
	}
}


function set_keyword_html(ret){
	$(".bottom").html("");
    if(ret != undefined){
        $("#body").html(ret);
		$("th").eq(0).css("width", "150px");
		$("th").eq(1).css("width", "150px");
		get_key_data();
    }
}


function keyClick(){
	get_html("/keyword.html", set_keyword_html);
	$("#wPage").text(5);
}

function set_is_admin(ret){
	$("#isAdmin").text(ret);
	//if(ret.toString() != "2" || $("#userCity").text() != "省级部门"){
	if(ret.toString() != "2"){
		$("#departManage").remove();
	}
}

function get_is_admin(){
	var urlData = get_url_data();
	jquery_ajax("/index/get_is_admin", {"userNo": urlData["userAcc"]}, set_is_admin)
}


function department_before(){
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		get_departManage_data();
	}
	$("#pageBelow").text($("#page").text());
}


function department_after(){
	var pageCount = $("#pageCount").text();
	var page = $("#page").text();
	if(page.toString() == pageCount.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		get_departManage_data();
	}
	$("#pageBelow").text($("#page").text());
}

function update_department(elem){
	if($("tbody tr").eq($("tbody tr").length -1).attr("increase") != undefined){
		dialogAlert("请提交后再添加!", false, []);
	}else {
		var department = $(elem).parent().parent().children("td").eq(0).text();
		var time = $(elem).parent().parent().children("td").eq(1).text();
		var create_user = $(elem).parent().parent().children("td").eq(2).text();
		$(elem).parent().parent().attr("update", true);
		$(elem).parent().parent().children("td").eq(0).html("<div style='background:#eee;' contenteditable='true'>"+department+"</div>");
		$(elem).parent().parent().children("td").eq(1).html(time);
		$(elem).parent().parent().children("td").eq(2).html(create_user);
		$(elem).parent().parent().children("td").eq(0).children("div").focus();
	}
}


function input_department_sucess(ret){
	if(ret == true){
		dialogAlert("提交成功!", false, []);
		get_info_data();
		get_dep_data();
		get_departManage_data();
	}else{
		dialogAlert("您填写的数据有问题, 请仔细检查后在作提交!", false, []);
	}
}


function input_department_data(elem){
	var province = $("#province").text();
	var city = $("#city").text();
	var department = $("#department").text();
	var urlData = get_url_data();
	jquery_ajax("/index/input_department_data", {"department_data": elem[0], "userAcc": urlData["userAcc"], "province": province, "city":city, "department":department}, input_department_sucess)
}


function input_department(){
	var department_update = false;
	var defaule = false;
	var department_data = "";
	$("tbody tr").each(function(){
		if($(this).attr("update") != undefined){
			if($(this).children("td").eq(1).text() != ""){
				department_update = true;
				department_data += $(this).attr("id") +"&"+$(this).children("td").eq(0).text() + ",update|"
			}else{
				defaule = true;
			}
		}
		if($(this).attr("increase") != undefined){
			/*if($(this).children("td").eq(0).children("div").text() != ""){
				department_update = true;
				department_data += $(this).children("td").eq(2).children("div").text() +"&"+ $(this).children("td").eq(3).text()+"&"+ $(this).children("td").eq(0).text()+"&"+ $(this).children("td").eq(1).text()+",increase|"
			}else{
				defaule = true;
			}*/
			if($(this).children("td").eq(0).children("div").text() == ""){  //一级部门为空
				dialogAlert("请输入一级部门!", false, []);
				defaule = true;
			} else if($(this).children("td").eq(1).children("div").text() == "" && $("#province").text() != "一级部门"){  //二级部门为空
				dialogAlert("请输入二级部门!", false, []);
				defaule = true;
			} else if($(this).children("td").eq(2).children("div").text() == "" && $("#city").text() != "二级部门"){  //三级部门为空
				dialogAlert("请输入三级部门!", false, []);
				defaule = true;
			} else{
				department_update = true;
				department_data += $(this).children("td").eq(2).children("div").text() +"&"+ $(this).children("td").eq(3).text()+"&"+ $(this).children("td").eq(0).text()+"&"+ $(this).children("td").eq(1).text()+",increase|"
			}
		}
	});
	if(department_update == true && defaule != true){
		confirmAlert("您确定要对这些写数据进行修改？", input_department_data, false, [department_data, ], []);
	}
	/*if(department_update == true && defaule == true){
		dialogAlert("您填写的数据有问题，请仔细检查后在作提交!", false, []);
	}
	if(department_update == false && defaule == true){
		dialogAlert("您填写的数据有问题，请仔细检查后在作提交!", false, []);
	}
	if(department_update == false && defaule == false){
		dialogAlert("您没有修改或增加任何用户,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
	}*/
}

function set_departManage_data(ret){
	html = "";
	if(ret != undefined) {
		for (var index = 0; index < ret["department_data"].length; index++) {
			html += "<tr id='"+ret["department_data"][index]["departmentId"]+"'>";
			html += "<td><input class='dep_checke' onclick='user_check_click(this)' type='checkBox' style='margin-right:10px;'>"+ret["department_data"][index]["province"]+"</td>";
			html += "<td>"+ret["department_data"][index]["city"]+"</td>";
			html += "<td>"+ret["department_data"][index]["departmentName"]+"</td>";
			html += "<td>"+ret["department_data"][index]["createTime"]+"</td>";
			if(ret["department_data"][index]["createUser"] != null){
				html += "<td><span style='cursor:pointer;' data-html='true' data-toggle='popover' data-trigger='hover' data-containter='body' data-placement='top' data-content='"+ret["department_data"][index]["createUser"]+"'>"+ret["department_data"][index]["createUser"]+"</span></td>";
			}
			/*html += "<td><button onclick='update_department(this)' type='button' class='btn btn-link' style='padding:0;'>修改</button></td>";*/
			html += "</tr>"
		}
		if(ret["count"].toString() == "0"){
			$("#page").text(1);
			$("#pageCount").text(1);
		}else{
			if($("#province").text() == "中央部门") {
				$("#pageCount").text(Math.ceil((parseInt(ret["count"]) - 1) / 20));
			} else {
				$("#pageCount").text(Math.ceil(parseInt(ret["count"]) / 20));
			}
		}
		$("#pageCountBelow").text($("#pageCount").text());
	}else{

	}
	$("#department_data").html(html);
	$("#depCount").text(parseInt(ret["count"]));
	$("#department_data tr td span").popover();
	$("#LoadingBar").css('display','none'); 
}


function delete_department_sucess(ret){
	$("#LoadingBar").css('display','none');
	if(ret == true){
		dialogAlert("删除成功！", false, []);
		get_info_data();
		get_dep_data();
		get_departManage_data();
	}else{
		dialogAlert("您的操作有误,请稍后重试！", false, []);
	}
}



function delete_department_data(elem){//删除部门
	$("#LoadingBar").show();
	var urlData = get_url_data();
	jquery_ajax("/index/delete_department_data", {"department_list": elem[0], "user_acc": urlData["userAcc"]}, delete_department_sucess)
}

function delete_department(){
	var update_department = false;
	$("tbody tr").each(function(){
		if($(this).attr("update") != undefined){
			update_department = true;
		}
	});
	if($("tbody tr").eq(0).attr("increase") != undefined || update_department == true){
		dialogAlert("请提交后再做删除动作!", false, []);
	}else {
		var delete_department = "";
		var breaktag = false;
		$(".dep_checke").each(function () {
			if ($(this).attr("checked") == "checked") {
				if($("#userDep").text() == "超高级管理员") {
					if($(this).parent().parent().children("td").eq(0).text() == "一级部门") {
						dialogAlert("您不能删除自己所在的部门！", false, []);
						breaktag = true;
						return;
					}
				} else if($("#isAdmin").text() == "2") {
					if($(this).parent().parent().children("td").eq(1).text() == "二级部门") {
						dialogAlert("您不能删除自己所在的部门！", false, []);
						breaktag = true;
						return;
					}
				} else if($(this).parent().parent().children("td").eq(2).text() == $("#userDep").text()) {
					dialogAlert("您不能删除自己所在的部门！", false, []);
					breaktag = true;
					return;
				}
				delete_department += $(this).parent().parent().attr("id") + "|";
			}
		});
		if(breaktag == true) {
			return;
		}
		if (delete_department != "") {
			confirmAlert("注意：删除部门时会将该部门相关的数据和所属该部门的人员一并删除，您确定要对这些部门进行删除操作吗？", delete_department_data, false, [delete_department,], []);
		} else {
			dialogAlert("您没有选中任何部门,可能是做了错误的操作,如有问题请联系我们的开发人员或工作人员,感谢您的合作,祝您工作生活愉快!", false, []);
		}
	}
}

/*function getLabel(elem) {
	$("#inputProvince").text($(elem).text());
	$("#selPro").css('display','none');
}

function getNewPro() {
	$("#inputProvince").text($("#newPro").val());
	$("#selPro").css('display','none');
}*/

function increase_department(){
	if($("tbody tr").eq(0).attr("increase") != undefined){
		dialogAlert("请提交后再添加!", false, []);
	} else if($("#department").text() != "三级部门") {
		dialogAlert("请不要在三级部门下添加部门!", false, []);
	} else {
		var html = '<tr increase="true">';
		if($("#province").text() == "一级部门") {
			html += '<td><div contenteditable="true" id="inputProvince" style="background:#eee;"></div></td>';
		} else {
			html += '<td><div contenteditable="false" id="inputProvince">' + $("#province").text() + '</div></td>';
		}
		if($("#city").text() == "二级部门") {
			html += '<td><div contenteditable="true" id="inputCity" style="background:#eee;"></div></td>';
		} else {
			html += '<td><div contenteditable="false" id="inputCity">' + $("#city").text() + '</div></td>';
		}
		html += '<td><div contenteditable="true" style="background:#eee;"></div></td>';
		html += '<td> '+get_current_time()+' </td>';
		html += '<td align="center"><button onclick="drop_column(this)" type="button" class="btn btn-link" style="padding:0;">取消</button></td></td>';
		html += "</tr>";
		if($("table tbody tr").length != 0){
			$("table tbody tr").eq(0).before(html);
		}else{
			$("table tbody").html(html);
		}
		/*$("#inputProvince").blur(function(){
			if($("#inputProvince").text() == "所有省"){
				$("#inputCity").text("所有市");
				document.getElementById("inputCity").contentEditable = false;
			}
			});*/
		/*$("#inputProvince").focus(function(){
			$("#selPro").show();
			$("#newPro").focus();
			});*/
		$("tbody tr").eq(0).children("td").eq(0).children("div").focus();
	}
}


function get_departManage_data(){
	var department = $("#department").text();
	if(department == "--请选择--"){
		dialogAlert("请选择部门!", false, []);
	}else{
		$("#LoadingBar").show();
		var urlData = get_url_data();
		var province = $("#province").text();
		var city = $("#city").text();
		var page = $("#page").text();
		var data = {"userAcc": urlData["userAcc"], "province": province, "city": city, "department": department, "page": page};
		jquery_ajax("/index/get_departManage_data", data, set_departManage_data);
		$("#selectAll").removeAttr("checked");
	}
}


function set_departManage_html(ret){
	$(".bottom").html("");
    if(ret != undefined){
        $("#body").html(ret);
		get_departManage_data()
    }
}


function departManage(){
	get_html("/departmentManage.html", set_departManage_html);
	$("#wPage").text(4);
}

function keybefore_page(){	//上一页(关键字)
	var page = $("#page").text();
	if(page.toString() == "1"){
		dialogAlert("已经到达第一页!", false, []);
	}else{
		$("#page").text(parseInt(page) - 1);
		if($("#key_select_data").val() !=""){
		keyspanSelectClick();
	}else{
		get_key_data();
	}
	}
	$("#pageBelow").text($("#page").text());
}


function keyafter_page(){	//下一页(关键字)
	var page = $("#page").text();
	var end_page = $("#pageCount").text();
	if(page.toString() == end_page.toString()){
		dialogAlert("已经到达最后一页!", false, []);
	}else{
		$("#page").text(parseInt(page) + 1);
		if($("#key_select_data").val() !=""){
		keyspanSelectClick();
	}else{
		get_key_data();
	}
	}
	$("#pageBelow").text($("#page").text());
}

function keyspanSelectClick(elem){	//关键字页面翻页
	if($("#key_select_data").val() !=""){
	spanClick(keyspanSelectClick,[elem, ]);
	}else{
	spanClick(get_key_data, [elem, ]);
}
}

function depspanSelectClick(elem){	//部门管理页面翻页
	spanClick(get_departManage_data, [elem, ]);
}

function reloadPage() {
	var wPage = $("#wPage").text();
	if(parseInt(wPage) == 1) {
		$("#selectLevel").val("所有");
		getUserErr();
	}else if(parseInt(wPage) == 2) {
		userManage();
	}else if(parseInt(wPage) == 3) {
		connClick();
	}else if(parseInt(wPage) == 4) {
		departManage();
	}else if(parseInt(wPage) == 5) {
		keyClick();		
	}else if(parseInt(wPage) == 6) {
		aboutClick();
	}else if(parseInt(wPage) == 7) {
		get_scan_file();
	}else if(parseInt(wPage) == 8) {
		userErrorCount();
	}else if(parseInt(wPage) == 9) {
		get_error_data_more();
	}else {
		firstClick();
	}
}

function usermanagespanSelectClick(elem){	//人员管理信息页面翻页
	if($("#select_data").val() != ""){
		spanClick(btnPeoSelectClick, [elem, ]);
		}else{
		spanClick(get_user_data, [elem, ]);
	}

}

function timespansearch() {
	$("#page").text(1);
	$("#personSearch").val("0");
	$("#select_data").val("");
	var startTime = $("#startTime").val();
	var endTime = $("#endTime").val();
	var date1 = new Date(startTime);
    var date2 = new Date(endTime);
    if(date1.getTime() > date2.getTime()){
		dialogAlert("结束时间必须大于开始时间！", false, []);
    } else {
		$("#timeSearch").val("1");
		get_user_error_data();
	}
}

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

function setOnline() {
	if($("#online").val() == "1") {
		$("#online").attr('value','0');
		$("#online").css('background-color','#9c9c9c');
	} else {
		$("#online").val("1");
		$("#online").css('background-color','#62e588');
		$("#offline").val("0");
		$("#offline").css('background-color','#9c9c9c');
	}
	get_user_online_data();
}

function setOffline() {
	if($("#offline").val() == "1") {
		$("#offline").val("0");
		$("#offline").css('background-color','#9c9c9c');
	} else {
		$("#offline").val("1");
		$("#offline").css('background-color','#f22222');
		$("#online").attr('value','0');
		$("#online").css('background-color','#9c9c9c');
	}
	get_user_offline_data();
}

function  getSingleKeyWord(keyWords,keyExtend,type) {  //keyWords为关键字原文，keyExtend为关键字上下文
	if (keyExtend == null){
		return keyExtend;
	}else{
	if(type == 1) {
		/*var start = keyWords.indexOf("关键字",0); 
		var end = keyWords.indexOf("重复次数",0); 
		var keyword = keyWords.substr(start + 4,end - start - 5); //得到关键字
		var keyPos = keyExtend.indexOf(keyword);  //关键字在关键字上下文中的位置
		var keyLevel = keyWords.substr(keyWords.indexOf("级别") + 3,1); //关键字级别*/
		var start = keyWords.indexOf("级别:0",0);   //例：(级别:0 关键字:中国人民共和国 重复次数:1)
		if(start == -1) {
			start = keyWords.indexOf("级别:1",0); 
			if(start == -1) {
				start = keyWords.indexOf("级别:2",0); 
			}
		}
		var end = keyWords.indexOf("重复次数",start); 
		var keyword = keyWords.substr(start + 9,end - start - 10); //得到关键字
		var keyPos = keyExtend.indexOf(keyword);  //关键字在关键字上下文中的位置
		var keyLevel = keyWords.substr(start + 3,1); //关键字级别
	} else if(type == 2) {
		var start = keyWords.indexOf("-",0); 
		var end = keyWords.indexOf("-",2); 
		var keyword = keyWords.substr(start + 1,end - start - 1); //得到关键字
		var keyPos = keyExtend.indexOf(keyword);  //关键字在关键字上下文中的位置
		var keyLevel = keyWords.substr(0,1); //关键字级别
	}
	var first = keyExtend.substr(0,keyPos);
	if(keyLevel == "0") {
		var second = "<font color='red' style='font-weight:800' >" + keyword + "</font>";
	} else if(keyLevel == "1") {
		var second = "<font color='#d2830d' style='font-weight:800' >" + keyword + "</font>";
	} else if(keyLevel == "2") {
		var second = "<font color='#009900' style='font-weight:800' >" + keyword + "</font>";
	}	
	var thirdLen = keyExtend.length - first.length - keyword.length; //最后一段长度
	var third = keyExtend.substr(keyPos + keyword.length,thirdLen);
	return first + second + third;
}
}

$(function(){
	get_is_admin();
	get_info_data();
	setTimeout("get_dep_data()","220");
	$(".index div").click(function(){
		clearn_index_style();
		$(this).css("background-color", "#01263a");
	});
	$("body").click(function(){
		$("#dpt_2").remove();
	})
	$("#grantInfo").hover(function(){
		get_grant_data();
	},function(){
		$("#grantDetail").hide();
	});
});

function get_grant_data(){
	jquery_ajax('/index/get_grant_data', {}, set_grant_data);
}

function set_grant_data(ret){
	var html = "";
	if(ret != undefined && ret != false){
		$("#grantDetail").show();
		var table="<table style='white-space: nowrap;'>";
		table += "<tr><td style='width:120px;'>授权单位：" + ret["ret_ukey"]["company"]+"</td></tr>";
		table += "<tr><td style='width:120px;'>最大用户规模：" + ret["ret_ukey"]["user_scale"]+"</td></tr>";
		table += "<tr><td style='width:120px;'>当前注册人数：" + ret["ret_ukey"]["install_num"]+"</td></tr>";
		table += "<tr><td style='width:120px;'>服务到期时间：" + ret["ret_ukey"]["expired_time"]+"</td></tr>";
		table +="</table>";
		$("#grantDetail").html(table);
	}
}
