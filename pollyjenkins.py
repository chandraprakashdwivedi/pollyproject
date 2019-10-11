import argparse
import base64
import time

import boto3
from github import Github

polly = boto3.client('polly', region_name='us-east-1')
bucket = 'polly-audiobucket'
repos_url = 'https://github.com/api/v3'
git_repo = 'SSML-Files'


def get_arguments():
    _parser = argparse.ArgumentParser()
    _parser.add_argument('--filename', '-f', required=True, help='filename comma separated string')
    _parser.add_argument('--pat_token', '-t', required=True, help='pat token created in jenkins')
    return _parser.parse_args()


def init(request_arguments):
    print(request_arguments)
    git_manager = create_connection(request_arguments.get("pat_token"))
    copy_object(build_audio_files(request_arguments, git_manager))


def create_connection(pat):
    return Github(base_url=repos_url, login_or_token=pat)


def get_data_file(file, git_manager):
    source_repo = git_manager.get_repo(git_repo)
    content_file = source_repo.get_contents(file)
    data = content_file.content
    decoded_content = base64.b64decode(data).decode('UTF-8')
    return decoded_content


def text_to_speech(file_content):
    response = polly.start_speech_synthesis_task(
        OutputFormat='mp3',
        OutputS3BucketName=bucket,
        OutputS3KeyPrefix='myrecording-',
        SampleRate='22050',
        Text=file_content,
        LanguageCode='en-US',
        TextType='ssml',
        VoiceId='Matthew'
    )

    s3_url = 'https://s3.us-east-1.amazonaws.com/polly-audiobucket/'
    audio = response['SynthesisTask']['OutputUri'].replace(s3_url, "")
    return audio


def copy_object(audio_files):
    for audio_file in audio_files:
        print("check your workspace for the Downloaded files")
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.download_file(bucket, audio_file, audio_file)


def build_audio_files(request_arguments, git_manager):
    audio_files = list()
    for argument in request_arguments.get("filename").split(','):
        print(argument)
        file_content = get_data_file(argument, git_manager)
        audio_file = text_to_speech(file_content)
        audio_files.append(audio_file)
        time.sleep(15)
    return audio_files


if __name__ == '__main__':
    args = get_arguments()
    init(args.__dict__)
