# SwissKnife
---

##### A multipurpose swiss knife like Application

**An application to compress any kind of file and extract data from PDFs**

### Features
---

- Seamless compression of images.
- Easy compression of PDF files.
- 1 Click resizing of MP4 Files.
- And many more

---

To achieve the requirement where the uploaded file is not stored on your Flask application's server but instead processed and returned to the user, you can follow a structured approach using client-side storage and processing along with server-side handling. Here’s how you can do it:

### Frontend (Client-Side)

#### File Upload
Allow users to upload files using an HTML form with `input type="file"`.

#### File Processing (Client-Side)
Use JavaScript to read the file contents and handle the upload process. Instead of storing the file in the server's filesystem, you'll keep it in memory (or local storage) until it's sent to the server for processing.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload Example</title>
</head>
<body>
    <input type="file" id="fileInput">
    <button onclick="uploadFile()">Upload</button>
    
    <script>
        function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file.');
                return;
            }
            
            // Read file content as ArrayBuffer
            const reader = new FileReader();
            reader.onload = function(event) {
                const fileData = event.target.result;
                
                // Call server endpoint to process the file data
                fetch('/process_file', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/octet-stream',
                    },
                    body: fileData,
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.blob(); // Assuming you expect Blob back
                })
                .then(blobData => {
                    // Create a download link for the processed file
                    const url = URL.createObjectURL(blo
```
## Backend (Flask Application)
##### Receive and Process File Implement a Flask route (/process_file in this example) to receive the file data, process it (e.g., compress it), and return the processed data.

```
python
Copy code
from flask import Flask, request, send_file
import io
import gzip

app = Flask(__name__)

@app.route('/process_file', methods=['POST'])
def process_file():
    file_data = request.data  # Get the file data sent from the client
    
    # Process the file data (e.g., compress it)
    compressed_data = compress_file(file_data)
    
    # Return the processed data as a downloadable file
    return send_file(
        io.BytesIO(compressed_data),
        as_attachment=True,
        attachment_filename='processed_file.zip',  # Adjust filename and extension as needed
        mimetype='application/zip'
    )

def compress_file(file_data):
    # Example: Compress using gzip
    with io.BytesIO() as buf:
        with gzip.GzipFile(fileobj=buf, mode='w') as f:
            f.write(file_data)
        compressed_data = buf.getvalue()
    
    return compressed_data

if __name__ == '__main__':
    app.run(debug=True)
```

**Explanation**
Client-Side: The HTML and JavaScript code sets up an interface for users to select a file, read its contents using FileReader, and send it to the Flask server via a fetch request. The server endpoint /process_file expects the file data as an ArrayBuffer or Blob.

**Server-Side:** Flask receives the file data, processes it (here, compressing it using gzip), and then returns the processed data as a downloadable file (application/zip in this case).

**Considerations**
- Security: Always validate and sanitize file uploads on both client and server sides to prevent security risks like file injection attacks.
- File Size: Handle large files appropriately on the client side to avoid memory and performance issues.
