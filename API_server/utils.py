import torch
import gc

def setting_device_status():
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("working on gpu")
    else:
        device = torch.device("cpu")
        print("working on cpu")

def empty_cache():
    gc.collect()
    torch.cuda.empty_cache()