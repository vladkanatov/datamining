from datetime import datetime
import importlib
import inspect

from loguru import logger
from .manager import user_agent
from datamining.manager.session import AsyncSession, AsyncProxySession

class Controller:

    def __init__(self):
        super().__init__()

        self.script = 'parser'
        self.user_agent = user_agent.random()

    def __str__(self) -> str:
        """Этот класс используется для запуска
        скриптов для парсинга информации с различных
        web-ресурсов"""

    async def load_script(self):
        try:
            parser_module = importlib.import_module(self.script)
            for name in dir(parser_module):
                obj = getattr(parser_module, name)
                if (
                        inspect.isclass(obj)
                        and issubclass(obj, Parser)
                        and obj != Parser
                ):
                    return obj()
        except Exception as e:
            logger.error(f"failed to load parser: {e}")

    async def run(self):
        script = await self.load_script()
        if script:
            try:
                await script.main()  # Запускаем async def main в parser.py
            except AttributeError as e:
                logger.error(f'parser down with error: {e}')
                return

            logger.info(f'the script {script.name} has successfully completed its work')
            if script.session is not None:
                await script.session.close()


class Parser(Controller):
    def __init__(self):
        super().__init__()

        self.session: AsyncSession = AsyncSession()
        # self.session: AsyncProxySession = AsyncProxySession()
        self.name = ''

    async def register_event(
            self,
            event_name: str,
            link: str,
            date: datetime,
            venue: str = None):

        event_name = event_name.replace('\n', ' ')
        if venue is not None:
            venue = venue.replace('\n', ' ')

        parser = self.name

        log_time_format = '%Y-%m-%d %H:%M:%S'
        normal_date = datetime.strftime(date, log_time_format)

        new_event = {
            "name": event_name,
            "link": link,
            "parser": parser,
            "date": normal_date,
            "venue_id": venue
        }

        r = await self.session.post('http://188.120.244.63:8000/put_event/', json=new_event)
        if r.status_code != 200:
            logger.error(f"the request to the allocator ended with the code: {r.status_code}")
