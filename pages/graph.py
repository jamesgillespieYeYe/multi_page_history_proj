from dash import Dash, dcc, html, Input, Output, State, dash_table, ctx, callback
import plotly.graph_objects as go
from functions import *
import functions as funcs
import copy
import json
import math
import dash



dash.register_page(__name__)

class NamedShape:
    def __init__(self, name, shape, id):
        self.name = name
        self.shape = shape
        self.id = id
    # def toJson(self):
    #     return json.dumps([self.id, self.name])
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)



#app = Dash(__name__)
# server = app.server
print("hi")
names = []
f = open("inputs.json")
data = json.load(f)
for i in data['functions']:
    names.append(i['name'])
    

def find_entry(name):
    for i in data['functions']:
        if i['name'] == name:
            return i
    return None


layout = html.Div(children=[
    html.H4('Jimbo\'s Demo', style={'textAlign':'center'}),
    #  html.Div(
    #     [
    #         html.Div(
    #             dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"]
    #             )
    #         )
    #         for page in dash.page_registry.values()
    #     ]
    # ),
    dcc.Graph(id="graph"),
    dcc.Dropdown(
        id='dropdown',
        #options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        options=[{'label': i, 'value': i} for i in names],
        value=''
    ),
    #html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line'}),
    dcc.Store(id='intermediate-value'),
    html.Div([
        html.H4('Coordinates',style={'display':'inline-block','margin-right':20, 'border': '1px solid black'}),
        dcc.Input(id="input1", type="text", placeholder="", debounce=True),
        ], style={'display':'inline-block', 'border': '1px solid black'}),
    html.Div(id='Description', style={'whiteSpace': 'pre-line', 'background-color':'black', 'color': 'Gray', 'text-align':'center'}),
    html.Div([
        html.Button('Back', id='back_button', n_clicks=0), 
        html.Button('Forward', id='forward_button', n_clicks=0)
    ]),
    dcc.Store(id='global_list'),
    html.Div(id='display_steps', style={'whiteSpace': 'pre-line', 'background-color':'grey', 'color': 'black'}),
    html.Div(id='textarea-state-example-output', style={'whiteSpace': 'pre-line', 'background-color':'black', 'color': 'green'}),
    html.Div(id='global_list_output', style={'whiteSpace': 'pre-line', 'background-color':'black', 'color': 'DarkGreen'}),
    dcc.Store(id='next_id'),
    dcc.Store(id='step')
])
@callback(
    Output('Description', 'children'),
    Input('dropdown', 'value')
)
def update_description(dropdown_value):
    if dropdown_value != None and dropdown_value != '': 
        obj = find_entry(dropdown_value)
        return obj['desc']

@callback(
    Output('display_steps', 'children'),
    Input('step', 'data'),
    Input('dropdown', 'value')
)
def update_step_output(steps_value, dropdown_value):
    
    
    val = json.loads(steps_value)[0]    #Step number
    obj = find_entry(dropdown_value)
    if obj == None or dropdown_value == "reset":
        return "Step: " + str(val)
    #Find what this step is
    ret = "Step: " + str(val)
    flist = obj['list']
    instr = flist[val - 1] 
    ret += ": "
    ret += instr['jname']
    ret += '('
    if type(instr['args']) == list:
        if type(instr['args'][0]) == str:
            for i in range(0, len(instr['args'])):
                ret += instr['args'][i]
                if i < len(instr['args']) - 1:
                    ret += ','
    ret += ')'
    return ret


    



@callback(
    Output('global_list_output', 'children'),
    Input('global_list', 'data')
)
def display_global_list(data):
    if data != None:
        ret = ""
        jlist = json.loads(data)
        for obj in jlist:
            ret += json.dumps(obj) + "\n"
        ret += "^ Last Object ^"
        return ret
    return None

@callback(
    Output('textarea-state-example-output', 'children'),
    Input('dropdown', 'value'),
)
def update_output(value):
    obj = find_entry(value)
    if (obj == None):
        return ""
    myStr = ""
    stepsStr = ""
    myStr += json.dumps(obj)
    myStr += '\n'
    flist = obj['list']
    for instr in flist:
        if type(instr['name']) == list:
            myStr += '('
            for n in instr['name']:
                myStr += n + " "
            myStr += ')'
            myStr += " <-----  "
            myStr += instr['jname']
        else:
            myStr += instr['name']
            myStr += " <-----  "
            myStr += instr['jname']
        args = instr['args']
        if (type(args) == list):
            if (type(args[0]) == str):
                myStr += '('
                for index in range(0, len(args)):
                    myStr += args[index]
                    if index < len(args) - 1:
                        myStr += ','
                myStr += ')'
        instr_obj = find_entry(instr['jname'])



        myStr += '\n'
    stepsout = "sometext"
    return myStr



def find_object(objects_list, name):
    for i in objects_list:
        if i.name == name:
            return i
    return None

def replace(global_list, new):
    newDict = json.loads(new)
    for i in range(0, len(global_list)):
        oldDict = json.loads(global_list[i])
        if oldDict['id'] == newDict['id']:
            global_list[i] = new
            return 0
    return -1
def inner_exec(command, figure, global_list, next_id, custom_args, overrides=False, dashed=False):
    objects = []
    if command != '':
        construction = find_entry(command)
        
        flist = construction['list']
        oldFlist = copy.deepcopy(flist)
        
        startIndex = 0
        
        if overrides == True:
            #Why am I hacking my own program?
            startIndex += len(custom_args)
            toReplace = []
            replaceWith = []
            for i in range(0, startIndex):
                
                toReplace.append(flist[i]['name'])
                replaceWith.append(custom_args[i].name)
            for instr in flist:
                curr_args = instr['args']
                for i in range(0, len(curr_args)):
                    curr_name = curr_args[i]
                    for j in range(0, len(toReplace)):
                        if curr_name == toReplace[j]:
                            
                            curr_args[i] = replaceWith[j]
            #Add args to objects list
            for arg in custom_args:
                objects.append(arg)


        for i in range(startIndex, len(flist)):
            args = []
            jname = flist[i]['jname']
            #print("jname here: ", jname, custom_args)
            #print("custom args: ", custom_args)
            if custom_args == None or (len(flist[i]['farg']) == 0) or overrides==True:
                    #Use default args
                for defaults in flist[i]['args']:
                    args.append(defaults)
            else:
                #Setup custom args
                for farg in flist[i]['farg']:
                    #print("APPENDING ", custom_args[farg])
                    args.append(custom_args[farg])
            for j in range(0, len(args)):
                if (type(args[j]) == str):
                    args[j] = find_object(objects, args[j])
                #print("args: ", args)
            if jname[0] != '!':
                fhandle = getattr(funcs, jname)
                if dashed == True:
                    ret = fhandle(args, True)
                else:
                    ret = fhandle(args)
                if (type(flist[i]['name']) == list):
                    if len(ret) != len(flist[i]['name']):
                        raise Exception("Number of objects returned does not match number expected")
                    for index in range(0, len(ret)):
                        newEntry = NamedShape(flist[i]['name'][index], ret[index], next_id)
                        objects.append(newEntry)
                        next_id += 1
                        figure.add_shape(ret[index])
                        annotate(figure, newEntry)
                    
                else:
                    newEntry = NamedShape(flist[i]['name'], ret, next_id)
                    objects.append(newEntry)
                    next_id += 1
                    figure.add_shape(ret)
                    annotate(figure, newEntry)
            else:   #Subroutines...
                
                currId = next_id
                
                #Run subroutine
               
                if type(args[0]) == NamedShape:
                    #Override case
                    #We want to "overwrite" the first len(args) shapes with our shapes
                    next_id = inner_exec(jname[1:len(jname)], figure, global_list, next_id, args, True, True)
                    
                else:
                    #Not overriding case
                    #exit()
                    next_id = inner_exec(jname[1:len(jname)], figure, global_list, next_id, args)

                # print("printing here")
                # for e in global_list:
                #     asDict = json.loads(e)
                #     print(asDict)
                #     #asNamedShape = NamedShape(asDict['name'], asDict['shape'], next_id)
                #     #objects.append(asNamedShape)
                # print("done")

                #Get result from global list
                #print("nextid here: ", next_id)
                #print("len: ", len(global_list))
                #retAsDict = json.loads(global_list[next_id - 1])
                if type(flist[i]['name']) == list:
                    for item in flist[i]['name']:
                        originalName = item[0]
                        originalShape = None
                        for i in range(0, len(global_list)):
                            currAsDict = json.loads(global_list[i])
                            if currAsDict['name'] == originalName:
                                newShape = NamedShape(item[2], currAsDict['shape'], currAsDict['id'])
                                objects.append(newShape)

                else:   #Append last item created to local list
                    retAsDict = json.loads(global_list[len(global_list) - 1])
                    ret = NamedShape(flist[i]['name'], retAsDict['shape'], retAsDict['id'])
                    #Rename result
                    ret.name = flist[i]['name']
                    #Add to local objects list
                    objects.append(ret)
                    figure.add_shape(ret.shape)
                    annotate(figure, ret)
                
        if (overrides == True):
            #print("Here!!!!")
            #print("oldflist: ", oldFlist)
            for i in range(0, len(flist)):
                #print("Replacing ", flist[i], "with", oldFlist[i])
                flist[i] = oldFlist[i]
        figure.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
        )
        for obj in objects:
            #print(obj)
            if replace(global_list, obj.toJson()) != 0:
                global_list.append(obj.toJson())
    return next_id

def count_objects(command_name, steps_value=None):
    obj = find_entry(command_name)
    flist = obj['list']
    num_objects = 0
    if steps_value == None:
        steps_value = len(flist)
    for i in range(0, steps_value):
        instr = flist[i]
        jname = instr['jname']
        if jname[0] == '!':
            num_objects += count_objects(jname[1:len(jname)])
            for arg in flist[i]['args']:
                if type(arg) == str:
                    num_objects = num_objects - 1
            #num_objects = num_objects - len(flist[i]['args'])
            if type(flist[i]['name']) == list:
                num_objects = num_objects - len(flist[i]['name'])
            else:
                num_objects = num_objects - 1
        if (type(instr['name']) == list):
            num_objects += len(instr['name'])
        else:
            num_objects += 1
    print("called on", command_name, "returning", num_objects)
    return num_objects


#Generate the figure in the state it would be after 'steps_value' steps
def populate_figure_with_steps(global_list_data, steps_value, dropdown_value):
    obj = find_entry(dropdown_value)
    flist = obj['list']
    #Get the number of objects to display
    #Some steps produce multiple objects, so we need to go through the list of the commands
    #to figure this out
    num_objects = count_objects(dropdown_value, steps_value)
    print("num_objects: ", num_objects)
    print("steps_value: ", steps_value)
    # for i in range(0, steps_value):
    #     instr = flist[i]
    #     if (type(instr['name']) == list):
    #         num_objects += len(instr['name'])
    #     else:
    #         num_objects += 1
    #     #
    #print("Numobjects: ", num_objects)
    #Now that we have the number of objects, we can reset the figure
    global_list = json.loads(global_list_data)
    shapesToAdd = []
    for i in range(0, num_objects):
        for j in range(0, len(global_list)):
            shapeAsDict = json.loads(global_list[j])
            if shapeAsDict['id'] == i:
                named_shape = NamedShape(shapeAsDict['name'], shapeAsDict['shape'], shapeAsDict['id'])
                shapesToAdd.append(named_shape)

    
    # print("globallist: ", global_list)
    # for i in range(0, num_objects):
    #     shapeAsDict = json.loads(global_list[i])
    #     named_shape = NamedShape(shapeAsDict['name'], shapeAsDict['shape'], shapeAsDict['id'])
    #     shapesToAdd.append(named_shape)

    #Setup variables for return
    figure = go.Figure()
    for shape in shapesToAdd:
        figure.add_shape(shape.shape)
        annotate(figure, shape)

    figure.update_yaxes(
    scaleanchor = "x",
    scaleratio = 1,
    )
    return figure

@callback(
    Output('graph', 'figure'),
    Output('intermediate-value', 'data'),
    Output('global_list', 'data'),
    Output('next_id', 'data'),
    Output('step', 'data'),
    #Output('steps', 'steps_table'),
    Input('dropdown', 'value'),
    Input('intermediate-value', 'data'),
    Input('input1', 'value'),
    Input('global_list', 'data'), 
    Input('next_id', 'data'),
    Input('step', 'data'),
    Input('back_button', 'n_clicks'),
    Input('forward_button', 'n_clicks')
)
def update_graph(dropdown_value, figure_data, custom_input, global_list_data, id_val, step, Back, Forward):
    
    #print("in update")
    #------------Forward and Backwards Buttons----------------
    if "back_button" == ctx.triggered_id and dropdown_value != "reset" and dropdown_value != '':
        print("Back button was pressed")
        steps_value = json.loads(step)[0]
        if (steps_value == 0):  #Cannot decrement more
            print("Cannot decrement further")
            figure = go.Figure()
            figure.update_yaxes(
            scaleanchor = "x",
            scaleratio = 1,
            )
            return (figure, figure.to_json(), global_list_data, id_val, json.dumps([steps_value]))

        print(steps_value)
        steps_value = steps_value - 1
        figure = populate_figure_with_steps(global_list_data, steps_value, dropdown_value)
        
        return (figure, figure.to_json(), global_list_data, id_val, json.dumps([steps_value]))
    elif "forward_button" == ctx.triggered_id and dropdown_value != "reset" and dropdown_value  != '':
        print("Forward button was pressed")
        steps_value = json.loads(step)[0]
        obj = find_entry(dropdown_value)
        if (steps_value >= len(obj['list'])):
            print("Cannot increment further")
            dff = json.loads(figure_data)
            figure = go.Figure(dff)
            return (figure, figure.to_json(), global_list_data, id_val, json.dumps([steps_value]))
        steps_value += 1
        figure = populate_figure_with_steps(global_list_data, steps_value, dropdown_value)
        return (figure, figure.to_json(), global_list_data, id_val, json.dumps([steps_value]))
    #----------Normal Execution--------------------
    #Setup id
    next_id = 0
    if id_val != None:
        next_id = json.loads(id_val)[0]
    startingID = next_id
    #Get json object for dropdown
    construction = find_entry(dropdown_value)
    #Get figure
    figure = None
    if (figure_data == None or dropdown_value == "reset"):
        figure = go.Figure()
        next_id = 0
    else:
        dff = json.loads(figure_data)
        figure = go.Figure(dff)
    #Get global objects list
    global_list = []
    if (dropdown_value != "reset" and global_list_data != None):
        global_list = json.loads(global_list_data)
    #Get args
    args = None
    if custom_input != None and custom_input != '':
        args = json.loads(custom_input)
        if (len(args) != len(construction['fargs'])):
            print("Error: Incorrect length of arguments")
    new_id = inner_exec(dropdown_value, figure, global_list, next_id, args)
    endID = new_id
    if (construction != None):
        step_val = len(construction['list'])
    else:
        step_val = 0
    #Call inner_exec
    global_list_ret = None
    if (len(global_list) == 0):  
        return (figure, figure.to_json(), None, json.dumps([new_id]), json.dumps([step_val]))
    else:
        return (figure, figure.to_json(), json.dumps(global_list), json.dumps([new_id]), json.dumps([step_val]))
    
    

def annotate(fig, named_shape):
    shape = named_shape.shape
    midX = (shape['x1'] + shape['x0']) / 2
    midY = (shape['y1'] + shape['y0']) / 2
    off = 0
    midX = midX + off
    midY = midY - off
    fig.add_annotation(
        align = "right",
        valign='bottom',
        x = midX,
        y = midY,
        text = str(named_shape.id) + "(" + named_shape.name + ")",
        showarrow=True
    )

def get_label(named_shape):
    shape = named_shape.shape
    midX = (shape['x1'] + shape['x0']) / 2
    midY = (shape['y1'] + shape['y0']) / 2
    off = 0
    midX = midX + off
    midY = midY - off
    return go.Scatter(
        x=[midX],
        y=[midY],
        mode="lines+markers+text",
        name="Lines, Markers and Text",
        text=[named_shape.id],
        textposition="bottom center",
        fill=shape['line_color'] 
    )

