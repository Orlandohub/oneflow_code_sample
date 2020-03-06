import boto3
import requests
from io import BytesIO, StringIO
from PIL import Image

s3 = boto3.resource('s3')
bucket_location = boto3.client('s3').get_bucket_location(Bucket="the-fit-data-lake")

def s3_upload_no_bg_img_from_file(filepath, dataset_id, dataset_type, created_by, body_view):
  im = Image.open(filepath)
  img_byte_arr = BytesIO()
  im.save(img_byte_arr, 'PNG')
  
  return s3.meta.client.put_object(Body=img_byte_arr.getvalue(), Bucket="the-fit-data-lake", Key=f'{dataset_type}/{created_by}/no-bg-{body_view}-photo/{dataset_id}.png')


def s3_upload_no_bg_img_from_url(url, dataset_id, dataset_type, created_by, body_view):
  r = requests.get(url)
  
  return s3.meta.client.put_object(Body=r.content, Bucket="the-fit-data-lake", Key=f'{dataset_type}/{created_by}/no-bg-{body_view}-photo/{dataset_id}.png')


def s3_upload_no_bg_resized_img_from_byte_array(byte_array, dataset_id, dataset_type, created_by, body_view):  
  s3.meta.client.put_object(Body=byte_array, Bucket="the-fit-data-lake", Key=f'{dataset_type}/{created_by}/no-bg-resized-keypoints-{body_view}-photo/{dataset_id}.png')
  object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
    bucket_location['LocationConstraint'],
    "the-fit-data-lake",
    f'{dataset_type}/{created_by}/no-bg-resized-keypoints-{body_view}-photo/{dataset_id}.png')

  return object_url


def s3_upload_no_bg_img_from_byte_array(byte_array, dataset_id, dataset_type, created_by, body_view):  
  return s3.meta.client.put_object(Body=byte_array, Bucket="the-fit-data-lake", Key=f'{dataset_type}/{created_by}/no-bg-{body_view}-photo/{dataset_id}.png')


def s3_upload_original_img_from_url(url, dataset_id, dataset_type, created_by, body_view):
  r = requests.get(url)
  
  return s3.meta.client.put_object(Body=r.content, Bucket="the-fit-data-lake", Key=f'{dataset_type}/{created_by}/{body_view}-photo/{dataset_id}.png')