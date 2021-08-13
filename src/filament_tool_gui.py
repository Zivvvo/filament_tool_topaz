import PySimpleGUI as sg
import subprocess 

form = sg.FlexForm('My first GUI')

tab1_layout = [
    [sg.T('Topaz2Filament', key = "TF")],
    [sg.InputText('topaz file', key='input_topaz'), sg.FileBrowse('Browse')],
    [sg.InputText('output directory', key = 'output_filament'), sg.FolderBrowse('Browse')],
    [sg.Button('Run', key = "Run1"), sg.Button("Cancel")]
]

tab2_layout = [[sg.T('Filament_tracer', key="FT")],
               [sg.InputText('input directory', key='input_tracer'), sg.FolderBrowse('Browse')],
               [sg.InputText('output directory', key='output_tracer'), sg.FolderBrowse('Browse')],
               [sg.Text('spacing'), sg.InputText('10', key='spacing')],
               [sg.Text('threshold'), sg.InputText('-5', key='threshold')],
               [sg.Text('eps'), sg.InputText('100', key = 'eps')],
               [sg.Text('min_samples'), sg.InputText('5', key = 'min_samples')],
               [sg.Text('produce images'), sg.Checkbox('produce images?', key="im")],
               [sg.Text('box size'), sg.InputText("256", key="box")],
               [sg.Text('min_part'), sg.InputText("10", key="min_part")],
               [sg.Text('Number of processors'), sg.InputText("2", key="Processors")],
               [sg.Button('Run', key = "Run2"), sg.Button("Cancel")]
               ]

tab3_layout = [[sg.T('Visualizer', key="V")],
               [sg.InputText('Filename', key = "Filename"), sg.FileBrowse()],
               [sg.Text("binfactor", key = "binfactor"), sg.InputText("1")],
               [sg.InputText("Box_file_directory", key = "Box_file_directory"), sg.FolderBrowse()],
               [sg.Text("prefix"), sg.InputText("")],
               [sg.Text("suffix"), sg.InputText("")],
               [sg.Text("Ground Truth"), sg.InputText()],
               [sg.Text("Save path"), sg.InputText(), sg.FolderBrowse()],
               [sg.Checkbox("Assort Color")],
               [sg.Button('Run', key = "Run2"), sg.Button("Cancel")]
               ]

layout = [
    [sg.TabGroup([[sg.Tab('Topaz2Filament', tab1_layout),
                   sg.Tab('Tracer', tab2_layout),
                   sg.Tab('Visualizer', tab3_layout)
                   ]])]]

window = sg.Window('Filament Tool').Layout(layout)

def run_topaz2filament(parameters):
    stdout, stderr = process.communicate()
    process = subprocess.Popen('python topaz_to_filament.py',parameters["input_topaz"], parameters["output_topaz"])

def run_filament_tracer(parameters):
    '''stdout, stderr = process.communicate()
    parameters = [str(x) for x in parameters]
    process = subprocess.Popen('python filament_trace.py', parameters["input_tracer"],parameters["output_tracer"],\
     parameters["spacing"], "-t", parameters["threshold"], "-eps", parameters["eps"],\
     "-min_samples", parameters["min_samples"], "-im", parameters["im"], "-box", parameters["box"],
     "-min_part", parameters["min_part"], "-processors", parameters["processors"])'''

while True:
    button, values = window.Read()
    print(button)
    print(values)
    if button in (None, "Quit", "Cancel"):
        window.Close()
        break
    elif button == 'Run1':
        print("Running Topaz2Filament parsing job")
        #sum_tab1(values["file 1"])

        run_topaz2filament(values)
        print("Parsing completed, please check your destination folder.")
    elif button == "Run2":
        print("Running Filament_tracer parsing job")
        
        run_filament_tracer(values)
window.Close()

window.finalize()