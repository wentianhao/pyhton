# encdoing:utf-8
import matplotlib.pyplot as plt

# 获取叶子节点
def getNumLeafs(intree):
    numLeafs = 0
    a = intree.keys()
    firstStr = [each for each in a]
    secondDict = intree[firstStr[0]]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

# 获取树的层数
def getTreeDepth(intree):
    maxDepth,thisDepth = 0,0
    a = intree.keys()
    firstStr = [each for each in a][0]
    secondDict = intree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getNumLeafs(secondDict[key])
        else:
            thisDepth = 1
        thisDepth = thisDepth
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

# 生成符合树结构的dict
def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},{'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}]
    return listOfTrees[i]

# 在父子节点间填充文本信息
def plotMidText(cntrpt,parentPt,txtString):
    xmid = (parentPt[0] - cntrpt[0])/2.0 + cntrpt[0]
    ymid = (parentPt[1] - cntrpt[1])/2.0 + cntrpt[1]
    creatPlot_ax1.text(xmid,ymid,txtString)

# 绘制树结构函数
def plotTree(intree,parentPt,nodeTxt,plotTree_yOff = 1.0):
    plotTree_totalW = float(getNumLeafs(intree))
    plotTree_totalD = float(getTreeDepth(intree))
    plotTree_xOff = -0.5 / plotTree_totalW
    numLeafs = getNumLeafs(intree)
    depth = getTreeDepth(intree)
    a = intree.keys()
    firstStr = [each for each in a][0]
    cntrPt = (plotTree_xOff + (1.0 + float(numLeafs))/2.0/plotTree_totalW,plotTree_yOff)
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict = intree[firstStr]
    plotTree_yOff = plotTree_yOff - 1.0/plotTree_totalW
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key),plotTree_yOff)
        else:
            plotTree_xOff = plotTree_xOff + 1.0/plotTree_totalW
            plotNode(secondDict[key],(plotTree_xOff,plotTree_yOff),cntrPt,leafNode)
            plotMidText((plotTree_xOff,plotTree_yOff),cntrPt,str(key))
    plotTree_yOff = plotTree_yOff + 1.0/plotTree_totalD

# 绘图
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    creatPlot_ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,textcoords='axes fraction',va='center',ha='center',bbox=dict(boxstyle='round4'),arrowprops = dict(arrowstyle = '<-'))

if __name__=='__main__':
    # 定义文本框
    decisionNode = dict(boxstyple='swatooth',fc='0.8')
    leafNode = dict(boxstyle='round4',fc=0.8)
    mytree = retrieveTree(1) # 取出符合决策树结构的数据，可自定义
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    creatPlot_ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree_yOff = 1.0 # 设置默认参数
    plotTree(mytree, (0.5, 1.0), '') # 调用绘制树结构图函数
    plt.show() # 图片展示
