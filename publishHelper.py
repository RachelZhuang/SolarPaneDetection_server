#-*-coding:utf-8
__author__ = 'suwen'
import os
import arcpy
import xml.dom.minidom as DOM
def CreateContectionFile(wrkspc,userName,password,serverName):
    con="http://"+str(serverName)+":6080/arcgis/admin"
    connection_file_path=str(wrkspc)+"/tmp.ags"
    #
    if os.path.exists(connection_file_path):
        os.remove(connection_file_path)
    agsname=os.path.basename(connection_file_path)
    arcpy.mapping.CreateGISServerConnectionFile("ADMINISTER_GIS_SERVICES",
                                                    wrkspc,
                                                    agsname,
                                                    con,
                                                    "ARCGIS_SERVER",
                                                    username=userName,
                                                    password=password,
                                                    save_username_password=True)

    return connection_file_path


def PublishService(connection_file_path,wrkspc,mapDoc):
    #get the serviceName
    serviceName =os.path.basename(mapDoc).replace(".mxd","")

    #create the .sddraft path
    sddraftname=os.path.basename(mapDoc).replace(".mxd",".sddraft")
    sddraft =str(wrkspc)+"/"+str(sddraftname)
    #create the .sd file path
    sdname=os.path.basename(mapDoc).replace(".mxd",".sd")
    sd=str(wrkspc)+"/"+str(sdname)
    #check the file exists or not
    if(os.path.exists(sd)):
        os.remove(sd)

    analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, serviceName, 'ARCGIS_SERVER',
                                              connection_file_path, True, '',None,None)
    #启用WMS
    doc = DOM.parse(sddraft)
    typeNames = doc.getElementsByTagName('TypeName')
    for typeName in typeNames:
      if typeName.firstChild.data == 'WMSServer':
        extention = typeName.parentNode
        for extElement in extention.childNodes:
            if extElement.tagName == 'Enabled':
                extElement.firstChild.data = 'true'

    f = open(sddraft,'w')
    doc.writexml(f, encoding='utf-8')
    f.close()

    arcpy.StageService_server(sddraft, sd)
    arcpy.UploadServiceDefinition_server(sd, connection_file_path)


def Publish(wrkspc,userName,password,serverName,mxdfolder):
    connection_file_path=CreateContectionFile(wrkspc,userName,password,serverName)
    mxds=os.listdir(mxdfolder)
    mxd_files=[]
    for file in mxds:
        if file.endswith(".mxd"):
            mxdpath=os.path.join(mxdfolder,file)
            mxd_files.append(mxdpath)

    for mxd in mxd_files:
        PublishService(connection_file_path,wrkspc,mxd)

# connection_file_path="D:\MxdPublisher"
# mxdfolder=u"D:\MxdPublisher"
# wrkspc=r"D:\MxdPublisher"
# serverName="localhost"
# userName="admin"
# password="jack121"
#
