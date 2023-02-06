# from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, \
#     PrimaryKeyConstraint, Numeric, SmallInteger
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm.session import sessionmaker, Session
# import time
# import asyncio
# import sqlalchemy
# import aioredis
# import json
#
# engine = create_engine("postgresql+psycopg2://username:secret@0.0.0.0:5432/database", echo=True,
#                        json_serializer=json.dumps)
#
# Base = declarative_base()
# session = sessionmaker(bind=engine)
# s_ = Session(bind=engine)
#
#
# class User(Base):
#     __tablename__ = "user"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#
#     def __repr__(self):
#         return "<User(name='{}',>".format(self.name)
#
#
# user_one = User(name="Shamil")
#
#
# class CustomJSONEncoder(json.JSONEncoder):
#     """
#     Override Flask's `JSONEncoder.default`, which is called
#     when the encoder doesn't handle a type.
#     """
#
#     def default(self, o):
#         if isinstance(o, User):
#             return o.id, o.name
#         else:
#             # raises TypeError: o not JSON serializable
#             return json.JSONEncoder.default(self, o)
#
#
# def init_db():
#     Base.metadata.create_all(engine)
#     for i in range(5):
#         user_one = User(name="Shamil" + str(i))
#         with session.begin() as s:
#             s.add(user_one)
#             s.commit()
#
# async def request():
#     redis = aioredis.from_url("redis://localhost:6379")
#     result = None
#     for i in range(5):
#         value = await redis.get("my-friends" + str(i))
#         if value is not None:
#             result = json.loads(value)
#             print("RESTUL of redis: ", result)
#
#         result = s_.query(User).all()
#         await redis.set("my-friends" + str(i), json.dumps(result, cls=CustomJSONEncoder))
#     print("RESULT of psql: ", result)
#
# async def main():
#     init_db()
#     redis = aioredis.from_url("redis://localhost:6379")
#     await request()
#     await request()
#
# if __name__ == "__main__":
#     asyncio.run(main())

# import sqlite3
# import asyncio
# import aioredis

# def get_my_friends():
#     connection = sqlite3.connect(database="database.db")
#     cursor = connection.cursor()
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER  PRIMARY KEY, name TEXT);''')
#     connection.commit()
#     # cursor.execute('''INSERT INTO users (id , name ) VALUES (1, 'Shamil');''')
#     # connection.commit()
#     cursor.execute('''SELECT * FROM users;''')
#     result = cursor.fetchall()
#     cursor.close()
#     return result
#
#
# if __name__ == "__main__":
#     print(get_my_friends())

import asyncio

import aioredis


async def main():
    redis = aioredis.from_url("redis://localhost")
    await redis.set("my-key", "value")
    value = await redis.get("my-key")
    print(value)


if __name__ == "__main__":
    asyncio.run(main())
