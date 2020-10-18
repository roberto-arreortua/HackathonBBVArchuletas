import boto3
import logging
from botocore.exceptions import ClientError
import time, urllib.request, json



BUCKET = "archuletas-bucket"
#FILE_NAME = "test"
FILE_NAME = "voice691"
FILE_PATH = "voice.wav"
FILE_FORMAT = "wav"
#FILE_FORMAT = "mp3"
LANGUAGE_CODE = "es-ES"

transcribe_job_name = FILE_NAME + "_job"
base_file_uri= "https://"+BUCKET+".s3.us-east-2.amazonaws.com/"
complete_file_name = FILE_NAME + "." + FILE_FORMAT


s3 = None
transcribe = None
comprehend = None


transcribe_json = None

def openConnection():
    global s3, transcribe, comprehend
    s3 = boto3.client('s3')
    transcribe = boto3.client('transcribe')
    comprehend = boto3.client('comprehend')
    print("Conected...")


def listBuckets():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')

def uploadFile():
    try:
        s3.upload_file(FILE_PATH, BUCKET, complete_file_name)
        print("File \""+ complete_file_name +"\" loaded")
    except ClientError as e:
        logging.error(e)
        return False
    return True

def transcribeSound():
    #Search job
    jobs = transcribe.list_transcription_jobs(
        JobNameContains=FILE_NAME,
        MaxResults=100
    )

    try: #If exist job
        jobName = jobs['TranscriptionJobSummaries'][0]['TranscriptionJobName']  # First job
        print("Job already exist!")
        getTranscriptionJob(jobs)
    except IndexError: #Not exist job
        print("Creating job!")
        return createJob()
    print("Finish transcription")

def getTranscriptionJob(jobs):

    jobName = jobs['TranscriptionJobSummaries'][0]['TranscriptionJobName']  # First job

    job_information = transcribe.get_transcription_job(
        TranscriptionJobName=jobName,
    )

    transcribe_job_url = job_information['TranscriptionJob']['Transcript']['TranscriptFileUri']

    with urllib.request.urlopen(transcribe_job_url) as url:
        global transcribe_json
        transcribe_json = json.loads(url.read().decode())

def createJob():
    job_name = transcribe_job_name
    job_uri = base_file_uri + complete_file_name
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat=FILE_FORMAT,
        LanguageCode=LANGUAGE_CODE,
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2
        }
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("\rNot ready yet...", end="")
        time.sleep(5)
    transcribe_job_url = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print("\n")
    with urllib.request.urlopen(transcribe_job_url) as url:
        global transcribe_jsontranscribe_json
        transcribe_json = json.loads(url.read().decode())
        return(transcribe_json)

def start(file_,file_name):
    print(file_,file_name)
    global FILE_NAME
    global FILE_PATH
    global transcribe_job_name
    global base_file_uri
    global complete_file_name
    FILE_NAME = file_name
    FILE_PATH = file_
    transcribe_job_name = FILE_NAME + "_job"
    base_file_uri= "https://"+BUCKET+".s3.us-east-2.amazonaws.com/"
    complete_file_name = FILE_NAME + "." + FILE_FORMAT


    global transcribe_jsontranscribe_json
    openConnection()
    uploadFile()
    data = transcribeSound()
    return data 

#start('../media/Voices/voize.wav')

#django/BBVAHackathon$