from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import scraputils

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

NEWS = scraputils.get_news("https://news.ycombinator.com/newest", 1)
for i in range(len(NEWS)):
    s = session()
    title = NEWS[i]['title']
    url = NEWS[i]['url']
    points = NEWS[i]['points']
    author = NEWS[i]['author']
    comments = NEWS[i]['comments']
    news = News(title=title, author=author, url=url, comments=comments, points=points)
    s.add(news)
    s.commit()

