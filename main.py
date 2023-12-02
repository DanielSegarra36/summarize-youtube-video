import os
from openai import OpenAI
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ''
        for transcript in transcript_list:
            transcript_text += transcript['text'] + ' '
        return transcript_text
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def save_to_file(text, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Transcript saved to '{filename}'")
    except Exception as e:
        print(f"Error saving file: {str(e)}")

def summarize_text(text):
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            # api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
            messages=[
              {"role": "system", "content": "You summarize YouTube videos solely on the video's transcript. Explain and highlight core concepts and key points in great detail."},
              {"role": "user", "content": text}
            ],
            # max_tokens=150  # Adjust the length of the summary as needed
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Replace 'VIDEO_ID' with the ID of the YouTube video you want to extract the transcript from
video_id = 'YsRaVK54GfM'
transcript = get_transcript(video_id)

if transcript:
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    save_to_file(transcript, f"transcript-{formatted_time}-{video_id}.txt")  # Save transcript to a file

    summarized_text = summarize_text(transcript)
    if summarized_text:
        print("Summarized Text:")
        print(summarized_text)
        current_datetime = datetime.now()
        formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        save_to_file(transcript, f"transcript-{formatted_time}-{video_id}.txt")  # Save transcript to a file