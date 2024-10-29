import pandas as pd
from os import listdir


class Logs():
    def __init__(self, subj=None):
        self.subj = subj
        self.file_name = subj + '.csv'


    def set_columns(self, columns_list):
        self.columns = columns_list
        if self.file_name not in listdir():
            print('File log not found')
            frame_data = pd.DataFrame(data=1, columns=self.columns, index=range(5))
            frame_data.to_csv(self.file_name)
            print('File created: ', self.file_name)

    def read_file(self):
        self.value = pd.read_csv(self.file_name)[self.columns]
        return self.value

    def add_file(self, add_data):
        add_dataframe = pd.DataFrame(data=[add_data], columns=self.columns)
        self.value = self.value._append(add_dataframe, ignore_index=True)[self.columns]
        self.value.to_csv(self.file_name)

    def del_file(self, ind):
        self.value = self.value.drop(index=[ind]).reset_index()[self.columns]
        self.value.to_csv(self.file_name)

    def max_id(self):

        n_id = self.value['Id'].max()
        if int(n_id) == n_id:
            return n_id
        else:
            return 0

StudentsLog = Logs('Students')
StudentsLog.set_columns(['Second_name', 'First_name', 'Third_name', 'Birth_year', 'Start_date', 'End_date', 'Status', 'Id'])
StudentsLog.read_file()

GroupsLog = Logs('Groups')
GroupsLog.set_columns(['Group_name', 'Group_start', 'Group_status', 'Id'])
if not 'All_students' in list(GroupsLog.read_file()['Group_name']):
    GroupsLog.add_file(['All_students',None, 'Active', 1])
GroupsLog.read_file()

