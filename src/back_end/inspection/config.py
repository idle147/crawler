from bidict import bidict

SOURCE_CROSSWALKS = bidict({
    "360渠道": "_360",
    "4399渠道": "_4399",
    "5577渠道": "_5577",
    "962渠道": "_962",
    "安智渠道": "anzhi"
})

STATE = ["已取消", "爬取数据中", "已完成"]

SCHEDULE_STATE = ["出错", "已启动", "未启动"]
