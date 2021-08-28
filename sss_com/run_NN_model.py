import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import plot_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.utils import plot_model, to_categorical

def convert(blist, rlist, allbssidlist, lengthOfNodes):
  tempnodelist = []
  for i in range(len(blist)):
    for j in range(lengthOfNodes):
      if (blist[i] == allbssidlist[j]):  # blist1 데이터가 전체 와이파이 노드중 어디에 매칭되냐 / j 는 노드의 인덱스
        tempnodelist.append(j)
        break
      if(j == lengthOfNodes-1):  # 새로운 데이터 올 때만 작동  / 매칭이 안된 것
        tempnodelist.append(-1)
  tempplist = [0 for j in range(lengthOfNodes)]
  for i in range(len(blist)):
    if(tempnodelist[i] != -1):
      tempplist[int(tempnodelist[i])] = rlist[i]
    else:
      tempplist[i] = 0
  return tempplist


def predictEntrace(testbssidlist, testrssilist, allbssidlist, the_model):
  lengthOfNodes = len(allbssidlist)
  mappedlist = convert(testbssidlist, testrssilist,
                       allbssidlist, lengthOfNodes)
  mappedlist = list(map(int, mappedlist))
  mappedlist = list(map(abs, mappedlist))
  finallistsample = np.array(mappedlist)
  finallistsample = finallistsample.reshape(
      1, lengthOfNodes).astype('float32')/100
  rawPrediction = the_model.predict(finallistsample)
  Entrance = rawPrediction.argmax() + 1
  return Entrance


def runNNmodel(testbssidlist, testrssilist):
    the_model = load_model("best_model.h5")
    print(the_model.summary())

    with open('allbssidlist.txt', 'r') as f:
        allbssidlist = json.loads(f.read())
        ans = predictEntrace(testbssidlist, testrssilist, allbssidlist, the_model)
        print("Model ans:", ans)
        return ans

testbssidlist = ["00:23:aa:02:31:b0",	"0a:23:aa:02:31:b2",	"0a:23:aa:02:31:b3",	"06:23:aa:02:31:a2",	"06:23:aa:02:31:a3",	"00:23:aa:02:31:a0",	"06:08:52:7c:d1:02", "06:08:52:7c:d1:03",	"0a:09:b4:76:0f:13",	"06:09:b4:76:0f:13"]

testrssilist = [-45,	-45,	-46,	-48,	-48,	-49,	-51,	-51,	-52,	-52]

print(runNNmodel(testbssidlist, testrssilist))