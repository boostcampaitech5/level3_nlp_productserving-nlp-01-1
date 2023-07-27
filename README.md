# 음악 생성 모델

# 1. 문제 정의

- **특정 장르 및 악기에 대한 표현이 부실함.**
    - 현재 musicgen은 국악에 대해서 생성하지만, 단순히 국악 외에 무드 정보에 대해 잘 따르지 않는 경향을 보이는 것을 확인.
    - 블로그 글, 소설, 키워드 등 한국 전통적 요소에 대해 폭 넓게 음악을 생성해내지 못하는 문제 발생.
    - fine tuning을 통해 국악 악기 및 장르를 학습하여, 한국 전통 문화 관련 text 정보가 들어왔을 때, 잘 생성해 낼 수 있도록 fine tuning을 시도해볼 수 있음.
- **하나의 악기에 대해 학습을 진행하여 악기 특화 기능 구현**
    - 현재 musicgen은 단일 악기에 대해서 생성하기 보다, 다른 여러 악기가 사용되는 음악이 주로 생성되는 경향이 있는 것을 확인.
    - 하나의 악기에 대해서만 장르, 분위기, 키워드 등에 따라 더욱 잘 생성되도록 하는 기능을 제공하는 것을 목표로 모델을 학습시킬 수 있을 것임.
- **생성된 음악의 퀄리티**
    - 현재 공개된 text2music generation 모델들이 생성한 음악은 유튜브 및 스트리밍 음원사이트의 음악보다 낮은 음질, 불협 등의 문제로 유저로부터 낮은 만족도를 느끼게 할 수 있음.
    - 모델 fine tuning, 생성된 음악에 대한 후처리 등의 방법을 통해, 생성된 음악의 퀄리티를 개선할 수 있을 것임.

# 2. 데이터셋

## 국악 Finetuning 데이터셋

국악에 대해 fine-tuning한 모델은 국악 음원을 잘 생성하지만, 국악 외에 잘 따르지 않는 경향을 보이는 것을 확인. 

fine tuning을 통해 특정 악기 및 장르를 학습하여, 기존의 장르에 특정 악기를 추가하거나 다른 장르를 융합된 결과를 기대하고 있음.

- 데이터셋 : aihub 국악 데이터셋
- 데이터 수 :  11,069개 (154,076초)
- 데이터 형식 : MID(악보파일), WAV(음원파일), JSON(가사, 속성 정보)
- Reference :  [국악 악보 및 음원 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=realm&dataSetSn=71470)

## 카테고리 정의 및 데이터 구축

- 데이터셋
    - musicgen 학습 및 평가에 사용한 데이터를 제공하는 사이트들의 카테고리 정보를 수집하여 정리.
- 데이터 형식
    - JSON(카테고리 정보 데이터)
    - **Instruments, Genres, Moods,Tempos, ETC** 5개의 필드를 정의하고, **Instruments, Genres, Moods** 3가지 필드에 대해 생성 여부 테스트 및 팀 회의를 거쳐 사용하지 않을 카테고리를 제거하는 작업을 수행.

# 3. 모델 구성

![Image](https://file.notion.so/f/s/47e921c2-2e87-435a-97d8-236447063558/Untitled.png?id=17d5ef93-197a-4639-a226-ecdb215af9db&table=block&spaceId=0825c815-092a-430c-9d39-95d69099fbe9&expirationTimestamp=1690567200000&signature=XnqUPWWAWwgt0WjoiIz8Q__0u0uJazblMoy4kjvn1bo&downloadName=Untitled.png)

# 4.모델 선택

## Riffusion

- 생성된 음악의 퀄리티가 MusicLM과 MusicGen과 비교하여 좋지 않다는 의견이 모아짐.

## MusicLM

- 모델이 공개되지 않음.
- 학습에 사용된 음악이 그대로 출력되는 경우가 존재.

## MusicGen

- 모델이 공개되어 있음.
- fine-tuning이 가능함이 확인 됨.
- 생성된 음악의 퀄리티가 비교적 좋은 것을 확인 됨.
- facebook research 측에서 추후에 trainer를 공개한다는 것을 Github에 명시함.

## 최종 모델 선택

- 생선된 음원의 음질과 음원이 입력된 문장, 또는 캡션에 어울리게 나오는지에 따라 평가를 진행.
- Riffusion은 다른 두 모델에 비해 음원이 입력에 알맞게 생성하지 않는 모습을 보여 탈락.
- MusicLM은 모델 및 코드가 공개적으로 배포되지 않았고, MusicGen Trainer가 존재하기 때문에 MusicGen을 최종적으로 선택
