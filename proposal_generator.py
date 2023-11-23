#!pip3 install huggingface-hub>=0.17.1
from ctransformers import AutoModelForCausalLM
import pandas as pd
import nltk
import xlrd
llm = AutoModelForCausalLM.from_pretrained("TheBloke/platypus-yi-34b-GGUF", model_file="platypus-yi-34b.Q4_K_M.gguf", model_type="llama", gpu_layers=0)
df = pd.read_excel("Test2.xlsx")


#Create function to post process output
def truncate_text(text, num_sentences):
    # Tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)

    # Select the first 'num_sentences' sentences
    truncated_text = ' '.join(sentences[:num_sentences])

    return truncated_text
#Initialize list for output
Output=[]
#from ctransformers import AutoModelForCausalLM
# Use each row in the spreadsheet as a prompt for text generationa and store the result as a list of strings
for index, row in df.iterrows():
    prompt='Answer the following from the point of view of Rubix, an Australian data consultancy specialising in data engineeering and data science who are responding to a tender request, .'+row['Question']+'Our response is:'
    llm = AutoModelForCausalLM.from_pretrained("TheBloke/platypus-yi-34b-GGUF", model_file="platypus-yi-34b.Q4_K_M.gguf", model_type="llama", gpu_layers=0)
    text_out=llm(prompt)
    truncated_text = truncate_text(text_out, 4)
    Output.append(truncated_text)
#Append LLM responses as new column 'Output' and write to Excel
df['Output']=Output
df.to_excel("OutputFileNew.xlsx")
