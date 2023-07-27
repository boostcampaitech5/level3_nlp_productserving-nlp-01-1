from train import train
from testgen import test_generate
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--train', type=bool, required=False, default=False)
parser.add_argument('--dataset_path', type=str, required=False, default='dataset')
parser.add_argument('--model_id', type=str, required=False, default='small')
parser.add_argument('--lr', type=float, required=False, default=0.0001)
parser.add_argument('--epochs', type=int, required=False, default=5)
parser.add_argument('--use_wandb', type=bool, required=False, default=False)
parser.add_argument('--save_path', type=str, required=False, default='models/')
parser.add_argument('--save_step', type=int, required=False, default=None)

parser.add_argument('--test', type=bool, required=False, default=False)
parser.add_argument('--state_dir', type=str, required=False,
                    default='models/lm_final.pt')
parser.add_argument('--wav_path', type=str, required=False, default='test.wav')
parser.add_argument('--caption', type=str, required=False, default=None)

args = parser.parse_args()

if args.train:
    train(
        dataset_path=args.dataset_path,
        model_id=args.model_id,
        lr=args.lr,
        epochs=args.epochs,
        use_wandb=args.use_wandb,
        save_path=args.save_path,
        save_step=args.save_step,
    )
    
if args.test:
    test_generate(
        model_id=args.model_id,
        state_dir=args.state_dir,
        wav_path=args.wav_path,
        caption=args.caption,
    )