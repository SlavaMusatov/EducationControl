from tkinter import *
from tkinter import ttk
from All_classes.file_logs import GroupsLog, StudentsLog
import datetime

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

label_test_image = ttk.Label(master=student_frames_list[0], text='Student image')
student_data = ttk.Label(master=frames_objects_dict['Student'], text='abcs\ndddd')
student_stats = Text(master=student_frames_list[2], height=5, wrap='word')
student_stats.insert('1.0', 'abcdef\nsdfafd')

label_test_image.pack()
student_data.place(relheight=0.485, relwidth=0.485, relx=0.505, rely=0.01)
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

group_groups_add = ttk.Button(master=group_frames_list[0], text='Добавить', command=lambda: (
    GroupsLog.add_file([group_groups_entry.get(), datetime.datetime.now(), 'Active', GroupsLog.max_id() + 1]),
    group_groups_list.insert(END, [GroupsLog.max_id(), group_groups_entry.get()]))
                              )

group_groups_add.place(relwidth=0.15, relx=0.52, y=20)

group_groups_list = Listbox(master=group_frames_list[0],
                            listvariable=Variable(value=GroupsLog.read_file().loc[:,['Id', 'Group_name']].values.tolist()), yscrollcommand=True,
                            xscrollcommand=True)
group_groups_list.pack(fill=BOTH, expand=True, pady=[50, 0])


def delete_group():
    ind = group_groups_list.curselection()[0]
    selected_str = group_groups_list.get(ind)
    if selected_str != 'All_students':
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

group_students_label = ttk.Label(master=group_frames_list[1], text=' Студент Ф. И. О. :')
group_students_label.pack(anchor='nw')

group_students_list_var = StudentsLog.read_file().loc[:, ['Id', 'Second_name', 'First_name', 'Third_name']].values.tolist()
group_students_list = Listbox(master=group_frames_list[1],
                              listvariable=Variable(value=[str(a)+' '+' '.join([*args]) for a, *args in group_students_list_var]), yscrollcommand=True,
                              xscrollcommand=True)


def add_student():
    add_data = [' ', ' ', ' ', ' ', ' ', ' ', 'Active', StudentsLog.max_id() + 1]
    add_names = group_students_entry.get().split(sep=' ', maxsplit=2)
    for i in range(len(add_names)):
        add_data[i] = add_names[i]

    add_data[4] = datetime.datetime.now()
    StudentsLog.add_file(add_data)
    group_students_list.insert(END,  str(add_data[7])+' ' +' '.join(list(add_data[0:4])))


group_students_add = ttk.Button(master=group_frames_list[1], text='Добавить', command=add_student)
group_students_add.place(relwidth=0.15, relx=0.52, y=20)

group_students_label_2 = ttk.Label(master=group_frames_list[1], text=' Список студентов группы:')
group_students_label_2.place(anchor='nw', y=50)


def new_list_of_group(x):
    group_students_list.delete(first=0, last=END)
    new_data = StudentsLog.read_file().loc[:, ['Id', 'Second_name', 'First_name', 'Third_name']].fillna(
        ' ').values.tolist()

    for elem in new_data:
        group_students_list.insert(END, ' '.join(str(el) for el in elem))


def delete_student():
    ind = group_students_list.curselection()[0]
    StudentsLog.del_file(ind)
    group_students_list.delete(ind)


def search_student():
    st = str(group_students_entry.get())
    ln = len(group_students_list.get(0, END))
    for a in range(ln):
        if st.lower() in group_students_list.get(a).lower():
            group_students_list.select_set(a)


group_students_delete = ttk.Button(master=group_frames_list[1], text='Удалить', command=delete_student)
group_students_delete.place(relwidth=0.15, relx=0.68, y=20)

group_students_search = ttk.Button(master=group_frames_list[1], text='Поиск', command=search_student)
group_students_search.place(relwidth=0.15, relx=0.84, y=20)

group_groups_list.bind('<<ListboxSelect>>', func=new_list_of_group)

group_students_list.pack(fill=BOTH, expand=True, pady=[50, 0])

# вкладка Курс

course_frames_list = [ttk.Frame(
    master=frames_objects_dict['Course'],
    borderwidth=3,
    relief=SOLID,
    padding=10
) for f_name in frames_dict['Course']]

course_frames_list[0].place(relheight=0.485, relwidth=0.485, relx=0.01, rely=0.01)
course_frames_list[1].place(relheight=0.485, relwidth=0.485, relx=0.505, rely=0.01)
course_frames_list[2].place(relheight=0.485, relwidth=0.98, relx=0.01, rely=0.505)

course_courses_entry = ttk.Entry(master=course_frames_list[0])
course_courses_entry.place(relwidth=0.48, relx=0.01, y=20)

course_courses_label = ttk.Label(master=course_frames_list[0], text=' Учебный курс:')
course_courses_label.pack(anchor='nw')

course_courses_add = ttk.Button(master=course_frames_list[0], text='Добавить')
course_courses_add.place(relwidth=0.24, relx=0.50, y=20)

course_courses_delete = ttk.Button(master=course_frames_list[0], text='Удалить')
course_courses_delete.place(relwidth=0.24, relx=0.75, y=20)

course_courses_label_2 = ttk.Label(master=course_frames_list[0], text=' Список всех курсов:')
course_courses_label_2.place(anchor='nw', y=50)

course_courses_list = Listbox(master=course_frames_list[0],
                              listvariable=Variable(value=['aaa', 'bbb', 'ccc', 'ddd']), yscrollcommand=True,
                              xscrollcommand=True)
course_courses_list.pack(fill=BOTH, expand=True, pady=[50, 0])

# =================================================================

course_stages_entry = ttk.Entry(master=course_frames_list[1])
course_stages_entry.place(relwidth=0.48, relx=0.01, y=20)

course_stages_label = ttk.Label(master=course_frames_list[1], text=' Стадия:')
course_stages_label.pack(anchor='nw')

course_stages_add = ttk.Button(master=course_frames_list[1], text='Добавить')
course_stages_add.place(relwidth=0.24, relx=0.50, y=20)

course_stages_delete = ttk.Button(master=course_frames_list[1], text='Удалить')
course_stages_delete.place(relwidth=0.24, relx=0.75, y=20)

course_stages_label_2 = ttk.Label(master=course_frames_list[1], text=' Список стадий курса:')
course_stages_label_2.place(anchor='nw', y=50)

course_stages_list = Listbox(master=course_frames_list[1],
                             listvariable=Variable(value=['aa1a', 'b1bb', 'cc1c', 'dd1d']), yscrollcommand=True,
                             xscrollcommand=True)
course_stages_list.pack(fill=BOTH, expand=True, pady=[50, 0])

# вкладка Статистика

root.mainloop()
