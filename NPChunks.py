import nltk
import math
document=str(open("1_tagged_corpus.txt","r+").read())
sentence=[]
kalimat=document.split(".")
for i in range(5):
    kata=kalimat[i].split(" ")
    temp1=[]
    for j in range(len(kata)):
        temp=kata[j].split("/")
        if(len(temp)==2):
            if(i==0 and j==0):
                temp1+=[('Transvision','NNP')]
            else:
                temp1+=[(temp[0],temp[1])]
    sentence+=[temp1]
print(sentence)
grammar="NP: {<NNP>+<Z>*<NNP>*|<NN>+<IN>*<JJ>*<FW>*<NNP>*<NN>*}"
cp=nltk.RegexpParser(grammar)
result=[]
convertedResult=[]
for i in range(5):
    result += [cp.parse(sentence[i])]
    convertedResult+=[nltk.chunk.tree2conlltags(result[i])]

f=open("2_hasil_np_tree.txt","w")
for i in range(len(result)):
    f.write(str(result[i]))
    f.write("\n")
f.close()
f=open("2_hasil_np_iob.txt","w")
for i in range(len(convertedResult)):
    f.write(str(convertedResult[i]))
    f.write("\n")
f.close()