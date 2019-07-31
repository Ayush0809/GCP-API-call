filepath = "/home/anurag/wishfin-python/audio/"     #Input audio file path
output_filepath = "/home/anurag/wishfin-python/transcripts/" #Final transcript path
bucketname = "anurag-wish" #Name of the bucket created in the step before



# Import libraries
from pydub import AudioSegment
import io
import os
#from google.cloud import speech
# from google.cloud.speech import enums
# from google.cloud.speech import types

#from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1.gapic import speech_client 
from google.cloud.speech_v1p1beta1.proto import cloud_speech_pb2 as speech
# from google.cloud.speech_v1p1beta1 import types
# from google.cloud.speech_v1p1beta1 import enums
 


import wave
from google.cloud import storage
import pandas as pd
import csv

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    if audio_file_name.split('.')[1] == 'wav':
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)


def google_transcribe(audio_file_name):

    file_name = filepath + audio_file_name

    

    bucket_name = bucketname
    source_file_name = filepath + audio_file_name
    destination_blob_name = audio_file_name

    upload_blob(bucket_name, source_file_name, destination_blob_name)

    gcs_uri = 'gs://' + bucketname + '/' + audio_file_name
    transcript = ''

    client = speech_client.SpeechClient()
    first_lang='hi-IN'
    second_lang='en'
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,

    sample_rate_hertz=8000,
    language_code=first_lang,

    audio_channel_count=1,
    enable_separate_recognition_per_channel=False,

    max_alternatives=6,

    )


    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=10000)

    confidence=0

    


    num=0

    for result in response.results:
        con=0
        tran=''
        for alternative in result.alternatives:
            if( alternative.confidence>con):
                con=alternative.confidence
                tran=alternative.transcript


        transcript += tran
        confidence=con

    
    return transcript,confidence 


def write_transcripts(transcript_filename,transcript):
    f= open(output_filepath + transcript_filename,"w+")
    f.write(transcript)
    f.close()

if __name__ == "__main__":
    data=[]
    for audio_file_name in os.listdir(filepath):

        if audio_file_name.split('.')[1] == 'wav':
            transcript , confidence = google_transcribe(audio_file_name)

            data.append([audio_file_name,transcript,confidence])
    with open("output.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerows(data)        
    f.close()
