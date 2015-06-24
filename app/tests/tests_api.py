import unittest
from src import app 

class ApiIssuesTestCase(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		self.client = app.test_client()

	def test_get_issues(self):
		res = self.client.get('/api/v2/issues')
		self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
	unittest.main()
