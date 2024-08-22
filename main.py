#pip install python-multipart
#pip install Image
#pip install opencv-python

from fastapi import BackgroundTasks, FastAPI, File, Query, UploadFile
from fastapi.responses import FileResponse 
from PIL import Image
import os
from random import randint
import uuid 
import cv2
 
app = FastAPI()

imageDir = "images/"
imageRsizePath = "images/resize/"
imageThumbPath = "images/thumb/"

app= FastAPI()


# RESIZE IMAGES FOR DIFFERENT DEVICES

def resize_image(filename: str): 
    image = Image.open(imageDir + filename, mode="r").convert('RGB')  
    print(f"Original size : {image.size}") # 5464x3640
    image.thumbnail((200, 200)) 
    image.save(imageThumbPath + "200_" + filename)
    print(image.getpixel((0, 0)))
    img = cv2.imread(imageDir + filename) 
    # Get original height and width
    print(f"Original Dimensions : {img.shape}") 
    # resize image by specifying custom width and height
    resized = cv2.resize(img, (1000, 800)) 
    print(f"Resized Dimensions : {resized.shape}")
    cv2.imwrite(imageRsizePath + "resize" + filename, resized)

 

@app.post("/uploadImage")
async def upload_and_resize(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    print(file.filename)
    ext = file.filename.split(".")
    file.filename = f"{uuid.uuid4()}.{ext[1]}"
    contents = await file.read()
 
    #save the file
    with open(f"{imageDir}{file.filename}", "wb") as f:
        f.write(contents)

    background_tasks.add_task(resize_image, filename=file.filename)    
 
    return {"filename": file.filename} 



@app.get("/OriginalImage/")
async def read_from_file():
    # get random file from the image directory
    files = os.listdir(imageDir)
    random_index = randint(0, len(files) - 1)
 
    path = f"{imageDir}{files[random_index]}" 
     
    return FileResponse(path)

 
@app.post("/imageReduce")
async def image_reduce():
    files1 = os.listdir(imageThumbPath)
    random_index1 = randint(0, len(files1) - 1)
 
    path1 = f"{imageThumbPath}{files1[random_index1]}" 
     
    return FileResponse(path1)

@app.post("/imageResize")
async def image_resize():
    files2 = os.listdir(imageRsizePath)
    random_index2 = randint(0, len(files2) - 1)
 
    path2 = f"{imageRsizePath}{files2[random_index2]}" 
     
    return FileResponse(path2)