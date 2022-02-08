# Import required modules 

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
from scipy.stats.kde import gaussian_kde
from numpy import linspace
#!pip install fitter
from fitter import Fitter


def make_window(theme):
    sg.theme(theme)
    menu_def = [['Application', ['Exit']],
                ['Help', ['About']]]
    menu_def = [['File', ['Open', 'Save', 'Properties', 'Exit' ]],
                ['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],
                ['Toolbar', ['---', 'Sample', 'Delay', '---', 'Display', 'Visualize']],
                ['Help', 'About...'],]
    right_click_menu_def = [[], ['Nothing', 'More Nothing', 'Exit']]

    # Table Data
    data = [["John", 10], ["Jen", 5]]
    headings = ["Name", "Score"]

    input_layout = [[sg.Menu(menu_def, key='-MENU-')],
                    [sg.Text('Row number from'),
                     sg.Input(key='Row_number_from', size=(10, 1)),
                     sg.Text('Row number to'),
                    sg.Input(key='Row_number_to', size=(10, 1))],
                    [sg.Text('Col number from '),
                     sg.Input(key='Column_number_from', size=(10, 1)),
                     sg.Text('Col number to '),
                     sg.Input(key='Column_number_to', size=(10, 1))
                    ],
                    [sg.Text('Column(s) name '),
                     sg.Input(key='Columns_name',size=(10, 1)), sg.Button('Show data')],
                    [sg.Button('Data describe'),sg.Button('Whole data')],
                    [sg.Combo(values=('Plot_ap_x', 'Plot_ap_y', 'Plot_ap_z',
                                      'Plot_on_the_same_set','Plot_on_one','3D_plot',
                                      'Result_statistical_model_1','Result_statistical_model_2','Result_distribution_fitting',
                                      'Time_domain_channel_circular_shifted_1','Time_domain_channel_circular_shifted_2',
                                      'Time_domain_channel_circular_shifted_3','Time_domain_channel_circular_shifted_4',
                                      'Channel_amplitude_client','Channel_amplitude_ap','Channel_phase_client','Channel_phase_ap',
                                      'Channel_amplitude_client_mean','Channel_amplitude_ap_mean','Channel_phase_client_mean','Channel_phase_ap_mean'),
                              default_value='Plot_ap_x', readonly=True, k='Combo'),
                     sg.Button('Draw plot')],
                    [sg.Text('Application running'),
                     sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, enable_events=True, key='-GIF-IMAGE-'), ],
                    [sg.Multiline(key='Mul_line', size=(60,20))],
                    [sg.Button(image_data=sg.DEFAULT_BASE64_ICON, key='-LOGO-')]]

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

    layout = [[sg.Text('Input dataset path'),
               sg.Input(default_text=r'RTT_dataset_sample.csv',
                        key='Input_dataset_path',expand_x=True,expand_y=True),
               sg.Button('Load_data'),
               sg.Button('Select and load')]]
    layout += [[sg.TabGroup([[sg.Tab('Main Interface', input_layout),
                              sg.Tab('Log Output', logging_layout),
                              sg.Tab('Theme Layout',  theme_layout)]], key='-TAB GROUP-')]]

    return sg.Window('RTT Data Automated Analysis', layout, right_click_menu=right_click_menu_def)

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
    window = make_window('BlueMono')

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
                    window['Mul_line'].print('Dataset loaded successfully! The dataset is empty')
                else:
                    # in this situation, the dataset might be empty, maybe return the amount of empty columns that presist
                    window['Mul_line'].print('Dataset loaded successfully!')

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
                    window['Mul_line'].print('Data loaded successfully! The dataset is empty')
                else:
                    window['Mul_line'].print('Data loaded successfully!')

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
                    make_plot_window('AP_positionX[m]','AP_positionX[m]',fig)

                elif values['Combo'] == 'Plot_ap_y':
                    plt.clf()
                    plt.plot(dataset['AP_positionY[m]'],marker ='o')
                    plt.title('Access Point Positions Y dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Y distance (meters) ')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionY[m]','AP_positionY[m]',fig)

                elif values['Combo'] == 'Plot_ap_z':
                    plt.clf()
                    plt.plot(dataset['AP_positionZ[m]'],color='red', marker ='o')
                    plt.title('Access Point Positions Z dimension')
                    plt.xlabel('Access Point ID')
                    plt.ylabel('Z distance (meters) ')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('AP_positionZ[m]','AP_positionZ[m]',fig)

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
                    make_plot_window('AP_positionXYZ[m]','AP_positionXYZ[m]',fig)

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
                    make_plot_window('AP_positionXYZ[m]','AP_positionXYZ[m]',fig)

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
                    make_plot_window('3D_plot','3D_plot',fig)

                elif values['Combo'] == 'Result_statistical_model_1':
                    plt.clf()
                    nrows = dataset.shape[0]
                    meand = 2.429761
                    sd = 13.484498
                    RTT = dataset['ToD_factor[m]']
                    x_norm = np.random.normal(meand, sd, nrows)
                    nbins = 50
                    plt.hist(RTT, bins=nbins)
                    plt.xlabel('RTT')
                    plt.ylabel('Count')
                    plt.title('Histogram of RTT data(blue) and normally distributed random data')
                    plt.hist(x_norm, bins=nbins)
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Result_statistical_model_1','Result_statistical_model_1',fig)

                elif values['Combo'] == 'Result_statistical_model_2':
                    plt.clf()
                    nrows = dataset.shape[0]
                    meand = 2.429761
                    sd = 13.484498
                    x_norm = np.random.normal(meand, sd, nrows)
                    RTT = dataset['ToD_factor[m]']
                    kde = gaussian_kde(x_norm)
                    kded = gaussian_kde(RTT)
                    dist_space = linspace(min(x_norm), max(x_norm), 100)  # 100
                    dist_spaced = linspace(min(RTT), max(RTT), 100)
                    plt.plot(dist_spaced, kded(dist_spaced))
                    plt.plot(dist_space, kde(dist_space))
                    plt.xlabel('RTT')
                    plt.ylabel('PDF')
                    plt.title('Probability density functions of RTT (blue) and a random normal dist.')
                    fig = plt.gcf()
                    make_plot_window('Result_statistical_model_2','Result_statistical_model_2',fig)

                elif values['Combo'] == 'Result_distribution_fitting':
                    plt.clf()
                    nrows = dataset.shape[0]
                    x_gamma = np.random.gamma(3.5, 0.5, nrows)
                    f = Fitter(x_gamma, distributions=['gamma', 'dweibull', 'uniform'])
                    f.fit()
                    f.summary()
                    fig = plt.gcf()
                    make_plot_window('Result_distribution_fitting','Result_distribution_fitting',fig)


                elif values['Combo'] == 'Time_domain_channel_circular_shifted_1':
                    plt.clf()
                    selected_row = 40
                    selected_data = dataset.iloc[selected_row]
                    channels_begin = 11
                    channel_batch_size = 114
                    channels_unpadded = selected_data[channels_begin:channels_begin + 2 * channel_batch_size]

                    np_channels = np.array(channels_unpadded)

                    np_channels_cplx = np.zeros_like(np_channels)

                    counter = 0
                    for ch_rsp in np_channels:
                        ch_rsp = complex(ch_rsp.replace('i', 'j'))
                        np_channels_cplx[counter] = ch_rsp
                        counter += 1

                    channels_unpadded_raw = np_channels_cplx

                    sub_channel_batch_size = 57

                    zeros_to_pad = 28
                    channels = np.zeros(2 * channel_batch_size + 28, dtype=complex)
                    current_index = 6
                    channels[current_index:sub_channel_batch_size + current_index] = channels_unpadded_raw[
                                                                                     :sub_channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size:channel_batch_size]
                    current_index += (sub_channel_batch_size + 11)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     channel_batch_size:sub_channel_batch_size + channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size + channel_batch_size:2 * channel_batch_size]

                    channels_client = channels[:128]
                    channels_ap = channels[128:]
                    channels_timedomain = np.fft.ifft(np.fft.ifftshift(channels_client))
                    plt.plot(channels_timedomain.real, label='real')
                    plt.plot(channels_timedomain.imag, '--', label='imaginary')
                    plt.title('Client')
                    plt.legend()
                    fig = plt.gcf()
                    make_plot_window('Time_domain_channel_circular_shifted_1','Time_domain_channel_circular_shifted_1',fig)

                elif values['Combo'] == 'Time_domain_channel_circular_shifted_2':
                    plt.clf()
                    selected_row = 40
                    selected_data = dataset.iloc[selected_row]
                    channels_begin = 11
                    channel_batch_size = 114
                    channels_unpadded = selected_data[channels_begin:channels_begin + 2 * channel_batch_size]

                    np_channels = np.array(channels_unpadded)

                    np_channels_cplx = np.zeros_like(np_channels)

                    counter = 0
                    for ch_rsp in np_channels:
                        ch_rsp = complex(ch_rsp.replace('i', 'j'))
                        np_channels_cplx[counter] = ch_rsp
                        counter += 1

                    channels_unpadded_raw = np_channels_cplx

                    sub_channel_batch_size = 57

                    zeros_to_pad = 28
                    channels = np.zeros(2 * channel_batch_size + 28, dtype=complex)
                    current_index = 6
                    channels[current_index:sub_channel_batch_size + current_index] = channels_unpadded_raw[
                                                                                     :sub_channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size:channel_batch_size]
                    current_index += (sub_channel_batch_size + 11)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     channel_batch_size:sub_channel_batch_size + channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size + channel_batch_size:2 * channel_batch_size]

                    channels_client = channels[:128]
                    channels_ap = channels[128:]
                    channels_timedomain_ap = np.fft.ifft(np.fft.ifftshift(channels_ap))
                    plt.plot(channels_timedomain_ap.real, label='real')
                    plt.plot(channels_timedomain_ap.imag, '--', label='imaginary')
                    plt.title('Access point')
                    plt.legend()
                    fig = plt.gcf()
                    make_plot_window('Time_domain_channel_circular_shifted_2','Time_domain_channel_circular_shifted_2',fig)

                elif values['Combo'] == 'Time_domain_channel_circular_shifted_3':
                    plt.clf()
                    selected_row = 40
                    selected_data = dataset.iloc[selected_row]
                    channels_begin = 11
                    channel_batch_size = 114
                    channels_unpadded = selected_data[channels_begin:channels_begin + 2 * channel_batch_size]

                    np_channels = np.array(channels_unpadded)

                    np_channels_cplx = np.zeros_like(np_channels)

                    counter = 0
                    for ch_rsp in np_channels:
                        ch_rsp = complex(ch_rsp.replace('i', 'j'))
                        np_channels_cplx[counter] = ch_rsp
                        counter += 1

                    channels_unpadded_raw = np_channels_cplx

                    sub_channel_batch_size = 57

                    zeros_to_pad = 28
                    channels = np.zeros(2 * channel_batch_size + 28, dtype=complex)
                    current_index = 6
                    channels[current_index:sub_channel_batch_size + current_index] = channels_unpadded_raw[
                                                                                     :sub_channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size:channel_batch_size]
                    current_index += (sub_channel_batch_size + 11)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     channel_batch_size:sub_channel_batch_size + channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size + channel_batch_size:2 * channel_batch_size]

                    channels_client = channels[:128]
                    channels_ap = channels[128:]
                    channels_timedomain = np.fft.ifft(np.fft.ifftshift(channels_client))
                    N_samples_to_shift = 10
                    channel_time_domain_circ_shifted = np.roll(channels_timedomain, N_samples_to_shift)
                    plt.plot(channel_time_domain_circ_shifted.real, label='real')
                    plt.plot(channel_time_domain_circ_shifted.imag, '--', label='imaginary')
                    plt.legend()
                    fig = plt.gcf()
                    make_plot_window('Time_domain_channel_circular_shifted_3','Time_domain_channel_circular_shifted_3',fig)

                elif values['Combo'] == 'Time_domain_channel_circular_shifted_4':
                    plt.clf()
                    selected_row = 40
                    selected_data = dataset.iloc[selected_row]
                    channels_begin = 11
                    channel_batch_size = 114
                    channels_unpadded = selected_data[channels_begin:channels_begin + 2 * channel_batch_size]

                    np_channels = np.array(channels_unpadded)

                    np_channels_cplx = np.zeros_like(np_channels)

                    counter = 0
                    for ch_rsp in np_channels:
                        ch_rsp = complex(ch_rsp.replace('i', 'j'))
                        np_channels_cplx[counter] = ch_rsp
                        counter += 1

                    channels_unpadded_raw = np_channels_cplx

                    sub_channel_batch_size = 57

                    zeros_to_pad = 28
                    channels = np.zeros(2 * channel_batch_size + 28, dtype=complex)
                    current_index = 6
                    channels[current_index:sub_channel_batch_size + current_index] = channels_unpadded_raw[
                                                                                     :sub_channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size:channel_batch_size]
                    current_index += (sub_channel_batch_size + 11)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     channel_batch_size:sub_channel_batch_size + channel_batch_size]
                    current_index += (sub_channel_batch_size + 3)
                    channels[current_index:current_index + sub_channel_batch_size] = channels_unpadded_raw[
                                                                                     sub_channel_batch_size + channel_batch_size:2 * channel_batch_size]

                    channels_client = channels[:128]
                    channels_ap = channels[128:]
                    channels_timedomain = np.fft.ifft(np.fft.ifftshift(channels_client))
                    N_samples_to_shift = 10

                    channel_time_domain_circ_shifted_ap = np.roll(channels_timedomain_ap, N_samples_to_shift)
                    plt.plot(channel_time_domain_circ_shifted_ap.real, label='real')
                    plt.plot(channel_time_domain_circ_shifted_ap.imag, '--', label='imaginary')
                    plt.legend()
                    fig = plt.gcf()
                    make_plot_window('Time_domain_channel_circular_shifted_4','Time_domain_channel_circular_shifted_4',fig)

                elif values['Combo'] == 'Channel_amplitude_client':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]
                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 22

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])

                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)
                    client_magnitude = np.abs(example_channel_in_freq_domain[0,])
                    client_magnitude = np.array([20 * np.log10(i) for i in client_magnitude])
                    client_magnitude1 = np.array([20 * np.log10(i) for i in np.abs(example_channel_in_freq_domain[1,])])
                    plt.plot(tone_frequencies, client_magnitude, tone_frequencies, client_magnitude1)
                    plt.title('Channel amplitude at client side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Amplitude[dB]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_amplitude_client','Channel_amplitude_client',fig)

                elif values['Combo'] == 'Channel_amplitude_ap':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]
                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)

                    measIndex2plot = 22

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])

                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)
                    ap_magnitude = np.abs(example_channel_in_freq_domain[2,])
                    ap_magnitude = np.array([20 * np.log10(i) for i in ap_magnitude])
                    ap_magnitude1 = np.array([20 * np.log10(i) for i in np.abs(example_channel_in_freq_domain[3,])])
                    plt.plot(tone_frequencies, ap_magnitude, tone_frequencies, ap_magnitude1)  # 20*np.log10
                    plt.title('Channel amplitude at AP side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Amplitude[dB]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_amplitude_ap','Channel_amplitude_ap',fig)

                elif values['Combo'] == 'Channel_phase_client':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]
                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 22

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])

                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)
                    client_phase = example_channel_in_freq_domain[0,]
                    client_phase = np.array([np.angle(i) for i in client_phase])
                    client_phase1 = np.array([np.angle(i) for i in example_channel_in_freq_domain[1,]])
                    plt.plot(tone_frequencies, client_phase, tone_frequencies, client_phase1)
                    plt.title('Channel phase at client side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Phase[rad]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_phase_client','Channel_phase_client',fig)

                elif values['Combo'] == 'Channel_phase_ap':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]
                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 22

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])

                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)
                    ap_phase = example_channel_in_freq_domain[2,]
                    ap_phase = np.array([np.angle(i) for i in ap_phase])
                    ap_phase1 = np.array([np.angle(i) for i in example_channel_in_freq_domain[3,]])
                    plt.plot(tone_frequencies, ap_phase, tone_frequencies, ap_phase1)
                    plt.title('Channel phase at AP side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Phase[rad]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_phase_ap','Channel_phase_ap',fig)

                elif values['Combo'] == 'Channel_amplitude_client_mean':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]

                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 20

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])
                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)

                    client_magnitude = np.abs(example_channel_in_freq_domain[0,])
                    client_magnitude = np.array([20 * np.log10(i) for i in client_magnitude])
                    client_magnitude1 = np.array([20 * np.log10(i) for i in np.abs(example_channel_in_freq_domain[1,])])

                    plt.plot(tone_frequencies, client_magnitude, tone_frequencies, client_magnitude1)
                    plt.title('Channel amplitude at client side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Amplitude[dB]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_amplitude_client_mean','Channel_amplitude_client_mean',fig)

                elif values['Combo'] == 'Channel_amplitude_ap_mean':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]

                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 20

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])
                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)

                    ap_magnitude = np.abs(example_channel_in_freq_domain[2,])
                    ap_magnitude = np.array([20 * np.log10(i) for i in ap_magnitude])
                    ap_magnitude1 = np.array([20 * np.log10(i) for i in np.abs(example_channel_in_freq_domain[3,])])

                    plt.plot(tone_frequencies, ap_magnitude, tone_frequencies, ap_magnitude1)  # 20*np.log10
                    plt.title('Channel amplitude at AP side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Amplitude[dB]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_amplitude_ap_mean','Channel_amplitude_ap_mean',fig)

                elif values['Combo'] == 'Channel_phase_client_mean':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]

                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 20

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])
                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)

                    client_phase = example_channel_in_freq_domain[0,]
                    client_phase = np.array([np.angle(i) for i in client_phase])
                    client_phase1 = np.array([np.angle(i) for i in example_channel_in_freq_domain[1,]])

                    plt.plot(tone_frequencies, client_phase, tone_frequencies, client_phase1)
                    plt.title('Channel phase at client side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Phase[rad]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_phase_client_mean','Channel_phase_client_mean',fig)

                elif values['Combo'] == 'Channel_phase_ap_mean':
                    plt.clf()
                    freqz = 312.5 * 1000 / 10 ** 6  # MHz
                    tones = [freqz * i for i in range(-58, -1)]
                    tones2 = [freqz * i for i in range(2, 59)]

                    tone_frequencies = tones + tones2  # in MHz
                    tone_frequencies = np.array(tone_frequencies)
                    measIndex2plot = 20

                    Channel_selection = dataset.iloc[measIndex2plot, 12:468]
                    Channel_selection = np.array(Channel_selection)
                    ch_mean = Channel_selection[-1]
                    Channel_selection = np.append(Channel_selection, ch_mean)
                    example_channel_in_freq_domain = np.reshape(Channel_selection, [4, 114])
                    fin_cplx_selection = np.zeros_like(example_channel_in_freq_domain)

                    dim1 = 0
                    for index_ant in example_channel_in_freq_domain:
                        dim2 = 0
                        for val in index_ant:
                            # example_channel_in_freq_domain[index_ant]
                            fin_cplx_selection[dim1, dim2] = complex(val.replace('i', 'j'))
                            dim2 += 1
                        dim1 += 1
                    example_channel_in_freq_domain = np.array(fin_cplx_selection)

                    ap_phase = example_channel_in_freq_domain[2,]
                    ap_phase = np.array([np.angle(i) for i in ap_phase])
                    ap_phase1 = np.array([np.angle(i) for i in example_channel_in_freq_domain[3,]])

                    plt.plot(tone_frequencies, ap_phase, tone_frequencies, ap_phase1)
                    plt.title('Channel phase at AP side')
                    plt.xlabel('Tone frequency[MHz]')
                    plt.ylabel('Phase[rad]')
                    # plt.show()
                    fig = plt.gcf()
                    make_plot_window('Channel_phase_ap_mean','Channel_phase_ap_mean',fig)

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
        elif event == "Set Theme":
            print("[LOG] Clicked Set Theme!")
            theme_chosen = values['-THEME LISTBOX-'][0]
            print("[LOG] User Chose Theme: " + str(theme_chosen))
            window.close()
            window = make_window(theme_chosen)

    window.close()
    exit(0)


if __name__ == '__main__':
    main()