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
    # PUT YOUR CODE HERE
    s = get_session(engine)
    ind = request.query["id"]
    label = request.query["label"]
    change_label(s, ind, label)
    redirect("/news")

@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    s = get_session(engine)
    get_new_news(s)
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    s = get_session(engine)
    model = NaiveBayesClassifier()
    train_set = s.query(News).filter(News.label != None).all()
    model.fit([clean(news.title).lower() for news in train_set], [news.label for news in train_set])
    test = s.query(News).filter(News.label == None).all()
    cell = list(map(lambda x: model.predict(x.title), test))
    return template("color_template", rows=list(map(lambda x: (x[1], colors[cell[x[0]]]), enumerate(test))))


if __name__ == "__main__":
    run(host="localhost", port=8080)

