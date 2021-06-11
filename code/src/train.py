import torch
import warnings
import pandas as pd
from transformers.optimization import  Adafactor 
from sklearn.model_selection import train_test_split
from transformers import T5Tokenizer, T5ForConditionalGeneration


def progress(loss,value, max=100):
    return HTML(""" Batch loss :{loss}
        <progress
            value='{value}'
            max='{max}',
            style='width: 100%'
        >
            {value}
        </progress>
    """.format(loss=loss,value=value, max=max))

def print_info():
    import os
    from psutil import virtual_memory
    ram_gb = virtual_memory().total / 1e9
    print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

    if ram_gb < 20:
        print('To enable a high-RAM runtime, select the Runtime > "Change runtime type"')
        print('menu, and then select High-RAM in the Runtime shape dropdown. Then, ')
        print('re-execute this cell.')
    else:
        print('You are using a high-RAM runtime!')

    gpu_info = !nvidia-smi
    gpu_info = '\n'.join(gpu_info)
    if gpu_info.find('failed') >= 0:
        print('Select the Runtime > "Change runtime type" menu to enable a GPU accelerator, ')
        print('and then re-execute this cell.')
    else:
        print(gpu_info)


# Confiuration
if torch.cuda.is_available():
    dev = torch.device("cuda:0") 
    print("Running on the GPU")
else:
    dev = torch.device("cpu")
    print("Running on the CPU")


train_df, val_df = data[:600], data[600:]
len(train_df), len(val_df)


# Read in data, train test split
data = pd.read_csv("key2text_full.csv", index_col=[0]) \
    .rename(columns = {"keywords": "input_text", "cluster_summary":"target_text"}) \
    .reset_index() \
    .sample(frac=1)

batch_size=5
num_of_batches=int(len(train_df)/batch_size)
num_of_epochs=10



# model set up
tokenizer = T5Tokenizer.from_pretrained('t5-base') # T5-Base (220 million parameters):
model = T5ForConditionalGeneration.from_pretrained('t5-base', return_dict=True)
#moving the model to device(GPU/CPU)
model.to(dev)

# define adam optimizer
optimizer = Adafactor(
    model.parameters(),
    lr=1e-3,
    eps=(1e-30, 1e-3),
    clip_threshold=1.0,
    decay_rate=-0.8,
    beta1=None,
    weight_decay=0.0,
    relative_step=False,
    scale_parameter=False,
    warmup_init=False
)



# Fine-tuning the model with data
model.train()

loss_per_10_steps=[]
for epoch in range(1,num_of_epochs+1):
    print('Running epoch: {}'.format(epoch))

    running_loss=0

    out = display(progress(1, num_of_batches+1), display_id=True)
    for i in range(num_of_batches):
    inputbatch=[]
    labelbatch=[]
    new_df=train_df[i*batch_size:i*batch_size+batch_size]
    for indx,row in new_df.iterrows():
        # for finetuning the T5, you need to add a self-defined prefix eg. "WebNLG"
        # so that T5 knows he should do this task you sepcifically defined
        # some tasks for pre-trained task: summarize: cola sentence: stsb sentence: 
        input = 'WebNLG: '+row['input_text']+'</s>' 
        labels = row['target_text']+'</s>'   
        inputbatch.append(input)
        labelbatch.append(labels)

    inputbatch=tokenizer.batch_encode_plus(inputbatch,padding=True,max_length=400,return_tensors='pt')["input_ids"]
    labelbatch=tokenizer.batch_encode_plus(labelbatch,padding=True,max_length=400,return_tensors="pt") ["input_ids"]
    inputbatch=inputbatch.to(dev)
    labelbatch=labelbatch.to(dev)

    # clear out the gradients of all Variables 
    optimizer.zero_grad()

    # Forward propogation
    outputs = model(input_ids=inputbatch, labels=labelbatch)
    loss = outputs.loss
    loss_num=loss.item()
    logits = outputs.logits
    running_loss+=loss_num
    if i%10 ==0:      
        loss_per_10_steps.append(loss_num)
    out.update(progress(loss_num,i, num_of_batches+1))

    # calculating the gradients
    loss.backward()

    #updating the params
    optimizer.step()
    
    running_loss=running_loss/int(num_of_batches)
    print('Epoch: {} , Running loss: {}'.format(epoch,running_loss))


# save model
torch.save(model.state_dict(),'pytoch_model_full_keywords.bin') # saving the model
