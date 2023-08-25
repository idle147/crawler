import time
import unittest

from scrapyd_api import ScrapydAPI, constants


class TestSrapyd(unittest.TestCase):

    def setUp(self) -> None:
        self.scrapyd = ScrapydAPI('http://127.0.0.1:6800')

    def tearDown(self):
        pass

    def _get_all_job(self, project_name):
        """ 获取所有的job名称 """
        return self.scrapyd.list_jobs(project_name)

    def test_projects(self):
        res = self.scrapyd.list_projects()
        self.assertTrue("piracy_crawl" in res)

    def test_spiders(self):
        res = self.scrapyd.list_spiders("piracy_crawl")
        self.assertTrue(len(res) == 5)
        self.assertTrue("_360" in res)
        self.assertTrue("_4399" in res)
        self.assertTrue("_962" in res)
        self.assertTrue("_5577" in res)
        self.assertTrue("anzhi" in res)

    def test_schedule(self):
        try:
            job_id = self.scrapyd.schedule('piracy_crawl', ['_5577', '_360'],
                                           user_id=1,
                                           keyword="平安京")
        except Exception:
            return self.assertTrue(False)
        else:
            # 判断job是否在运行
            while True:
                status = self.scrapyd.job_status('piracy_crawl', job_id)
                if status == constants.FINISHED:
                    self.assertTrue(True)
                    time.sleep(3)
                    return

    def test_simultaneous_processing(self):
        job_id_1 = self.scrapyd.schedule('piracy_crawl', '_360', user_id=1, keyword="平安京")
        job_id_2 = self.scrapyd.schedule('piracy_crawl', '_5577', user_id=1, keyword="平安京")
        time.sleep(6)
        job_list = self._get_all_job('piracy_crawl')
        id_list = [item["id"] for item in job_list["running"]]
        self.assertTrue(job_id_1 in id_list)
        self.assertTrue(job_id_2 in id_list)
