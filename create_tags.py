import sqlite3
import qrcode
import os

def make_qr(product_id, base_url="http://127.0.0.1:5000"):
    qr_dir = os.path.join("static", "qrcodes")
    os.makedirs(qr_dir, exist_ok=True)

    qr_url = f"{base_url}/reports/{product_id}"
    qr_path = os.path.join(qr_dir, f"product_{product_id}.png")

    img = qrcode.make(qr_url)
    img.save(qr_path)

    return qr_path



def calculate(materials, db_path="greenscan.db"):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        total_weight = 0.0
        score_ws = 0.0
        years_ws = 0.0

        for raw_name, raw_weight in materials.items():
            name = (raw_name or "").strip()
            try:
                weight = float(raw_weight)
            except (TypeError, ValueError):
                weight = 0.0

            if weight <= 0:
                continue

            cursor.execute(
                """
                SELECT biodegradability_percent, decomposition_years
                FROM materials
                WHERE name = ? COLLATE NOCASE
                """,
                (name,)
            )
            row = cursor.fetchone()
            if row is None:
                print(f"[WARN] Material not found in DB: '{name}'")
                continue

            biodeg = float(row[0])
            years = float(row[1] if row[1] is not None else 0)

            score_ws += biodeg * weight
            years_ws += years * weight
            total_weight += weight

        if total_weight == 0:
            return 0, 0, "Unknown"

        degradability_score = score_ws / total_weight
        degradability_years = years_ws / total_weight

        if degradability_score <= 50:
            degradability_status = "Low"
        elif degradability_score <= 70:
            degradability_status = "Moderate"
        else:
            degradability_status = "High"

        return round(degradability_score, 2), round(degradability_years, 2), degradability_status
