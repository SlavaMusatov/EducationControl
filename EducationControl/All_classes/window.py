from tkinter import *
from tkinter import ttk
from All_classes.file_logs import *
import datetime
from All_classes.student_picture import generate_picture
from PIL import *
from PIL import ImageTk
from os import remove

root = Tk()
root.title('Education Control')
root.geometry('1000x1000+0+0')

notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)

frames_dict = {
    'Student': ['Image', 'Personal_data', 'Personal_stats'],
    'Group': ['Groups_list', 'Students_in_group', 'Stats'],
    'Course': ['Course_list', 'Stages_in_course', 'Course_descriprion', 'Add_course'],
    'Stats': ['Number_of_students', 'Number_of_groups', 'Student_rating']
}

frames_objects_dict = {frame_name: ttk.Frame(notebook) for frame_name in frames_dict}


def create_frame(frame_name):
    frames_objects_dict[frame_name].pack(fill=BOTH, expand=True)
    notebook.add(frames_objects_dict[frame_name], text=frame_name)


for f_name in frames_dict: create_frame(f_name)

# вкладка Студент


student_frames_list = [ttk.Frame(
    master=frames_objects_dict['Student'],
    borderwidth=3,
    relief=SOLID,
    padding=10
) for f_name in frames_dict['Student']]

student_frames_list[0].place(relheight=0.485, relwidth=0.485, relx=0.01, rely=0.01)
student_frames_list[1].place(relheight=0.485, relwidth=0.485, relx=0.505, rely=0.01)
student_frames_list[2].place(relheight=0.485, relwidth=0.98, relx=0.01, rely=0.505)

label_test_image = ttk.Label(master=student_frames_list[0], text='ФОТО:')
label_test_image.pack()

student_data = ttk.Label(master=student_frames_list[1],
                         text='''Фамилия:
Имя:
Отчество:
 
Группа: 
Дата поступления:
Дата рождения: ''')
student_stats = Text(master=student_frames_list[2], height=5, wrap='word')
student_stats.insert('1.0', 'Тест1\nТест2')


student_data.pack(anchor = NW)
student_stats.pack()

                                                                                    # вкладка Группа

group_frames_list = [ttk.Frame(
    master=frames_objects_dict['Group'],
    borderwidth=3,
    relief=SOLID,
    padding=10
) for f_name in frames_dict['Group']]

group_frames_list[0].place(relheight=0.485, relwidth=0.485, relx=0.01, rely=0.01)
group_frames_list[1].place(relheight=0.485, relwidth=0.485, relx=0.505, rely=0.01)
group_frames_list[2].place(relheight=0.485, relwidth=0.98, relx=0.01, rely=0.505)

group_groups_entry = ttk.Entry(master=group_frames_list[0])
group_groups_entry.place(relwidth=0.50, relx=0.01, y=20)


group_groups_label = ttk.Label(master=group_frames_list[0], text=' Учебная группа:')
group_groups_label.pack(anchor='nw')

student_canvas = Canvas(master = student_frames_list[0], bg='white', height = 420, width = 320)
student_canvas.pack()


def create_group():
    GroupsLog.add_file([group_groups_entry.get(), datetime.datetime.now(), 'Active', GroupsLog.max_id() + 1]),
    group_groups_list.insert(
        END,

            f'{GroupsLog.max_id()} {group_groups_entry.get()}'

    )
    GroupsLog.read_file()

group_groups_add = ttk.Button(master=group_frames_list[0], text='Добавить', command=create_group)

group_groups_add.place(relwidth=0.15, relx=0.52, y=20)

group_groups_var = GroupsLog.read_file().loc[:, ['Id', 'Group_name']].values.tolist()

group_groups_list = Listbox(master=group_frames_list[0],
                            listvariable=Variable(
                                value=[f'{elem[0]} {elem[1]}' for elem in group_groups_var]
                            ),
                            yscrollcommand=True,
                            xscrollcommand=True)
group_groups_list.pack(fill=BOTH, expand=True, pady=[50, 0])


def delete_group():
    ind = group_groups_list.curselection()[0]
    selected_id = int(group_groups_list.get(ind)[0])
    if selected_id != 1:
        GroupsLog.del_file(ind)
        group_groups_list.delete(ind)


def search_group():
    st = str(group_groups_entry.get())
    ln = len(group_groups_list.get(0, END))
    for i in range(ln):
        if st.lower() in str(group_groups_list.get(i)).lower():
            group_groups_list.select_set(i)


group_groups_delete = ttk.Button(master=group_frames_list[0], text='Удалить', command=delete_group)
group_groups_delete.place(relwidth=0.15, relx=0.68, y=20)

group_groups_search = ttk.Button(master=group_frames_list[0], text='Поиск', command=search_group)
group_groups_search.place(relwidth=0.15, relx=0.84, y=20)

group_groups_label_2 = ttk.Label(master=group_frames_list[0], text=' Список всех групп:')
group_groups_label_2.place(anchor='nw', y=50)

# =================================================================


group_students_entry = ttk.Entry(master=group_frames_list[1])
group_students_entry.place(relwidth=0.50, relx=0.01, y=20)

group_students_label = ttk.Label(master=group_frames_list[1], text=' Студент id: Ф. И. О.  - Группа №')
group_students_label.pack(anchor='nw')

group_students_list_var = StudentsLog.read_file().loc[:,
                          ['Id', 'Second_name', 'First_name', 'Third_name', 'Id_group']].values.tolist()
group_students_list = Listbox(
    master=group_frames_list[1],
    listvariable=Variable(value=[f'id: {a} ' + ' '.join([str(e) for e in elem]) + f' - group {b}' for a, *elem, b in
                                 group_students_list_var]),
    yscrollcommand=True,
    xscrollcommand=True
)


def add_student():

    group_number = group_groups_entry.get().split(sep=' ')[0]
    if group_number == '':
        return None
    else: group_number = int(group_number)

    is_id = True if group_students_entry.get()[:2] == 'id' else False

    if group_number == 1 and not is_id:

        add_data = [' ', ' ', ' ', ' ', ' ', ' ', 'Active', StudentsLog.max_id() + 1, 1]
        add_names = group_students_entry.get().split(sep=' ', maxsplit=2)
        for i in range(len(add_names)):
            add_data[i] = add_names[i]

        add_data[4] = datetime.datetime.now()
        StudentsLog.add_file(add_data)
        group_students_list.insert(
            END,
            f'id: {add_data[7]} ' + ' ' + ' '.join(add_data[0:3]) + f' group{add_data[8]}'
        )
        img = generate_picture()

        img.save(f'Images/Student_Id_{add_data[7]}.png', "PNG")

    else:
        try:
            student_number = group_students_entry.get().split(' ')[1]

        except:
            return None
        StudentsLog.add_data(student_number, 'Id_group', group_number)
        new_list_of_group(1)
        group_students_entry.delete(0, END)
    fill_entry_group(1)


group_students_add = ttk.Button(master=group_frames_list[1], text='Добавить', command=add_student)
group_students_add.place(relwidth=0.15, relx=0.52, y=20)

group_students_label_2 = ttk.Label(master=group_frames_list[1], text=' Список студентов группы:')
group_students_label_2.place(anchor='nw', y=50)


def new_list_of_group(x):
    group_students_list.delete(first=0, last=END)
    new_data = StudentsLog.read_file().loc[:, ['Id', 'Second_name', 'First_name', 'Third_name', 'Id_group']].fillna(
        ' ').values.tolist()

    for a, *elem, b in new_data:
        group_students_list.insert(
            END, f'id: {a} ' + ' '.join([str(el) for el in elem]) + f' group {b}'
        )


def fill_entry_group(x):
    try:
        ind = group_groups_list.curselection()[0]
    except:
        return None

    name_to_entry1 = group_groups_list.get(ind)

    group_groups_entry.delete(0, END)
    group_groups_entry.insert(0, name_to_entry1)
    group_number = int(name_to_entry1.split(' ')[0])

    if group_number == 1:
        new_list_of_group(x)

        actual_groups = [int(x) for x in GroupsLog.read_file()['Id'].drop_duplicates().tolist()]




        for num in range(group_students_list.size()):
            num_group = int(group_students_list.get(num).split(' ')[-1])

            if not (num_group in actual_groups) or num_group ==1:

                group_students_list.select_set(num)

    else:

        student_id_df = StudentsLog.read_file()
        student_id_list = student_id_df[student_id_df['Id_group'].astype(int) == int(group_number)]['Id'].tolist()
        group_students_list.delete(0, END)

        for elem in student_id_list:

            list_to_add = StudentsLog.read_file()[StudentsLog.read_file()['Id'] == elem][
                ['Id', 'Second_name', 'First_name', 'Third_name', 'Id_group']].values.tolist()[0]

            group_students_list.insert(
                END,
                f'id: {list_to_add[0]} '+ ' '.join([str(x) for x in list_to_add[1:4]])+f' group {list_to_add[4]}'
                                   )


def delete_student():
    group_number = group_groups_entry.get().split(' ')[0]
    try:
        group_number = int(group_number)
    except:
        group_number = 1

    ind = group_students_list.curselection()[0]
    group_students_list.delete(ind)

    student_id = group_students_entry.get().split(' ')[1]

    if group_number ==1:
        StudentsLog.del_file(ind)
        try:
            remove(f'Images/Student_Id_{student_id}.png')
        except:
            pass

    else:
        StudentsLog.add_data(student_id, 'Id_group', 1)


def search_student():
    st = str(group_students_entry.get())
    ln = len(group_students_list.get(0, END))
    for a in range(ln):
        if st.lower() in group_students_list.get(a).lower():
            group_students_list.select_set(a)


def fill_entry_student(x):

    if group_students_list.size()==0:
        return None

    try:
        ind = group_students_list.curselection()[0]
    except:
        return None

    if is_frame_student == False:
        return None

    group_students_entry.delete(0, END)
    name_to_entry2 = group_students_list.get(ind)
    group_students_entry.insert(0, name_to_entry2)

    student_id = int(name_to_entry2.split(' ')[1])

    try:

        img = Image.open(f'Images/Student_Id_{student_id}.png')
        img = ImageTk.PhotoImage(img)
        student_canvas.image = img
        student_canvas.create_image(160, 210, image=img)

    except:
        pass

    student_df = StudentsLog.read_file()
    student_df = student_df[student_df['Id']==student_id].head(1)
    group_id = student_df['Id_group'].values[0]

    group_name = GroupsLog.read_file()[GroupsLog.read_file()['Id'] == int(group_id)]['Group_name'].values[0]
    student_data_str = f'''Фамилия: {student_df['Second_name'].values[0]}
Имя: {student_df['First_name'].values[0]}
Отчество: {student_df['Third_name'].values[0]}
 
Группа id: {group_id} {group_name}
Дата поступления: {'.'.join(student_df['Start_date'].values[0].split(' ')[0].split('-')[::-1])}
Дата рождения: '''
    student_data.text = student_data_str
    student_data.config(text=student_data_str)


group_students_delete = ttk.Button(master=group_frames_list[1], text='Удалить', command=delete_student)
group_students_delete.place(relwidth=0.15, relx=0.68, y=20)

group_students_search = ttk.Button(master=group_frames_list[1], text='Поиск', command=search_student)
group_students_search.place(relwidth=0.15, relx=0.84, y=20)

group_groups_list.bind('<<ListboxSelect>>', func=fill_entry_group)
group_students_list.bind('<<ListboxSelect>>', func=fill_entry_student)

def set_frame_true(x):
    global is_frame_student
    is_frame_student = True

def set_frame_false(x):
    global is_frame_student
    is_frame_student= False


group_students_list.bind('<Enter>', func=set_frame_true)
group_groups_list.bind('<Enter>', func=set_frame_false)

group_students_list.pack(fill=BOTH, expand=True, pady=[50, 0])

                                                                        # вкладка Курс

course_frames_list = [ttk.Frame(
    master=frames_objects_dict['Course'],
    borderwidth=3,
    relief=SOLID,
    padding=10
) for f_name in frames_dict['Course']]

def add_course():
    max_id = CourseInfo.max_id()
    try:
        course_name = course_courses_entry.get()
    except:
        return None
    CourseInfo.add_file([max_id+1, course_name, datetime.datetime.now()])
    course_courses_list.insert(END, f'{max_id+1} {course_name}')

def delete_course():
    try:
        ind = course_courses_list.curselection()[0]
    except:
        return None

    id_course_to_del = int(course_courses_list.get(ind).split(' ')[0])

    df_stages = StagesLog.read_file()

    id_stages_to_del = df_stages[df_stages['Id_course']==id_course_to_del]['Id_stage'].drop_duplicates().values.tolist()

    df_stages = df_stages[df_stages['Id_course'] != id_course_to_del].reset_index()
    del df_stages['index']
    df_stages.to_csv(StagesLog.file_name)

    df2_stages = StagesInfo.read_file()
    df2_stages= df2_stages[~df2_stages['Id'].isin(id_stages_to_del)]
    df2_stages.to_csv(StagesInfo.file_name)
    course_stages_list.delete(0, END)


    CourseInfo.del_file(ind)
    course_courses_list.delete(ind)

def search_course():
    course_name = course_courses_entry.get()

    for ind in range(course_courses_list.size()):
        elem = course_courses_list.get(ind)
        if course_name.lower() in elem.lower():
            course_courses_list.select_set(ind)

def courses_action(x):
    try:
        ind = course_courses_list.curselection()[0]
    except:
        return None
    input_str = course_courses_list.get(ind)
    course_courses_entry.delete(0, END)
    course_courses_entry.insert(0, input_str)

    course_number = int(course_courses_list.get(course_courses_list.curselection()[0]).split(' ')[0])
    course_stages_list.delete(0, END)
    df = StagesLog.read_file()
    stage_index_list = df[df['Id_course'] == course_number]['Id_stage'].drop_duplicates().tolist()
    course_stages_list.delete(0, END)

    df2 = StagesInfo.read_file()

    for num in stage_index_list:
        try:
            string = df2[df2['Id']==num].loc[:,['Id', 'Name_stage']].values.tolist()[0]

        except: continue
        string = 'id: ' + ' '.join([str(i) for i in string])
        course_stages_list.insert(END, string)


course_frames_list[0].place(relheight=0.485, relwidth=0.485, relx=0.01, rely=0.01)
course_frames_list[1].place(relheight=0.485, relwidth=0.485, relx=0.505, rely=0.01)
course_frames_list[2].place(relheight=0.485, relwidth=0.98, relx=0.01, rely=0.505)

course_courses_entry = ttk.Entry(master=course_frames_list[0])
course_courses_entry.place(relwidth=0.50, relx=0.01, y=20)

course_courses_label = ttk.Label(master=course_frames_list[0], text=' Учебный курс:')
course_courses_label.pack(anchor='nw')

course_courses_add = ttk.Button(master=course_frames_list[0], text='Добавить', command=add_course)
course_courses_add.place(relwidth=0.15, relx=0.52, y=20)

course_courses_delete = ttk.Button(master=course_frames_list[0], text='Удалить', command=delete_course)
course_courses_delete.place(relwidth=0.15, relx=0.68, y=20)

course_courses_search = ttk.Button(master= course_frames_list[0], text='Поиск', command=search_course)
course_courses_search.place(relwidth = 0.15, relx=0.84, y = 20)

course_courses_label_2 = ttk.Label(master=course_frames_list[0], text=' Список всех курсов:')
course_courses_label_2.place(anchor='nw', y=50)


course_courses_var = \
    [f'{elem[0]} {elem[1]}' for elem in CourseInfo.read_file().loc[:, ['Id', 'Name_course']].values.tolist()]
course_courses_list = Listbox(master=course_frames_list[0],
                              listvariable=Variable(value=course_courses_var), yscrollcommand=True,
                              xscrollcommand=True)
course_courses_list.pack(fill=BOTH, expand=True, pady=[50, 0])
course_courses_list.bind('<<ListboxSelect>>', func=courses_action)

# =================================================================

def add_stage():

    try:
        course_id = int(course_courses_entry.get().split(' ')[0])

    except:
        return None
    max_id = StagesInfo.max_id()
    stage_name = course_stages_entry.get()

    try:
        line_index = course_stages_list.curselection()[0]
        stage_id = course_stages_list.get(line_index).split(' ')[1]
        course_df = StagesLog.read_file()
        row_num = \
            course_df[(course_df['Id_course'] == int(course_id)) & (course_df['Id_stage'] == int(stage_id))].index[0]

        print(row_num)

        course_df.loc[row_num-.5] = [course_id, max_id+1, datetime.datetime.now()]
        course_df = course_df.sort_index().reset_index()

        del course_df['index']
        course_df.to_csv(StagesLog.file_name)

    except:
        line_index=END

        StagesLog.add_file([course_id, max_id + 1, datetime.datetime.now()])

    StagesInfo.add_file([max_id + 1, stage_name, datetime.datetime.now()])
    course_stages_list.insert(line_index, f'id: {max_id+1} {stage_name}')




def delete_stage():
    try:
        ind = course_stages_list.curselection()[0]

    except:
        return None
    stage_id = course_stages_list.get(ind).split(' ')[1]

    course_stages_list.delete(ind)
    df = StagesInfo.read_file()
    id_to_del = df[df['Id']==int(stage_id)].index.drop_duplicates()[0]

    StagesInfo.del_file(id_to_del)


def search_stage():
    stage_name = course_stages_entry.get()

    for ind in range(course_stages_list.size()):
        elem = course_stages_list.get(ind)
        if stage_name.lower() in elem.lower():
            course_stages_list.select_set(ind)

def stages_action(x):
    pass                                                    # действие пока отменено



course_stages_entry = ttk.Entry(master=course_frames_list[1])
course_stages_entry.place(relwidth=0.50, relx=0.01, y=20)

course_stages_label = ttk.Label(master=course_frames_list[1], text=' Стадия:')
course_stages_label.pack(anchor='nw')

course_stages_add = ttk.Button(master=course_frames_list[1], text='Добавить', command=add_stage)
course_stages_add.place(relwidth=0.15, relx=0.52, y=20)

course_stages_delete = ttk.Button(master=course_frames_list[1], text='Удалить', command=delete_stage)
course_stages_delete.place(relwidth=0.15, relx=0.68, y=20)

course_stages_search = ttk.Button(master= course_frames_list[1], text='Поиск', command=search_stage)
course_stages_search.place(relwidth = 0.15, relx=0.84, y = 20)

course_stages_label_2 = ttk.Label(master=course_frames_list[1], text=' Список стадий курса:')
course_stages_label_2.place(anchor='nw', y=50)

course_stages_var = [f'id: {elem[0]} {elem[1]}' for elem in StagesInfo.read_file().loc[:,['Id', 'Name_stage']].drop_duplicates().values.tolist()]
course_stages_list = Listbox(master=course_frames_list[1],
                             listvariable=Variable(value=course_stages_var), yscrollcommand=True,
                             xscrollcommand=True)
course_stages_list.pack(fill=BOTH, expand=True, pady=[50, 0])
course_stages_list.bind('<<ListboxSelect>>', func=stages_action)

# вкладка Статистика

#root.mainloop()
