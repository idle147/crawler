from django.conf import settings
from rest_framework import serializers

from .config import SCHEDULE_STATE, STATE
from .models import InfoModel, ScheduledModel, StateModel


class InfoSerializer(serializers.ModelSerializer):
    """ 爬虫条目序列化 """
    source = serializers.SerializerMethodField()
    keyword = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_source(self, obj):
        return obj.source_state.source

    def get_keyword(self, obj):
        return obj.source_state.keyword

    def get_icon(self, obj):
        return settings.IMAGE_URL + obj.icon

    class Meta:
        model = InfoModel
        fields = ("id", "title", "link", "content", "icon", "is_piracy", "source", "keyword")


class PiracySerializer(serializers.ModelSerializer):
    """ 盗版条目序列化 """
    source = serializers.SerializerMethodField()
    icon = serializers.SerializerMethodField()

    def get_source(self, obj):
        return obj.source_state.source

    def get_icon(self, obj):
        return settings.IMAGE_URL + obj.icon

    class Meta:
        model = InfoModel
        ordering = ['source']
        fields = ("id", "title", "icon", "link", "content", "source")


class StateSerializer(serializers.ModelSerializer):
    """ 爬虫状态条目序列化 """
    source = serializers.SerializerMethodField()

    def get_source(self, obj):
        state_info = {}
        for level in obj:
            source_info = level.source
            state_changed = level.state

            # 数据内容转换
            state_changed = STATE[
                state_changed] if state_changed is not None and 0 <= state_changed <= 2 else state_changed

            state_info[source_info] = state_changed
        return state_info

    class Meta:
        model = StateModel
        fields = ("date", "+", "source")
        # fields = ("date", "source")


class ScheduledSerializer(serializers.ModelSerializer):
    """ 定时方案序列化 """
    sources = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    def get_sources(self, obj):
        sources_str = obj.sources_list
        return sources_str.split(",")

    def get_state(self, obj):
        return SCHEDULE_STATE[obj.state]

    class Meta:
        model = ScheduledModel
        fields = ("id", "keyword", "sources", "schedule", "state")
