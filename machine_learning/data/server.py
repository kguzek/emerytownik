from datetime import datetime

from flask import Flask, jsonify, request
from generate_synthetic import wylicz_emeryture

app = Flask(__name__)


all_records = []


@app.route("/records", methods=["GET"])
def get_records():
    return jsonify(all_records), 200


@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)
        required_fields = [
            "yearOfBirth",
            "gender",
            "salary",
            "employedSinceYear",
            "expectedEmployedUntilYear",
            "nationalRetirementAge",
            "allowAbsences",
        ]

        # Validate required fields
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Validate gender
        if data["gender"] not in ["male", "female"]:
            return jsonify({"error": "Gender must be 'male' or 'female'"}), 400

        current_year = datetime.now().year
        age = current_year - data["yearOfBirth"]

        result = wylicz_emeryture(
            plec=data["gender"][0],
            wynagrodzenie_brutto=data["salary"],
            rok_rozpoczecia=data["employedSinceYear"],
            rok_zakonczenia=data["expectedEmployedUntilYear"],
            # wiek_emerytalny=data["nationalRetirementAge"],
            kapital_poczatkowy=data["savings"] if "savings" in data else 0,
            wiek=age,
            # suma_wplaconych_skladek=data["totalContributions"]
            absence=data["allowAbsences"],
        )

        if data["ignore"] != "true":
            record = data.copy()
            record.update(result)
            record["generated_at"] = datetime.now().isoformat()
            all_records.append(record)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
