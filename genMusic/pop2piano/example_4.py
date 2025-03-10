# Example of processing multiple audio files in batch (Using Pop2PianoFeatureExtractor and Pop2PianoTokenizer)
import time

import librosa
from transformers import Pop2PianoForConditionalGeneration, Pop2PianoFeatureExtractor, Pop2PianoTokenizer

# feel free to change the sr to a suitable value.
audio1, sr1 = librosa.load("/Users/apple/Music/网易云音乐/Tommee-Profitt_Brooke-Can_t-Help-Falling-In-Love-_LIGHT_.wav", sr=44100)
audio2, sr2 = librosa.load("/Users/apple/Desktop/pythonProject/torchL/genMusic/musicLab/fromNetEase/xunzhang.wav", sr=44100)
model = Pop2PianoForConditionalGeneration.from_pretrained("sweetcocoa/pop2piano")
feature_extractor = Pop2PianoFeatureExtractor.from_pretrained("sweetcocoa/pop2piano")
tokenizer = Pop2PianoTokenizer.from_pretrained("sweetcocoa/pop2piano")

inputs = feature_extractor(
    audio=[audio1, audio2], 
    sampling_rate=[sr1, sr2], 
    return_attention_mask=True, 
    return_tensors="pt",
)
# Since we now generating in batch(2 audios) we must pass the attention_mask
model_output = model.generate(
    input_features=inputs["input_features"],
    attention_mask=inputs["attention_mask"],
    composer="composer1",
)
tokenizer_output = tokenizer.batch_decode(
    token_ids=model_output, feature_extractor_output=inputs
)["pretty_midi_objects"]

# Since we now have 2 generated MIDI files
current = str(time.time())
tokenizer_output[0].write("outputs/midi_output_4_"+ current +".mid")
tokenizer_output[1].write("outputs/midi_output_4_"+ current +".mid")