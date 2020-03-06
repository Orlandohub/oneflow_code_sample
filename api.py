import requests

def get_body_key_points(data):
  r = requests.post(
    'http://dualstack.ec2co-ecsel-13ww2805c9j7z-1622921773.eu-west-1.elb.amazonaws.com:5000/measurements/keypoints',
    data=data,
    headers={"Content-Type": "application/json"}
  )
  
  return r.json()

def get_extra_body_key_points(data):
  r = requests.post(
    'http://dualstack.ec2co-ecsel-dnvuzvdjt2pb-921178460.eu-west-1.elb.amazonaws.com:5000/keypoints',
    data=data,
    headers={"Content-Type": "application/json"}
  )

  return r.json()

def get_body_segmentation(data):
  r = requests.post(
    'http://63.34.107.181/segmentation',
    data=data,
    headers={"Content-Type": "application/json"}
  )
  pprint.pprint(r.status_code)
  return r.json()


def get_composite_linear_measurements(data):
  r = requests.post(
    'http://34.250.180.12/measurements/get-composite-linear-measurements',
    data=data,
    headers={"Content-Type": "application/json"}
  )
  # pprint.pprint(r.status_code)
  return r.json()

def get_linear_measurements(data):
  r = requests.post(
    'http://63.34.107.181/measurements/get-linear-measurements',
    data=data,
    headers={"Content-Type": "application/json"}
  )
  # pprint.pprint(r.status_code)
  return r.json()