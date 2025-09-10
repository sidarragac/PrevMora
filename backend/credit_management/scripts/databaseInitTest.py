import sys
import os

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from ..app.models import (
    base,
    Alert,
    Client,
    Credit,
    Installment,
    Manager,
    Portfolio,
    Reconciliation
)


script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../..")))

db_path = os.path.join(script_dir, 'database.db')
db_url = f"sqlite:///{db_path}"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

base.Base.metadata.drop_all(engine)
base.Base.metadata.create_all(engine)

print("\nTablas creadas en la base de datos:")
inspector = inspect(engine)
for table_name in inspector.get_table_names():
    print(f"- {table_name}")

session.close()
engine.dispose()

# cd /home/Halbacis/codigo/PrevMora/backend
# python -m credit_management.scripts.DatabaseInitDevelopment