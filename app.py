from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/offer_letter')
def offer_letter():
    return render_template('offer_letter.html')

@app.route('/relieving_letter')
def relieving_letter():
    return render_template('relieving_letter.html')

@app.route('/generate_offer_letter', methods=['POST'])
def generate_offer_letter():
    employee_name = request.form['employee_name']
    employee_id = request.form['employee_id']
    department = request.form['department']
    designation = request.form['designation']
    join_date = request.form['join_date']
    salary = request.form['salary']

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    font_path_regular = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
    font_path_bold = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path_regular))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))

    header = Paragraph(f'<strong>Offer Letter</strong>', styles['Title'])
    elements.append(header)
    elements.append(Spacer(1, 12))

    content = f"""
    <p>Dear {employee_name},</p>
    <p>We are pleased to offer you the position of {designation} in the {department} department.</p>
    <p>Your employee ID will be {employee_id}.</p>
    <p>Your start date will be {join_date} and your annual salary will be ₹{salary}.</p>
    <p>We look forward to having you join our team.</p>
    <p>Best regards,</p>
    <p>HR Department</p>
    """
    content_paragraph = Paragraph(content, styles['Normal'])
    elements.append(content_paragraph)
    
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='offer_letter.pdf')

@app.route('/generate_relieving_letter', methods=['POST'])
def generate_relieving_letter():
    employee_name = request.form['employee_name']
    employee_id = request.form['employee_id']
    department = request.form['department']
    designation = request.form['designation']
    join_date = request.form['join_date']
    relieve_date = request.form['relieve_date']

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    font_path_regular = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
    font_path_bold = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans-Bold.ttf')
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path_regular))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', font_path_bold))

    header = Paragraph(f'<strong>Relieving Letter</strong>', styles['Title'])
    elements.append(header)
    elements.append(Spacer(1, 12))

    content = f"""
    <p>Dear {employee_name},</p>
    <p>This is to acknowledge that you have been relieved from your duties as {designation} in the {department} department.</p>
    <p>Your employee ID was {employee_id}.</p>
    <p>Your tenure with us was from {join_date} to {relieve_date}.</p>
    <p>We appreciate your contributions and wish you all the best for your future endeavors.</p>
    <p>Best regards,</p>
    <p>HR Department</p>
    """
    content_paragraph = Paragraph(content, styles['Normal'])
    elements.append(content_paragraph)
    
    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='relieving_letter.pdf')

if __name__ == '__main__':
    app.run(debug=True)
