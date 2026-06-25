from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://postgres:Kovilvenni@localhost:5432/bluestock_mf"
)
print(engine.url)