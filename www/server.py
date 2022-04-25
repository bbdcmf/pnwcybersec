from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastai.vision import *
from fastai.vision.all import *
from pathlib import Path
from io import BytesIO
import sys, uvicorn, aiohttp, asyncio, hashlib, torch
import PIL.Image as Image
import mysql.connector

async def get_bytes(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


PARENT_PATH = './www/' # we might have to play with this, escepially if you start in www
# ^ joey='./www/' ryan=''
app = Starlette()

learn = load_learner(PARENT_PATH+'../ai/models/3-21-22-resnet50-train2-pretrained-epoch_50-bs-32-98.21%.pkl') # uses the folder of your console

with open(PARENT_PATH+'secret.json') as s:
    print('Starting mysql with secret.json')
    secret = json.load(s)
    db = mysql.connector.connect(
        host=secret['host'],
        user=secret['user'],
        password=secret['password'],
        database=secret['database']
    )

cursor = db.cursor(buffered=True)

@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    name = (data['file'].filename)
    true_class = data["class_true"]
    return predict_image_from_bytes(bytes, true_class, name)


@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    data = await request.form()
    true_class = request.query_params["url_class_true"]
    return predict_image_from_bytes(bytes, true_class)


def predict_image_from_bytes(bytes, true_class, name):
    """
        Predict function which will be called by either classify_url or by upload
        and return the True class as well as the scores. 
        Note: scores are not probabilites, and we may use activation like Softmax
              or sigmoid to convert these scores into probabilities.
    """
    imgByteArr = bytearray(bytes)
    ln = np.size(imgByteArr)
    width = int(ln**0.5)
    g = np.reshape(imgByteArr[:width * width], (width, width)) # Reshape bytearray so it is square
    g = np.uint8(g) # Ensure data is between 0 and 255, where 0=black and 1=white
    img = Image.fromarray(g)
    file_hash = hashlib.sha256(bytes).hexdigest()
    img.save(PARENT_PATH+"imgs/"+true_class+"/"+file_hash+'.exe.png')
    class_, predictions, losses = learn.predict(PARENT_PATH+"imgs/"+true_class+"/"+file_hash+'.exe.png')
    probs = sorted(zip(['goodware','malware'], map(float, losses)),key=lambda p: p[1],reverse=True)

    if probs[0][0] == 'malware':
        color = 'red'
    elif probs[0][0] == 'goodware':
        color = 'green'
    
    cursor.execute("SELECT * FROM known WHERE file_hash=%s", [file_hash]) # get the rows
    if cursor.rowcount > 0: # if the hash already exists
        cursor.execute("UPDATE known SET cnt = cnt + 1 WHERE file_hash=%s", [file_hash])
    else: # if the hash is new
        cursor.execute("INSERT INTO known (file_hash, label_pred, label_true) VALUES (%s, %s, %s)", [file_hash, class_, true_class])# make sure this follows the format for the lable ENUM
    db.commit()
    
    cursor.execute("SELECT file_hash, cnt FROM known ORDER BY (cnt) DESC LIMIT 5")
    results = cursor.fetchall()
    table = """<table style="margin: auto"><tr><th>File</th><th>Count</th></tr>"""
    for result in results:
        table = table + """<tr><td>""" + str(result[0]) + """</td><td>""" + str(result[1]) + """</td></tr>"""
    table = table + """</table>"""

    cursor.execute("SELECT cnt FROM known WHERE file_hash=%s", [file_hash])
    cnt_of_hash = str(cursor.fetchall()[0][0])

    return HTMLResponse(
    """
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Malware Detection with Machine Learning</title>
    </head>
    <script>
        function dropHandler(ev) {
        console.log('File(s) dropped');
            // Prevent default behavior (Prevent file from being opened)
            ev.preventDefault();

            if (ev.dataTransfer.items) {
                // Use DataTransferItemList interface to access the file(s)
                for (var i = 0; i < ev.dataTransfer.items.length; i++) {
                    // If dropped items aren't files, reject them
                    if (ev.dataTransfer.items[i].kind === 'file') {
                        var file = ev.dataTransfer.items[i].getAsFile();
                        console.log('... file[' + i + '].name = ' + file.name);
                        let fileInput = document.querySelector('input');
                        fileInput.files = ev.dataTransfer.files;
                    }
                }
            } else {
                // Use DataTransfer interface to access the file(s)
                for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                    console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
                }
            }
        }

        function dragOverHandler(ev) {
            console.log('File(s) in drop zone');

            // Prevent default behavior (Prevent file from being opened)
            ev.preventDefault();
        }
        
        function change_url_class() {
            document.getElementById("url_class_true").value = document.getElementById("class_true").value;
        }
    </script>
    <style>
    	
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 10px;
        }
        
        #drop_zone {
            border: 5px solid red;
            width:  200px;
            height: 100px;
            text-align: center;
        }

        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-gap: 20px;
        }
        .content {
            margin: 2em;
        }
        
    </style>
    <header style="text-align: center;">
        <h1>Malware Detection with Machine Learning!!!!1</h1>
    </header>
    <body>
        <div class="container">
            <div class="content">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    Is the program goodware or malware:
                    <select id="class_true" name="class_true">
                        <option value="unknown">Unknown</option>
                        <option value="goodware">Goodware</option>
                        <option value="malware">Malware</option>
                    </select><br/>
                    Select a program to upload:
                    <input type="file" name="file">
                    <div id="drop_zone" name="file-drop" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);">
                        <p>Or drag it here</p>
                    </div><br>
                    <input type="submit" value="Predict" style="padding: 5px;">
                </form><br><br>
                Or submit a URL:
                <form action="/classify-url" method="get">
                    <input type="url" name="url">
                    <input type="submit" value="Fetch and analyze image">
                    <input type="hidden" value="" id="url_class_true" name="url_class_true">
                </form>
            </div>
            <div class="content">
                <h2>Results for """ + name + """</h2>
                <h3>Prediction:</h3><p style='color:""" + color + """;'>"""+ probs[0][0] + """
                </p><h3>This file has been searched """ + cnt_of_hash + """ times</h3>
                <h3>Probabilities:</h3>
                <table><tr><th>""" + probs[0][0] + """</th><td>""" + str(round(probs[0][1]*100, 2)) + """%
                </td></tr><tr><th>""" + probs[1][0] + """</th><td>""" + str(round(probs[1][1]*100, 2)) + """%
                </td></tr></table>
            </div>
        </div>
        """ + table + """
        		
    </body>
    <footer style="position: absolute; bottom: 0; width: 100%; height: 2.5rem;">
        <p>Created by: <a href="http://www.github.com/bbdcmf" target="_blank">Ryan Frederick</a> & <a href="http://www.github.com/JoeyShapiro" target="_blank">Joseph Shaprio</a> and with the advising of Ricardo Calix Ph.D.</p>
    </footer>
    
    """)


@app.route("/")
def form(request):
    return HTMLResponse(open(PARENT_PATH+'views/index.py').read()) # Currently selecting if the program being uploaded is malware or goodware only work if the user is uploading from their computer, gotta figure out how to format it so when someone upload from a link they can still select if its malware or goodware


@app.route("/form")
def redirect_to_homepage(request):
    return RedirectResponse("/")


if __name__ == "__main__":
    # To run this app start application on server with python
    # python FILENAME serve
    # ex: python server.py server
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8082)
