from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

import cv2
import imutils

import pyttsx3

# import smtplib
# import imghdr
# from email.message import EmailMessage

import telegram
import asyncio

# Image server link

imgLink = 'http://192.168.1.4:4747/video'

# Want to receive email?
isSendEmail = True

# SmartHome email account
# EMAIL_ADDRESS = "thucphungbd@gmail.com"
# EMAIL_PASSWORD = "0973209729"

#bot telegram
bot = telegram.Bot(token='5981765791:AAFt5RjPEgxXj5pk1Dh9xmrbnoM9HBtMDwc')
chat_id = '6075039245'

# msg = EmailMessage()
# msg['Subject'] = 'Abnormal behavior detected!'
# msg['From'] = EMAIL_ADDRESS
# msg['To'] = 'thucphung0101@gmail.com'  # user email

# msg.set_content('Suspicious person detected!')

cap = cv2.VideoCapture(0)

def capture_image_email():
    print("Capture image 1...")
    set,frame = cap.read()
    cv2.imwrite('C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_email1.png', frame)
    print("captured 1 ")

    print("Capture image 2...")
    # frame = imutils.url_to_image(imgLink)
    set,frame=cap.read()
    cv2.imwrite('C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_email2.png', frame)
    print("captured 2 ")

async def send_telegram():
    capture_image_email()
    # Replace file_path with the path of your image
    file_path = 'C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_email1.png'

    try:
        with open(file_path, 'rb') as f:
            await bot.send_photo(chat_id=chat_id, photo=f)
            print("Image sent successfully!")
    except Exception as e:
        print("Error sending image:", e)

    # Replace file_path with the path of your image
    file_path = 'C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_email2.png'

    try:
        with open(file_path, 'rb') as f:
            await bot.send_photo(chat_id=chat_id, photo=f)
            print("Image sent successfully!")
    except Exception as e:
        print("Error sending image:", e)


# def send_email():
#     capture_image_email()
#     files = ['C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_email1.png', 'C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_email2.png']
#     # files = ['img_email1.png', 'img_email2.png', 'img_email3.png']

#     for file in files:
#         with open(file, 'rb') as f:
#             file_data = f.read()
#             file_type = imghdr.what(f.name)
#             file_name = f.name

#         msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

#     try:
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#             print("Logged in...")
#             smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#             print("Sending email...")
#             smtp.send_message(msg)
#             print("Email has been sent!")

#             return True
#     except smtplib.SMTPAuthenticationError:
#         print("unable to sign in")
#         return False


# Setting for audio
audio = pyttsx3.init()
audio.setProperty('rate', 150)
audio.setProperty('volume', 0.6)




# Capture image from server
def capture_image():

    set,frame = cap.read()
    # Thay đổi kích thước ảnh
    frame = imutils.resize(frame,)

    # Hiển thị ảnh trên màn hình
    cv2.imshow("Camera", frame)
    # Ghi ảnh vào file capture.jpg khi bấm phím cách
    cv2.imwrite("C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_detect.png", frame)


    


isSended = False
tryCount = 0


# Face mask detection
def check_face_mask(index):
    isMask = False
    global isSended
    global isSendEmail
    global tryCount

    if index == 1 or index == 3:  # If without face mask
        isMask = False
        isSendEmail = True
    elif index == 0:  # If with face mask
        isMask = True
        isSended = False
        isSendEmail = False
        audio.setProperty('volume', 0.6)

    if not isMask:
        # If need to send email and it is not sent
        if isSendEmail and not isSended:
            tryCount = tryCount + 1

            if tryCount <= 2:  # If tried times <= 2 -> continue
                isSended = asyncio.run( send_telegram())
            else:  # "Sleep"
                isSendEmail = False

            if tryCount >= 6:  # Retry to send email
                tryCount = 0
                isSendEmail = True

        # Say "Wear your face mask"
        audio.say("Wear your face mask")
        if audio.getProperty('volume') <= 0.9:
            audio.setProperty('volume', audio.getProperty('volume') + 0.1)
        elif audio.getProperty('volume') < 1.0:
            audio.setProperty('volume', 1.0)


# Face detection
def face_detection():
    # Disable scientific notation for clarity
    global isMask
    np.set_printoptions(suppress=True)
    # Load the model
    model = load_model('E:\\TN5\\keras_model.h5',compile=False)
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # Replace this with the path to your image
    image = Image.open('C:\\Users\\Windows 10\\Downloads\\smartHome\\IoT_SmartHome_Camera_PythonGateway\\img_detect.png')
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    print(prediction)

    # Custom output
    name = ["With Mask", "Without mask", "Back ground", "Wrong mask"]
    index = -1
    max_value = -1
    for i in range(0, len(prediction[0])):
        if max_value < prediction[0][i]:
            max_value = prediction[0][i]
            index = i
    print("Ket Qua : ", name[index])
    print("Chinh Xac: ", max_value)

    isSendEmail = False
    isSended = False
    tryCount = 0
    check_face_mask(index)


while True:
    capture_image()
    face_detection()

    # For audio
    audio.runAndWait()

