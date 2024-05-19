#Code Contrtibuted By Vansh Kumar
#email_id:1) vanshkr22@gmail.com  2)vansh.kumar.ug21@nsut.ac.in
#contact_no: +91-9311610564
#Blackcoffer Intern Test Assignment

#For approach and dependecies of this code an Instruction.pdf is also submitted


import numpy as np
import pandas as pd
import requests
import re
import os
from bs4 import BeautifulSoup

#Data Extraction Using BeautifulSoup

df=pd.read_excel("Input.xlsx")
column_name = 'URL'
def extract_article_title(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article_title = soup.find('title')
    return article_title.text if article_title else "No Title Found"

def extract_article_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article_text = soup.find("div", class_="td-post-content tagdiv-type")
    
    if article_text is None:
        article_text = soup.find("div", class_="tdb-block-inner.td-fix-index")
               
    return article_text.text if article_text else "No Text Found"

def clean_filename(title):
    # Remove or replace invalid characters in the title for a filename
    invalid_chars = r'[\/:*?"<>|]'
    cleaned_title = re.sub(invalid_chars, '_', title)
    return cleaned_title[:50]  # Truncate to avoid long filenames

for index, value in df[column_name].items():
    article_title = extract_article_title(value)
    article_text = extract_article_text(value)

    cleaned_file_name = f"{clean_filename(article_title)}.txt"
    with open(cleaned_file_name, 'w+', encoding='utf-8') as file:
        file.write(article_text)


#Textual Analysis Block begins here
        
def load_words_from_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding, errors='replace') as file:
        words=set(word.strip() for word in file.readlines())
    return words

def compare_create_dictionary(article_path, positive_words_path, negative_words_path, stop_words_folder):
    positive_words=load_words_from_file(positive_words_path)
    negative_words=load_words_from_file(negative_words_path)
    
    
    article_words=set()
    
    with open(article_path, 'r', encoding='utf-8', errors='replace') as article_file:
        article_words.update(word.lower() for word in article_file.read().split())
    
    result_dict={}
    for stop_word_file in os.listdir(stop_words_folder):
        stop_word_file_path=os.path.join(stop_words_folder, stop_word_file)
        stop_words=load_words_from_file(stop_word_file_path)
        
        for word in article_words:
            if word in positive_words and word not in stop_words:
                result_dict[word]='positive-word'
            elif word in negative_words and word not in stop_words:
                result_dict[word]='negative-word'
    
    return result_dict   

def count_syllables(word):
    exceptions={"es", "ed"}
    
    lower_word=word.lower()
    
    if lower_word.endswith("es") and lower_word not in exceptions:
        return 1
    elif lower_word.endswith("ed") and lower_word not in exceptions:
        return 1
    else:
        vowels = "aeiouy"
        return sum(1 for char in word if char.lower() in vowels)
    
def syllables_per_word(article_path):
    with open(article_path, 'r', encoding='utf-8') as article_file:
        content=article_file.read()
        
    #tokenize the content into words
    words=re.findall(r'\b\w+\b', content)
    
    #count syllables for each word
    syllable_counts=sum(count_syllables(word) for word in words)
    
    return syllable_counts

def count_complex_words(article_path):

    with open(article_path, 'r', encoding='utf-8') as article_file:
        content = article_file.read()

    sentences = re.split(r'[.!?]', content)
    words = re.findall(r'\b\w+\b', content)

    num_sentences = len(sentences)
    num_words = len(words)
    num_complex_words = sum(1 for word in words if count_syllables(word) > 2)

    return num_complex_words, num_words, num_sentences

def count_personal_pronouns(article_path):
    personal_pronouns_regex = re.compile(r'\b(?:I|we|my|ours|us)\b', re.IGNORECASE)

    with open(article_path, 'r', encoding='utf-8') as article_file:
        content = article_file.read()

    # Find all matches of personal pronouns using regex
    personal_pronouns_matches = personal_pronouns_regex.findall(content)

    # Exclude instances where "US" might refer to the country name
    personal_pronouns_matches = [pronoun for pronoun in personal_pronouns_matches if pronoun.lower() != 'us']

    
    pronoun_counts = {pronoun.lower(): personal_pronouns_matches.count(pronoun) for pronoun in set(personal_pronouns_matches)}

    return pronoun_counts

def count_alphabetical_characters(article_path):
    with open(article_path, 'r', encoding='utf-8') as article_file:
        content = article_file.read()

    
    alphabetical_count = sum(char.isalpha() for char in content)

    return alphabetical_count


def clean_filename(title):
    # Remove or replace invalid characters in the title for a filename
    invalid_chars = r'[\/:*?"<>|]'
    cleaned_title = re.sub(invalid_chars, '_', title)
    return cleaned_title[:50]  # Truncate to avoid long filenames


# Iterating each file one by one, calculating all the analytical parameters and creating a DataFrame as per Output Data Structure given along with the problem statement

column_name='URL'
df2=pd.read_excel("Output Data Structure.xlsx")

URL_ID=[]
URLS=[]
pos_score=[]
neg_score=[]
Pol_score=[]
Sub_score=[]
avgsen_len=[]
per_complex=[]
fog_ind=[]
comp_words=[]
tot_words=[]
syll_cnt=[]
per_cnt=[]
avgwor_len=[]

i=0
for index, value in df2[column_name].items():
    article_title = extract_article_title(value)
    #article_text = extract_article_text(value)

    cleaned_file_name = f"{clean_filename(article_title)}.txt"
    master_dict_folder="MasterDictionary"
    article_path=cleaned_file_name
    positive_words_path=os.path.join(master_dict_folder, "positive-words.txt")
    negative_words_path=os.path.join(master_dict_folder, "negative-words.txt")
    stop_words_folder="StopWords"

    result=compare_create_dictionary(article_path, positive_words_path, negative_words_path, stop_words_folder)

    positive_score = 0
    negative_score = 0

    for key in result:
        if result[key] == 'positive-word':
            positive_score += 1
        else:
            negative_score += 1

    #print(f"Positive Score: {positive_score}, Negative Score: {negative_score}")

    Polarity_score=(positive_score-negative_score)/((positive_score+negative_score)+0.000001)
    #print(f"Polarity Score:{Polarity_score}")

    Subjectivity_score=(positive_score+negative_score)/(len(result)+0.000001)
    #print(f"Subjectivity Score: {Subjectivity_score}")


    Complex_words, Total_words, Total_sentences=count_complex_words(article_path)

    #print(f"Complex Words:{Complex_words}, Total words:{Total_words}, Total_sentences:{Total_sentences}")

    #analysis of Readability
    avg_sentence_len=Total_words/Total_sentences
    percentage_complex=Complex_words/Total_words
    Fog_index=0.4*(avg_sentence_len+percentage_complex)
    #print(f"Fog index:{Fog_index}")
    Syllable_count=syllables_per_word(article_path)/Total_words
    count_personal=sum(count_personal_pronouns(article_path).values())
    avg_word_len=count_alphabetical_characters(article_path)/Total_words
    
    
    output={}
    
    
    URLS.append(value)
    pos_score.append(positive_score)
    neg_score.append(negative_score)
    Pol_score.append(Polarity_score)
    Sub_score.append(Subjectivity_score)
    avgsen_len.append(avg_sentence_len)
    per_complex.append(percentage_complex)
    fog_ind.append(Fog_index)
    comp_words.append(Complex_words)
    tot_words.append(Total_words)
    syll_cnt.append(Syllable_count)
    per_cnt.append(count_personal)
    avgwor_len.append(avg_word_len)
    
    if(i<9):
        URL_ID.append("blackassign"+"000"+str(i+1))
        i+=1
    elif(i>=9 and i<99):
        URL_ID.append("blackassign"+"00"+str(i+1))
        i+=1
    else:
        URL_ID.append("blackassign"+"0"+str(i+1))
        
    output['URL_ID']=URL_ID    
    output['URL']=URLS
    output['POSITIVE SCORE']=pos_score
    output['NEGATIVE SCORE']=neg_score
    output['POLARITY SCORE']=Pol_score
    output['SUBJECTIVITY SCORE']=Sub_score
    output['AVG SENTANCE LENGTH']=avgsen_len
    output['PERCENTAGE OF COMPLEX WORDS']=per_complex
    output['FOG INDEX']=fog_ind
    output['AVG NUMBER OF WORDS PER SENTENCE']=avgsen_len
    output['COMPLEX WORD COUNT']=comp_words
    output['WORD COUNT']=tot_words
    output['SYLLABLE PER WORD']=syll_cnt
    output['PERSONAL PRONOUNS']=per_cnt
    output['AVG WORD LENGTH']=avgwor_len
    

##for key, value in output.items():
   ## print(f"{key}: {value}")    
    
df=pd.DataFrame(output)
output_file='output_data.xlsx'

df.to_excel(output_file, index=False)
df.head()