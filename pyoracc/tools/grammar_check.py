'''
Here provide some rough guidelines about how the GrammarCheck class works.

Firstly, it is an individial object for checking a ATF file which will be 
created before parsing. It will be passed into the ATFLexer and AtfParser 
(for common, oracc, or cdli type) as an class attribute. Then you may collect 
the necessary information during the parsing(lex or yacc). For example, you 
may collect the line number or offset of the ID line, or language line. 
After the parsing, you may utilize the collected information to perform required 
format checking, and collect error(s). A rough workflow is shown below:

1. create GrammerCheck()
2. pass as an attribute of ATFLexer & AtfParser 
3. collect information while parsing 
4. perform checking& collect errors after parsing 
5. you may utilize the errors to print information

more detail for each step is presneted below:

1. << create the GrammerCheck() >> & 2.<< pass as an attribute of ATFLexer & AtfParser >>
 These two happen in the pyoracc.atf.common.atffile. It is very simple and no need to change.

3. << collect information while parsing >>
 More development should usually start from here. 
 1) As the GrammerCheck is a attribute (g_check) of ATFLexer & AtfParser, you may invoke the methods 
    of g_check to collect information during the parsing. This require developer to know the parsing flow 
    in the ATFLexer & AtfParser. For easy code management, the methods for collecting information is usually
    written in the "conmmon function section". Also you may add more attributes in this class for managing the 
    collected information.

 2) Here, a sepcial error collection proccess will be performed during the parsing, which is to collect the default 
    errors from Lex and Yacc. It will be add to the self.errors_yacc and self.errors_lex attributs, which are lists. 

4. << perform checking& collect errors after parsing >>   
 
 1) Once the parsing is finished, GrammerCheck will be invoked a method called check(), which happens in the
    pyoracc.atf.common.atffile. check() methods will perform all checkings which have been implemented.
    Currently there are mainly three types of checking(line_check(), structure_check(), lex_yacc_check()).
        * line_check() is for checking the error inside lines
        * structure_check() is for checking components, e.g. is there a ID line or more than one ID lines?
        * lex_yacc_check() is a special check which should always be done after all checking, it is used to 
          check if the line number of default errors, if it is not there it will be added to the self.errors.
    For easy management, you usually should add new function at each corresponding section below.

 2) for collecting errors, all errors after each check function should be add to the self.errors attribute.
    Here, we do not directly collect error message, instead we collect a list of objects which conatins necessary
    inforation to made error message later.

    For each error object, err_id (a int) is the only required attribute. e.g. {err_id:1}.
    We use err_id to distinguish different error, and we will use ErrorsTemplate class in pyoracc.tools.errors_template
    to reproduce message whenever you have the self.errors.

    For developer, you may customize other attributes of error object which will be used to produce error message.
                   you may find which err_id has been used in the pyoracc.tools.errors_template, and we may create file for better management in the future.

    Also you should use self.errors_line_set to record the errors lines when you find errors, this is for convenient when we perform 
    lex_yacc_check().

5. After you get the self.errors, you may use them to do other things.
   You may use ErrorsTemplate class in pyoracc.tools.errors_template to produce error messages.

More detail, may be add when more developments are added.
'''


import re
from pyoracc.tools.errors_template import ErrorsTemplate

et=ErrorsTemplate()

class GrammarCheck(object):
    def __init__(self,orig_input,atf_id):
        self.errors = []  #error list {err_id:int, line:intlist, colmun:intlist, tocken:str}, since it is a dict, it is easy to extend 
        self.errors_yacc = [] #error list {error_id:int, line:intlist, colmun:intlist, tocken:str}
        self.errors_lex = []

        self.orig_input = orig_input.strip()
        
        self.errors_line_set=set()

        self.ids = [] # id lines, e.g. &P123456 = AB 78, 910
        self.lans = [] # language lines, e.g. #atf: lang akk 
        self.objs = [] # objects lines, e.g. @tablet
        self.surfaces = [] # surfarces lines, e.g. @column 2
        self.trans = [] # transliterration lines, e.g. 1. dub-sar
        self.dollars = [] # $ comment lines, e.g. $ blank space 
        self.links = [] # >>
        self.sharp_comments= [] # #-comment  

        self.atf_id=atf_id
    ''' strating test section '''

    # def print_test(self):
    #     '''
    #     For debug use only 
    #     '''

    #     self.check()
    #     print('----(GrammarCheck----')
    #     print(self.ids)
    #     print(self.lans)
    #     print(self.objs)
    #     print(self.surfaces)
    #     print(self.trans)
    #     print(self.dollars)
    #     for i in self.errors:
    #         print(et.error2str(0,i))
    #     # print(self.orig_input.split('\n'))
    #     print('----GrammarCheck)----')
    
    ''' ending test section '''

    ''' strating conmmon function section '''

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
        # print(self.surfaces)

    def add_trans(self,tran_id,tran_line):
        '''
        :params tran_id: str, transliterration id
        :params tran_line: int, the line number in segmented file
        :return: N/A

        add id and line number of transliterration line (e.g. 4. szu nam-ti-la-ni) to the self.trans as a tuple (tran_id,tran_line)
        '''
        
        tran_id = tran_id.replace('.','')
        tran_id = tran_id.replace('\'','')
        tran_id = tran_id.lower()
        # print(tran_id)
        rule = re.match(r'\d+', tran_id)
        if rule:
            tmp_id = rule.group(0)
            if len(tmp_id)<len(tran_id):
                tmp_extra = ord(tran_id[len(tmp_id):][0])
                tmp_offset = ord('a')
                if tmp_extra>=97 and tmp_extra<=122:
                    tmp_id = tmp_id + str(tmp_extra - tmp_offset)
                else:
                    tmp_id = tmp_id + '0'
            else:
                tmp_id = tmp_id + '0'
        elif tran_id[0:2] == '>>':
            return 
        else:
            tmp_id='99999'
        # print(tmp_id)
        # tmp_id=tran_id.replace('\'','')
        # tmp_id=tmp_id.replace('.','')
        self.trans.append((tmp_id,tran_line))

    def add_links(self,link):
        '''
        :params link: int, the line of link
        :return: N/A

        add line number of link line (e.g. >> ) to the self.links
        '''
        self.links.append(link)


    def add_dollars(self,dollar):
        '''
        :params dollar: int, the line number in segmented file
        :return: N/A

        add line number of dollar comments line (e.g. $ blank space) to the self.dollars
        '''
        self.dollars.append(dollar)

    def add_sharp_comment(self,sharp):
        '''
        :params sharp: int, the line number in segmented file
        :return: N/A

        add line number of sharp comments line (e.g. $ blank space) to the self.dollars
        '''
        self.sharp_comments.append(sharp)


    def add_yacc_error(self,token,line,offset):
        '''
        :params token: str, the error token 
        :params line: int, the line (p.lineno) of the error point in segmented file
        :params offset: int, the offset (p.lexpos) of the error point in segmented file
        :return: N/A

        error ID. is -2 

        find the column no. of the yacc error token by using offset no., and put it into self.errors_yacc
        yacc default error No. is -2 
        '''
        
        column=self.find_column(offset)
        tmp_err={'err_id':-1,'line':line,'column':column,'token':token}
        self.errors_yacc.append(tmp_err)

    def add_lex_error(self,char,line,offset):
        '''
        :params char: str, the error character 
        :params line: int, the line (p.lineno) of the error point in segmented file
        :params offset: int, the offset (p.lexpos) of the error point in segmented file
        :return: N/A

        error ID. is -1 

        find the column no. of the lex error character by using offset no., and put it into self.errors
        yacc default error No. is -1 
        '''
        column=self.find_column(offset)
        tmp_err={'err_id':-2,'line':line,'column':column,'token':char}
        self.errors_lex.append(tmp_err)

    ''' ending conmmon function section '''

    ''' starting line check section '''

    def find_column(self, offset):
        '''
        :params offset: int, the offset (p.lexpos) of the error point in segmented file
        :return: int, the column number of offset

        find the column no. in orginal input by using the offset no. of the char.
        '''
        line_start = self.orig_input.rfind('\n', 0, offset) + 1
        return (offset - line_start) + 1

    def line_ascii_test(self,line_n,line):
        '''
        :params line_n: int, the line No. of the checking line
        :params line: str, the line for checking
        :return: list, [line_n,(column No.,char)], a list whose 0th item is line_n and the rest is the tuple contains column No. and char for non-ascii char

        find if a line contains non-ascii char, and reture the accii char's column No. and char
        '''
        tmp_pair=[line_n]
        for i in range(len(line)):
            if ord(line[i])>=128:
                tmp_pair.append((i+1,line[i]))
        return tmp_pair

    def is_nested_bracket(self,line):
        '''
        :params line: str, the line for checking
        :return: int, 0: no nested
                      1: same type brackets nested
                      2: [ nested inside {} or ()



        find if a line contains nested brackets
        '''
        stack=[]
        l_brackets={'{','(','['} #,'<'
        r_brackets={')','}',']'} # '>',
        for i in line:
            if (i in l_brackets):# and len(set(stack).intersection(l_brackets))>0:
                if (i in stack):
                    return 1
                if i=='[' and (('{' in stack) or ('(' in stack)):
                    return 2 
            if (len(stack)>0):
                if (i in r_brackets) and ((i=='}' and stack[-1]=='{') or (i==')' and stack[-1]=='(') or (i==']' and stack[-1]=='[')):#(i=='>' and stack[-1]=='<') or 
                    stack.pop()
                elif (i in r_brackets) or (i in l_brackets):
                    stack.append(i)
            elif (i in r_brackets) or (i in l_brackets):
                stack.append(i)
        return 0

    def is_incomplete_bracket(self,line):
        '''
        :params line: str, the line for checking
        :return: bool, if there are incomplete brackets return True else return False

        find if a line contains incomplete brackets
        '''
        stack=[]
        l_brackets={'{','(','['}#,'<'
        r_brackets={')','}',']'}#'>',
        for i in line:
            if (len(stack)>0):
                if (i in r_brackets) and ((i=='}' and stack[-1]=='{') or (i==')' and stack[-1]=='(') or (i==']' and stack[-1]=='[')):#(i=='>' and stack[-1]=='<') or 
                    stack.pop()
                elif (i in r_brackets) or (i in l_brackets):
                    stack.append(i)
            elif (i in r_brackets) or (i in l_brackets):
                stack.append(i)
        return (len(stack)>0)

    def tranline_nested_bracket_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 10, 23

        find if a trans line contains nested brackets, and put the error into self.errors and put the error line into self.errors_line_set
            error 10: for same type brackets nested
            error 23: for [ nested inside {} or ()
        '''
        tmp_lines1 = []
        tmp_lines2 = []
        for i in self.trans:
            error_int = self.is_nested_bracket(seg_input[i[1]-1])
            if error_int == 1:
                tmp_lines1.append(i[1])
                self.errors_line_set.add(i[1])
            elif error_int == 2:
                tmp_lines2.append(i[1])
                self.errors_line_set.add(i[1])
        if len(tmp_lines1)>0:
            tmp_err={'err_id':10,'line':tmp_lines1}
            self.errors.append(tmp_err)
        if len(tmp_lines2)>0:
            tmp_err={'err_id':23,'line':tmp_lines2}
            self.errors.append(tmp_err)

    def line_incomplete_bracket_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 11

        find if a trans line contains incomplete brackets, and put the error into self.errors and put the error line into self.errors_line_set
        '''

        tmp_lines = []
        for i in range(len(seg_input)-1):
            if self.is_incomplete_bracket(seg_input[i]):
                tmp_lines.append(i+1)
                self.errors_line_set.add(i+1)
        if len(tmp_lines)>0:
            tmp_err={'err_id':11,'line':tmp_lines}
            self.errors.append(tmp_err)


    def tranline_ASCII_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 12

        find if a trans line contains non-ASCII char, and put the error into self.errors and put the error line into self.errors_line_set
        '''

        tmp_lcpairs = [] # [org_line, (err_col,err_token)]
        for i in self.trans:
            tmp_lcpair = self.line_ascii_test(i[1],seg_input[i[1]-1]) 
            if len(tmp_lcpair) > 1:
                tmp_lcpairs.append(tmp_lcpair)
                self.errors_line_set.add(tmp_lcpair[0])
        if len(tmp_lcpairs) > 0:
            tmp_err = {'err_id':12,'lcpairs':tmp_lcpairs}
            self.errors.append(tmp_err)

    def tranline_numFollowsign_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 13

        find if all the numbers in the trans line following a sign e.g. 1(asz@c) or 1/2(asz@c), and put the error into self.errors and put the error line into self.errors_line_set
        '''

        tmp_lines = []
        for i in self.trans:
            line = seg_input[i[1]-1]
            # rule1=re.findall( r'\d\(.+?\)', line)
            rule1 = re.findall( r'\s\d+\/\d+[^\(]', line)   
            rule2 = re.findall( r'\s\d+[^\(]', line)
            rule3 = []
            for j in rule2:
                if '/' not in j: 
                    rule3.append(j)
            if len(rule3+rule1)!= 0:
                tmp_lines.append(i[1])
                self.errors_line_set.add(i[1])
                # bad_token=(re.findall( r'\d[^\(|^.]', line)+re.findall( r'\d\(.+?[^\(|^.]', line)
                # for j in bad_token:
                    # line    
        if len(tmp_lines) > 0:
            tmp_err = {'err_id':13,'line':tmp_lines}
            self.errors.append(tmp_err)

    def tranline_no_char_c_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 21

        no char c is allowed in trans line, if find, put the error into self.errors and put the error line 
        into self.errors_line_set
        
        '''

        tmp_lines = []
        for i in self.trans:
            line = seg_input[i[1]-1]
            line = line[line.find(' '):]
            idx = line.find('c')
            if idx!=-1:
                tmp_lines.append(i[1])
                self.errors_line_set.add(i[1])
        print(tmp_lines)
        if len(tmp_lines)>0:
            tmp_err={'err_id':21,'line':tmp_lines}
            self.errors.append(tmp_err) 


    def tranline_start4digits_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 14, 15

        find if all the trans line satrting a number(error 14) and the number is at most 4 digits(error 15),
        and put the error into self.errors and put the error line into self.errors_line_set
        '''

        tmp_lines1 = []
        tmp_lines2 = []
        for i in self.trans:
            line = seg_input[i[1]-1]
            rule = re.match(r'\d+?[a-z]?\'?\.', line)#[A-Z]?            
            if rule:
                digits_str = re.match(r'\d+',rule.group(0)).group(0)
                if len(digits_str)>4:
                    tmp_lines2.append(i[1])
                    self.errors_line_set.add(i[1])
            else:
                tmp_lines1.append(i[1])
                self.errors_line_set.add(i[1])
        if len(tmp_lines1)>0:
            tmp_err={'err_id':14,'line':tmp_lines1}
            self.errors.append(tmp_err)
        if len(tmp_lines2)>0:
            tmp_err={'err_id':15,'line':tmp_lines2}
            self.errors.append(tmp_err)

    def line_first_sign_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 17

        find if all the lines satrting by one of the &, #, @, $, >>, and number within 4 digits,
        and put the error into self.errors and put the error line into self.errors_line_set
        '''

        tmp_lines = []
        for i in range(len(seg_input)-1):
            rule = re.match(r'\d+?\.?[a-z]?[A-Z]?\'?\.|@|#|&|\>\>|\$', seg_input[i])
            if rule or seg_input[i]=='':
                pass
            else:
                tmp_lines.append(i+1)
                self.errors_line_set.add(i+1)
        if len(tmp_lines)>0:
            tmp_err={'err_id':17,'line':tmp_lines}
            self.errors.append(tmp_err)
    
    def line_no_brackets3periods_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 19,

        (...) is not allowed, if find, put the error into self.errors and put the error line 
        into self.errors_line_set
        '''     
        tmp_lines = []
        for i in range(len(seg_input)-1):
            idx = seg_input[i].find('(...)')
            if idx!=-1:
                tmp_lines.append(i+1)
                self.errors_line_set.add(i+1)
        if len(tmp_lines)>0:
            tmp_err={'err_id':19,'line':tmp_lines}
            self.errors.append(tmp_err)

    def line_no_xxx_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 20,

        xxx is not allowed, if find, put the error into self.errors and put the error line 
        into self.errors_line_set
        '''     
        tmp_lines = []
        for i in range(len(seg_input)-1):
            idx = seg_input[i].find('xxx')
            if idx!=-1:
                tmp_lines.append(i+1)
                self.errors_line_set.add(i+1)
        if len(tmp_lines)>0:
            tmp_err={'err_id':20,'line':tmp_lines}
            self.errors.append(tmp_err)

    def surfaceline_seal_follow_label_check(self,seg_input):
        '''
        :params seg_input: list, a list of lines which segemented from the original input
        :return: N/A

        error ID: 22,

        @seal must be followed by a label (say `@seal 1'), if no lable, put the error into 
        self.errors and put the error line into self.errors_line_set
        '''     
        tmp_lines = []
        for i in range(len(seg_input)-1):
            idx = seg_input[i].find('@seal')
            if idx!=-1:
                rule = rule = re.match(r'@seal\s\d+', seg_input[i])
                if rule:
                    pass
                else:
                    tmp_lines.append(i+1)
                    self.errors_line_set.add(i+1)
        if len(tmp_lines)>0:
            tmp_err={'err_id':22,'line':tmp_lines}
            self.errors.append(tmp_err)

    def no_blanklines_check(self,seg_input):
        '''
        :return: N/A

        error ID: 24

        no blank lines inside a text, if find, put the error into 
        self.errors
        '''
        tmp_lines = []
        for i in range(len(seg_input)-1):
            if seg_input[i]=='':
                tmp_lines.append(i+1)
                self.errors_line_set.add(i+1)
        if len(tmp_lines)>0:
            tmp_err={'err_id':24,'line':tmp_lines}
            self.errors.append(tmp_err)


    def line_check(self):
        '''
        :params N/A
        :return: N/A

        invoke all the checking on lines
        '''

        seg_input=self.orig_input.split('\n')
        self.tranline_nested_bracket_check(seg_input)
        self.tranline_ASCII_check(seg_input)
        self.tranline_numFollowsign_check(seg_input)
        self.tranline_start4digits_check(seg_input)
        self.tranline_no_char_c_check(seg_input)
        self.line_incomplete_bracket_check(seg_input)
        self.line_first_sign_check(seg_input)
        self.line_no_brackets3periods_check(seg_input)
        self.line_no_xxx_check(seg_input)
        self.surfaceline_seal_follow_label_check(seg_input)
        self.no_blanklines_check(seg_input)
    
    ''' ending line check section '''

    ''' starting structure check section '''

    def structure_IdLanObj_order_check(self):
        '''
        :params N/A
        :return: N/A
        error ID: 0, 1, 2
        check the order of ID, Language, and object line.
        '''

        '''check the order of ID, language, and object'''
        # print(self.sharp_comments)
        if len(self.ids)==1 and len(self.lans)==1 and len(self.objs)==1:
            if self.ids[0]!=1:
                tmp_err={'err_id':0,'line':self.ids}
                self.errors.append(tmp_err)
                self.errors_line_set.add(self.ids[0])
            if self.lans[0]!=2:
                for i in range(self.ids[0]+1,self.lans[0]):
                    if i not in self.sharp_comments:
                        tmp_err={'err_id':1,'line':self.lans}
                        self.errors.append(tmp_err)
                        self.errors_line_set.add(self.lans[0])
                        break
            if self.objs[0]!=3:
                for i in range(self.lans[0]+1,self.objs[0]):
                    if i not in self.sharp_comments:
                        tmp_err={'err_id':2,'line':self.objs}
                        self.errors.append(tmp_err)
                        self.errors_line_set.add(self.objs[0])
                        break
    

    def structure_IDLine_check(self):
        '''
        :params N/A
        :return: N/A
        error ID: 3, 4 

        check if there is only one ID line. (&P010032 = CT 50, 019)
        '''

        '''check ID line'''
        if len(self.ids)<1:
            tmp_err={'err_id':3}
            self.errors.append(tmp_err)
        elif len(self.ids)>1:
            tmp_err={'err_id':4,'line':self.ids}
            self.errors.append(tmp_err)
            self.errors_line_set.add(self.ids[0])
    
    def structure_LanLine_check(self):
        '''
        :params N/A
        :return: N/A
        error ID: 5, 6 
        
        check if there is only one language line. (#atf: lang akk)
        '''

        '''check language line'''
        if len(self.lans)<1:
            tmp_err={'err_id':5}
            self.errors.append(tmp_err)
        elif len(self.lans)>1:
            tmp_err={'err_id':6,'line':self.lans}
            self.errors.append(tmp_err)
            self.errors_line_set.add(self.lans[0])
    
    def structure_ObjLine_check(self):
        '''
        :params N/A
        :return: N/A
        error ID: 7, 8 
        
        check if there is only one obj line. (@tablet)
        '''

        '''check objects line'''
        if len(self.objs)<1:
            tmp_err={'err_id':7}
            self.errors.append(tmp_err)
        # elif len(self.objs)>1:
        #     tmp_err={'err_id':8,'line':self.objs}
        #     self.errors.append(tmp_err)
        #     self.errors_line_set.add(self.objs[0])

    def structure_dollarOrTrans_check(self):
        '''
        :params N/A
        :return: N/A
        error ID: 9
        
        check if there is at least 1 dollar comment line (e.g. $ blank space) or 1 surface line (e.g. @column 2) with 1 transliterration line (e.g. 1. dub-sar)
        '''

        '''check $comment or transliterration line'''
        if len(self.dollars)<1 and len(self.surfaces)<1 and len(self.trans)<1:
            tmp_err={'err_id':9}
            self.errors.append(tmp_err)

    def structure_transSeq_check(self):
        '''
        :params N/A
        :return: N/A
        error ID: 16
        
        check if there is the number of transliterration lines are sequencial
        '''

        '''check surface and transliterration sequence'''
        # print(self.trans)
        # print(self.surfaces)
        if len(self.surfaces)<=1 or len(self.trans)<1:
            return 
        tmp_lines=[]
        tmp_start=1          
        tmp_surfaces=self.surfaces[:]
        tmp_surfaces.append(int(self.trans[-1][1]+1))    
        for i in range(1,len(tmp_surfaces)):
            tmp_bound = int(tmp_surfaces[i])
            tmp_pre = int(self.trans[tmp_start-1][0]) if len(self.trans[tmp_start-1][0])>=1 else 99999
            for j in range(tmp_start,len(self.trans)):
                curr_id = int(self.trans[j][0]) if len(self.trans[j][0])>=1 else -1
                curr_line = int(self.trans[j][1])
                if curr_line >= tmp_bound:
                    tmp_start = j+1
                    break
                if tmp_pre >= curr_id:
                    tmp_lines.append(curr_line-1)
                    self.errors_line_set.add(curr_line-1)
                tmp_pre = curr_id
        if len(tmp_lines)>0:
            tmp_err={'err_id':16,'line':tmp_lines}
            self.errors.append(tmp_err)

    def structure_transLinkOrder_check(self):
        trans_lines = []
        for i in self.trans:
            trans_lines.append(i[1])
        tmp_lines = []
        for i in range(len(self.links)):
            if ((self.links[i]-1) not in trans_lines) and ((self.links[i]-1) not in self.sharp_comments):
                tmp_lines.append(self.links[i])
                self.errors_line_set.add(self.links[i])
        if len(tmp_lines) > 0:
            tmp_err = {'err_id':18,'line':tmp_lines}
            self.errors.append(tmp_err)

        



    def structure_check(self):
        '''
        :return: N/A

        invoke all the structure checks
        '''
        self.structure_IdLanObj_order_check()
        self.structure_IDLine_check()
        self.structure_LanLine_check()
        self.structure_ObjLine_check()
        self.structure_dollarOrTrans_check()
        self.structure_transSeq_check()
        self.structure_transLinkOrder_check()
        
        ''' ending structure check section '''
        

    def lex_yacc_check(self):
        '''
        :return: N/A

        check whether the line of default errors (lex and yacc) are already in the self.errors, 
        if not put the default errors into self.errors. 
        '''
        for i in self.errors_yacc:
            if i['line'] not in self.errors_line_set:
                self.errors.append(i)
        for i in self.errors_lex:
            if i['line'] not in self.errors_line_set:
                self.errors.append(i)


    def check(self):
        '''
        :return: N/A

        To check the whole data collected during the parsing, use this method. 
        '''

        try:
            self.structure_check()
            self.line_check()
            ''''''
            self.lex_yacc_check() # must be done last
        except:
            raise SyntaxError('!!!!!!! grammar_check BUG !!!!!!  '+str(self.atf_id))


