import string

def readData(pathName):
    sentencesList = []
    punctuations = ".،:؛!؟*\"\'«»"
    with open(pathName,encoding="utf8") as f:
        for line in f.readlines():
            line = line.translate(str.maketrans('', '', punctuations))
            sentencesList.append(line)
    return sentencesList

def findWords(sentencesList):
    wordsList = []
    for sentence in sentencesList:
        words = sentence.split()
        for word in words:
            wordsList.append(word)
    return wordsList

def findUnigramFrequencies(wordsList):
    freqDic = dict()
    for i in wordsList:
        if not i in freqDic:
            if wordsList.count(i) >= 2:
                freqDic[i] = wordsList.count(i)
    return freqDic

def findPairedWords(sentencesList,uniFreqDict):
    pairsWordsList = []
    for sentence in sentencesList:
        words = sentence.split()
        for i in range(len(words)-1):
            if words[i] in uniFreqDict and words[i + 1] in uniFreqDict: 
                pair = words[i] + "," + words[i + 1]
                pairsWordsList.append(pair)
    return pairsWordsList

def findPairedFrequency(sentencesList,uniFreqDict):
    pairsWordsList = findPairedWords(sentencesList,uniFreqDict)
    frequencyPairedDict = {}
    for pair in pairsWordsList:
        if pair in frequencyPairedDict:                  
            frequencyPairedDict[pair] += 1
        else:
            frequencyPairedDict.update({pair: 1})
    return frequencyPairedDict

def buildUnigram(uniDict):
    uniModel = {}
    total = sum(uniDict.values())
    for word, count in uniDict.items():
        uniModel[word] = count / total
    return uniModel

def buildBigram(biDict,uniDict):
    bigramModel = {}
    for pair, count in biDict.items():
        tmp_list = pair.split(",")
        bigramModel[pair] = count / uniDict.get(tmp_list[0])
    return bigramModel

def backOffModel(pairWords,bigram_model,uni_model,l3,l2,l1,e):
    if pairWords in bigram_model:
        probb = bigram_model[pairWords]
    else:
        probb = 0
    tmp = (pairWords.split(","))[1]
    if tmp in uni_model:
        probu = uni_model[tmp]
    else:
        probu = 0
    return l3*probb + l2*probu + l1*e

def findPoet(poem,ferdowsiUni,fedowsiBi,hafezUni,hafezBi,molaviUni,molaviBi):
    ferdowsi = 1
    hafez = 1
    molavi = 1
    words = poem.split(" ")
    l1 = 0.2
    l2 = 0.7
    l3 = 0.1
    e = 0.0001
    for i in range(len(words) - 1):
        pairWords = words[i] + "," + words[i + 1]
        ferdowsi *= backOffModel(pairWords,fedowsiBi,ferdowsiUni,l3,l2,l1,e)
        hafez *= backOffModel(pairWords,hafezBi,hafezUni,l3,l2,l1,e)
        molavi *= backOffModel(pairWords,molaviBi,molaviUni,l3,l2,l1,e)
    if ferdowsi>hafez and ferdowsi>molavi:
        return 1
    elif hafez>ferdowsi and hafez>molavi:
        return 2
    else:
        return 3

if __name__ == "__main__":
    ferdowsiSentencesList = readData("./AI_P3/train_set/ferdowsi_train.txt")
    hafezSentencesList = readData("./AI_P3/train_set/hafez_train.txt")
    molaviSentencesList = readData("./AI_P3/train_set/molavi_train.txt")

    ferdowsiWordsList = findWords(ferdowsiSentencesList)
    hafezWordsList = findWords(hafezSentencesList)
    molaviWordsList = findWords(molaviSentencesList)

    ferdowsiUniFreqDict = findUnigramFrequencies(ferdowsiWordsList)
    hafezUniFreqDict = findUnigramFrequencies(hafezWordsList)
    molaviUniFreqDict = findUnigramFrequencies(molaviWordsList)

    ferdowsiBiFreqDic = findPairedFrequency(ferdowsiSentencesList,ferdowsiUniFreqDict)
    hafezBiFreqDic = findPairedFrequency(hafezSentencesList,hafezUniFreqDict)
    molaviBiFreqDic = findPairedFrequency(molaviSentencesList,molaviUniFreqDict)

    ferdowsi_uni_model = buildUnigram(ferdowsiUniFreqDict)
    ferdowsi_bigram_model = buildBigram(ferdowsiBiFreqDic,ferdowsiUniFreqDict)

    hafez_uni_model = buildUnigram(hafezUniFreqDict)
    hafez_bigram_model = buildBigram(hafezBiFreqDic,hafezUniFreqDict)

    molavi_uni_model = buildUnigram(molaviUniFreqDict)
    molavi_bigram_model = buildBigram(molaviBiFreqDic,molaviUniFreqDict)

    poems = open("./AI_P3/test_set/testcase.txt",encoding="utf8")
    count  = 0 
    total = 0
    for line in poems.readlines():
        poem = line.split("\t")
        poet = int(poem[0])
        re = findPoet(poem[1],ferdowsi_uni_model,ferdowsi_bigram_model,hafez_uni_model,hafez_bigram_model,molavi_uni_model,molavi_bigram_model)
        if re == poet :
            count+=1
        total+=1
    print(count / total)