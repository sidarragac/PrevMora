import sys
import os

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from credit_management.app.models.base import Base
from credit_management.app.models.Alert import Alert
from credit_management.app.models.Alert_Type import Alert_Type
from credit_management.app.models.Client import Client
from credit_management.app.models.Client_State import Client_State
from credit_management.app.models.Contact_Method import Contact_Method
from credit_management.app.models.Contact_Result import Contact_Result
from credit_management.app.models.Credit import Credit
from credit_management.app.models.Credit_State import Credit_State
from credit_management.app.models.Installment import Installment
from credit_management.app.models.Installment_State import Installment_State
from credit_management.app.models.Manager import Manager
from credit_management.app.models.Manager_Zone import Manager_Zone
from credit_management.app.models.Payment_Channel import Payment_Channel
from credit_management.app.models.Portfolio import Portfolio
from credit_management.app.models.Reconciliation import Reconciliation


script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.abspath(os.path.join(script_dir, "../..")))

db_path = os.path.join(script_dir, 'database.db')
db_url = f"sqlite:///{db_path}"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print("\nTablas creadas en la base de datos:")
inspector = inspect(engine)
for table_name in inspector.get_table_names():
    print(f"- {table_name}")

session.close()
engine.dispose()

# cd /home/Halbacis/codigo/PrevMora/backend
# python -m credit_management.scripts.DatabaseInitDevelopment