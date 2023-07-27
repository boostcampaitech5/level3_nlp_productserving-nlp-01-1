import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import normalize_audio

import torch

def test_generate(model_id, state_dir, save_dir, caption):

    model = MusicGen.get_pretrained(model_id)

    self = model

    self.lm.load_state_dict(torch.load(state_dir))

    attributes, prompt_tokens = self._prepare_tokens_and_attributes([caption], None)
    print("attributes:", attributes)
    print("prompt_tokens:", prompt_tokens)

    duration = 30

    use_sampling = True
    top_k = 250
    top_p = 0.0
    temperature = 1.0
    cfg_coef = 3.0
    two_step_cfg = False

    assert duration <= 30, "The MusicGen cannot generate more than 30 seconds"

    self.generation_params = {
        'max_gen_len': int(duration * self.frame_rate),
        'use_sampling': use_sampling,
        'temp': temperature,
        'top_k': top_k,
        'top_p': top_p,
        'cfg_coef': cfg_coef,
        'two_step_cfg': two_step_cfg,
    }

    with self.autocast:
        gen_tokens = self.lm.generate(prompt_tokens, attributes, callback=None, **self.generation_params)
        
    assert gen_tokens.dim() == 3
    print("gen_tokens information")
    print("Shape:", gen_tokens.shape)
    print("Dtype:", gen_tokens.dtype)
    print("Contents:", gen_tokens)

    with torch.no_grad():
        gen_audio = self.compression_model.decode(gen_tokens, None)
    print("gen_audio information")
    print("Shape:", gen_audio.shape)
    print("Dtype:", gen_audio.dtype)
    print("Contents:", gen_audio)

    gen_audio = gen_audio.cpu()
    torchaudio.save(save_dir, gen_audio[0], self.sample_rate)
    torchaudio.save('noramlized_' + save_dir, normalize_audio(gen_audio[0]), self.sample_rate)
