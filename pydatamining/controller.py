from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from loguru import logger # type: ignore
from kafka import KafkaProducer # type: ignore
import json
from decouple import config # type: ignore
from pydatamining.manager import user_agent
from pydatamining.manager.session import AsyncSession, AsyncProxySession

KAFKA_TOPIC = config('KAFKA_TOPIC')
KAFKA_BROKER = config('KAFKA_BROKER')

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)

# Названия полей включают в себя `event` для парсинга из Kafka
@dataclass
class Event:
    Name: str
    URL: str
    Date: datetime
    Venue: str = None
    ImageURL: str = None
    City: str = None

    def json(self):
        return asdict(self)

class Parser:
    def __init__(self):
        self.session = None
        
    @property
    def user_agent(self):
        return user_agent.random()

    async def initialize(self):
        """Асинхронная инициализация."""
        self.session = AsyncSession()
        return self

    async def sendto_kafka(self, event: Event):
        event.Name = event.Name.replace('\n', ' ')
        if event.Venue is not None:
            event.Venue = event.Venue.replace('\n', ' ')

        event.Date = event.Date.replace(tzinfo=timezone.utc).isoformat()
        
        event_data = json.dumps(event.json(), ensure_ascii=False).encode("utf-8")
        
        producer.send(KAFKA_TOPIC, event_data)
        producer.flush()