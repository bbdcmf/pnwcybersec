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
app = Starlette()

learn = load_learner(PARENT_PATH+'../ai/models/3-21-22-resnet50-train2-pretrained-epoch_50-bs-32-98.21%.pkl') # uses the folder of your console

db = mysql.connector.connect(
    host="localhost",
    user="yourusername",
    password="yourpassword",
    database="db"
)

cursor = db.cursor()

@app.route("/upload", methods=["POST"])
async def upload(request):
    data = await request.form()
    bytes = await (data["file"].read())
    true_class = data["class_true"]
    return predict_image_from_bytes(bytes, true_class)


@app.route("/classify-url", methods=["GET"])
async def classify_url(request):
    bytes = await get_bytes(request.query_params["url"])
    return predict_image_from_bytes(bytes)


def predict_image_from_bytes(bytes, true_class):
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

    statement = "SELECT * FROM known"
    cursor.execute(statement)
    if cursor.rowcount() > 0:
        statement = "UPDATE known SET cnt = cnt + 1 WHERE file_hash=(%s)"
        val = (file_hash)
        cursor.execute(statement, val)
    else:
        statement = "INSERT INTO known (file_hash, label) VALUES (%s, %s)"
        val = (file_hash, class_) # make sure this follows the format for the lable ENUM
        cursor.execute(statement, val)
    db.commit()

    return JSONResponse({ # maybe also return the NEW count here
        "Prediction": class_,
        "Probabilities": sorted(
            zip(['goodware','malware'], map(float, losses)),
            key=lambda p: p[1],
            reverse=True
        )
    })


@app.route("/")
def form(request):
    return HTMLResponse(open(PARENT_PATH+'views/index.py').read()) # Currently selecting if the program being uploaded is malware or goodware only work if the user is uploading from their computer, gotta figure out how to format it so when someone upload from a link they can still select if its malware or goodware
    # return HTMLResponse(
    # """
    #     <h3>Malware Detection with Machine Learning<h3>
    #     <form action="/upload" method="post" enctype="multipart/form-data">
    #         Is the program goodware or malware:
    #         <select id="class_true" name="class_true">
    #             <option value="unknown">Unknown</option>
    #             <option value="goodware">Goodware</option>
    #             <option value="malware">Malware</option>
    #         </select><br/>
    #         Select program to upload:
    #         <input type="file" name="file">
    #         <input type="submit" value="Predict">
    #     </form>
    #     Or submit a URL:
    #     <form action="/classify-url" method="get">
    #         <input type="url" name="url">
    #         <input type="submit" value="Fetch and analyze image">
    #     </form>
    # """)


@app.route("/form")
def redirect_to_homepage(request):
    return RedirectResponse("/")


if __name__ == "__main__":
    # To run this app start application on server with python
    # python FILENAME serve
    # ex: python server.py server
    if "serve" in sys.argv:
        uvicorn.run(app, host="0.0.0.0", port=8082)
