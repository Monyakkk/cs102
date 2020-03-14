from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    news_label = request.query.label
    news_id = request.query.id
    s = session()
    changing_news = s.query(News).get(news_id)
    changing_news.label = news_label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():

    pages_parsed = 10
    s = session()
    old_news_list = s.query(News).all()
    new_rows = 0

    probable_news = get_news("https://news.ycombinator.com/newest", pages_parsed)
    for news in probable_news:
        #is_new = True
        for old_news in old_news_list:
            if (news['title'] == old_news.title and news['author'] == old_news.author):
                #is_new = False
                break
        #if is_new == True:
        else:
            new_news = News(title=news['title'],
                        author=news['author'],
                        url=news['url'],
                        points=news['points'])
            s.add(new_news)
            new_rows +=1
            if new_rows == 50:
                s.commit()
                print("Commited ", new_rows,  " news")
                redirect("/news")
                return     
        


@route("/classify")
def classify_news():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    training_rows = s.query(News).filter(News.label != None).all()
    X, y = [], []
    for news in training_rows:
        X.append(news.title)
        y.append(news.label)
    model = NaiveBayesClassifier()
    model.fit(X, y)  
    unclassified_news = []
    for news in rows:
        unclassified_news.append(news.title)
    predicted_labels = model.predict(unclassified_news)
    for news, label in zip(rows, predicted_labels):
        news.label = label
    classified_news = sorted(rows, key=lambda news: news.label)
    return template('predicted.tpl', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)

