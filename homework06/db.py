from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

s = session()
news_list = get_news("https://news.ycombinator.com/newest", 0)

for dictionaries in news_list:
    
    news = News(title=dictionaries['title'],
                author=dictionaries['author'],
                url=dictionaries['url'],
                points=dictionaries['points'])
    s.add(news)
s.commit()

