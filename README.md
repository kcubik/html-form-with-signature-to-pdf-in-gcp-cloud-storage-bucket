# HTML Form With Signature To PDF In GCP Cloud Storage Bucket

A simple Google App Engine application to provide a HTML form with a signature pad. The form content can saved to a PDF file and stored in a GCP Cloud Storage Bucket. The application uses the following components:

* [Bootstrap CSS](https://getbootstrap.com/) v4.5.2
* [Flask](https://github.com/pallets/flask) v1.1.2
* [Google App Engine (Standard Environment)](https://cloud.google.com/appengine/)
* [PyFPDF](https://github.com/reingart/pyfpdf) v1.7.2
* [SignaturePad](https://github.com/szimek/signature_pad) v2.3.2

## Modifications to app.yaml
Change `BUCKET_NAME` to name of your Cloud Storage Bucket.
```shell
env_variables:
  CLOUD_STORAGE_BUCKET: "BUCKET_NAME"
```

## Bootstrap CSS
Include the `Bootstrap CSS` file in your HTML head container.
```shell
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
```

## Flask
Use `pip` to install the `Flask` Python package so that you can test the application locally.
```shell
pip install Flask
```

Include the `Flask` module in your [Requirements.txt](#Requirementstxt) file.

## Google App Engine (Standard Environment)
See Google's [Using Cloud Storage](https://cloud.google.com/appengine/docs/standard/python3/using-cloud-storage) documentation for using the [default bucket](https://cloud.google.com/appengine/docs/standard/python3/using-cloud-storage#default_bucket) for your App Engine application.

You will need to specify the Cloud Storage Bucket name in the `app.yaml` file.

You must include the `google-cloud-storage` module in your [Requirements.txt](#Requirements.txt) file.

## PyFPDF
Use `pip` to install the pyfpdf package so that you can test the application locally.
```shell
pip install fpdf
```

You must include the `fpdf` module in your [Requirements.txt](#Requirements.txt) file.

## SignaturePad
Include the `signature_pad` javascript file in your HTML head container.
```shell
<script src="https://cdn.jsdelivr.net/npm/signature_pad@2.3.2/dist/signature_pad.min.js">
```

## Adding UTF-8 Support to PDF Files
See the [PyFPDF Unicode documentation](https://pyfpdf.readthedocs.io/en/latest/Unicode/index.html) for details on adding UTF-8 support to PDF files.

Example:
1. Download a font file, e.g. the [DejaVu](https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip/download) package from SourceForge
2. Unpack the files and save your preferred `.ttf` file to the `fonts` directory in the source code tree
3. Specify the `.ttf` file in `main.py`
```shell
pdf.add_font("DejaVu", "", "fonts/DejaVuSansCondensed.ttf", uni=True)
```

When you run the application locally to test it the font file will be serialised by the Python Pickle module. This will result in the following files being created automatically.

* DejaVuSansCondensed.pkl
* DejaVuSansCondensed.cw127.pkl

These automatically generated Pickling files must be included when you deploy the application to GAE.

## Testing
Use the [Local Development Server](https://cloud.google.com/appengine/docs/standard/python/tools/using-local-server) to run the application locally.

```script
dev_appserver.py \
--env_var GOOGLE_APPLICATION_CREDENTIALS="/Users/kevin/Development/gcp-credentials/credentials.json" \
--application=GAE-APP-ID
```

This depends on having a GCP service account with read/write permissions for the Cloud Storage Bucket. See Google's [Getting started with authentication](https://cloud.google.com/docs/authentication/getting-started) documentation for setting up a Service Account.

## Requirements.txt
Specify the Python modules that must be loaded by Google App Engine.
```script
# requirements.txt
Flask==1.1.2
fpdf==1.7.2
google-cloud-storage
```

## Deploying
Deploy the application use the standard `gcloud` command.

```script
gcloud app deploy --project=PROJECT_ID
```

## Examples

* [Screenshot of the HTML Form](https://github.com/kcubik/html-form-with-signature-to-pdf-in-gcp-cloud-storage-bucket/tree/master/examples/Example-HTML-Form.png)
* [An example PDF File](https://github.com/kcubik/html-form-with-signature-to-pdf-in-gcp-cloud-storage-bucket/tree/master/examples/Example-PDF-File.pdf)
