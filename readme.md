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
