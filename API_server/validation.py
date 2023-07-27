from typing import List, Union
from pydantic import BaseModel

def valid_inputs_simple_category(inputs):
    if len(inputs.genres + inputs.instruments + inputs.moods) == 0:
        # 요청받은 request의 데이터에 genres, instruments, moods, etc 모두 누락된 경우 422 Unprocessable Entity 상태 코드와 함께 예외 발생
        print("[simple_category] 필수 정보가 누락되어 요청이 들어옴.")
        return False
    return True

def valid_inputs_choice_category(inputs):
    if len(inputs.genres + inputs.instruments + inputs.moods) + len(inputs.etc) == 0:
        # 요청받은 request의 데이터에 genres, instruments, moods 모두 누락된 경우 422 Unprocessable Entity 상태 코드와 함께 예외 발생
        print("[choice_category] 필수 정보가 누락되어 요청이 들어옴.")
        return False
    return True

def valid_inputs_text_analysis(inputs):
    if len(inputs.text) == 0:
        # 요청받은 request의 데이터에 text가 누락된 경우 422 Unprocessable Entity 상태 코드와 함께 예외 발생
        print("[text_analysis] 필수 정보가 누락되어 요청이 들어옴.")
        return False
    return True