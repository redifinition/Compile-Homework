# -*- coding: utf-8 -*-
"""
LR(0)

@author: leoy
"""

from bottomTopAlgorithm.LRk_state_transfer_generation  import LR0

class LR0Table:
    
    def __init__(self,sentences):
        
        self.lr0 = LR0()
        self.lr0.setGrammar(sentences)
        self.lr0.calculateDFA()
        self.action = [[["",-1] for i in range(len(self.lr0.grammarManager.VT) + 1)] for j in range(len(self.lr0.states))]
        self.goto = [[-1 for i in range(len(self.lr0.grammarManager.VN) - 1)] for j in range(len(self.lr0.states))]
        
        self.getTranslationArrayWithNumber()
        self.get_LR0_analysis_table()
        
    
    def get_VN_index_for_goto(self,c):
        '''
        获得非终结符在VN的位置，要去掉起始符
        '''
        startIndex = -1
        for index in range(len(self.lr0.grammarManager.VN)):
            if "'" in self.lr0.grammarManager.VN[index]:
                startIndex = index
                break
        
        if c in self.lr0.grammarManager.VN:
            idx = self.lr0.grammarManager.VN.index(c)
            if idx > startIndex:
                idx = idx - 1
        return idx
    
    def getTranslationArrayWithNumber(self):
        
        '''
        通过DFA获得带有状态所含规约项目产生式编号的状态矩阵
        '''
        #想法是当前位置到右边待规约语句的最后时，表示可以规约
        
        self.reducibleProduction = {}
        
        for index, state in enumerate(self.lr0.states):
            for i in range(len(state)):                
                curState = state[i]
                if len(curState[1]) == curState[2]:
                    self.reducibleProduction[index] = self.lr0.grammarManager.get_number_of_sentence([curState[0],curState[1]])
    
    def get_LR0_analysis_table(self):
        """
        获得LR0分析表
        
        Returns
        -------
        填充self.action与self.goto

        """
        
        for index, state in enumerate(self.lr0.states):
            for i in range(len(state)):
                curState = state[i]
                
                if curState[2] < len(curState[1]) and self.lr0.grammarManager.isVT(curState[1][curState[2]]):
                    self.action[index][self.lr0.grammarManager.VT.index(curState[1][curState[2]])] = ["s",self.lr0.translationArray.get((index,curState[1][curState[2]]))]
                elif "'" in curState[0] and curState[2] == len(curState[1]):
                    self.action[index][-1] =["acc",-1]
                elif curState[2] == len(curState[1]):
                    for j in range(len(self.action[0])):
                        self.action[index][j] = ["r",self.reducibleProduction.get(index)]

            
        for key in self.lr0.translationArray.keys():
            if key[1] in self.lr0.grammarManager.VN:
                self.goto[key[0]][self.get_VN_index_for_goto(key[1])] = self.lr0.translationArray.get(key)
        
    
    def getVisibleLR0Table(self):
        
        strLine_VT = []
        strLine_VN = []
        strLine_VT.append(" ")
        strLine_VN.append(" ")
        for c in self.lr0.grammarManager.VT:
            strLine_VT.append(c)
        strLine_VT.append("#")
        
        for n in self.lr0.grammarManager.VN:
            if "'" not in n:
                strLine_VN.append(n)
        
        strLines_VT = []
        strLines_VT.append(strLine_VT)
        strLines_VN = []
        strLines_VN.append(strLine_VN)
        
        for index,act in enumerate(self.action):
            strLine_VT = []
            strLine_VN = []
            strLine_VT.append(str(index))
            strLine_VN.append(str(index))

            for i,item in enumerate(act):
                if item[0] == 'acc':
                    strLine_VT.append(item[0])
                elif item[0] != "":
                    strLine_VT.append(item[0]+str(item[1]))
                else:
                    strLine_VT.append(" ")
            for it in self.goto[index]:

                if it != -1:
                    strLine_VN.append(str(it))
                else:
                    strLine_VN.append(" ")
            
            strLines_VT.append(strLine_VT)
            strLines_VN.append(strLine_VN)
            
        self.visibleTable_VT = strLines_VT
        self.visibleTable_VN = strLines_VN
    
    def showVisibleLR0Table(self):
        print("action Table:")
        for item in self.visibleTable_VT:
            for char in item:
                print("%3s"%(char),end=" ")
            print("\n")
        print("goto Table:")
        for item in self.visibleTable_VN:
            for char in item:
                print("%3s"%(char),end=" ")
            print("\n")

            
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
if __name__ == "__main__":
    sentences = ["S->E", "E->E+T", "E->T", "T->T*F", "T->F", "F->(E)", "F->i"]
    table = LR0Table(sentences)
    table.getVisibleLR0Table()
    table.showVisibleLR0Table()          
