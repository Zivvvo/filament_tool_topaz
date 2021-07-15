import PySimpleGUI as sg

form = sg.FlexForm('My first GUI')

tab1_layout = [
    [sg.Text('Topaz2Filament', key = "TF")],
    [sg.InputText('topaz file', key='input'), sg.FileBrowse('Browse')],
    [sg.InputText('output directory', key = 'output'), sg.FolderBrowse('Browse')]
]

tab2_layout = [[sg.Text('Filament_tracer', key="FT")],
               [sg.InputText('input directory', key='input1'), sg.FolderBrowse('Browse')],
               [sg.InputText('output directory', key='output1'), sg.FolderBrowse('Browse')],
               [sg.Text('spacing'), sg.InputText('10', key='spacing')],
               [sg.Text('threshold'), sg.InputText('-5', key='threshold')],
               [sg.Text('eps'), sg.InputText('100', key = 'eps')],
               [sg.Text('min_samples'), sg.InputText('5', key = 'min_samples')],
               [sg.Text('produce images'), sg.Checkbox('produce images?')],
               [sg.Text('box size'), sg.InputText("256", key="box")],
               [sg.Text('min_part'), sg.InputText("10", key="min_part")],
               [sg.Text('Number of processors'), sg.InputText("2", key="Processors")],


               ]

tab3_layout = [[sg.Text('Visualizer', key="V")],
               [sg.InputText('Filename'), sg.FileBrowse()],
               [sg.Text("binfactor"), sg.InputText("1")],
               [sg.InputText("Box_file_directory"), sg.FolderBrowse()],
               [sg.Text("prefix"), sg.InputText("")],
               [sg.Text("suffix"), sg.InputText("")],
               [sg.Text("Ground Truth"), sg.InputText()],
               [sg.Text("Save path"), sg.InputText(), sg.FolderBrowse()],
               [sg.Checkbox("Assort Color")]]

layout = [
    [sg.TabGroup([[sg.Tab('Topaz2Filament', tab1_layout),
                   sg.Tab('Tracer', tab2_layout),
                   sg.Tab('Visualizer', tab3_layout)
                   ]])],
    [sg.Button('Run'), sg.Button("Cancel")]]

window = sg.Window('Filament Tool').Layout(layout)

while True:
    button, values = window.Read()
    print(button)
    print(values)
    if button in (None, "Quit", "Cancel"):
        window.Close()
        break
    elif button == 'Run':
        if values["file 1"] != "data 1":
            print("Running first tab")
            #sum_tab1(values["file 1"])
            print("Output generation completed. Please Close Window")

        if values["file 2"] != "data 2":
            print("Running second tab")
            #multiply_tab2(values["file 2"])
            print("Completed. Please Close Window")

window.Close()

window.finalize()