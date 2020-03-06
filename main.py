import requests
import datetime
import base64
import json
from timeit import default_timer as timer
from PIL import Image
from io import BytesIO
from pony.orm import *

from models import (
  BaseGroundTruth,
  NoBackgroundModel,
  CompositeLinearMeasurements,
  OldCompositeLinearMeasurements,
  LinearMeasurements,
  BodyKeyPoints,
  get_ground_truth,
  save_no_bg_model_new_entry,
  db
)
from s3_utils import (
  s3_upload_no_bg_img_from_file,
  s3_upload_no_bg_img_from_url,
  s3_upload_original_img_from_url,
  s3_upload_no_bg_img_from_byte_array,
  s3_upload_no_bg_resized_img_from_byte_array,
  bucket_location)

from api import (
  get_body_key_points,
  get_extra_body_key_points,
  get_body_segmentation,
  get_composite_linear_measurements,
  get_linear_measurements
)

def get_img_dimension(content):
  '''
  Return width & height from image
  '''
  im = Image.open(BytesIO(content))
  width, height = im.size
  return width, height

@db_session
def upload_gt_photos_to_s3():
  '''
  Fetch Ground Truth Caesar data from SQL db & upload to S3 Bucket
  '''
  c = 0
  result = BaseGroundTruth.select(lambda i: i.created_by == "caesar")[:]
  start = timer()
  for r in result:
    c += 1
    original_front_photo_url = r.front_photo
    original_profile_photo_url = r.profile_photo
    d = [s3_upload_original_img_from_url(url, r.dataset_id, "synthetic-data", "caesar", "front" if key == 0 else "side") for key, url in enumerate([original_front_photo_url, original_profile_photo_url])]
  end = timer()
  print(end - start)


@db_session
def save_original_resized_images_on_no_bg_model():
  c = 0
  res = NoBackgroundModel.select()[:]
  for i in res:
    c += 1
    front_url = upload_original_resized_photo_to_s3(i, "front")
    profile_url = upload_original_resized_photo_to_s3(i, "side")

    i.set(resized_original_front_photo=front_url, resized_original_profile_photo=profile_url)

    commit()
    print(c)


def remove_white_bg(url):
  '''
  Remove all white pixels from image & make them transparent
  '''
  r = requests.get(url).content
  img = Image.open(BytesIO(r))
  img = img.convert("RGBA")
  datas = img.getdata()

  newData = []
  for item in datas:
      if item[0] > 230 and item[1] > 230 and item[2] > 230:
          newData.append((0, 0, 0, 0))
      else:
          newData.append(item)

  img.putdata(newData)

  
  img_byte_arr = BytesIO()
  img.save("img_byte_arr.png", 'PNG')
  # return img_byte_arr.getvalue()


def upload_resized_photo(byte_array, dataset_id, dataset_type, created_by, body_view):
  object_url = s3_upload_no_bg_resized_img_from_byte_array(byte_array, dataset_id, dataset_type, created_by, body_view)

  return object_url


def resize_photo(url, dimension):
  r = requests.get(url)

  original_photo = Image.open(BytesIO(r.content))
  original_photo = original_photo.resize((dimension[0], dimension[1]), Image.ANTIALIAS)

  img_byte_arr = BytesIO()
  original_photo.save(img_byte_arr, 'PNG')
  return img_byte_arr.getvalue()


def resize_and_upload(url, body_view, dataset_id):
  img = Image.open(BytesIO(requests.get(url).content))
  print(img.size[1])
  if img.size[1] > 380:
    width = int(380 * img.size[0] / img.size[1])
    image = img.resize((width, 380), Image.ANTIALIAS)

  
    print(image.size)
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, 'PNG')
   
    res = upload_no_bg_photo(img_byte_arr.getvalue(), dataset_id, "synthetic-data", "caesar", body_view)
    print(res)

@db_session
def resize_no_bg():
  c = 0
  gt = BaseGroundTruth.select(lambda i: i.created_by == "caesar")[10:200]
  for g in gt:
    res = NoBackgroundModel.get(dataset_id=g.dataset_id)
    print(res.dataset_id)
    if res:
      c += 1
      resize_and_upload(res.front_photo, "front", res.dataset_id)
      resize_and_upload(res.profile_photo, "side", res.dataset_id)









