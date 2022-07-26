import heapq
import re
from fastapi import FastAPI
from fastapi.responses import FileResponse
import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk.probability import FreqDist
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


s = requests.get(
    'https://www.azlyrics.com/lyrics/akon/beautiful.html')
s.encoding = 'utf-8'
html = s.text

soup = BeautifulSoup(html, "lxml")
text = soup.text


# tokenizing the text
tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
token = tokenizer.tokenize(text)

clean_text = str(re.sub("\s{2,}", " ", text))
# tokenizing the text
data_words = word_tokenize(clean_text)
data_sent = sent_tokenize(clean_text)

# removing stop words
stop_words = set(stopwords.words('english'))
data_words_filt = [w for w in data_words if w not in stop_words]


# pos tags
pos_tags = nltk.pos_tag(data_words_filt)

# named entity representaion
namedEntity = nltk.ne_chunk(pos_tags, binary=True)

# putting all nouns, proper nouns and verbs into lists
NOUNS = [w[0] for w in pos_tags if (w[1] == 'NN') and (len(w[0])) > 1]
PNOUNS = [w[0] for w in pos_tags if (w[1] == 'NNP') and (len(w[0])) > 1]
VERBS = [w[0] for w in pos_tags if (w[1] == 'VB') and (len(w[0])) > 1]

# getting the top most common 10 nouns
fdist_nouns = FreqDist(NOUNS)
fdist_pnouns = FreqDist(PNOUNS)
fdist_verbs = FreqDist(VERBS)

top_verbs = fdist_verbs.most_common(20)
top_nouns = fdist_nouns.most_common(10)
top_pnouns = fdist_pnouns.most_common(10)

labels = [word[0] for word in top_nouns]
values = [word[1] for word in top_nouns]


plt.figure(figsize=(10, 5), dpi=100)
plt.title('Top 10 Relevant Noun: Song Language')
plt.bar(labels, values)
plt.legend('Nouns')
plt.savefig('Nouns')
# plt.show()


# ploting nouns used
x = [word[0] for word in top_pnouns]
y = [word[1] for word in top_pnouns]

plt.figure(figsize=(10, 5), dpi=100)
plt.title('Most common Proper Nouns: Setting of Music')
plt.plot(x, y, 'g.-', label='ProperNouns')
plt.legend()

plt.savefig('properNouns')
# plt.show()


# ploting nouns used
x = [word[0] for word in top_verbs]
y = [word[1] for word in top_verbs]

plt.figure(figsize=(10, 5), dpi=100)
plt.title('Verbs mostly used in Presidential Statement')
plt.plot(x, y, 'r.-', label='Verbs')
plt.legend()

# plt.show()

frequency_table = {}
for word in data_words_filt:
    if(len(word) > 1):
        if word not in frequency_table.keys():
            frequency_table[word] = 1
        else:
            frequency_table[word] += 1

max_freq = max(frequency_table.values())

for word in frequency_table.keys():
    frequency_table[word] = frequency_table[word]/max_freq


# Algorithm for scoring a sentence by its word
sentence_weight = dict()

for sentence in data_sent:
    sent_count = len(sentence)
    sent_minus_stops_count = 0
    for word_weight in frequency_table:
        if word_weight in sentence.lower():
            sent_minus_stops_count = sent_minus_stops_count+1
            if sentence in sentence_weight:
                sentence_weight[sentence] = sentence_weight[sentence] + 1
            else:
                sentence_weight[sentence] = frequency_table[word_weight]
    #sentence_weight[sentence] = sentence_weight[sentence]


# GETTING THE DOCUMENT ABSTRACT...

summary_sentences = heapq.nlargest(7, sentence_weight, key=sentence_weight.get)
summary = ' '.join(summary_sentences[1:2])
# print(summary)
#print("\nLength of Summary ", len(summary))


app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Lyric(BaseModel):
    name: str


# the api endpoint

@app.get("/")
def read_root():
    return {"sentences": data_sent}


@app.post("/post-lyrics")
def postLyrics(lyric: Lyric):
    print(lyric)
    return "Success"


@app.get("/common-words")
def common_words():
    return {"commonNouns": top_nouns, "commonVerbs": top_verbs, "commonPnouns": top_pnouns}


@app.get("/graphs-noun", response_class=FileResponse)
def getNounGraph():
    return "Nouns.png"


@app.get("/graphs-pnoun", response_class=FileResponse)
def getPnounGraph():
    return "properNouns.png"


@app.get("/summary")
def getSummary():
    return summary
