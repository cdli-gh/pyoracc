import re
import json
import pkg_resources
resource_package = __name__ 
class SignWordProcessor(object): 
    def __init__(self):
        self.ap_mapping = self.init_atfid_pid_mapping()
        self.sign_list, self.word_list = self.init_word_sign_list()
        self.pt_mapping = self.init_pid_text_mapping()

    def init_atfid_pid_mapping(self):
        tmp_file_link = pkg_resources.resource_filename(__name__, 'jsons/atfid_to_pid.json')
        with open(tmp_file_link ,'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict

    def init_word_sign_list(self):
        tmp_file_link = pkg_resources.resource_filename(__name__, 'jsons/word_sign.json')
        with open(tmp_file_link ,'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict['signs'], load_dict['words']

    def init_pid_text_mapping(self):
        tmp_file_link = pkg_resources.resource_filename(__name__, 'jsons/pid_to_text.json')
        with open(tmp_file_link ,'r') as load_f:
            load_dict = json.load(load_f)
        return load_dict

    def pid_to_text(self,pid):
        return self.pt_mapping[str(pid)]


    def get_pid(self,atfid):
        if atfid in self.ap_mapping:
            pid = self.ap_mapping[atfid]
        else:
            pid = -2
        return pid

    def is_pid_in_signlist(self,pid):
        if str(pid) in self.sign_list:
            return True
        else:
            return False

    def is_pid_in_wordlist(self,pid):
        if str(pid) in self.word_list:
            return True
        else:
            return False

    def check_sign(self,pid,sign):
        if pid < 0:
            return False
        if sign in self.sign_list[str(pid)]:
            return True
        return False

    def check_word(self,pid,word):
        if pid == -1:
            return False
        if word in self.word_list[str(pid)]:
            return True
        return False


    def check(self):
        '''
        :return: N/A

        To check the whole data collected during the parsing, use this method. 
        '''
        return


