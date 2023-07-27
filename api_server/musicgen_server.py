from fastapi import FastAPI, HTTPException, status
from typing import List, Union
from pydantic import BaseModel
from audiocraft.models import musicgen
from fastapi.responses import JSONResponse #, FileResponse
import torch
import time

from monitoring import print_information, print_caption, print_request_processing_time
from text_preprocessing import generate_music_caption, generate_music_caption_text_analysis
from utils import setting_device_status, empty_cache
from validation import valid_inputs_simple_category, valid_inputs_choice_category, valid_inputs_text_analysis


class SimpleInput(BaseModel):
    genres: Union[List[str], None]
    instruments: Union[List[str], None]
    moods: Union[List[str], None]
    duration: int
    tempo: str

class CategoryInput(BaseModel):
    genres: Union[List[str], None]
    instruments: Union[List[str], None]
    moods: Union[List[str], None]
    etc: Union[List[str], None]
    duration: int
    tempo: str

class TextInput(BaseModel):
    etc: Union[List[str], None]
    text: str
    duration: int
    tempo: str    
    
class MusicOutput():
    def __init__(self, music, caption, sample_rate):
        self.music: List[List[List[float]]] = music
        self.caption: List[str] = caption
        self.sample_rate: int= sample_rate
    
    def get_json(self):
        return {
            "music" : self.music,
            'caption' : self.caption,
            'sample_rate' : self.sample_rate,
        }    


app = FastAPI()

model = musicgen.MusicGen.get_pretrained('medium', device='cuda') # musicgen 모델 정의

sample_number = 4


@app.post("/simple_category")
async def simple_category(inputs: SimpleInput):
    print_information(inputs)
    start_time = time.time()
    empty_cache()
    
    if not valid_inputs_simple_category(inputs):
        raise HTTPException(status_code=422, detail="genres, instruments, moods 중 적어도 하나는 필요합니다.")
    
    text = generate_music_caption(inputs, is_simple=True)
    texts = [text] * sample_number
    
    # caption에 대한 음악 생성
    model.set_generation_params(duration=inputs.duration)
    audio_values = model.generate(texts, progress=True)

    music_output = MusicOutput(music=audio_values.cpu().numpy().tolist(), caption=texts, sample_rate=model.sample_rate)

    empty_cache()
    torch.backends.cudnn.benchmark = True
    print_caption(text)
    setting_device_status()
    end_time = time.time()
    print_request_processing_time(start_time, end_time)
    return JSONResponse(content=music_output.get_json(), status_code=status.HTTP_200_OK)

@app.post("/choice_category")
async def choice_category(inputs: CategoryInput):
    print_information(inputs)
    start_time = time.time()
    empty_cache()
    
    if not valid_inputs_choice_category(inputs):
        raise HTTPException(status_code=422, detail="genres, instruments, moods, etc 중 적어도 하나는 필요합니다.")
    
    text = generate_music_caption(inputs, is_simple=False)
    texts = [text] * sample_number
    
    # caption에 대한 음악 생성
    model.set_generation_params(duration=inputs.duration)
    audio_values = model.generate(texts, progress=True)

    music_output = MusicOutput(music=audio_values.cpu().numpy().tolist(), caption=texts, sample_rate=model.sample_rate)

    empty_cache()
    torch.backends.cudnn.benchmark = True
    print_caption(text)
    setting_device_status()
    end_time = time.time()
    print_request_processing_time(start_time, end_time)
    return JSONResponse(content=music_output.get_json(), status_code=status.HTTP_200_OK)

@app.post("/text_analysis")
def text_analysis(inputs: TextInput):
    print_information(inputs)
    start_time = time.time()
    empty_cache()
    
    if not valid_inputs_text_analysis(inputs):
        raise HTTPException(status_code=422, detail="text 입력은 필수입니다.")
    
    text = generate_music_caption_text_analysis(inputs)
    texts = [text] * sample_number
    
    # caption에 대한 음악 생성
    model.set_generation_params(duration=inputs.duration)
    audio_values = model.generate(texts, progress=True)

    music_output = MusicOutput(music=audio_values.cpu().numpy().tolist(), caption=texts, sample_rate=model.sample_rate)

    empty_cache()
    torch.backends.cudnn.benchmark = True
    print_caption(text)
    setting_device_status()
    end_time = time.time()
    print_request_processing_time(start_time, end_time)
    return JSONResponse(content=music_output.get_json(), status_code=status.HTTP_200_OK)
    
