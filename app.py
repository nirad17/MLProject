from flask import Flask, request, render_template

from src.pipline.predict_pipeline import CustomData, PredictPipeline
from src.pipline.train_pipeline import TrainPipeline

application = Flask(__name__)

app= application

@app.route('/')
def index():
    train = TrainPipeline()
    score = train.initiate_training()
    return render_template("index.html", score= score)

@app.route('/predictdata',methods=[ "GET","POST"])
def predict_datapoint():
    if request.method=="GET":
        return render_template("home.html")
    else:
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race-ethnicity'),
            parental_level_of_education=request.form.get('parental-education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test-preparation'),
            reading_score=float(request.form.get('reading-score')),
            writing_score=float(request.form.get('writing-score'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])
if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)