from typing import List, Union
from pydantic import BaseModel

def generate_music_caption(inputs, is_simple) -> str:
    sentence_parts = []

    if inputs.genres:
        if inputs.moods:
            sentence_parts.append(', '.join(inputs.moods))

        if inputs.genres:
            sentence_parts.append(', '.join(inputs.genres))

        if inputs.instruments:
            instruments_part = ', '.join(inputs.instruments)
            if len(inputs.instruments) > 1:
                if len(inputs.instruments) == 2:
                    sentence_parts.append(f"with {inputs.instruments[0]} and {inputs.instruments[-1]}")
                else:
                    sentence_parts.append(f"with {', '.join(inputs.instruments[:-1])}, and {inputs.instruments[-1]}")
            else:
                sentence_parts.append(instruments_part)
    else :
        if inputs.instruments:
            instruments_part = ', '.join(inputs.instruments)
            if len(inputs.instruments) > 1:
                if len(inputs.instruments) == 2:
                    sentence_parts.append(f"a {inputs.instruments[0]} and {inputs.instruments[-1]}")
                else:
                    sentence_parts.append(f"a {', '.join(inputs.instruments[:-1])}, and {inputs.instruments[-1]}")    
            else:
                sentence_parts.append(instruments_part)
              
        if inputs.moods:
            sentence_parts.append(', '.join(inputs.moods))
    
    if not is_simple:
        if inputs.etc:
            sentence_parts.append(', '.join(inputs.etc))
        
    if "Auto" not in inputs.tempo:
        sentence_parts.append(inputs.tempo + ' bpm')

    return ', '.join(sentence_parts)

def generate_music_caption_text_analysis(inputs) -> str:
    caption = inputs.text + ' ' + ', '.join(inputs.etc)
    return caption