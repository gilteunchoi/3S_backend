from tensorflow.keras.models import Sequential, load_model
import numpy as np


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


def predictEntrace(testbssidlist, testrssilist, allbssidlist, model):
  lengthOfNodes = len(allbssidlist)
  mappedlist = convert(testbssidlist, testrssilist,
                       allbssidlist, lengthOfNodes)
  mappedlist = list(map(int, mappedlist))
  mappedlist = list(map(abs, mappedlist))
  finallistsample = np.array(mappedlist)
  finallistsample = finallistsample.reshape(
      1, lengthOfNodes).astype('float32')/100
  rawPrediction = model.predict(finallistsample)
  Entrance = rawPrediction.argmax() + 1
  return Entrance


def runNNmodel(testbssidlist, testrssilist):
    model = load_model("best_model.h5")
    print(model.summary())

    with open('allbssidlist.txt', 'r') as f:
        allbssidlist = f.read()
        print(allbssidlist)
        return predictEntrace(testbssidlist, testrssilist, allbssidlist, model)

