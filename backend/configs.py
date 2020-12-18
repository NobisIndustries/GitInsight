import json
import secrets
from pathlib import Path
from typing import List, Dict

from pydantic.main import BaseModel

from helpers.path_helpers import DATA_DIR


class JsonBaseConfig(BaseModel):
    @classmethod
    def load(cls):
        config_path = cls.__get_absolute_config_path()
        if not config_path.exists():
            cls().save_file()
        config = cls.parse_file(config_path, content_type='json')
        cls._after_load(config)
        return config

    def save_file(self):
        config_path = self.__get_absolute_config_path()
        config_path.parent.mkdir(exist_ok=True, parents=True)
        with config_path.open('w', encoding='utf-8') as f:
            json.dump(self.dict(), f, indent=2)

    @classmethod
    def __get_absolute_config_path(cls):
        return Path(DATA_DIR, cls._get_config_path())

    @classmethod
    def _get_config_path(cls):
        raise NotImplementedError()

    @classmethod
    def _after_load(cls, config):
        pass


class AuthorsConfig(JsonBaseConfig):
    @classmethod
    def _get_config_path(cls):
        return 'authors.json'

    authors: Dict[str, Dict[str, str]] = {}


class TeamsConfig(JsonBaseConfig):
    @classmethod
    def _get_config_path(cls):
        return 'teams.json'

    @classmethod
    def _after_load(cls, config):
        fallback_team = {
            'UNKNOWN': {
                'team_display_name': 'Unknown team',
                'team_display_color': '#cccccc',
                'team_description': 'This is a fallback team for everyone that has not been assigned to a team yet.',
                'team_contact_link': ''
            }
        }
        if 'UNKNOWN' not in config.teams:
            config.teams.update(fallback_team)

    teams: Dict[str, Dict[str, str]] = {}


class CrawlConfig(JsonBaseConfig):
    @classmethod
    def _get_config_path(cls):
        return 'crawl.json'

    pull_before_update: bool = False
    tracked_branches: List[str] = []
    update_interval_minutes: int = 60 * 24
    update_base_time: str = '04:00'
    webhook_token: str = secrets.token_urlsafe(32)
