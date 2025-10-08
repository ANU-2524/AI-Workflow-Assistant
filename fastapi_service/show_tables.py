from sqlalchemy import create_engine, inspect
from config import DATABASE_URL  # Change to your actual config path if needed

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
print(inspector.get_table_names())
