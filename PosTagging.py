import docx2txt
import re

def cariJumlahTag(tag, data):
    count = 0
    for word in data:
        if tag == word:
            count = count + 1
    return count

def likelihood(kata, tag, data):
    count = 0
    Px = kata+"/"+tag
    for word in data:
        if Px == word:
            count = count + 1
    return count

def maximal(data):
    nilai = data[0]
    tag = 0
    for i in range(len(data)):
        if data[i] > nilai:
            nilai = data[i]
            tag = i
    return nilai, tag

def hitungAkurasi(dataBenar, dataTotal):
    akurasi = dataBenar/dataTotal
    return akurasi

if __name__ == '__main__':
    raw_corp = docx2txt.process("1_raw_corpus.docx")
    tandaBaca = re.findall(r'[^A-Za-z0-9\ ]', raw_corp)

    kata = re.sub(r'[^A-Za-z0-9\ ]', "", raw_corp)
    kataSplit = kata.split()
    seluruhData = kataSplit+tandaBaca


    docB = open("1_tagged_corpus.txt", "r", encoding="utf-8-sig")
    taggedCourpus = docB.read()
    docB.close()
    dataWithTagged = taggedCourpus.split(" ")
    dataTag = re.findall(r'\/[A-Z]{1,3}', taggedCourpus)

    for i in range(len(dataTag)):
        dataTag[i] = re.sub(r'\/',"",dataTag[i])

    tagSet = ["CC","CD","FW","IN","JJ","NEG","NN","NNP","NND","PR","PRP","RB","SC","SYM","VB","Z"]
    rawDataUji = [["Transvision menghadirkan produk yaitu streaming box yang menggunakan teknologi smartphone androidTM yang merupakan smartphone canggih terbaru ."],
                ["GoogleTM Assistant mengeksplorasi hal bagi pengguna , GoogleTM Assistant juga dapat menjadi teknologi canggih dan powerful ."],
                ["Samsung memiliki produk smartphone yang memiliki fitur unggulan yang canggih ."],
                ["Ruang keluarga merupakan pusat dari kegiatan kehangatan keluarga ."],
                ["Desainnya yang terbuka sesuai tema interior dengan kebutuhan seluruh anggota keluarga ."]]

    hasilPengujian =[]
    for i in range(len(rawDataUji)):
        dataHasilTag = []
        for kalimat in rawDataUji[i]:
            kataDataUji = kalimat.split(" ")
            for word in kataDataUji:
                kemunculan = []
                for tag in tagSet:
                    nilaiTag = cariJumlahTag(tag,dataTag)
                    NaiveBayes = (nilaiTag/len(seluruhData))*(likelihood(word, tag, dataWithTagged)/nilaiTag)
                    kemunculan.append(NaiveBayes)
                max, indexTagMax = maximal(kemunculan)
                tagMax = tagSet[indexTagMax]
                hasilCariTag = word+"/"+tagMax
                dataHasilTag.append(hasilCariTag)
            hasilPengujian.append(dataHasilTag)

    groundTruth = [["Transvision/NNP","menghadirkan/VB","produk/NN","yaitu/SC","streaming/FW","box/FW","yang/SC","menggunakan/VB","teknologi/NN","smartphone/FW","androidTM/NNP","yang/SC","merupakan/SC","smartphone/FW","canggih/NN","terbaru/JJ","./SYM"],
                   ["GoogleTM/NNP","Assistant/NNP","mengeksplorasi/VB","hal/NN","bagi/IN","pengguna/NN",",/SYM","GoogleTM/NNP","Assistant/NNP","juga/SC","dapat/VB","menjadi/VB","teknologi/NN","canggih/NN","dan/CC","powerful/FW","./SYM"],
                   ["Samsung/NNP","memiliki/VB","produk/NN","smartphone/FW","yang/SC","memiliki/VB","fitur/NN","unggulan/NN","yang/SC","canggih/NN","./SYM"],
                   ["Ruang/NN","keluarga/NN","merupakan/SC","pusat/NN","dari/IN","kegiatan/NN","kehangatan/NN","keluarga/NN","./SYM"],
                   ["Desainnya/NN","yang/SC","terbuka/JJ","sesuai/JJ","tema/NN","interior/NN","dengan/IN","kebutuhan/NN","seluruh/CD","anggota/NN","keluarga/NN","./SYM"]]

    count = 0
    totalTagDataUji = 0
    for i in range(len(groundTruth)):
        for j in range(len(groundTruth[i])):
            totalTagDataUji = totalTagDataUji + 1
            if hasilPengujian[i][j] == groundTruth[i][j]:
                count = count + 1
        akurasi = hitungAkurasi(count, totalTagDataUji)
        print("akurasi data uji ke-", i + 1," : ",akurasi, "/", akurasi * 100, "%")
    akurasi = hitungAkurasi(count,totalTagDataUji)
    print("akurasi data uji keseluruhan\t: ",akurasi,"/",akurasi*100,"%")

