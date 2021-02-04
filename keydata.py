from datetime import datetime, timedelta
from requests import session
import json

class jetty_data:

    def __init__(self, config, cookie):
        self.config = config
        self.header = {
            "accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Host": "10.25.150.103:19095",
            "Referer": "http://10.25.150.103:19095/d/Kz4-4g6Wk/guan-jian-zhi-biao-zhan-shi-tu?orgId=1&refresh=30m",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53",
            "x-dashboard-id": "99",
            "x-grafana-org-id": "1",
            "x-panel-id": "8"
        }
        self.param = {
            "query": "(jetty_queued_thread_pool_threads{unit=\"myapp\",pod=~\"gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456fdvfs|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bjhfn|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bcnfs|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456z9fnm|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bw5t6\"}-jetty_queued_thread_pool_threads_idle{unit=\"myapp\",pod=~\"gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456fdvfs|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bjhfn|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bcnfs|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456z9fnm|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bw5t6\"})/jetty_queued_thread_pool_threads_max{unit=\"myapp\",pod=~\"gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456fdvfs|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bjhfn|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bcnfs|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456z9fnm|gateway-service-private-prod-2\\\\.2\\\\.0-20201015172229-775b8456bw5t6\"}",
            "start": f"{int((datetime.now()-timedelta(minutes=30)).timestamp())}",
            "end": f"{int(datetime.now().timestamp())}",
            "step": "20"
        }
        self.url = "http://10.25.150.103:19095/api/datasources/proxy/1/api/v1/query_range"
        self.s = session()
        self.status = True
    
    def getdata(self):
        r = self.s.get(self.url, params=self.param, headers=self.header, timeout=10)
        if r.status_code == 200:
            return r
        else:
            print(f"jetty 接口响应不正常 code: {r.status_code}")
            self.status = False
    
    def judge(self):
        len_status = False
        value_status = True
        result = self.getdata()
        # writejson(result.json())
        if result != None and self.status:
            try:
                res = result.json()["data"]["result"]
                for i in res:
                    if len(i["values"]) > 10:
                        len_status = True
                    for v in i["values"]:
                        if float(v[1]) > self.config["jetty"]:
                            value_status = False
            except Exception as e:
                print(e)
                self.ecpt(result)
                print("jetty 数据解析失败")
                self.status = False
        self.judgeresult(len_status, value_status)
    
    def ecpt(self, data):
        with open("./except/jetty.txt", "wb") as f:
            f.write(data.content())
    
    def judgeresult(self, len_status, value_status):
        if len_status and value_status:
            print("jetty 数据正常")
        elif len_status:
            print("jetty 占用率太高")
            self.status = False
        elif value_status:
            print("jetty 无新数据产生")
            self.status = False


class baserequest:

    def __init__(self, config, cookie):
        self.config = config
        self.url = "http://10.25.150.103:19095/api/tsdb/query"
        self.s = session()
        self.status = True
        self.header = {
            "accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "content-type": "application/json",
            "Cookie": cookie,
            "Host": "10.25.150.103:19095",
            "Origin": "http://10.25.150.103:19095",
            "Referer": "http://10.25.150.103:19095/d/Kz4-4g6Wk/guan-jian-zhi-biao-zhan-shi-tu?orgId=1&refresh=30m",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53",
            "x-grafana-org-id": "1"
        }
    
    def getdata(self):
        r = self.s.post(self.url, json=self.param, headers=self.header, timeout=10)
        if r.status_code == 200:
            return r
        else:
            print(f"{self.name} 接口响应不正常 code: {r.status_code}")
            self.status = False
            self.ecpt(r)
            
    def judge_len(self):
        len_status = False
        result = self.getdata()

        if result != None and self.status:
            try:
                res = result.json()["results"]
                writejson(res)
                for k in res:
                    if len(res[k]["series"][0]["points"]) > 0:
                        len_status = True
            except Exception as e:
                print(e)
                self.ecpt(result)
                print(f"{self.name} 数据解析失败")
                self.status = False
        self.judgeresult_len(len_status)
    
    def judgeresult_len(self, len_status):
        if len_status:
            print(f"{self.name} 数据正常")
        else:
            print(f"{self.name} 无新数据产生")
            self.status = False

    def judge_value(self):
        len_status = False
        value_status = True
        config = self.config[self.config_name]
        result = self.getdata()
        if result != None and self.status:
            try:
                res = result.json()["results"]
                for k in res:
                    if len(res[k]["series"][0]["points"]) > 10:
                        len_status = True
                    for i in res[k]["series"][0]["points"]:
                        if config["flag"] == "s" and i[config["index"]] < config["value"]:
                            value_status = False
                        elif config["flag"] == "l" and i[config["index"]] > config["value"]:
                            value_status = False
            except Exception as e:
                print(e)
                self.ecpt(result)
                print(f"{self.name} 数据解析失败")
                self.status = False
        self.judgeresult_value(len_status, value_status)
    
    def judgeresult_value(self, len_status, value_status):
        if len_status and value_status:
            print(f"{self.name} 数据正常")
        elif value_status:
            print(f"{self.name} 无新数据产生")
            self.status = False
        elif len_status:
            print(f"{self.name} 超出标准范围")
            self.status = False
    
    def ecpt(self, data):
        with open(f"./except/{self.name}.txt", "wb") as f:
            f.write(data.content)


class webgate(baserequest):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(window_start_time/1000,1m),\n  avg(total) AS \"APP网关\"\nFROM ng_total_count\nWHERE\n  $__unixEpochFilter(window_start_time/1000) AND\n  topic = 'nginxaccess'\nGROUP BY 1\nORDER BY $__unixEpochGroup(window_start_time/1000,1m)",
                "format":"time_series"},{
                "refId":"B",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(window_start_time/1000,1m),\n  avg(total) AS \"活动网关\"\nFROM ng_total_count\nWHERE\n  $__unixEpochFilter(window_start_time/1000) AND\n  topic = 'activity_nginxaccess'\nGROUP BY 1\nORDER BY $__unixEpochGroup(window_start_time/1000,1m)",
                "format":"time_series"},{
                "refId":"C",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(window_start_time/1000,1m),\n  avg(total) AS \"日志上报网关\"\nFROM ng_total_count\nWHERE\n  $__unixEpochFilter(window_start_time/1000) AND\n  topic = 'lori-log'\nGROUP BY 1\nORDER BY $__unixEpochGroup(window_start_time/1000,1m)",
                "format":"time_series"}]
        }
        self.name = "网关请求总量"
    
    def judge(self):
        self.judge_len()
        

class frontpage(baserequest):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(windows_start_time/1000,1m),\n  avg((invoke_time_total/invoke_sum)) AS \"音乐首页\"\nFROM interface_statistics_out\nWHERE windows_start_time >= $__unixEpochFrom() * 1000 \n  AND windows_start_time < $__unixEpochTo() * 1000 \n  AND interface_name = '/bmw/page-data/index-show/v1.0'\nGROUP BY 1\nORDER BY $__unixEpochGroup(windows_start_time/1000,1m)",
                "format":"time_series"},{
                "refId":"B",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(windows_start_time/1000,1m),\n  avg((invoke_time_total/invoke_sum)) AS \"现场首页\"\nFROM interface_statistics_out\nWHERE windows_start_time >= $__unixEpochFrom() * 1000 \n  AND windows_start_time < $__unixEpochTo() * 1000\n  AND interface_name = '/v1.0/template/indexfun-new/release'\nGROUP BY 1\nORDER BY $__unixEpochGroup(windows_start_time/1000,1m)",
                "format":"time_series"},{
                "refId":"C",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(windows_start_time/1000,1m),\n  avg((invoke_time_total/invoke_sum)) AS \"个人主页\"\nFROM interface_statistics_out\nWHERE windows_start_time >= $__unixEpochFrom() * 1000 \n  AND windows_start_time < $__unixEpochTo() * 1000  AND\n  interface_name = '/v2.0/user/getMyPage.do'\nGROUP BY 1\nORDER BY $__unixEpochGroup(windows_start_time/1000,1m)",
                "format":"time_series"}]
        }
        self.name = "首页响应"
    
    def judge(self):
        self.judge_len()


class login(baserequest):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(windows_start_time/1000,1m),\n  avg((invoke_success_num_all/invoke_sum)) AS \"登陆成功率\"\nFROM interface_statistics_out\nWHERE\n  $__unixEpochFilter(windows_start_time/1000) AND\n  interface_name = '/v1.0/user/tokenvalidate.do'\nGROUP BY 1\nORDER BY $__unixEpochGroup(windows_start_time/1000,1m)",
                "format":"time_series"}]
            }
        self.name = "登陆成功率"
        self.config_name = "login"
    
    def judge(self):
        self.judge_value()


class restime(baserequest):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(windows_start_time/1000,1m),\n  avg((invoke_time_total/invoke_sum)) AS \"响应时长\"\nFROM interface_statistics_out\nWHERE\n  $__unixEpochFilter(windows_start_time/1000) AND\n  interface_name = '/v2.0/content/listen-url'\nGROUP BY 1\nORDER BY $__unixEpochGroup(windows_start_time/1000,1m)",
                "format":"time_series"}]
            }
        self.name = "响应时长"
        self.config_name = "restime"
    
    def judge(self):
        self.judge_value()


class search(baserequest):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":60000,
                "maxDataPoints":892,
                "datasourceId":13,
                "rawSql":"SELECT\n  $__unixEpochGroupAlias(windows_start_time/1000,1m),\n  avg((invoke_time_total/invoke_sum)) AS \"搜索加载时延\"\nFROM interface_statistics_out\nWHERE\n  $__unixEpochFilter(windows_start_time/1000) AND\n  interface_name = '/v1.0/content/search_all.do'\nGROUP BY 1\nORDER BY $__unixEpochGroup(windows_start_time/1000,1m)",
                "format":"time_series"}]
        }
        self.name = "搜索加载时延"
        self.config_name = "search"
    
    def judge(self):
        self.judge_value()


class vrbtbase:

    def __init__(self, config, cookie):
        self.config = config
        self.url = "http://10.26.60.154:3000/api/tsdb/query"
        self.s = session()
        self.status = True
        self.header = {
            "accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "content-type": "application/json",
            "Cookie": cookie,
            "Origin": "http://10.26.60.154:3000",
            "Referer": "http://10.26.60.154:3000/d/DWPqF3tGk/shi-pin-cai-ling-xian-wang-zhi-biao-zhan-shi?orgId=1&refresh=30m",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53",
            "x-grafana-org-id": "1"
        }

    def getdata(self):
        r = self.s.post(self.url, json=self.param, headers=self.header, timeout=10)
        if r.status_code == 200:
            return r
        else:
            print(f"{self.name} 接口响应不正常 code: {r.status_code}")
            self.status = False
            self.ecpt(r)
            
    def judge_len(self):
        len_status = False
        result = self.getdata()

        if result != None and self.status:
            try:
                res = result.json()["results"]
                writejson(res)
                for k in res:
                    if len(res[k]["series"][0]["points"]) > 0:
                        len_status = True
            except Exception as e:
                print(e)
                self.ecpt(result)
                print(f"{self.name} 数据解析失败")
                self.status = False
        self.judgeresult_len(len_status)
    
    def judgeresult_len(self, len_status):
        if len_status:
            print(f"{self.name} 数据正常")
        else:
            print(f"{self.name} 无新数据产生")
            self.status = False
    
    def ecpt(self, data):
        with open(f"./except/{self.name}.txt", "wb") as f:
            f.write(data.content)


class vrbt1(vrbtbase):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":1800000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  SUM(total_count) AS `开销户调用量`\nFROM api_count_by_prov_opt\nWHERE\n  window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000 AND \n  (api = 'cljz:/jboss-net/services/VRBTUserManage2/VRBTSubscribeEvt' OR \n  api = 'cljz:/jboss-net/services/VRBTUserManage2/VRBTUnSubscribeEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"},{
                "refId":"B",
                "intervalMs":1800000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  (sum(success_count)/sum(total_count)) AS \"开销户成功率\"\nFROM api_count_by_prov_opt\nWHERE\n window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000 AND \n (api = 'cljz:/jboss-net/services/VRBTUserManage2/VRBTSubscribeEvt' OR \n api = 'cljz:/jboss-net/services/VRBTUserManage2/VRBTUnSubscribeEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"}]
            }
        self.name = "开销户调用量"
    
    def judge(self):
        self.judge_len()


class vrbt2(vrbtbase):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":120000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  sum(total_count) AS \"订购调用量\"\nFROM api_count_by_prov_opt\nWHERE\n  window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000  AND\n  (api = 'cljz:/jboss-net/services/VRBTUserToneManage2/VRBTPresentToneEvt' OR \n  api = 'cljz:/jboss-net/services/VRBTUserToneManage2/VRBTOrderToneEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"},{
                "refId":"B",
                "intervalMs":120000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n   (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  (sum(success_count)/sum(total_count)) AS \"订购成功率\"\nFROM api_count_by_prov_opt\nWHERE\n  window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000  AND\n  (api = 'cljz:/jboss-net/services/VRBTUserToneManage2/VRBTPresentToneEvt' OR api = 'cljz:/jboss-net/services/VRBTUserToneManage2/VRBTOrderToneEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"}]
            }
        self.name = "订购调用量"
    
    def judge(self):
        self.judge_len()


class vrbt3(vrbtbase):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":f"{int((datetime.now()-timedelta(minutes=30)).timestamp()*1000)}",
            "to":f"{int(datetime.now().timestamp()*1000)}",
            "queries":[{
                "refId":"A",
                "intervalMs":120000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  sum(total_count) AS \"设置调用量\"\nFROM api_count_by_prov_opt\nWHERE\n  window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000  AND\n  (api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTAddSettingEvt' OR\n  api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTModSettingEvt' OR\n  api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTDelSettingEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"},{
                "refId":"B",
                "intervalMs":120000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  (sum(success_count)/sum(total_count)) AS \"设置成功率\"\nFROM api_count_by_prov_opt\nWHERE\n window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000 AND\n  (api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTAddSettingEvt' OR\n  api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTModSettingEvt' OR\n  api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTDelSettingEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"}]
            }
        self.name = "设置调用量"
    
    def judge(self):
        self.judge_len()


class vrbt4(vrbtbase):

    def __init__(self, config, cookie):
        super().__init__(config, cookie)
        self.param = {
            "from":"1612186492159",
            "to":"1612272892159",
            "queries":[{
                "refId":"A",
                "intervalMs":120000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  sum(total_count) AS \"查询调用量\"\nFROM api_count_by_prov_opt\nWHERE\n  window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000 AND\n(api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTQuerySettingEvt' OR\n api = 'cljz:/jboss-net/services/VRBTUserToneManage2/VRBTQueryToneEvt' OR\n api = 'cljz:/jboss-net/services/VRBTUserManage2/QueryVRBTStatusEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"},{
                "refId":"B",
                "intervalMs":120000,
                "maxDataPoints":714,
                "datasourceId":4,
                "rawSql":"SELECT\n  (window_start_time DIV (1000 * 60 * 30)) * 30 * 60 AS `time`,\n  (sum(success_count)/sum(total_count)) AS \"查询成功率\"\nFROM api_count_by_prov_opt\nWHERE\n window_start_time >= $__unixEpochFrom() * 1000 AND window_start_time < $__unixEpochTo() * 1000 AND\n(api = 'cljz:/jboss-net/services/VRBTUserToneSetManage2/VRBTQuerySettingEvt' OR\n api = 'cljz:/jboss-net/services/VRBTUserToneManage2/VRBTQueryToneEvt' OR\n api = 'cljz:/jboss-net/services/VRBTUserManage2/QueryVRBTStatusEvt')\nGROUP BY `time`\nORDER BY `time`",
                "format":"time_series"}]
            }
        self.name = "查询调用量"
    
    def judge(self):
        self.judge_len()


def judge(key_cookie, vrbt_cookie):
    config = {
        "jetty": 80,
        "login": {"flag": "s",
                  "index": 0,
                  "value": 0.8},
        "restime": {"flag": "l",
                    "index": 0,
                    "value": 1000},
        "search": {"flag": "l",
                   "index": 0,
                   "value": 3000}
    }
    keydata = [
        jetty_data(config, key_cookie),
        webgate(config, key_cookie),
        frontpage(config, key_cookie),
        login(config, key_cookie),
        restime(config, key_cookie),
        search(config, key_cookie),
        vrbt1(config, vrbt_cookie),
        vrbt2(config, vrbt_cookie),
        vrbt3(config, vrbt_cookie),
        vrbt4(config, vrbt_cookie)
    ]
    for i in keydata:
        i.judge()
        if i.status == False:
            return False


def writejson(data):
    with open("./data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    key_cookie = "SL_GWPT_Show_Hide_tmp=1; SL_G_WPT_TO=en; SL_wptGlobTipTmp=1; grafana_session=342bd7aa24c9bd9ee5d186dd2fd4d893"
    vrbt_cookie = "SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; grafana_session=a56812284747bf1a4f0a32cf1a3d20cd"
    judge(key_cookie, vrbt_cookie)
    # print(int((datetime.now()-timedelta(minutes=30)).timestamp()))


