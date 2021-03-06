import torch
import json
# import sys

# sys.path.append("./")
import myutils

def pred(path2vido):
    model_type = "rnn"
    model = myutils.get_model(model_type=model_type, num_classes=181)
    model.eval()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # input: replace these with the video dir you wanna predict
    frames, v_len = myutils.get_frames(path2vido, n_frames=16)
    # len(frames), v_len

    # load model
    path2weights = "weights.pt"
    model.load_state_dict(torch.load(path2weights))
    model.to(device)

    imgs_tensor = myutils.transform_frames(frames, model_type)
    # print(imgs_tensor.shape, torch.min(imgs_tensor), torch.max(imgs_tensor))

    with torch.no_grad():
        out = model(imgs_tensor.to(device)).cpu()
        # print(out.shape)
        predidx  = torch.argmax(out).item()

        with open('idx2text.txt', 'r') as f:
            idx2text = f.read().replace("\'", "\"")
            idx2text = json.loads(idx2text)
            predtext = (list(idx2text.items())[predidx][0])

        # print(pred)
        return predtext