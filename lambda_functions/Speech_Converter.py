import json
import boto3

print("calling lambda fucntion")


polly = boto3.client('polly')
bucket = 'serverless-polly.com'


def lambda_handler(event,context):
    print("event", event)
    
    requested_resource = event['resource']
    http_method = event['httpMethod']
    if http_method == 'POST':
      return post_call_method(requested_resource,event,bucket)
    else:
      return get_call_method(requested_resource,event,bucket)

def post_call_method(requested_resource,event,bucket):
    if '/lambda_functions/TextToSpeech' == requested_resource:
        return TextToSpeech(event,bucket)
    else:
         return create_response(body='URL Not Found.', status_code=500)
        
def get_call_method(requested_resource,event,bucket):
        return create_response(body='URL Not Found', status_code=500)


def TextToSpeech(event,bucket):
    if 'body' in event and event['body'] is not None:
        body = event['body']

    print(body)

    response = polly.start_speech_synthesis_task(
        OutputFormat= 'mp3',
        OutputS3BucketName= bucket,
        OutputS3KeyPrefix='myrecording-',
        SampleRate= '22050',
        Text= body,
        TextType= 'text',
        VoiceId='Aditi',
        LanguageCode='en-US'
    )
    
    gen_url= response['SynthesisTask']['OutputUri']

    print(response)    

    return create_response(gen_url)
        

def create_response(body, status_code=200):
    body_json = {'message': body, 'status_code':status_code}
    return {
          "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body_json)
        }
