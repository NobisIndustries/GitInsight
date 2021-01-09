import json
from pathlib import Path
from typing import Dict

from pydantic.main import BaseModel

from helpers.path_helpers import CONFIG_DIR
from helpers.security_helpers import get_random_token
from server.endpoints.auth_data_models import UserInternal, create_default_user


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
        return Path(CONFIG_DIR, cls._get_config_path())

    @classmethod
    def _get_config_path(cls):
        raise NotImplementedError()

    @classmethod
    def _after_load(cls, config):
        pass


class AuthorInfoConfig(JsonBaseConfig):
    @classmethod
    def _get_config_path(cls):
        return 'author_info.json'

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

    authors: Dict[str, Dict[str, str]] = {}
    teams: Dict[str, Dict[str, str]] = {}


class CrawlConfig(JsonBaseConfig):
    @classmethod
    def _get_config_path(cls):
        return 'crawl.json'

    update_before_crawl: bool = True
    limit_tracked_branches_days_last_activity: int = 90
    crawl_periodically_active: bool = False
    crawl_periodically_crontab: str = '00 4 * * *'
    webhook_active: bool = False
    webhook_token: str = get_random_token()


class ProjectDescriptionConfig(JsonBaseConfig):
    @classmethod
    def _get_config_path(cls):
        return 'project_description.json'

    repo_name: str = 'My Repo'
    start_page_text: str = ('# Welcome to GitInsight - a better git history\n\n'
                            '## What is this about?\n\n'
                            'You want to get a feeling for your repository: *Which development team maintains '
                            'which part? What part is most active? Who can I ask for help with this class I\'ve never '
                            'seen before? And are there architectural problems that I haven\'t noticed yet?*\n\n'
                            'GitInsight lets you assign teams to the contributors of a git repository. Various '
                            'analyses combine these metadata with the edit history of every tracked file to provide '
                            'you with better overview.\n\n'
                            '## What to do next?\n\n'
                            'You should first [create teams and assign contributors to '
                            'them](/config/authors_and_teams). You can also configure when and how GitInsight [updates '
                            'its database](/config/db_update) with new changes. Lastly you can also edit the repo '
                            'title and this text to better tailor this application to your visitors.')


class Authentication(JsonBaseConfig):
    # You could (and probably should) do user management with a database instead, but for the time being
    # this must do.
    @classmethod
    def _get_config_path(cls):
        return 'users.json'

    jwt_secret: str = ''
    jwt_expires_in_min: int = 30
    users: Dict[str, UserInternal] = create_default_user()
