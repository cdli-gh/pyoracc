import re

class ContentExtracter(object):
    def __init__(self):
        self.tokenList = list()
        self.signList = list()

    def InsertTokenMy(self, line, p):
        # print(4)
        tempToken = p.findall(line)
        if tempToken:
            
            for tokens in tempToken[0].split():
                tempList = self.CleanToken(tokens)
                if tempList:
                    self.tokenList.append(tempList)

    def CheckFrequency(self):
        for tokens in self.tokenList:
            self.GenerateSign(tokens)

    def CleanToken(self, token):
        symbols = ['<','>','#','!','?','[',']','_']
        for symbol in symbols:
            if symbol in token:
                token = token.replace(symbol,'')
        if "{+" in token:
            if token.find("+") != 1:
                temp = token[:token.find("{+")]
                self.tokenList.append(temp)
            temp = token[token.find("{+")+1:token.find("}")]
            self.tokenList.append(temp)
            if token.find("}") != len(token)-1:
                temp = token[token.find("}")+1:]
                self.tokenList.append(temp)
            return None
        return token

    def GenerateSign(self, word):
        temp = word.split('-')
        finalTemp = list()
        finalSignList = list()
        for splitWords in temp:
            iterItem = splitWords.split(':')
            for signs in iterItem:
                finalTemp.append(signs)
        for element in finalTemp:
            if '{' in element and '}' in element:
                if element.rfind('{') == 0:
                    finalSignList.append(element[element.rfind('{')+1:element.rfind('}')])
                    finalSignList.append(element[element.rfind('}')+1:])
                else:
                    finalSignList.append(element[:element.rfind('{')])
                    finalSignList.append(element[element.rfind('{')+1:element.rfind('}')])
            else:
                finalSignList.append(element)
        detected = False
        temp = ""

        if "(" in word and ")" in word and len(finalSignList) == 1:
            self.signList.append(finalSignList[0])
        if "(" in word and ")" in word:
            for signs in finalSignList:
                if "(" in signs:
                    temp += signs
                    detected = True
                elif detected and not ")" in signs:
                    temp += "-"+signs
                elif ")" in signs and detected:
                    temp += signs
                    detected = False
                    self.signList.append(temp)
                    temp = ""
                else:
                    self.signList.append(signs)
        else:
            for signs in finalSignList:
                self.signList.append(signs)

    def CreateTokens(self,segtment_input):
        p = re.compile("[0-9]+\'?. (.*)")
        self.tokenList = list()
        self.signList = list()
        for line in segtment_input:
            # print(line)
            if len(line)<=0:
                # print(1)
                continue
            if line[0].isdigit():
                # print(2)
                self.InsertTokenMy(re.sub("($(.)*$)","",line), p)
                if "$)" in line and "($" in line:
                    # print(3)
                    # print(line[line.find('$)')])
                    tmp_len = line.find('$)')+2
                    if len(line) >tmp_len:
                        self.InsertTokenMy(line[tmp_len], p)
                else:
                    self.InsertTokenMy(line, p)
        
        self.CheckFrequency()
        self.tokenList = list(set(self.tokenList))
        self.signList = list(set(self.signList))
        # print(self.tokenList)
        # print(self.signList)


    def ReturnTokens(self):
        # print(self.tokenList)
        # print(self.signList)
        return self.tokenList, self.signList

# if __name__ == "__main__":
#     objExtract = ContentExtracter()
#     segtment_input = []
#     with open('./Database/test1.atf') as fileHandle:
#         for line in fileHandle:
#             segtment_input.append(line)
#     objExtract.CreateTokens(segtment_input)
#     tokens,signs=objExtract.ReturnTokens()
#     print(tokens)
#     print(signs)