import boto3
import json
from flask import Flask, request, abort
from src.validation_schemas import AliasSchema, UserEventsSchema, ProfileSchema 


app = Flask(__name__)
firehose = boto3.client('firehose')
BUCKET = '***REMOVED***'

alias_schema = AliasSchema()
user_events_schema = UserEventsSchema()
profile_schema = ProfileSchema()


def put_firehose_record(validation_schema, delivery_stream_name: str):
    content = request.get_json()
    dumped_content = json.dumps(content)
    loaded_content = json.loads(dumped_content)
    errors = validation_schema.validate(loaded_content)
    if errors:
        response = abort(400, str(errors))
    else:
        # Create a new object in order to generate fields that were not specified in the post request and have default values
        # Validation on the dumped_object is not possible as it throws errors in case of unexpected fields instead of returning them as a response
        record_object = validation_schema.create_object(content)
        dumped_object = validation_schema.dumps(record_object)
        print(dumped_object)
        response = firehose.put_record(DeliveryStreamName=delivery_stream_name, Record={'Data': dumped_object})
        response = response["ResponseMetadata"]
    return response
    

@app.route('/track', methods=['POST'])
def log_user_events():
    response = put_firehose_record(validation_schema=user_events_schema, delivery_stream_name='log_user_events')
    return response


@app.route('/profile', methods=['POST'])
def create_user_profile():
    response = put_firehose_record(validation_schema=profile_schema, delivery_stream_name='user_profiles')
    return response


@app.route('/alias', methods=['POST'])
def link_users():
    response = put_firehose_record(validation_schema=alias_schema, delivery_stream_name='link_users')
    return response


