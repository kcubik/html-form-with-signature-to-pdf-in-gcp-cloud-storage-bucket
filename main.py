import base64, io, os, random, string
from google.cloud import storage, exceptions
from flask import Flask, render_template, request, make_response, redirect, url_for, send_from_directory, send_file
import fpdf

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the Cloud Storage Bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ.get("CLOUD_STORAGE_BUCKET"))
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

def blob_exists(path):
    """Checks that a blob exists in the Cloud Storage bucket."""
    # path = "storage-object-name"
    #
    # Returns: Boolean
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ.get("CLOUD_STORAGE_BUCKET"))
    blob = bucket.blob(path)
    return blob.exists()

def download_blob(path):
    """Returns a blob from the Cloud Storage bucket as Byte String."""
    # path = "storage-object-name"
    #
    # Return: Byte String
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.environ.get("CLOUD_STORAGE_BUCKET"))
    blob = bucket.blob(path)
    try:
        result = blob.download_as_string()
    except exceptions.NotFound:
        return False
    return result

@app.route("/")
def index():
    """Render the agreement page using the HTML template."""
    return render_template("agreement.html")

@app.route("/save-agreement", methods=["POST"])
def save_agreement():
    """Capture the form data and save to a PDF in a Cloud Storage bucket."""
    if request.method == "POST":

        # Create the PDF file
        pdf = fpdf.FPDF(format="A4")
        pdf.set_auto_page_break(0)
        pdf.add_page()

        # Use the DejaVu font so that we can support UTF-8 characters
        pdf.add_font("DejaVu", "", "fonts/DejaVuSansCondensed.ttf", uni=True)
        pdf.set_font("DejaVu", "", 13)

        # PDF File: Heading
        pdf.set_xy(0, 5)
        pdf.cell(txt="Heading for the PDF file",
                ln=1, h=5.0, align="C", w=0, border=0)
        pdf.ln()

        # PDF File: First Section Heading
        pdf.set_font("DejaVu", "", 12.0)
        pdf.cell(txt="First Section Heading for the PDF file", ln=1, h=5.0,
                align="C", w=0, border=0)
        pdf.ln()

        # PDF file: Opening Paragraph
        pdf.set_font("DejaVu", "", 8.0)
        pdf.multi_cell(txt="Opening paragraph for for the PDF file.",
                h=5.0, align="L", w=0, border=0)
        pdf.ln()

        # PDF file: Content from the HTML Form Fields
        pdf.cell(txt="Name: " + str(request.form.get("name")), ln=1, h=5.0,
                align="L", w=0, border=0)
        pdf.ln()
        pdf.cell(txt="Position: " + str(request.form.get("position")), ln=1,
                h=5.0, align="L", w=0, border=0)
        pdf.ln()
        pdf.cell(txt="Company: " + str(request.form.get("company")), ln=1,
                h=5.0, align="L", w=0, border=0)
        pdf.ln()
        pdf.cell(txt="Mobile: " + str(request.form.get("mobile")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Landline: " + str(request.form.get("landline")), ln=1,
                h=5.0, align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Email: " + str(request.form.get("email")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Website: " + str(request.form.get("website")), ln=1,
                h=5.0, align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Address: " + str(request.form.get("address1")), ln=1,
                h=5.0, align="L", w=0,  border=0)
        pdf.cell(txt="Address: " + str(request.form.get("address2")), ln=1,
                h=5.0, align="L", w=0,  border=0)
        pdf.cell(txt="Town: " + str(request.form.get("town")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.cell(txt="County: " + str(request.form.get("county")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.cell(txt="Postcode: " + str(request.form.get("postcode")), ln=1,
                h=5.0, align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Item: " + str(request.form.get("item")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.ln()
        pdf.multi_cell(txt="Item Detail: "
                + str(request.form.get("itemdetail")), h=5.0, align="L", w=0,
                border=0)
        pdf.ln()
        pdf.cell(txt="Value: " + str(request.form.get("value")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Expiry: " + str(request.form.get("expiry")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.ln()

        # PDF File: Second Section Heading
        pdf.cell(txt="Second Section Heading:", ln=1, h=5.0, align="L", w=0, border=0)

        # PDF File: Second Section Content
        terms = ("1. First item in the general terms and conditions.",
                "2. Second item in the general terms and conditions.",
                "3. Third item in the general terms and conditions.")
        pdf.multi_cell(txt=terms[0], h=5.0, align="L", w=0, border=0)
        pdf.multi_cell(txt=terms[1], h=5.0, align="L", w=0, border=0)
        pdf.multi_cell(txt=terms[2], h=5.0, align="L", w=0,  border=0)
        pdf.ln()
        pdf.cell(txt="Date: " + str(request.form.get("date")), ln=1, h=5.0,
                align="L", w=0,  border=0)
        pdf.ln()

        # PDF File: Second Section Content - Signature
        # Save the HTML canvas image to a temporary PNG file
        # (This utilises the /tmp directory that's available on App Engine)
        rfn = "".join(random.choice(string.ascii_letters) for _ in range(10))
        signature = open("/tmp/"+rfn+".png", "wb")
        k, v = str(request.form.get("image_data")).split(",")
        signature.write(base64.b64decode(v))
        signature.close()
        pdf.cell(txt="Signed:", ln=1, h=5.0, align="L", w=0, border=0)
        pdf.image("/tmp/"+rfn+".png", w=80)

        # PDF File: Logos in Footer
        y = pdf.get_y()
        pdf.image("static/Logo1.jpg", w=30)
        pdf.image("static/Logo2.jpg", w=30, x=210-50, y=y)
        filename = "-".join(("agreement", rfn,
                "NoName" if request.form.get("name") == "" else str(request.form.get("name")),
                "NoCompany" if request.form.get("company") == "" else str(request.form.get("company"))))

        # PDF File: Save the PDF and Upload to Cloud Storage
        # Save the HTML form data to a temporary PDF file
        # (This utilises the /tmp directory that's available on App Engine)
        filename = filename+".pdf"
        file_path = "/tmp/"+filename
        pdf.output(file_path, "F")

        # PDF File: Upload the PDF to Cloud Storage Bucket
        upload_blob(file_path, filename)

        # Return result
        if blob_exists(filename):
            return "<p>Download the PDF file: <a href='/pdf/"+filename+"'>"+filename+"</a></p>"
        return "<p>Could not generate PDF - <a href='javascript:history.back()'>Go Back</a></p>"

@app.route("/pdf/<path:path>")
def send_pdf(path):
    """Downlands a PDF file in the Cloud Storage bucket and sends it."""
    # path = "storage-object-name"
    #
    # Return: Binary Stream
    result = download_blob(path)
    if result:
        return send_file(io.BytesIO(result), as_attachment=True,
                mimetype="application/pdf", attachment_filename=path)
    return "<p>File not found. Please notify the the website administrator. <a href='javascript:history.back()'>Go Back</a></p>"

@app.route("/favicon.ico")
def favicon():
    """Render the favicon."""
    return send_from_directory(os.path.join(app.root_path, "static"),
            "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.errorhandler(404)
def not_found(e):
    """Render the File Not Found page."""
    return render_template("404.html")

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
