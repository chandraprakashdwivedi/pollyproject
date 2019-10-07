import json
import boto3
import argparse
import base64
import time
import wget
import requests

from github import Github


polly = boto3.client('polly', region_name= 'us-east-1')
bucket = 'polly-audiobucket'


def get_arguments():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--filename', '-f', required=True, help='filename comma separated string')
    #_parser.add_argument('--role', '-r', required=True, help='role name')
    #_parser.add_argument('--account_number', '-a', required=True, help='account number')
    return _parser.parse_args()


def aws_assume_role(account_number, role):
    sts_client = boto3.client('sts')
    role_arn = "arn:aws:iam::" + account_number + ":role/" + role

    assumedRoleObject = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRole")

    return assumedRoleObject['Credentials']


def getDataFile(file):
    token = ''  #attach your token or app id
    g = Github(token)
    repos_url = 'https://github.com/api/v3'
    g = Github(base_url=repos_url, login_or_token=token)
    sourceRepo = g.get_repo('polly/SSML-Files')
    contentFile = sourceRepo.get_contents(file)
    data = contentFile.content
    decoded_content = base64.b64decode(data).decode('UTF-8')
    return decoded_content


def TextToSpeech(fileContent):
    # print(fileContent)
    response = polly.start_speech_synthesis_task(
        OutputFormat='mp3',
        OutputS3BucketName=bucket,
        OutputS3KeyPrefix='myrecording-',
        SampleRate='22050',
        Text=fileContent,
        LanguageCode='en-US',
        TextType='ssml',
        VoiceId='Matthew'
    )

    url = response['SynthesisTask']['OutputUri']
    print(url)
    return url


def DownloadFile(polly_url):
    wget.download(polly_url, '.')
    print("Check your Download files in workspace")


if __name__ == '__main__':
    args = get_arguments()
    # credentials = aws_assume_role(args.account_number, args.role)
    # polly = boto3.client(
    #     'polly',
    #     region_name="us-east-1",
    #     aws_access_key_id=credentials['AccessKeyId'],
    #     aws_secret_access_key=credentials['SecretAccessKey'],
    #     aws_session_token=credentials['SessionToken'], )

    request_arguments = args.__dict__
    for i in request_arguments.get("filename").split(','):
        fileContent = getDataFile(i)
        polly_url = TextToSpeech(fileContent)
        time.sleep(15)
        DownloadFile(polly_url)
