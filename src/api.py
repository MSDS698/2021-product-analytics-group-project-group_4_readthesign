import os
import time
import torch
import pandas as pd
import transformers
import pandas as pd
import torch.nn as nn
from typing import List
from fastapi import FastAPI
from fastapi import FastAPI, Query
from transformers import T5Tokenizer, T5ForConditionalGeneration

class BERTDataset:
    def __init__(self, texts, targets, max_len=64):
        self.texts = texts
        self.targets = targets
        self.tokenizer = transformers.BertTokenizer.from_pretrained("bert-base-uncased", do_lower=True)
        self.max_len = max_len
        
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        inputs = self.tokenizer.encode_plus(
            text=text,
            text_pair=None,
            add_special_tokens=True,
            max_length=self.max_len,
            padding="max_len",
            truncation=True
        )
        resp = {
            "ids":torch.tensor(inputs["input_ids"], dtype=torch.long),
            "mask":torch.tensor(inputs["attention_mask"], dtype=torch.long),
            "token_type_ids":torch.tensor(inputs["token_type_ids"], dtype=torch.long),
            "targets":torch.tensor(self.targets[idx], dtype=torch.long)
        }
        return resp


class TextModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = transformers.BertModel.from_pretrained("bert-base-uncased", return_dict=False)
        self.bert_drop = nn.Dropout(0.3)
        self.out = nn.Linear(768, 1)
    
    def forward(self, ids, mask, token_type_ids, targets=None):
        _, x = self.bert(ids, attention_mask=mask, token_type_ids=token_type_ids)
        x = self.bert_drop(x)
        x = self.out(x)
        return x, 0, {}


def generate(text, model, tokenizer):
    model.eval()
    input_ids = tokenizer.encode("WebNLG:{} </s>".format(text), return_tensors="pt")
    # input_ids.to(dev)
    s = time.time()
    outputs = model.generate(input_ids)
    gen_text = tokenizer.decode(outputs[0]).replace('<pad>','').replace('</s>','')
    elapsed = time.time() - s
    # print('Generated in {} seconds'.format(str(elapsed)[:4]))
    return gen_text, elapsed


model_name = '/home/jansonboss/lexisNexis/witness_expert/text_generation/model/pytoch_model_test_keywords.bin'
model = T5ForConditionalGeneration.from_pretrained(
            model_name, 
            return_dict=True,
            config='/home/jansonboss/lexisNexis/witness_expert/text_generation/config/t5-base-config.json'
        )
tokenizer = T5Tokenizer.from_pretrained('t5-base') # T5-Base (220 million parameters):

# initialize fastapi
app = FastAPI()
@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/predict")
def fetch_predictions(text: str):
    generated_text, elasped = generate(text=text, model=model, tokenizer=tokenizer)
    return {"time used": elasped, "input": text, "generated text": generated_text}

@app.get("/items/")
def read_items(q: List[int] = Query(None)):
    return {"q": q}


# if __name__ == "__main__":
#     pass

    # in terminal run:
    # cd to the src and run following
    # uvicorn api:app --reload
    # ui interface: http://127.0.0.1:8000/redoc