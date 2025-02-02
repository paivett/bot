import logging
import sys

from eduzen_bot.models import EventLog, Question, User

logger = logging.getLogger()


def create_db_tables():
    User.create_table()
    Question.create_table()
    EventLog.create_table()
    logger.info("Tables created!")


if __name__ == "__main__":
    sys.exit(create_db_tables())
