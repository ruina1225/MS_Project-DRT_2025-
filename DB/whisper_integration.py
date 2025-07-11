# whisper 음성인식 실행
def transcribe_audio(audio_file_path: str) -> str:
    import whisper
    # 모델 불러오기 (tiny, base, small, medium, large 중 선택 가능)
    model = whisper.load_model("base")

    # 오디오 파일 이름 입력 (예: audio.mp3) -> 파일 경로 파라미터로 받음 
    result = model.transcribe(audio_file_path)

    # 결과 리턴
    return(result["text"])