from .DAL_ukey import DAL_insert_ukey_info,DAL_get_ukey_info
def BLL_insert_ukey_info():
	data = load_granted_info()
	company = data["company"]
	user_scale = data["user_scale"]
	expired_time = data["expired_time"]
	install_num = DAL_get_install_num()[0][0]
	DAL_insert_ukey_info(company,user_scale,install_num,expired_time)


def BLL_get_ukey_info():
	ukey_info = DAL_get_ukey_info()
	ret_ukey = {}
	for index in ukey_info:
		ret_ukey["company"] = index[0]
		ret_ukey["user_scale"] = index[1]
		ret_ukey["install_num"] = index[2]
		ret_ukey["expired_time"] = index[3]
	return ret_ukey





