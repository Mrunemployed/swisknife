from flask import Flask, render_template,url_for,redirect,request,jsonify, send_file,session
from pdftools import tools
import os

app = Flask(__name__)
app.secret_key = "pdf data table extracter"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pdf/renderfiles")
def renderfilesloc():
    return jsonify(session['doc_images'])

@app.route("/jpeg-compressor")
def second_page():
    return render_template("jpeg-compressor.html")

@app.route("/pdf/render_image")
def render():
    filepath = request.args.get('filepath','')
    if filepath and 'doc_images' in session.keys():
        print("filepath::::::::::::",filepath)
        return send_file(filepath,mimetype='image/png')
    elif not filepath and 'doc_images' in session.keys():
        return send_file(session['doc_images'][0],mimetype='image/png')
    else:
        return "<h1>Not Found<h1>"
    # print("rendering....",filepath)
    # return send_file(filepath,as_attachment=False)

@app.route("/upload",methods=['POST','GET'])
def upload_handler():
    if request.method == 'POST':
        file = request.files['fileup']
        session['filename'] = file.filename
        session['filetype'] = file.mimetype
        print(session['filename'])
        
        if session['filename'] != '':

            if file.mimetype != 'application/pdf':
                error = 'Please select PDF Files to proceed'
                return render_template("upload.html",error=error)
            
            else:
                data = file.stream.read()
                path = os.path.dirname(os.path.abspath(__file__))
                path = os.path.join(path,session['filename'])
                with open(path, "wb") as upload:
                    upload.write(data)
                path = os.path.abspath(os.path.dirname(__file__))
                uploads_path = os.path.join(path,"uploads",session['filename'])
                message = "File uploaded successfully!!!"
                session['filepath'] = uploads_path
                return redirect(url_for('pdf'))
        else:
            return render_template("upload.html",error='Select a file to upload')
            
    else:
        return render_template("upload.html")

@app.route("/pdf")
def pdf():
    if 'filepath' in session.keys():
        pdft = tools(pdfpath=session['filepath'])
        pages = pdft.pdf_to_mages()
        if isinstance(pages,list):
            session['doc_images'] = pages
            return render_template("extract_from_pdf.html")
        else:
            pass
    else:
        return redirect(url_for("upload_handler"))

@app.route("/pdf/read")
def read_pdf_text():
    page = request.args.get('page','')
    extype = request.args.get('type','')
    pdf_pages = tools(session['filepath'])
    page = pdf_pages.extract_text(int(page),extype=extype)
    # return jsonify(page)
    return page

@app.route("/draw")
def draw():
    return render_template("draw.html")

# if __name__=='__main__':
app.run(debug=True)