import streamlit as st
import requests
import  io
from PIL import Image
import cv2
import phonenumbers
from pathlib import Path
import phonenumbers
from phonenumbers import geocoder
import math
import PIL.ExifTags
from geopy.geocoders import Nominatim
import pandas
from Helper.helperFunc import get_model_predict

url=" http://192.168.29.213:8501"



def main():

  st.set_page_config(page_title="Plastic Detector")
  st.title(" 🌊Detect Plastics and Improve Marine Life 🐠🦈 ") 

  img=st.file_uploader("Upload the image in jpg or jpeg for Detection",type=['jpg','jpeg'])
  number=st.text_input("Enter Your Phone Number With Country Code")
  # video=st.file_uploader("Upload the video in mp4 format",type=['mp4'])



  if img is not None:
    # st.image(Image.open(img),caption="Uploaded",use_column_width=True)
    if st.button("perform prediction"):
      detect_plastic( Image.open(img),number)
    else:
     st.image(Image.open(img),caption="Uploaded",use_column_width=True)

from PIL import Image, ExifTags

def geo(img):
    """
    Extracts GPS coordinates from an image's EXIF metadata.

    Args:
        img (Image): The input PIL Image object.

    Returns:
        tuple: Latitude and Longitude as floats if available, else (None, None).
    """
    try:
        exif = img._getexif()
        if not exif:
            return None, None

        gps_info = exif.get(PIL.ExifTags.TAGS.get('GPSInfo'))
        if not gps_info:
            return None, None

        # Extract latitude and longitude
        n = gps_info.get(2)  # Latitude
        e = gps_info.get(4)  # Longitude
        if not n or not e:
            return None, None

        # Convert GPS coordinates to decimal format
        ltd = float((n[0] * 60 + n[1]) * 60 + n[2]) / 3600
        lng = float((e[0] * 60 + e[1]) * 60 + e[2]) / 3600
        return ltd, lng
    except Exception as e:
        # Log any unexpected errors for debugging
        print(f"Error in geo function: {e}")
        return None, None



def live(number):
    divided=phonenumbers.parse(number)  
    if(phonenumbers.is_valid_number(divided)):
      location=geocoder.description_for_number(divided,"en")
      geolocator=Nominatim(user_agent="geoapiExercises")
      locate=geocoder.description_for_number(divided,'en')
      location=geolocator.geocode(locate)
      lat=location.latitude
      lng=location.longitude
      return 1,lat,lng
    else:
       return 0,0,0
       
 

def dist(ltd1,lng1,ltd2,lng2):
    R = 6371;
    p1 = ltd1 * math.pi/180;
    p2 = ltd2 * math.pi/180;
    dp = (ltd2-ltd1) * math.pi/180;
    dl = (lng2-lng1) * math.pi/180;

    a = math.sin(dp/2) * math.sin(dp/2) +math.cos(p1) * math.cos(p2) *math.sin(dl/2) * math.sin(dl/2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));

    d = R * c;
    return d

import io
import requests
from PIL import Image
import streamlit as st

from PIL import Image, ImageDraw
import requests
import io
import streamlit as st

def draw_bounding_boxes(image, boxes):
    """
    Draw bounding boxes on the image.
    :param image: PIL image object
    :param boxes: List of tuples [(x1, y1, x2, y2), ...] representing bounding box coordinates
    :return: Image with bounding boxes drawn
    """
    draw = ImageDraw.Draw(image)

    for box in boxes:
        x1, y1, x2, y2 = box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)  # Red bounding box with 3-pixel width

    return image

def detect_plastic(image: Image, numb):
    # API endpoint
    api_img = "http://localhost:6942/predict_save_image"

    # Convert image to bytes
    image_byte = io.BytesIO()
    image.save(image_byte, format="JPEG")
    image_byte = image_byte.getvalue()

    # Process the image with the prediction API
    response = requests.post(api_img, files={"file": image_byte})

    if response.status_code == 200:
        try:
            # If the response is an image (binary data), we open it directly
            processed_image = Image.open(io.BytesIO(response.content))

            # Show the image with plastic detected
            st.image(processed_image, caption="Plastic Detected", use_column_width=True)
        
        except Exception as e:
            # Handle any errors in opening the image
            st.error(f"Error processing the image: {e}")

    else:
        st.error(f"Error detecting objects. API responded with status code: {response.status_code}")
        
if __name__=="__main__":
  main()
