"""SafeProgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
#from django.contrib import admin
from WEB import login
from WEB import index
from WEB import oprate
from WEB import selfcheck

urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^about$', oprate.about),
    url(r'^$', login.login),
    url(r'^login$', login.login),
    url(r'^loginScanSelf$', login.loginScanSelf),
    url(r'^first.html$', oprate.first),
    url(r'^userErrorCount.html$', oprate.userErrorCount),
    url(r'^errorDataMore.html$', oprate.errorDataMore),
    url(r'^userScan.html$', oprate.userScan),
    url(r'^userConn.html$', oprate.userConn),
    url(r'^departmentManage.html$', oprate.departmentManage),
    url(r'^userManage.html$', oprate.userManage),
    url(r'^userError.html$', oprate.user_error),
    url(r'^keyword.html$', oprate.keyword),
    url(r'^querySelf.html$', selfcheck.querySelf),
    url(r'^userQuery.html$', selfcheck.userQuery),
    url(r'^userQueryCount.html$', selfcheck.userQueryCount),
    url(r'^passwdChange.html$', selfcheck.passwdChange),
    url(r'^source404.html$', selfcheck.source404),
    url(r'^login/user_login$', login.user_login),
    url(r'^login/indentifying_code$', login.indentifying_code),
    url(r'^index/userAcc=[A-Za-z0-9_]+$', index.index),
    url(r'^indexScanSelf/userAcc=[A-Za-z0-9_]+$', index.indexScanSelf),
    url(r'^index/get_dep_count$', index.get_dep_count),
    url(r'^index/get_dep_user_count$', index.get_dep_user_count),
    url(r'^index/get_user_error$', index.get_user_error),
    url(r'^index/get_user_error_bytime$', index.get_user_error_bytime),
    url(r'^index/get_user_error_byperson$', index.get_user_error_byperson),
    url(r'^index/get_user_error_detail$', index.get_user_error_detail),
    url(r'^index/get_departManage_data$', index.get_departManage_data),
    url(r'^index/get_user_conn_data$', index.get_user_conn_data),
    url(r'^index/get_dpt_data$', index.get_dpt_data),
    url(r'^index/user_error$', index.user_error),
    url(r'^index/del_user_error$', index.del_user_error),
    url(r'^index/close_net$', index.close_net),
    url(r'^index/scan_file$', index.scan_file),
    url(r'^index/scan_self$',index.scan_self),
    url(r'^index/remove_self$', index.remove_self),
    url(r'^index/input_user_data$', index.input_user_data),
    url(r'^index/get_user_data$', index.get_user_data),
    url(r'^index/get_user_data_select', index.get_user_data_select),
    url(r'^index/reset_user$', index.reset_user),
    url(r'^index/get_is_admin$', index.get_is_admin),
    url(r'^index/get_scan_file$', index.get_scan_file),
    url(r'^index/get_scan_file_bytime$', index.get_scan_file_bytime),
    url(r'^index/delete_key_data$', index.delete_key_data),
    url(r'^index/get_key_data$', index.get_key_data),
    url(r'^index/get_user_key_select$', index.get_user_key_select),
    url(r'^index/input_key_data$', index.input_key_data),
    url(r'^index/delete_department_data$', index.delete_department_data),
    url(r'^index/quit$', index.quit),
    url(r'^index/download_file', index.download_file),
    url(r'^index/download_client', index.download_client),
    url(r'^index/input_department_data', index.input_department_data),
    url(r'^index/delete_user_data$', index.delete_user_data),
    url(r'^selfcheck/get_selfcheck_data$',selfcheck.get_selfcheck_data),
    url(r'^selfcheck/get_selfcheck_count_data$',selfcheck.get_selfcheck_count_data),
    url(r'^selfcheck/set_selfcheck_data$',selfcheck.set_selfcheck_data),
    url(r'^selfcheck/delete_mulrecord_data$',selfcheck.delete_mulrecord_data),
    url(r'^selfcheck/delete_timespan_data$',selfcheck.delete_timespan_data),
    url(r'^selfcheck/set_newpasswd$',selfcheck.set_newpasswd),
    url(r'^index/import_excel$',index.import_excel),
    url(r'^index/download_excel_file',index.download_excel_file),
    url(r'^index/get_grant_data$', index.get_grant_data)
]
