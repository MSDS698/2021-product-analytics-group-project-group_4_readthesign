import torch
import time
import json
import warnings
import pandas as pd
from transformers.optimization import  Adafactor 
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration

if torch.cuda.is_available():
  dev = torch.device("cuda:0") 
  print("Running on the GPU")
else:
  dev = torch.device("cpu")
  print("Running on the CPU")



def generate(text):
    model.eval()
    input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), return_tensors="pt")  # Batch size 1
    # input_ids.to(dev)
    s = time.time()
    outputs = model.generate(input_ids)
    gen_text = tokenizer.decode(outputs[0]).replace('<pad>','').replace('</s>','')
    elapsed = time.time() - s
    print('Generated in {} seconds'.format(str(elapsed)[:4]))
    return gen_text

# loading the model
model_name = './model/pytoch_model_full_keywords.bin'
tokenizer = T5Tokenizer.from_pretrained('t5-base') # T5-Base (220 million parameters):
# loading the configuation
model = T5ForConditionalGeneration.from_pretrained(model_name, return_dict=True,config='./config/t5-base-config.json')

body = {}
prediction = []


val_df = pd.read_csv("./data/val.csv")
# predict keywords
for id, i, j in zip(val_df.cluster_id, val_df.input_text, val_df.target_text):
    result = generate(i)
    print("cluster id: ", id)
    print("keywords: ", i)
    print("validation: ", j)
    print("Generated: ", result, "\n")
    prediction.append(result)

body['message'] = 'OK'
body['input'] = [i for i in val_df.input_text]
body['prediction'] = prediction

response = {
    "statusCode": 200,
    "body": json.dumps(body),
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }
}

# print(response)
