from django.shortcuts import render
from django.http import HttpResponse
import os
import django
django.setup()
from .forms import CommentForm
from .models import comments
import ast,_ast
import sys
import nltk
import string
import scipy.sparse
import profanity
from profanity import profanity
from nltk import pos_tag
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim import corpora, models
import logging
from profanity import profanity
import re
from nltk.stem import wordnet
from nltk.corpus import stopwords
from urllib.request import urlopen
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt2
from wordcloud import WordCloud
import numpy as np
import os
# Create your views here.

def home(request):
	if request.method=='POST':
		form=CommentForm(request.POST)
		#com=request.POST.get(['comment'])
		com=form['comment'].value()
		if form.is_valid():
			if(profanity.contains_profanity(com)):
				print('Badwords present')
				posts=comments.objects.all()
				args={'form':form,'posts':posts}
				return render(request,'Form.html',args)
			else:
				stop_words = set(stopwords.words('english'))
				tokenizer=nltk.tokenize.punkt.PunktSentenceTokenizer()
				tokens=tokenizer.tokenize(com)
				tokens2=list()
				index=0
				for i in tokens:
					tokens2=tokens2+word_tokenize(tokens[index])
					index=index+1
				print('\n\n\nSentence tokens',tokens)
				print('\n\n\nWord tokens',tokens2)

				filtered_sentence = []
				for w in tokens2:
				    if w.lower() not in stop_words and w not in string.punctuation:
				        filtered_sentence.append(w.lower())
				print('\n\n\nFiltered tokens',filtered_sentence)

				tagged=pos_tag(filtered_sentence)
				print('\n\n\nPOS tagging',tagged)
				candNouns=[word for word,pos in tagged if(pos=='NN'or pos=='NNS' or pos=='NNP' or pos=='NNPS')]
				print('\n\n\nCandidate nouns',candNouns)

				bigram=list(ngrams(candNouns,2))
				result=[list(i) for i in bigram] 
				print('\n\n\nBigrams',result)

				dictionary = corpora.Dictionary(result)
				print(dictionary)
				    
				corpus = [dictionary.doc2bow(text) for text in result]
				print(corpus)

				ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)

				print(ldamodel.print_topics(num_topics=5,num_words=2))
				form.save()
				posts=comments.objects.all()
				args={'form':form,'posts':posts}
				return render(request,'Form.html',args)
	else:
		positive=[]
		posper=[]
		negper=[]
		def split_line(line):
		    cols = line.split("\t")
		    return cols

		def get_words(cols):
		    words_ids = cols[4].split(" ")
		    words = [w.split("#")[0] for w in words_ids]
		    return words

		def get_positive(cols):
		    return cols[2]

		def get_negative(cols):
		    return cols[3]

		def get_objective(cols):
		    return 1 - (float(cols[2]) + float(cols[3]))

		def get_gloss(cols):
		    return cols[5]

		def get_scores(filepath, sentiword):
			f = open(filepath)
			totalobject = 0.0
			count = 0.0
			totalpositive = 0.0
			totalnegative = 0.0
			for line in f:
				if not line.startswith("#"):
					cols = split_line(line)
					words = get_words(cols)
					for word in sentiword:
						if word in words:
							if word == "not":
								totalobject = totalobject + 0
								totalpositive = totalpositive +0
								totalnegative = totalnegative + 16
								count =count + 1
							else:
								totalobject = totalobject + get_objective(cols)
								totalpositive = totalpositive + float(get_positive(cols))
								totalnegative = totalnegative + float(get_negative(cols))
								count =count + 1
			if count >0:
				if totalpositive > totalnegative :
					positive.append(1)
					posper.append(totalpositive)
					print("Positive word : 1")
					print("Positive value : ",totalpositive)
					print("Negative value : ",totalnegative)
				else :
					positive.append(-1)
					negper.append(totalnegative)
					print("Negative : -1")
					print("Positive value : ",totalpositive)
					print("Negative value : ",totalnegative)
				print("average object Score : ",totalobject/count)
		print("Etered")
		reviews=comments.objects.all()
		l=list()
		com=""
		print(len(reviews))
		for rev in reviews:
			com=(rev.comment)
			l.append(com)
			print(l)
		for i in l:
			comment = i
			sentiword = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", comment).split())
			stop_words = set(stopwords.words('english'))
			sentiword = sentiword.lower().split(" ")
			filtered_sentence = [w for w in sentiword  if not w in stop_words ]
			get_scores("C:/Users/HP/Desktop/forum/discussion/SentiWordNet_3.0.0_20130122.txt",filtered_sentence)
		if len(posper)==0:
			posi=0
		else:
			posi=sum(posper)/len(posper)
		if len(negper)==0:
			negi=0
		else:
			negi=sum(negper)/len(negper)
		print(posi,negi)
		str=""
		for i in filtered_sentence:
			str=str+" "+i
		print(str)
		wordcloud = WordCloud(width=2500,height=2000).generate(str)
		if os.path.isfile("C:/Users/HP/Desktop/forum - Copy/discussion/static/images/bar.png"):
			os.remove("discussion/static/images/bar.png")
		if os.path.isfile("C:/Users/HP/Desktop/forum - Copy/discussion/static/images/wordcloud.png"):
			os.remove("discussion/static/images/wordcloud.png")
		f1=plt.figure(1)
		plt.imshow(wordcloud, interpolation="bilinear")
		plt.axis("off")
		f1.savefig("C:/Users/HP/Desktop/forum - Copy/discussion/static/images/wordcloud.png")
		f2=plt.figure(2)
		label=['Positive','Negitive']
		percentage=[posi,negi]
		index = np.arange(len(label))
		plt.bar(index,percentage)
		plt.xticks(index, label, fontsize=5, rotation=30)
		plt.title('Reaction')
		f2.savefig("C:/Users/HP/Desktop/forum - Copy/discussion/static/images/bar.png")
		form=CommentForm()
		posts=comments.objects.all()
		args={'form':form,'posts':posts}
		return render(request,'Form.html',args)