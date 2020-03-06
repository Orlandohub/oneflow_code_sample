import csv
import datetime
from pony.orm import *
from psycopg2.extras import execute_values

db = Database()

class BodyKeyPoints(db.Entity):
  _table_ = "body_key_points_json_model"
  dataset_id = Optional(str)
  body_key_points = Optional(Json)

class LinearMeasurements(db.Entity):
  _table_ = "linear_measurements_model"
  dataset_id = Optional(str)
  arm_length = Optional(str)
  inseam_length = Optional(str)
  shoulder_to_chest_length = Optional(str)
  shoulder_width = Optional(str)
  torso_length = Optional(str)
  createdAt = Optional(datetime.datetime, column="createdAt", default=datetime.datetime.utcnow)
  updatedAt = Optional(datetime.datetime, column="updatedAt", default=datetime.datetime.utcnow)


class OldCompositeLinearMeasurements(db.Entity):
  _table_ = "old_composite_linear_measurements_model"
  dataset_id = Optional(str)
  bicep = Optional(str)
  chest = Optional(str)
  hip = Optional(str)
  neck = Optional(str)
  neck_segmentation = Optional(str)
  seat = Optional(str)
  thigh = Optional(str)
  waist = Optional(str)
  wrist = Optional(str)

class CompositeLinearMeasurements(db.Entity):
  _table_ = "composite_linear_measurements_model"
  dataset_id = Optional(str)
  bicep = Optional(FloatArray)
  chest = Optional(FloatArray)
  hip = Optional(FloatArray)
  neck = Optional(FloatArray)
  neck_segmentation = Optional(FloatArray)
  seat = Optional(FloatArray)
  thigh = Optional(FloatArray)
  waist = Optional(FloatArray)
  wrist = Optional(FloatArray)

class BaseGroundTruth(db.Entity):
  _table_ = "base_ground_truth"
  dataset_id = Optional(str)
  dataset_type = Optional(str)
  has_missing_fields = Optional(bool)
  missing_fields = Optional(FloatArray)
  created_by = Optional(str)
  front_photo = Optional(str)
  profile_photo = Optional(str)
  height = Optional(str)
  gender = Optional(str)
  cup_size = Optional(str)
  low_neck_circumference = Optional(str)
  high_neck_circumference = Optional(str)
  chest_circumference = Optional(str)
  under_chest_circumference = Optional(str)
  waist_circumference = Optional(str)
  hip_circumference = Optional(str)
  seat_circumference = Optional(str)
  thigh_circumference = Optional(str)
  bicep_circumference = Optional(str)
  wrist_circumference = Optional(str)
  arm_length = Optional(str)
  torso_length = Optional(str)
  inseam_length = Optional(str)
  shoulder_to_chest_length = Optional(str)
  shoulder_width = Optional(str)
  back_width = Optional(str)


class NoBackgroundModel(db.Entity):
  _table_ = "no_background_model"
  dataset_id = Required(str, unique=True)
  front_photo = Required(str)
  profile_photo = Required(str)
  resized_original_front_photo = Optional(str)
  resized_original_profile_photo = Optional(str)
  resized_no_bg_front_photo = Optional(str)
  resized_no_bg_profile_photo = Optional(str)
  method = Optional(str)

# set_sql_debug(True)
db.bind(provider='postgres', user='root', password='Vn4jmhXYZjJQChHexPh8Kv4kyxhLcWF6', host='34.255.100.120', database='thefit')
db.generate_mapping(create_tables=True)

@db_session
def get_ground_truth(dataset_id=None):
  if dataset_id:
    result = BaseGroundTruth.select(lambda i: i.dataset_id == dataset_id)[:]
  else:
    result = BaseGroundTruth.select()

  return result


@db_session
def save_no_bg_model_new_entry(
  dataset_id,
  front_photo,
  profile_photo,
  resized_original_front_photo,
  resized_original_profile_photo,
  resized_no_bg_front_photo,
  resized_no_bg_profile_photo,
  method):
  try:
    no_bg_ins = NoBackgroundModel.get(dataset_id=dataset_id)
    if no_bg_ins:
      no_bg_ins.set(
        dataset_id=dataset_id,
        front_photo=front_photo,
        profile_photo=profile_photo,
        resized_original_front_photo=resized_original_front_photo,
        resized_original_profile_photo=resized_original_profile_photo,
        resized_no_bg_front_photo=resized_no_bg_front_photo,
        resized_no_bg_profile_photo=resized_no_bg_profile_photo,
        method=method
      )
      commit()
    else:
      new_entry = NoBackgroundModel(
        dataset_id=dataset_id,
        front_photo=front_photo,
        profile_photo=profile_photo,
        resized_original_front_photo=resized_original_front_photo,
        resized_original_profile_photo=resized_original_profile_photo,
        resized_no_bg_front_photo=resized_no_bg_front_photo,
        resized_no_bg_profile_photo=resized_no_bg_profile_photo,
        method=method

      )
      commit()
  except Exception as e:
    raise e
