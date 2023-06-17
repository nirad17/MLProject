from flask import Flask, request, render_template

application = Flask(__name__)

app= application

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predictdata',methods=[ "GET","POST"])
def predict_datapoint():
    if request.method=="GET":
        return render_template("home.html")
    else:
        pass
if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)