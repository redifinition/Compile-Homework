# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 00:32:19 2021

@author: 1851055 汪明杰
"""

import copy

from bottomTopAlgorithm.GrammarManager import GrammarManager
from graphviz import Digraph
import uuid


class LR0:
    def __init__(self):
        self.grammarManager = GrammarManager()
        # self.grammarManager.getInput()

        # 状态转移矩阵
        self.translationArray = dict()

    def setGrammar(self, sentences):
        self.grammarManager.getStr(sentences)

    def getClosure(self, initialRelation):
        """
        计算initialRelation的闭包
        """
        result = [initialRelation]

        # 闭包中的数量是否增加
        newAppear = True
        while newAppear:
            newAppear = False
            for res in result:
                # 获取.右边的符号
                if res[2] >= len(res[1]):
                    continue

                rightSymbol = res[1][res[2]]
                # 查看该符号是否出现在sentences中
                for i in range(len(self.grammarManager.sentences)):
                    if self.grammarManager.sentences[i][0] == rightSymbol:
                        # 查看result中是否已经有该符号
                        hasSymbol = False
                        for j in result:
                            if j[0] == self.grammarManager.sentences[i][0] and \
                                    j[1] == self.grammarManager.sentences[i][1] and \
                                    j[2] == 0:
                                hasSymbol = True
                                break

                        # 如果该结果还没有出现在闭包中，则加入
                        if not hasSymbol:
                            result.append([self.grammarManager.sentences[i][0], \
                                           self.grammarManager.sentences[i][1], 0])
                            newAppear = True
        return result

    def getGoIX(self, I, X):
        """
        在状态I下接受符号X，所产生的[[]]
        """
        result = []
        for i in I:
            if i[2] >= len(i[1]):
                continue
            # 下一个字符
            if i[1][i[2]] == X:
                if not [i[0], i[1], i[2] + 1] in result:
                    result.append([i[0], i[1], i[2] + 1])
        # 对result中每一个表达式计算闭包
        newResult = result
        for i in result:
            tempResults = self.getClosure(i)
            # 对于tempResults中的每一个元素
            for j in tempResults:
                if not j in result:
                    newResult.append(j)
        return newResult

    def calculateDFA(self):
        """
        计算DFA
        一个 LR0 DFA 当中的产生式状态是一个三元组，分别表示以下含义：
        1. 产生式左部
        2. 产生式右部
        3. 当前接受位置
        Example: E->a·B 对应的三元组为["E","aB",1]
        """
        # 每一个状态闭包，应当是一个集合
        initialRelation = [self.grammarManager.sentences[0][0], \
                           self.grammarManager.sentences[0][1], 0]
        initialState = self.getClosure(initialRelation)

        self.states = [initialState]

        # 从initialState开始扩展
        hasGrown = True
        while hasGrown:
            hasGrown = False
            newStates = copy.deepcopy(self.states)

            for i, item in enumerate(self.states):

                # 遍历终结符
                for j in self.grammarManager.VT:

                    newState = self.getGoIX(item, j)

                    # 为空，则表示不可以接受该符号
                    if newState == []:
                        continue

                    # 判断新状态是否已经存在
                    if newState in newStates:
                        # 获取newState下标
                        newStateIndex = newStates.index(newState)

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = newStateIndex
                    else:
                        # 加入新状态
                        newStates.append(newState)
                        hasGrown = True

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = len(newStates) - 1

                # 遍历非终结符
                for j in self.grammarManager.VN:

                    newState = self.getGoIX(item, j)

                    # 为空，则表示不可以接受该符号
                    if newState == []:
                        continue

                    # 判断新状态是否已经存在
                    if newState in newStates:
                        # 获取newState下标
                        newStateIndex = newStates.index(newState)

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = newStateIndex
                    else:
                        # 加入新状态
                        newStates.append(newState)
                        hasGrown = True

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = len(newStates) - 1

            self.states = newStates

    def getStateStr(self,index):
        showLabel = ""
        item=self.states[index]
        for j,jtem in enumerate(item):
            if j!=0:
                showLabel += "\n"
            showLabel += jtem[0] + "->"
            for t in range(len(jtem[1])):
                if t == jtem[2]:
                    showLabel += "·"
                showLabel += jtem[1][t]
            if jtem[2] >= len(jtem[1]):
                showLabel += "·"
            
        return showLabel


    def getImage(self):
        """
        绘图
        """
        if len(self.translationArray) == 0:
            self.calculateDFA()

        imgUrl = '基于 LR(0)项目的 DFA图' + str(uuid.uuid1())

        g = Digraph(imgUrl, format="png")

        # 添加结点
        for index, item in enumerate(self.states):
            showLabel = ""
            # str(index)+"     "
            for j in item:
                showLabel += j[0] + "->"
                for t in range(len(j[1])):
                    if t == j[2]:
                        showLabel += "·"
                    showLabel += j[1][t]
                if j[2] >= len(j[1]):
                    showLabel += "·"
                showLabel += "\l"
            g.node(name=str(index), label=showLabel, xlabel=str(index), shape="box")

        # 添加边
        for i in self.translationArray:
            g.edge(str(i[0]), str(self.translationArray[(i[0], i[1])]), label=str(i[1]))

        return imgUrl, g


class LR1:
    def __init__(self):
        self.grammarManager = GrammarManager()
        # self.grammarManager.getInput()

    def setGrammar(self, sentences):
        self.grammarManager.getStr(sentences)

    def getClosure(self, initialRelation):
        """
        计算initialRelation的闭包
        """

        result = [initialRelation]

        # 闭包中的数量是否增加
        newAppear = True
        while newAppear:
            newAppear = False

            for res in result:
                # 获取.右边的符号
                if res[2] >= len(res[1]):
                    continue
                rightSymbol = res[1][res[2]]

                # 查看是否有该产生式 rightSymbol-> xxx
                for i in range(len(self.grammarManager.sentences)):
                    if self.grammarManager.sentences[i][0] == rightSymbol:
                        # rightSymbol-> self.grammarManager.sentences[i][1]
                        # 接下来是确定 First(beta a),其中beta为再下一个字符
                        initialFirst = ""
                        if res[2] + 1 < len(res[1]):
                            initialFirst += res[1][res[2] + 1]
                        initialFirst += res[3]  # res[3]为预测符
                        # print("initialFirst为", initialFirst)
                        # 计算First(initialFirst)
                        firstResultSet = self.grammarManager.getFirstSet(initialFirst)

                        # print("firstResultSet为", firstResultSet)

                        # firstSet中的终结符
                        for vt in firstResultSet:
                            # 如果不是终结符或者#，则不考虑
                            if not (vt in self.grammarManager.VT or vt == '#'):
                                continue

                            # 是终结符，则查看该结果是否已经出现过
                            newRes = [rightSymbol, self.grammarManager.sentences[i][1], 0, vt]

                            if not newRes in result:
                                result.append(newRes)
                                newAppear = True
        return result

    def getGoIX(self, I, X):
        """
        计算Go(I,X):即在状态I下接受输入X
        """
        result = []
        for i in I:
            if i[2] >= len(i[1]):
                continue
            # 下一个字符
            if i[1][i[2]] == X:
                if not [i[0], i[1], i[2] + 1, i[3]] in result:
                    state_item = [i[0], i[1], i[2] + 1, i[3]]
                    if state_item[2] == len(state_item[1]):
                        # 如果是规约项的话，就增加第五个元素表示规约项
                        state_item.append(self.grammarManager.get_number_of_sentence(state_item))
                    result.append(state_item)
        # 对result中每一个表达式计算闭包
        newResult = result
        for i in result:
            tempResults = self.getClosure(i)
            # 对于tempResults中的每一个元素
            for j in tempResults:
                if not j in result:
                    newResult.append(j)
        return newResult

    '''
    一个 LR1 DFA 当中的产生式状态是一个四元组，分别表示以下含义：
    1. 产生式左部
    2. 产生式右部
    3. 当前接受位置
    4. 当前状态式接受字符
    5. 可能有的项，表示规约产生式的编号
    Example: E->a·B, # 对应的四元组为["E","aB",1,'#']
    备注：为了方便使用，在这里一个四元组的展望符只能是一个字符
    因此， E->a·B, #|a 被存为两个四元组：["E","aB",1,'#']和["E","aB",1,'a']
    如果这个状态项将要被规约，则是一个五元组：["E","aB",1,'#',1] 最后一个数字表示规约的产生式的编号
    '''

    def calculateDFA(self):
        """
        计算DFA
        """
        # 每一个状态闭包，应当是一个集合
        initialRelation = [self.grammarManager.sentences[0][0],
                           self.grammarManager.sentences[0][1], 0, '#']
        initialState = self.getClosure(initialRelation)

        self.states = [initialState]
        # 状态转移矩阵
        self.translationArray = dict()

        # 从initialState开始扩展
        hasGrown = True
        while hasGrown:
            hasGrown = False
            newStates = copy.deepcopy(self.states)

            for i, item in enumerate(self.states):

                # 遍历终结符
                for j in self.grammarManager.VT:

                    newState = self.getGoIX(item, j)

                    # 为空，则表示不可以接受该符号
                    if newState == []:
                        continue

                    # 判断新状态是否已经存在
                    if newState in newStates:
                        # 获取newState下标
                        newStateIndex = newStates.index(newState)

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = newStateIndex
                    else:
                        # 加入新状态
                        newStates.append(newState)
                        hasGrown = True

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = len(newStates) - 1

                # 遍历非终结符
                for j in self.grammarManager.VN:

                    newState = self.getGoIX(item, j)

                    # 为空，则表示不可以接受该符号
                    if newState == []:
                        continue

                    # 判断新状态是否已经存在
                    if newState in newStates:
                        # 获取newState下标
                        newStateIndex = newStates.index(newState)

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = newStateIndex
                    else:
                        # 加入新状态
                        newStates.append(newState)
                        hasGrown = True

                        # 填充状态转移矩阵
                        self.translationArray[(i, j)] = len(newStates) - 1

            self.states = newStates

    def get_merged_looking_forward_string(self):
        """
        通过这个函数将LR1状态转移矩阵的展望符合并。合并后的 state 四元组：
        [左部, 右部, 当前位置, [展望符列表]]
        :return: 一个合并过的状态 DFA
        """
        # print(self.states)
        new_states = []
        for index, item in enumerate(self.states):
            new_item = []
            cur_item = copy.deepcopy(item)
            item = copy.deepcopy(item)
            while len(item) > 0:
                result = []
                basic_line = [item[0][0], item[0][1], item[0][2]]
                # 有可能是规约项，有第五个元素
                if len(item[0]) > 4:
                    basic_line.append(item[0][4])
                for i in cur_item:
                    if i[0] == basic_line[0] and i[1] == basic_line[1] and i[2] == basic_line[2]:
                        # 将item.index(i)移除
                        result.append(i[3])
                        # 有可能是规约项，有第五个元素
                        if len(i) > 4:
                            basic_line.append(i[4])
                        item.remove(i)

                # 排序，按照字母顺序输出，这样好看
                result.sort()

                # 将item整理成一个数组
                looking_forwards = []
                for kindex, kitem in enumerate(result):
                    looking_forwards.append(kitem)
                state_item = [basic_line[0], basic_line[1], basic_line[2], looking_forwards]
                if len(basic_line) > 3:
                    state_item.append(basic_line[3])
                new_item.append(state_item)
            new_states.append(new_item)
        # print(new_states)
        # self.states = new_states
        # 这里可以选直接覆盖原来的 states 或者返回一个处理好的 states，看需求吧
        return new_states

    def get_numbered_and_looking_forward_transfer_array(self):
        """
        在 state transfer array 里添加规约项标号和展望符，满足 3.7，3.8 的输入格式
        :return: 新的状态转移矩阵
        """
        new_transfer_array = copy.deepcopy(self.translationArray)
        merged_states = self.get_merged_looking_forward_string()
        for index, state in enumerate(merged_states):
            for state_item in state:
                if len(state_item) > 4:
                    new_transfer_array[(index, "no")] = state_item[4]
                    new_transfer_array[(index, "lft")] = state_item[3]

        return new_transfer_array

    def getStateStr(self,index):
        item=self.states[index]
        # 对item合并状态
        newItem = []
        curItem = copy.deepcopy(item)
        item = copy.deepcopy(item)
        while len(item) > 0:
            result = []
            basicLine = [item[0][0], item[0][1], item[0][2]]
            for i in curItem:
                if i[0] == basicLine[0] and i[1] == basicLine[1] and i[2] == basicLine[2]:
                    # 将item.index(i)移除
                    result.append(i[3])
                    item.remove(i)

            # 排序，按照字母顺序输出，这样好看
            result.sort()

            # 将item整理成一个字符串
            preStr = ""
            for kindex, kitem in enumerate(result):
                if kindex != 0:
                    preStr += "|"
                preStr += kitem
            
            newItem.append([basicLine[0], basicLine[1], basicLine[2], preStr])

        showLabel = ""
        # str(index)+"     "
        for jndex,j in enumerate(newItem):

            if jndex!=0:
                showLabel += "\n"

            showLabel += j[0] + "->"
            for t in range(len(j[1])):
                if t == j[2]:
                    showLabel += "·"
                showLabel += j[1][t]
            if j[2] >= len(j[1]):
                showLabel += "·"

            showLabel += "," + j[3]

            
        
        return showLabel

    def getImage(self):
        """
        绘图
        """
        if len(self.translationArray) == 0:
            self.calculateDFA()

        imgUrl = '基于 LR(1)项目的 DFA图' + str(uuid.uuid1())

        g = Digraph(imgUrl, format="png")

        # 添加结点
        for index, item in enumerate(self.states):

            # 对item合并状态
            newItem = []
            curItem = copy.deepcopy(item)
            item = copy.deepcopy(item)
            while len(item) > 0:
                result = []
                # print("itemwei",item[0][0],item[0][1],item[0][2])
                basicLine = [item[0][0], item[0][1], item[0][2]]
                for i in curItem:
                    if i[0] == basicLine[0] and i[1] == basicLine[1] and i[2] == basicLine[2]:
                        # 将item.index(i)移除
                        result.append(i[3])
                        item.remove(i)

                # 排序，按照字母顺序输出，这样好看
                result.sort()

                # 将item整理成一个字符串
                preStr = ""
                for kindex, kitem in enumerate(result):
                    if kindex != 0:
                        preStr += "|"
                    preStr += kitem
                newItem.append([basicLine[0], basicLine[1], basicLine[2], preStr])

            showLabel = ""
            # str(index)+"     "
            for j in newItem:
                showLabel += j[0] + "->"
                for t in range(len(j[1])):
                    if t == j[2]:
                        showLabel += "·"
                    showLabel += j[1][t]
                if j[2] >= len(j[1]):
                    showLabel += "·"

                showLabel += "," + j[3]

                showLabel += "\l"
            g.node(name=str(index), label=showLabel, xlabel=str(index), shape="box")

        # 添加边
        for i in self.translationArray:
            g.edge(str(i[0]), str(self.translationArray[(i[0], i[1])]), label=str(i[1]))

        return imgUrl, g


if __name__ == '__main__':
    """
    测试：
4
S'->S
S->BB
B->aB
B->b

3
E'->E
E->(E)
E->i
    """
    # lr0 = LR1()
    # lr0.calculateDFA()
    # lr0.getImage()
    # print(lr0.translationArray)
    # print(lr0.states)
    lr1 = LR0()
    lr1.grammarManager.getInput()
    lr1.calculateDFA()
    lr1.getImage()
# =============================================================================
#     print(lr1.states)
#     print(lr1.get_merged_looking_forward_string())
#     print(lr1.get_numbered_and_looking_forward_transfer_array())
#     print(lr1.translationArray)
# =============================================================================
    print(lr1.states)
    print(len(lr1.states))
    print(lr1.translationArray)
    print(lr1.getGoIX(0,'('))