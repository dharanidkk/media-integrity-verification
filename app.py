from flask import Flask, render_template, request
from media_verifier.nlp_detector import NLPDetector
from media_verifier.drvga import assess_credibility
from media_verifier.audit_chain import append_audit_record

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024  # 100 KB request limit
detector = None

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    text = ""

    if request.method == "POST":
        text = request.form.get("news_text", "").strip()
        try:
            global detector
            if detector is None:
                detector = NLPDetector()
            prediction = detector.predict(text)
            assessment = assess_credibility(text, prediction)

            final_label = prediction["label"]
            result = {
                "prediction": final_label,
                "fake_probability": round(prediction["fake_probability"] * 100, 2),
                "authentic_probability": round(prediction["authentic_probability"] * 100, 2),
                "credibility_score": assessment["credibility_score"],
                "explanation": assessment["explanation"],
            }
            audit = append_audit_record(text, result)
            result["input_sha256"] = audit["input_sha256"]
            result["record_hash"] = audit["record_hash"]
            result["timestamp_utc"] = audit["timestamp_utc"]
        except (ValueError, FileNotFoundError) as exc:
            error = str(exc)
        except Exception:
            app.logger.exception("Verification failed")
            error = "Verification failed. Check the terminal for details."

    return render_template("index.html", result=result, error=error, text=text)

if __name__ == "__main__":
    app.run(debug=True)
