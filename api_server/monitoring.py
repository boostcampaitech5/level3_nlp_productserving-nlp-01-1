from pydantic import BaseModel
import datetime
import pytz
import time

def print_information(inputs):
    timezone = pytz.timezone('Asia/Seoul') # 한국의 시간대 설정
    now = datetime.datetime.now(timezone) # 현재 시간
    korean_time = now.strftime('%Y년 %m월 %d일 %H시 %M분 %S초') # 형식 포맷팅
    
    print('=' * 50)
    print(f'current time : {korean_time}')
    print(f'inputs : {inputs}')

def print_caption(text):
    print(f'caption : {text}')

def print_request_processing_time(start_time, end_time):
    execution_time_seconds = end_time - start_time
    minutes, seconds = int(execution_time_seconds // 60), int(execution_time_seconds % 60)
    print(f"음악생성 요청 처리시간: {minutes}분 {seconds}초")    