import unittest
from .DAL_ukey import DAL_insert_ukey_info,DAL_get_install_num
from .BLL_ukey import BLL_get_ukey_info

class TestServ(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	def test_DAL_insert_ukey_info(self):
		company = "西安理工大学"
		user_scale = 1000
		installNum = 123
		serviceUtilTime = 1494562908
		self.assertTrue(0 != DAL_insert_ukey_info(company,user_scale,installNum,serviceUtilTime))
	def test_DAL_install_num(self):
            self.assertTrue(len(DAL_get_install_num()) != 0)
	def test_BLL_get_ukey_info(self):
            self.assertTrue(len(BLL_get_ukey_info()) == 4) 
