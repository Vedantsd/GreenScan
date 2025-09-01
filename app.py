from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

import db_helper
import create_tags

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display():
    if request.method == 'POST':
        materials = request.form.getlist('materials')
        return render_template('index.html', materials=materials)
    return render_template('index.html', materials=None)


# ---------------------------------------------------------------------------------------------------------------

@app.route('/print-tags', methods=['POST'])
def calculate():
    selected_materials = request.form.getlist('selected_materials')
    prod_name = request.form.get('prod_name')

    quantities = {}
    for m in selected_materials:
        quantities[m] = request.form.get(f'quantity_{m}')
    print("Final Materials with Quantities:", quantities)

    degradability_score, degradability_years, degradability_status = create_tags.calculate(quantities)
    product_id = db_helper.add_product(prod_name, degradability_status, degradability_score, degradability_years)
    
    create_tags.make_qr(product_id)

    product = db_helper.get_report_data(product_id)
    return render_template("print-tags.html", product=product)


# ---------------------------------------------------------------------------------------------------------------

@app.route('/reports/<int:product_id>', methods=['GET'])
def show_report(product_id):
    row = db_helper.get_report_data(product_id)
    if not row:
        return f"No product found with id {product_id}", 404
    return render_template("reports.html", product=row)


# ---------------------------------------------------------------------------------------------------------------

@app.route("/download-tags/<int:product_id>")
def download_tags(product_id):
    product = db_helper.get_report_data(product_id)
    if not product:
        return f"No product found with id {product_id}", 404

    filepath = os.path.join("static", f"product_{product_id}_tags.pdf")

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    qr_size = 40 * mm
    margin = 10 * mm
    cols, rows = 4, 10
    x_start = margin
    y_start = height - margin - qr_size

    for i in range(40): 
        col = i % cols
        row = (i // cols) % rows

        x = x_start + col * (qr_size + margin)
        y = y_start - row * (qr_size + margin)

        c.drawString(x, y + qr_size + 10, product['name'])

        qr_path = os.path.join("static", f"qrcodes/product_{product_id}.png")
        if os.path.exists(qr_path):
            c.drawImage(qr_path, x, y, qr_size, qr_size, preserveAspectRatio=True)
        else:
            c.rect(x, y, qr_size, qr_size)  

        c.setFont("Helvetica", 6)
        c.drawString(x, y - 5, f"Status: {product['decomposability_status']}")
        c.drawString(x, y - 15, f"Score: {product['decomposability_percent']}%")
        c.drawString(x, y - 25, f"Years: {product['decomposition_years']}")

        if (i + 1) % (cols * rows) == 0 and i != 0:
            c.showPage()

    c.save()

    return send_file(filepath, as_attachment=True)



# ---------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
