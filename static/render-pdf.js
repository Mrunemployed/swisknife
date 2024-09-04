const frame = document.getElementById('pdframe');
let currpage=0;
const extrDestTextBox = document.getElementById('data');
const previous = document.getElementById('previouspage');
const next = document.getElementById('nextpage');
previous.addEventListener('click',previouspage);
next.addEventListener('click',nextpage);

const extractTransition = document.getElementById('collapseOne');
const startExtraction = document.getElementById('startExt');

startExtraction.addEventListener('click',startExtracting);
// const iframe = document.getElementById('pdframe')

// function adjustIframeheight(){
//     iframe.style.height = iframe.contentWindow.document.body.scrollHeight+'px';
// }

function nextpage(){
    currpage++;
    load(currpage)
}

function load(page){
    // fetch("{{url_for('renderfilesloc')}}")
    fetch("/pdf/renderfiles")
    .then(response =>{
        if(!response.ok){
            throw new Error('Network response was not OK');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if(data.length > 0){
            if (data[page] !== undefined){
                frame.src="pdf/render_image"+`?filepath=${data[page]}`;
                console.log("page being requested for: ",page);
            }

        }
        else{
            page = data.length-1;
            currpage=page;
            frame.src="pdf/render_image"+`?filepath=${data[page]}`;
            console.log("page being requested for: ",page);
            // console.log(page);
        }
    })
    .catch(error => {
        console.error(error);
        throw error;
    });
}

function previouspage(){
    currpage--;
    if (currpage<0){
        currpage = 0;
    }
    load(currpage)
}

function startExtracting(){
    console.log(currpage,"getting page data");
    getExtractedtText(currpage)
}

function getExtractedtText(page){
    // fetch("{{url_for('read_pdf_text')}}"+`?page=${page}`)
    fetch(`/pdf/read?page=${page}&type=text`)
    .then(response => {
        if (!response.ok){
            throw new Error("Failed to receive response from server while extracting text");
        }
        return response.json();
    })
    .then(data =>{
        data = JSON.stringify(data,null,2)
        data = data.replace(/\\n/g,'<br>')
        extrDestTextBox.innerHTML = `${data}`;
    })
    .catch(error =>{
        console.log(error);
        throw error;
    })
}
