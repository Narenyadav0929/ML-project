from flask import Flask, render_template, request
from src.logger import logger
from src.pipeline.predict_pipeline import CustomData, predict_pipeline
from src.exception import CustomException
import math

application = Flask(__name__)

app = application

@app.route('/')
def index():
    return render_template('index.html')

@app.get("/health")
def health():
    return "OK", 200

@app.route('/predictdatapoint.html',methods=['GET','POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        # data=CustomData(
        #     gender=request.form.get('gender'),
        #     race_ethnicity=request.form.get('ethnicity'),
        #     parental_level_of_education=request.form.get('parental_level_of_education'),
        #     lunch=request.form.get('lunch'),
        #     test_preparation_course=request.form.get('test_preparation_course'),
        #     reading_score=float(request.form.get('writing_score')),
        #     writing_score=float(request.form.get('reading_score'))

        # )
        # pred_df = data.get_data_as_data_frame()
        # print(pred_df)

        # predeict_pipeline_ = predict_pipeline()

        # results = predeict_pipeline_.predict(pred_df)
        # return render_template('home.html',results=results[0])
        form_values = request.form.to_dict(flat=True)

        def _parse_score(raw_value: str, label: str) -> float:
            if raw_value is None or not str(raw_value).strip():
                raise ValueError(f"Missing {label}")

            try:
                score_value = float(raw_value)
            except (TypeError, ValueError) as conversion_error:
                raise ValueError(f"Non-numeric {label}") from conversion_error

            if math.isnan(score_value) or not 0 <= score_value <= 100:
                raise ValueError(f"{label} out of range")

            return score_value

        try:
            reading_score = _parse_score(form_values.get('reading_score'), 'reading score')
            writing_score = _parse_score(form_values.get('writing_score'), 'writing score')
        except ValueError:
            logger.warning(
                "Invalid score values submitted: reading=%s, writing=%s",
                form_values.get('reading_score'),
                form_values.get('writing_score'),
            )
            return (
                render_template(
                    'home.html',
                    error_message="Please provide valid numeric scores between 0 and 100.",
                    form_values=form_values,
                ),
                400,
            )

        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=reading_score,
                writing_score=writing_score,
            )
            pred_df = data.get_data_as_data_frame()

            predict_pipeline_instance = predict_pipeline()

            results = predict_pipeline_instance.predict(pred_df)
            prediction = float(results[0])
            logger.info("Successfully generated prediction for submitted datapoint")
            return render_template(
                'home.html',
                results=prediction,
                form_values=form_values,
            )
        except CustomException as custom_error:
            logger.exception("Domain error while generating prediction")
            return (
                render_template(
                    'home.html',
                    error_message=str(custom_error),
                    form_values=form_values,
                ),
                200,
            )
        except Exception as unexpected_error:
            logger.exception("Unexpected error while generating prediction")
            return (
                render_template(
                    'home.html',
                    error_message="We ran into an unexpected issue while generating the prediction. Please try again later.",
                    form_values=form_values,
                ),
                200,
            )




if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=False,port=8000)
    # app.run(host='0.0.0.0', port=8080, debug=True)