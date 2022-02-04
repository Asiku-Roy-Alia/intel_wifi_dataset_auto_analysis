import os
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
from mpl_toolkits import mplot3d


def make_window(theme):
    sg.theme(theme)
    menu_def = [['Application', ['Exit']],
                ['Help', ['About']]]
    menu_def = [['File', ['Open', 'Save', 'Properties', 'xit' ]],
                ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
                ['Toolbar', ['---', 'Sample', 'Delay', '---', 'Display', 'Visualize']],
                ['Help', 'About...'],]
    right_click_menu_def = [[], ['Nothing', 'More Nothing', 'Exit']]

    # Table Data
    data = [["John", 10], ["Jen", 5]]
    headings = ["Name", "Score"]

    input_layout = [[sg.Menu(menu_def, key='-MENU-')],
                    [sg.Text('Anything that requires user-input is in this tab!')],
                    [sg.Text('Row number from or a single row'),
                     sg.Input(key='Row_number_from', size=(10, 1)),
                     sg.Text('Row number to'),
                    sg.Input(key='Row_number_to', size=(10, 1))],
                    [sg.Text('Column_number_from or a single column'),
                     sg.Input(key='Column_number_from', size=(10, 1)),
                     sg.Text('Column_number_to'),
                     sg.Input(key='Column_number_to', size=(10, 1))
                    ],
                    [sg.Text('Column(s) name '),
                     sg.Input(key='Columns_name',size=(10, 1))],
                    [ sg.Button('Show data')],
                    [sg.Button('Data describe'),sg.Button('Whole data')],
                    [sg.Combo(values=('Plot_ap_x', 'Plot_ap_y', 'Plot_ap_z',
                                      'Plot_on_the_same_set','Plot_on_one','3D_plot'),
                              default_value='Plot_ap_x', readonly=True, k='Combo'),
                     sg.Button('Draw plot')], 
                    [sg.Text('Application running'),
                     sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-'), ],
                    [sg.Multiline(key='Mul_line', size=(60,20))],
                    [sg.Button('Button'), sg.Button('Popup'),
                     sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGO-')]]

    asthetic_layout = [[sg.T('Anything that you would use for asthetics is in this tab!')],
                       [sg.Image(data=sg.DEFAULT_BASE64_ICON, k='-IMAGE-')],
                       [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='-PROGRESS BAR-'),
                        sg.Button('Test Progress bar')]]

    logging_layout = [[sg.Text("Anything printed will display here!")], [sg.Output(key='log_output',size=(60, 25), font='Courier 8')]]

    graphing_layout = [[sg.Text("Anything you would use to graph will display here!")],
                       [sg.Graph((200, 200), (0, 0), (200, 200), background_color="black", key='-GRAPH-',
                                 enable_events=True)],
                       [sg.T('Click anywhere on graph to draw a circle')],
                       [sg.Table(values=data, headings=headings, max_col_width=25,
                                 background_color='black',
                                 auto_size_columns=True,
                                 display_row_numbers=True,
                                 justification='right',
                                 num_rows=2,
                                 alternating_row_color='black',
                                 key='-TABLE-',
                                 row_height=25)]]

    specalty_layout = [[sg.Text("Any \"special\" elements will display here!")],
                       [sg.Button("Open Folder")],
                       [sg.Button("Open File")]]

    theme_layout = [[sg.Text("See how elements look under different themes by choosing a different theme here!")],
                    [sg.Listbox(values=sg.theme_list(),
                                size=(20, 12),
                                key='-THEME LISTBOX-',
                                enable_events=True)],
                    [sg.Button("Set Theme")]]

    layout = [[sg.Text('Input datapath'),
               sg.Input(default_text=r'RTT_datasplit2.csv',
                        key='Input_dataset_path',expand_x=True,expand_y=True),
               sg.Button('Load_data'),
               sg.Button('Select and load')]]
    layout += [[sg.TabGroup([[sg.Tab('Input Elements', input_layout),
                              sg.Tab('Asthetic Elements', asthetic_layout),
                              sg.Tab('Graphing', graphing_layout),
                              sg.Tab('Specialty', specalty_layout),
                              sg.Tab('Theming', theme_layout),
                              sg.Tab('Output', logging_layout)]], key='-TAB GROUP-')]]

    return sg.Window('Auto Data Analyst', layout, right_click_menu=right_click_menu_def)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def make_plot_window(window_name, plot_name, fig):

    # fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    # t = np.arange(0, 3, .01)
    # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    layout = [[sg.Text(plot_name)],
              [sg.Canvas(key='-CANVAS-')],
              [sg.Button('Ok')]]
    window = sg.Window(window_name, layout, finalize=True,
                       font='Helvetica 18')
    # add the plot to the window
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    event, values = window.read()

    window.close()


def main():
    window = make_window(sg.theme())

    dataset=[]
    # This is an Event Loop
    while True:
        event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
        window['-GIF-IMAGE-'].update_animation(sg.DEFAULT_BASE64_LOADING_GIF, time_between_frames=100)
        if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
            print('===============================================')
            print('                                               ')
            print('============     ', event, '     ==============')
            print('                                               ')
            print('===============================================')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ', values[key])

        if event in (None, 'Exit'):
            print("[LOG] Clicked Exit!")
            break

        elif event == 'Load_data':
            Input_dataset_path = values['Input_dataset_path']

            # to avoid escape character appearing in the dataset path
            dataset_path=Input_dataset_path.replace('\\','/')

            # to judge whether the file exist
            if not os.path.exists(dataset_path):
                window['Mul_line'].print(' file does not exist ')
            else:
                #implement to read .csv and .xlsx file
                file_name = dataset_path.split('/')[-1]

                if file_name.endswith('.csv'):
                    dataset = pd.read_csv(dataset_path)
                else:
                    dataset = pd.read_excel(dataset_path)

                # to test whether the dataset is empty
                if len(dataset) == 0:
                    window['Mul_line'].print('Load succeed! The dataset is empty')
                else:
                    # in this situation, the dataset might be empty, maybe return the amount of empty columns that presist
                    window['Mul_line'].print('Load succeed!')

        # if put 'Select and load' and 'Load_data' together, it runs slowly!
        elif event == 'Select and load':
            Input_dataset_path = sg.popup_get_file('filename to open', no_window=True)

            dataset_path = Input_dataset_path.replace('\\', '/')

            if not os.path.exists(dataset_path):
                window['Mul_line'].print(' file does not exist ')
            else:
                file_name = dataset_path.split('/')[-1]

                if file_name.endswith('.csv'):
                    dataset = pd.read_csv(dataset_path)
                else:
                    dataset = pd.read_excel(dataset_path)

                if len(dataset) == 0:
                    window['Mul_line'].print('Load succeed! The dataset is empty')
                else:
                    window['Mul_line'].print('Load succeed!')

        elif event == 'Show data':#consider number is out of range

            row_number_from = values['Row_number_from']
            row_number_to = values['Row_number_to']
            col_name = values['Columns_name']
            col_number_from = values['Column_number_from']
            col_number_to = values['Column_number_to']
            is_input_right=True
            # if len(col_name) == 0:
            #   window['Mul_line'].print('test here!')
            # all is empty
            if len(dataset) == 0:
                window['Mul_line'].print('no dataset')
            elif len(row_number_from) == 0 and len(row_number_to) == 0  and\
               len(col_name) == 0 and len(col_number_from)==0 and len(col_number_to) == 0:
                window['Mul_line'].print('please input something, now the search range is empty!')
            else:
                # col_name  can not exist with any other number together
                if len(col_name) != 0 and \
                   (len(col_number_from) != 0 or len(col_number_to) != 0 or
                    len(row_number_from) != 0 or len(row_number_to) != 0):
                    window['Mul_line'].print('please do not input column_name and column position together !')
                    is_input_right=False
                #check the row input and col input are numbers
                if is_input_right and len(row_number_from) != 0:
                    for ch in row_number_from :
                        if ch not in '0123456789':
                            window['Mul_line'].print('please input right row_number_from!')
                            is_input_right=False
                            break
                if is_input_right and len(row_number_to) != 0:
                    for ch in row_number_to:
                        if ch not in '0123456789':
                            window['Mul_line'].print('please input right_row_to!')
                            is_input_right = False
                            break
                if is_input_right and len(col_number_from) != 0:
                    for ch in col_number_from:
                        if ch not in '0123456789':
                            window['Mul_line'].print('please input right col_number_from!')
                            is_input_right = False
                            break
                if is_input_right and len(col_number_to) != 0:
                    for ch in col_number_to:
                        if ch not in '0123456789':
                            window['Mul_line'].print('please input right col_number_to!')
                            is_input_right = False
                            break

                # 0 <= row_number_from
                if is_input_right and len(row_number_from) !=0 :
                    if 0 > int(row_number_from):
                        is_input_right=False
                        window['Mul_line'].print('please input right row_number_from!')

                #row_number_from < row_number_to
                if is_input_right and len(row_number_from) !=0 and len(row_number_to) != 0:
                    if int(row_number_from) > int(row_number_to):
                        is_input_right=False
                        window['Mul_line'].print('please input right row_number_from and row_number_to!')

                # 0 <= col_number_from
                if is_input_right and len(col_number_from) !=0 :
                    if 0 > int(col_number_from):
                        is_input_right=False
                        window['Mul_line'].print('please input right col_number_from!')

                #row_number_from < row_number_to
                if is_input_right and len(col_number_from) !=0 and len(col_number_to) != 0:
                    if int(col_number_from) > int(col_number_to):
                        is_input_right=False
                        window['Mul_line'].print('please input right col_number_from and col_number_to!')

                #check the columns name is right:
                All_columns_name=dataset.columns.tolist()
                chosen_names=[]
                if is_input_right and len(col_name) != 0 and len(All_columns_name) !=0 :
                    chosen_names = col_name.split(' ')
                    for name in chosen_names:
                        if name not in All_columns_name:
                            window['Mul_line'].print('Col name is wrong')
                            is_input_right=False
                            break

                #print data with right from and to and names
                if is_input_right:
                    #columns_name exist
                    if len(col_name) != 0:
                        window['Mul_line'].print(dataset[chosen_names])
                    #read a exact position number
                    elif len(row_number_from) != 0 and len(row_number_to) ==0 and\
                            len(col_number_from) != 0 and len(col_number_to) == 0:
                        window['Mul_line'].print(dataset.iloc[int(row_number_from),int(col_number_from)])
                    #read a single row
                    elif len(row_number_from) != 0 and len(row_number_to) ==0 and\
                            len(col_number_from) == 0 and len(col_number_to) == 0:
                        window['Mul_line'].print(dataset.iloc[int(row_number_from)])
                    #read a single col
                    elif len(row_number_from) == 0 and len(row_number_to) ==0 and\
                            len(col_number_from) != 0 and len(col_number_to) == 0:
                        window['Mul_line'].print(dataset.iloc[:,int(col_number_from)])
                    #read a single row with specific cols
                    elif len(row_number_from) != 0 and len(row_number_to) ==0 and\
                            len(col_number_from) != 0 and len(col_number_to) != 0:
                        window['Mul_line'].print(dataset.iloc[int(row_number_from),int(col_number_from):int(col_number_to)])
                    #read a single col with specific rows
                    elif len(row_number_from) != 0 and len(row_number_to) !=0 and\
                            len(col_number_from) != 0 and len(col_number_to) == 0:
                        window['Mul_line'].print(dataset.iloc[int(row_number_from):int(row_number_to),int(col_number_from)])
                    #read with specific rows and cols
                    elif len(row_number_from) != 0 and len(row_number_to) != 0 and\
                            len(col_number_from) != 0 and len(col_number_to) != 0:
                        window['Mul_line'].print(dataset.iloc[int(row_number_from):int(row_number_to), int(col_number_from):int(col_number_to)])

        elif event == 'Data describe':
            if len(dataset) != 0:
                df_describe=dataset.describe()
                window['Mul_line'].print('data describe!')
                window['Mul_line'].print(df_describe)
            else:
                window['Mul_line'].print('no data!')

        elif event == 'Whole data':
            if len(dataset) != 0:
                window['Mul_line'].print('whole data!')
                window['Mul_line'].print(dataset)
            else:
                window['Mul_line'].print('no data!')

        elif event == 'Draw plot':
            # Plot the AP X positions for all access point
            if len(dataset) == 0:
                window['Mul_line'].print('no data!')
            else:

                if values['Combo'] == 'Plot_ap_x':
                    plt.clf()
                    plt.plot(dataset['AP_positionX[m]'], color='green', marker='o')
                    plt.title('Access Point Positions X dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('X distance (meters) ')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionX[m] test','AP_positionX[m] test',fig)

                elif values['Combo'] == 'Plot_ap_y':
                    plt.clf()
                    plt.plot(dataset['AP_positionY[m]'],marker ='o')
                    plt.title('Access Point Positions Y dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Y distance (meters) ')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionY[m] test','AP_positionY[m] test',fig)

                elif values['Combo'] == 'Plot_ap_z':
                    plt.clf()
                    plt.plot(dataset['AP_positionZ[m]'],color='red', marker ='o')
                    plt.title('Access Point Positions Z dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Z distance (meters) ')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionZ[m] test','AP_positionZ[m] test',fig)

                elif values['Combo'] == 'Plot_on_the_same_set':
                    plt.clf()
                    plt.figure(figsize=(15, 3))
                    plt.subplot(131)
                    plt.plot(dataset['AP_positionX[m]'], color='green', marker ='o')
                    plt.title('Access Point Positions X dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('X distance (meters) ')
                    plt.subplot(132)
                    plt.plot(dataset['AP_positionY[m]'],marker ='o')
                    plt.title('Access Point Positions Y dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Y distance (meters) ')

                    plt.subplot(133)
                    plt.plot(dataset['AP_positionZ[m]'],color='red', marker ='o')
                    plt.title('Access Point Positions Z dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Z distance (meters) ')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionXYZ[m] test','AP_positionXYZ[m] test',fig)

                elif values['Combo'] == 'Plot_on_one':
                    plt.clf()
                    plt.plot(dataset['AP_positionX[m]'], color='green', marker ='o')
                    plt.plot(dataset['AP_positionY[m]'],marker ='o')
                    plt.plot(dataset['AP_positionZ[m]'],color='red', marker ='o')
                    plt.title('Access Point Positions all dimensions')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Distance (meters)')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionXYZ2[m] test','AP_positionXYZ2[m] test',fig)

                elif values['Combo'] == '3D_plot':
                    plt.clf()
                    ax = plt.axes(projection='3d')
                    ax.scatter3D(dataset['AP_positionX[m]'], dataset['AP_positionY[m]'], dataset['AP_positionZ[m]'],
                                 color='g');
                    ax.set_xlabel('x (m)')
                    ax.set_ylabel('y (m)')
                    ax.set_zlabel('z (m)')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionX[m] test','AP_positionX[m] test',fig)











        # elif event == 'About':
        #     print("[LOG] Clicked About!")
        #     sg.popup('PySimpleGUI Demo All Elements',
        #              'Right click anywhere to see right click menu',
        #              'Visit each of the tabs to see available elements',
        #              'Output of event and values can be see in Output tab',
        #              'The event and values dictionary is printed after every event')
        # elif event == 'Popup':
        #     print("[LOG] Clicked Popup Button!")
        #     sg.popup("You pressed a button!")
        #     print("[LOG] Dismissing Popup!")
        # elif event == 'Test Progress bar':
        #     print("[LOG] Clicked Test Progress Bar!")
        #     progress_bar = window['-PROGRESS BAR-']
        #     for i in range(1000):
        #         print("[LOG] Updating progress bar by 1 step (" + str(i) + ")")
        #         progress_bar.UpdateBar(i + 1)
        #     print("[LOG] Progress bar complete!")
        # elif event == "-GRAPH-":
        #     graph = window['-GRAPH-']  # type: sg.Graph
        #     graph.draw_circle(values['-GRAPH-'], fill_color='yellow', radius=20)
        #     print("[LOG] Circle drawn at: " + str(values['-GRAPH-']))
        # elif event == "Open Folder":
        #     print("[LOG] Clicked Open Folder!")
        #     folder_or_file = sg.popup_get_folder('Choose your folder')
        #     sg.popup("You chose: " + str(folder_or_file))
        #     print("[LOG] User chose folder: " + str(folder_or_file))
        # elif event == "Open File":
        #     print("[LOG] Clicked Open File!")
        #     folder_or_file = sg.popup_get_file('Choose your file')
        #     sg.popup("You chose: " + str(folder_or_file))
        #     print("[LOG] User chose file: " + str(folder_or_file))
        # elif event == "Set Theme":
        #     print("[LOG] Clicked Set Theme!")
        #     theme_chosen = values['-THEME LISTBOX-'][0]
        #     print("[LOG] User Chose Theme: " + str(theme_chosen))
        #     window.close()
        #     window = make_window(theme_chosen)

    window.close()
    exit(0)


if __name__ == '__main__':
    main()