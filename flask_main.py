from flask import Flask, render_template, request, redirect
from gathering_text import get_twitter_text
from nocache import nocache

app = Flask("Twitter Analyze")

@app.route("/")
@nocache
def home():
    return render_template("mainPage.html")
    
@app.route("/results")
def results():
    keyword = request.args.get('keyword')
    if keyword:
        text_analyze = get_twitter_text(keyword)
    else:
        return redirect("/")
    return render_template("resultsPage.html", searchingBy=keyword, resultsNumber=len(text_analyze), text_analyze=text_analyze)
app.run()