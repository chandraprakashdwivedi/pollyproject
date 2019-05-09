import json
import boto3

print("calling lambda fucntion")

bucket = 'serverless-polly.com'


def lambda_handler(event, context):
    print("event", event)
    
    requested_resource = event['resource']
    http_method = event['httpMethod']
    if http_method == 'POST':
      return post_call_method(requested_resource,event,bucket)
    else:
      return get_call_method(requested_resource,event,bucket)

def post_call_method(requested_resource,table,event):
    if '/lambda_functions/login' == requested_resource:
        return login_call(table, event)
    else:
         return create_response(body='Not Found.', status_code=500)
        
def get_call_method(requested_resource,table,event,bucket):
    if '/lambda_functions/upload' == requested_resource:
        return sign_s3(event,bucket)
    else:
        return create_response(body='Not Found', status_code=500)






def create_response(body, status_code=200):
    body_json = {'message': body, 'status_code':status_code}
    return {
          "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body_json)
        }
