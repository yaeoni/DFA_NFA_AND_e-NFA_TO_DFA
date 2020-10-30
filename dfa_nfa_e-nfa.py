
#ABOUT DFA
# load, accept
class DFA:
    def __init__(self):
        print("DFA 입니다.")
        print("table을 보고 싶으시면 loadDFA함수를, 문자열 accept여부를 확인하고 싶으시면 accept 함수를 실행시켜 주세요 ! ")

    state = ["A", "B", "C"]
    symbol = ["0", "1"]

    table = {"A":{'0':"A", '1':"B"},
        "B":{'0':"C", '1':"A"},
        "C":{'0':"B", '1':"C"}}
    
    startState = ["A"]
    finalState = ["A"]

    def loadDFA(self):
        print("DFA Transition Table")
        print("---------------------------")
        print("        0           1    ") 
        print("---------------------------")
        #print(self.table["A"])
        for state in self.state:
            print(state, " |   " , end= "")
            for symbol in self.symbol:
                print(''.join(self.table[state][symbol]), "           ", end = "")
            print("", end="\n")
        print("---------------------------")

    def accept(self):
        w = input("string을 입력 해주세요 : ")
        states = self.startState
        final = self.finalState
        
        for char in w:
            temp = []
            for state in states:
                temp += self.table[state][char]
        
        states = temp
        
        if(states == final):
            print("accept")
            return
        else:
            print("reject")
            return
 
"""
# DFA 사용 예시
a = DFA()
a.loadDFA()
a.accept()
"""

#ABOUT NFA
# load, accept
class NFA:
    def __init__(self):
        print("NFA 입니다.")
        print("table을 보고 싶으시면 loadNFA함수를, 문자열 accept여부를 확인하고 싶으시면 accept 함수를 실행시켜 주세요 ! ")

    state = ["A", "B", "C", "D"]
    symbol = ["0", "1"]

    table = {"A": {"0":["A","B"], "1":["A","C"]},
            "B":{"0":["D"],"1":["*"]},
            "C":{"0":["*"],"1":["D"]},
            "D":{"0":["D"], "1":["D"]}}

    startState = ["A"]
    finalState = ["D"]
    
    def loadNFA(self):
        print("NFA Transition Table")
        print("---------------------------")
        print("        0           1    ") 
        print("---------------------------")
        #print(self.table["A"])
        for state in self.state:
            print(state, " |   " , end= "")
            for symbol in self.symbol:
                print(''.join(self.table[state][symbol]), "       ", end = "")
            print("", end="\n")
        print("---------------------------")

    def accept(self):
        w = input("string을 입력 해주세요 : ")
        states = self.startState
        for char in w:
            temp = []
            for state in states:
                temp += self.table[state][char]
            states = temp

        for final in self.finalState:
            if(final in states):
                print("accept")
                return
        print("reject")
        return

"""
# NFA 사용 예시
a = NFA()
a.loadNFA()
a.accept()
"""

#ABOUT e-NFA
# load, e-NFA to DFA
class eNFA:
    def __init__(self):
        print("e-NFA 입니다.")
        print("table을 보고 싶으시면 loadNFA함수를, DFA로 변환하고 싶으시다면 toDFA함수를 실행시켜 주세요! ")

    table = { "A" : {"0" :["E"], "1" :["B"], "eps" : ["*"]}, 
        "B": {"0":["*"], "1":["C"], "eps":["D"]}, 
        "C": {"0":["*"], "1":["D"], "eps":["*"]},
        "D": {"0":["*"], "1":["*"], "eps":["*"]},
        "E": {"0":["F"], "1":["*"], "eps":["B", "C"]},
        "F": {"0":["D"], "1":["*"], "eps":["*"]}}
    
    startState = ["A"]
    finalState = ["D"]
    state = ["A", "B", "C", "D", "E", "F"]
    symbols = ["0", "1", "eps"]

    def loadeNFA(self):
        print("e-NFA Transition Table\n")
        print("------------------------------------")
        print("        0           1         eps") 
        print("------------------------------------")
        for state in self.state:
            print(state, " |   " , end= "")
            for symbol in self.symbols:
                print(''.join(self.table[state][symbol]), "          ", end = "")
            print("", end="\n")
        print("------------------------------------\n")

    def loadDFA(self, table):

        symbols = [0,1]

        print("After the subset construction\n")
        
        for item in table:
            for symbol in symbols:
                if(table[item].get(symbol)):
                    print("(",item, ",", symbol, ") = ", "{", " ".join(table[item][symbol]), "}")
            
        
        

    def getEachClosure(self):
        temp={}
        cl_table ={}
        for key, value in self.table.items():
            temp[key] = [key]+value['eps']
        #print(temp)

        for val in temp.values():
            cl_temp= []
            key = val[0]
            cl_temp.extend(temp[key])
            for char in val :
                if(char !="*"):
                    cl_temp.extend(temp[char])
            cl_table[key] = sorted(list(set(cl_temp)))
            if "*" in cl_table[key]:
                        cl_table[key].remove("*")
        return cl_table


    def getClosure(self, input):
        closure = self.getEachClosure()
        cl = []
        for char in input:
            cl.extend(closure[char])
        if "*" in cl:
                cl.remove("*")
        return cl
    

    def toDFA(self):
        start = self.startState
        final = self.finalState
        finalDfa = {}
        states =[]
        symbol = ["0", "1"]
        inputCl = [self.getClosure(start)]
        while(inputCl):
            for temp in inputCl:
                while temp not in states and temp != final:
                    states.append(temp)

                    newTransition = {}

                    for i in range (0,2):
                            # new state = 이놈들이 0과 1을 보고 갈 수 있는 state 
                            newState = []
                            tempTransition ={}
                            for char in temp:
                                newState.extend(self.table[char][str(i)])
                            newState = sorted(list(set(newState)))
                            
                            # *은 삭제
                            while "*" in newState:
                                newState.remove("*")
                            newInput = self.getClosure(newState)
                        
                            if (newInput != []):
                                inputCl.append(newInput)
                                tempTransition[i] = newInput
                                newTransition.update(tempTransition)
                                
                            
                    finalDfa[''.join(temp)] = newTransition

                            
                inputCl.remove(temp)
        self.loadDFA(finalDfa)
        #return finalDfa

"""
# e-NFA 사용 예시
a = eNFA()
a.loadeNFA()
a.toDFA()
"""