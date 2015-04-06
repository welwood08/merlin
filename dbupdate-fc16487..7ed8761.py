from Core.db import session

from sqlalchemy.sql import text
from Core.config import Config

prefix = Config.get("DB", "prefix")

session.execute(text("ALTER TABLE %splanetscan ADD COLUMN sold_res INTEGER DEFAULT 0;" % (prefix,)))

session.execute(text("ALTER TABLE alliance ALTER COLUMN score TYPE BIGINT;"))
session.execute(text("ALTER TABLE alliance ALTER COLUMN score_total TYPE BIGINT;"))
session.execute(text("ALTER TABLE alliance ALTER COLUMN value_total TYPE BIGINT;"))

session.execute(text("ALTER TABLE alliance_history ALTER COLUMN score TYPE BIGINT;"))
session.execute(text("ALTER TABLE alliance_history ALTER COLUMN score_total TYPE BIGINT;"))
session.execute(text("ALTER TABLE alliance_history ALTER COLUMN value_total TYPE BIGINT;"))

session.execute(text("ALTER TABLE alliance_temp ALTER COLUMN score TYPE BIGINT;"))
session.execute(text("ALTER TABLE alliance_temp ALTER COLUMN score_total TYPE BIGINT;"))
session.execute(text("ALTER TABLE alliance_temp ALTER COLUMN value_total TYPE BIGINT;"))

session.commit()
session.close()
