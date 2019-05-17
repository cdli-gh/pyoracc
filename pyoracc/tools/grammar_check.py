from pyoracc.tools.errors_template import ErrorsTemplate

et=ErrorsTemplate()

class GrammarCheck(object):
    def __init__(self,orig_input):
        self.errors = [] #error list [error_id:int, line:intlist, colmun:intlist, tocken:str]
        self.errors_yacc = [] #errors list wait to be checked

        self.orig_input = orig_input

        self.ids = [] # id lines, e.g. &P123456 = AB 78, 910
        self.lans = [] # language lines, e.g. #atf: lang akk 
        self.objs = [] # objects lines, e.g. @tablet
        self.surfaces = [] # surfarces lines, e.g. @column 2
        self.trans = [] # transliterration lines, e.g. 1. dub-sar
        self.dollars = [] # $ comment lines, e.g. $ blank space 


    def print_test(self):
        self.structure_check()
        print('----(GrammarCheck----')
        print(self.ids)
        print(self.lans)
        print(self.objs)
        print(self.surfaces)
        print(self.trans)
        print(self.dollars)
        for i in self.errors:
            print(et.error2str(i[0],0,i[1],i[2],i[3]))
        for i in self.errors_yacc:
            print(et.error2str(i[0],0,i[1],i[2],i[3]))
        # print(self.orig_input.split('\n'))
        print('----GrammarCheck)----')


    def add_id(self,idn):
        '''
        :params id: int, the line number in segmented file
        :return: N/A

        add line number of atf id line (e.g. &P010032 = CT 50, 019) to the self.ids
        '''
        self.ids.append(idn)

    def add_lan(self,lan):
        '''
        :params lan: int, the line number in segmented file
        :return: N/A

        add line number of language protocal line (e.g. #atf: lang akk) to the self.lans
        '''
        self.lans.append(lan)

    def add_objs(self,obj):
        '''
        :params obj: int, the line number in segmented file
        :return: N/A

        add line number of object type line (e.g. @tablet) to the self.objs
        '''
        self.objs.append(obj)

    def add_surfaces(self,surface):
        '''
        :params surface: int, the line number in segmented file
        :return: N/A

        add line number of surface line (e.g. @reverse) to the self.surfaces
        '''
        self.surfaces.append(surface)

    def add_trans(self,tran_id,tran_line):
        '''
        :params tran_id: str, transliterration id
        :params tran_line: int, the line number in segmented file
        :return: N/A

        add id and line number of transliterration line (e.g. 4. szu nam-ti-la-ni) to the self.trans as a tuple (tran_id,tran_line)
        '''
        self.trans.append((tran_id,tran_line))

    def add_dollars(self,dollar):
        '''
        :params dollar: int, the line number in segmented file
        :return: N/A

        add line number of dollar comments line (e.g. $ blank space) to the self.dollars
        '''
        self.dollars.append(dollar)

    def add_yacc_error(self,token,line,offset):
        '''
        :params token: str, the error token 
        :params line: int, the line (p.lineno) of the error point in segmented file
        :params offset: int, the offset (p.lexpos) of the error point in segmented file
        :return: N/A

        find the column no. of the yacc error token by using offset no., and put it into self.errors_yacc
        yacc default error No. is -1 
        '''
        column=self.find_column(offset)
        self.errors_yacc.append([-1,[line],[column],token])


    def add_lex_error(self,char,line,offset):
        '''
        :params char: str, the error character 
        :params line: int, the line (p.lineno) of the error point in segmented file
        :params offset: int, the offset (p.lexpos) of the error point in segmented file
        :return: N/A

        find the column no. of the lex error character by using offset no., and put it into self.errors
        yacc default error No. is -1 
        '''
        column=self.find_column(offset)
        self.errors.append([-2,[line],[column],char])

    def find_column(self, offset):
        line_start = self.orig_input.rfind('\n', 0, offset) + 1
        return (offset - line_start) + 1

    def nested_bracket_check(self,line):
        stack=[]
        l_brackets={'{','(','<'}
        r_brackets={'>',')','}'}
        for i in line:
            if (i in l_brackets) and len(set(stack).intersection(l_brackets))>0:
                return True
            if (len(stack)>0):
                if (i in r_brackets) and (i=='>' and stack[-1]=='<') or (i=='}' and stack[-1]=='{') or (i==')' and stack[-1]=='('):
                    stack.pop()
                elif (i in r_brackets) or (i in l_brackets):
                    stack.append(i)
            elif (i in r_brackets) or (i in l_brackets):
                stack.append(i)
        return False

    def incomplete_bracket_check(self,line):

        
        stack=[]
        l_brackets={'{','(','<'}
        r_brackets={'>',')','}'}
        for i in line:
            if (len(stack)>0):
                if (i in r_brackets) and (i=='>' and stack[-1]=='<') or (i=='}' and stack[-1]=='{') or (i==')' and stack[-1]=='('):
                    stack.pop()
                elif (i in r_brackets) or (i in l_brackets):
                    stack.append(i)
            elif (i in r_brackets) or (i in l_brackets):
                stack.append(i)
        return (len(stack)>0)

    def tranline_nested_bracket_check(self,seg_input):
        tmp_lines = []
        for i in self.trans:
            if self.nested_bracket_check(seg_input[i[1]-1]):
                tmp_lines.append(i[1])
        if len(tmp_lines)>0:
            self.errors.append([10,tmp_lines,[],''])

    def line_incomplete_bracket_check(self,seg_input):
        tmp_lines=[]
        for i in range(len(seg_input)):
            if self.incomplete_bracket_check(seg_input[i]):
                tmp_lines.append(i+1)
        if len(tmp_lines)>0: 
            self.errors.append([11,tmp_lines,[],''])

    def line_check(self):
        seg_input=self.orig_input.split('\n')
        self.tranline_nested_bracket_check(seg_input)
        self.line_incomplete_bracket_check(seg_input)

    # def tranline_ASCII_check(self,seg_input):

    # def tranline_sign_reading_check(self,seg_input):

    # def line_check(self):






    def structure_check(self):
        '''
        :return: N/A

        check different rules and append error message to self.error_str
        '''

        '''check the order of ID, language, and object'''
        if len(self.ids)==1 and len(self.lans)==1 and len(self.objs)==1:
            if self.ids[0]!=1:
                self.errors.append([0,self.ids,[],''])
            if self.lans[0]!=2:
                self.errors.append([1,self.lans,[],''])
            if self.objs[0]!=3:
                self.errors.append([2,self.objs,[],''])
    
        '''check ID line'''
        if len(self.ids)<1:
            self.errors.append([3,[],[],''])
        elif len(self.ids)>1:
            self.errors.append([4,self.ids,[],''])
        
        '''check language line'''
        if len(self.lans)<1:
            self.errors.append([5,[],[],''])
        elif len(self.lans)>1:
            self.errors.append([6,self.lans,[],''])

        '''check objects line'''
        if len(self.objs)<1:
            self.errors.append([7,[],[],''])
        elif len(self.objs)>1:
            self.errors.append([8,self.objs,[],''])

        '''check $comment or transliterration line'''
        if len(self.dollars)<1 and len(self.surfaces)<1 and len(self.trans)<1:
            self.errors.append([9,[],[],''])
        
        '''check surface and transliterration sequence (to be done)'''

        self.line_check()


