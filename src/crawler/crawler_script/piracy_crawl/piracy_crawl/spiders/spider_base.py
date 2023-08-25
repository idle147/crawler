from inspection.models import StateModel, UserModel
from scrapy import Spider

from ..items import InfoItem


class SpiderBase(Spider):

    def __init__(self, key_words, state_id, *args, **kwargs):
        # 读取User_model
        super().__init__(*args, **kwargs)
        self.state_model, self.user_model = self.get_state_model(state_id)
        self.keyword = key_words

    # 用来专门处理item
    def item_opt(self, title, link, content, icon, source):
        item = InfoItem()
        item["keyword"] = self.keyword
        item["source"] = source
        item["source_state"] = self.state_model
        item["owner"] = self.user_model
        item['title'] = title
        item['link'] = link
        item['content'] = content
        item['icon'] = icon
        return item

    def get_user_model(self, id):
        """ 利用ID获取Django用户模型 """
        try:
            user_model = UserModel.objects.get(id=int(id))
        except Exception as e:
            raise ValueError(f"输入的用户ID:{id}, 数据库内查无信息, 错误原因:{e}") from e
        else:
            return user_model

    def get_state_model(self, id):
        """ 利用ID获取Django的state模型 """
        try:
            state_model = StateModel.objects.get(id=int(id))
        except Exception as e:
            raise ValueError(f"输入的状态ID:{id}, 数据库内查无信息, 错误原因:{e}") from e
        else:
            return state_model, state_model.owner
