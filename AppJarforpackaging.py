import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from appJar import gui

app = gui('Window', '1000x800')
app.showSplash("Detectors Incorporated \n Data Exploration Tool", fill='red', stripe='black', fg='white', font=64)
app.addLabel("title", "Sensor Data Exploration tool")
app.setLabelBg("title", "White")
app.setBg('silver')

startpos=0
filepath=""
##takes txt/csv, cleans it of errors from the trasmission from device to laptop, and returns pandas dataframe of the file
def data_to_parse(filepath):
    data=pd.read_csv(filepath, header = None,error_bad_lines=False)
    data.dropna(axis='columns',thresh=10,inplace=True)
    data.dropna(axis='rows',how='any',inplace=True)
    data.columns=['4.3um','3.8um','2.7um','UV','none1','none2','none3','4.3um25hz','3.8um25hz','2.7um25hz','DC','none4']
    parsed={'Ch1':data['4.3um'],'Ch2':data['3.8um'],'Ch3':data['2.7um'],'UV':data['UV']}
    df=pd.DataFrame(parsed)
    return df
##takes pandas dataframe, and produces graph from it.
def df_to_graph(df,plotname):
    fig = app.addPlotFig(plotname)
    ax = fig.add_subplot(111)
    ax.plot('Ch1',data=df,color='red')
    ax.plot('Ch2',data=df,color='green')
    ax.plot('Ch3',data=df,color='blue')
    ax.plot('UV',data=df,color='orange')
    ax.set_title(plotname)
    
##makes an array that is formated like an image for slicing
def df_to_numpyarr(df):
    global numpyarrlen
    df['maxir']=df[['Ch1','Ch2','Ch3']].max(axis=1)
    maxIR=df.maxir.max()
    if maxIR >255:
        scaling_factor=maxIR/255
    else: 
        scaling_factor =1
    df['scaled_Ch1']=(df['Ch1']/scaling_factor).round().astype(int)
    df['scaled_Ch2']=(df['Ch2']/scaling_factor).round().astype(int)
    df['scaled_Ch3']=(df['Ch3']/scaling_factor).round().astype(int)
    numpyarr=df[['scaled_Ch1','scaled_Ch2','scaled_Ch3']].to_numpy().astype(np.uint8)
    numpyarrlen=len(numpyarr)
    
    numpyarr=numpyarr.reshape(1,numpyarrlen,3)
    ##stacks it a few times so its not a 1 pixel line
    for i in range(5):
        numpyarr=np.vstack((numpyarr,numpyarr))
    ##makes a greyscale line for the UV
    df['scaled_UV']=(df['UV']/2).round().astype(int)
    
    UVarr=df[['scaled_UV']].to_numpy()
    UVarr=np.where(UVarr<255,UVarr,255).astype(np.uint8)
    UVlen=len(UVarr)
    UVarr=UVarr.reshape(1,UVlen,1)
    UVarrcopy=np.copy(UVarr)
    for j in range(2):
        UVarr=np.dstack((UVarr,UVarrcopy))
    for k in range(5):
        UVarr=np.vstack((UVarr,UVarr))
    UVIR_numpyarr=np.vstack((numpyarr,UVarr)).astype(np.uint8)
    return UVIR_numpyarr
        
    return numpyarr
def numpyarr_to_img(numpyarr,showall=0):
    global startpos
    start= startpos
    ##sets image window to 600 points, 2minutes at 5 samples per second
    stop=start+600
    ##toggles between showing all or 600 sample slice
    if showall==0:
        ##handles cases to prevent asking for slice outside of range
        if len(numpyarr[0])<600:
            start=0
            stop=600
        if len(numpyarr[0])<start:
            startpos=len(numpyarr[0])-150
            start=startpos
            stop=start+600
        if len(numpyarr[0])<stop:
            filler=np.zeros((64,600,3))
            numpyarr=np.hstack((numpyarr,filler))
         #returns RGB image of slice
        numpyslice=numpyarr[:,start:stop,:].astype(np.uint8)
    else:
        numpyslice=numpyarr
    im = Image.fromarray(numpyslice)
    fire_pic = ImageTk.PhotoImage(im)
    return fire_pic

## updates the opened data file
def show_data():
    global filepath
    filepath=app.getEntry("datafile")
    app.reloadImageData("fire_pic_all", numpyarr_to_img(df_to_numpyarr(data_to_parse(filepath)),showall=1), fmt="PhotoImage")
    app.reloadImageData("fire_pic", numpyarr_to_img(df_to_numpyarr(data_to_parse(filepath))), fmt="PhotoImage")
    df_to_graph(data_to_parse(filepath),"Opened Data")

## defines which options show which data
def show_compare():
    option=app.getOptionBox("Compare Light Source")
    if option=="flourescent":
        app.reloadImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("flourescentLamp6inrandommod.txt"))), fmt="PhotoImage")
    if option=="Halogen":
        app.reloadImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("halogensim.txt"))), fmt="PhotoImage")
    if option=="Blackbody Radiation 370C":
        app.reloadImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("blackbodysim.txt"))), fmt="PhotoImage")
    if option=="ArcWelding":
        app.reloadImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("arcweldingsim.txt"))), fmt="PhotoImage")
    if option=="Methane":
        app.reloadImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("methane.txt"))), fmt="PhotoImage")
    if option=="Acetylene.txt":
        app.reloadImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("acetylene.txt"))), fmt="PhotoImage")
    

## makes afile-path finding entry that updates the images and plots when changed
app.addFileEntry("datafile")
app.setEntryChangeFunction("datafile", show_data)

## makes a drop down menu that updates the fire-color image to the selected type for comparisons
app.addOptionBox("Compare Light Source", ["Methane","Acetylene","flourescent","ArcWelding", "Halogen", "handwave", "Blackbody Radiation 370C","flourescent Through PP Window", "Halogen Through PP Window", "Handwave Through PP Window", "Blackbody Radiation 370C Through PP Window"])
app.setOptionBoxChangeFunction("Compare Light Source",show_compare)


## setting functions for navigation buttons
def press(btnName):
    global startpos
    global filepath
    if btnName == ">>>":
        startpos+=150
        app.reloadImageData("fire_pic",numpyarr_to_img(df_to_numpyarr(data_to_parse(filepath))), fmt="PhotoImage")
    if btnName == "<<<":
        startpos-=150
        if startpos<0:
            startpos=0
        app.reloadImageData("fire_pic",numpyarr_to_img(df_to_numpyarr(data_to_parse(filepath))), fmt="PhotoImage")

## buttoms for navigating opened file and instantiating image blocks to be updaded with dif pictures
app.addButtons( ["<<<", ">>>"], press, colspan=2)
app.addImageData("fire_pic_all", numpyarr_to_img(df_to_numpyarr(data_to_parse("blank.txt")),showall=1), fmt="PhotoImage")
app.addImageData("fire_pic", numpyarr_to_img(df_to_numpyarr(data_to_parse("blank.txt"))), fmt="PhotoImage")
app.addImageData("FAsources", numpyarr_to_img(df_to_numpyarr(data_to_parse("blank.txt"))), fmt="PhotoImage")

##Launches app
app.go()