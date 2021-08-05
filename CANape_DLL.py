# -*- coding:utf-8 -*-

import os
import ctypes
import ctypes.wintypes
import time
import function
import xlrd_import_excel
import xlwt_output_excel
import security_access


class TTaskInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('description', ctypes.c_char_p), ('taskId', ctypes.c_ushort)]


class TCalibrationObjectValueEx(ctypes.Union):
    class value_t(ctypes.Structure):
        _pack_ = 1
        _fields_ = [('type', ctypes.c_int), ('value', ctypes.c_double)]

    class axis_t(ctypes.Structure):
        _pack_ = 1
        _fields_ = [('type', ctypes.c_int),
                    ('dimension', ctypes.c_short),
                    ('pAxis', ctypes.POINTER(ctypes.c_double)),
                    ('oAxis', ctypes.c_ulong)]

    class ascii_t(ctypes.Structure):
        _pack_ = 1
        _fields_ = [('type', ctypes.c_int),
                    ('len', ctypes.c_short),
                    ('pAscii', ctypes.c_char_p),
                    ('oAscii', ctypes.c_ulong)]

    class curve_t(ctypes.Structure):
        _pack_ = 1
        _fields_ = [('type', ctypes.c_int),
                    ('dimension', ctypes.c_short),
                    ('pAxis', ctypes.POINTER(ctypes.c_double)),
                    ('oAxis', ctypes.c_ulong),
                    ('pValues', ctypes.POINTER(ctypes.c_double)),
                    ('oValues', ctypes.c_ulong)]

    class map_t(ctypes.Structure):
        _pack_ = 1
        _fields_ = [('type', ctypes.c_int),
                    ('xDimension', ctypes.c_short),
                    ('yDimension', ctypes.c_short),
                    ('pXAxis', ctypes.POINTER(ctypes.c_double)),
                    ('oXAxis', ctypes.c_ulong),
                    ('pYAxis', ctypes.POINTER(ctypes.c_double)),
                    ('oYAxis', ctypes.c_ulong),
                    ('pValues', ctypes.POINTER(ctypes.c_double)),
                    ('oValues', ctypes.c_ulong)]

    _pack_ = 1
    _fields_ = [('type', ctypes.c_int),
                ('value', value_t),
                ('axis', axis_t),
                ('ascii', ascii_t),
                ('curve', curve_t),
                ('map', map_t)]
    del value_t
    del axis_t
    del ascii_t
    del curve_t
    del map_t


# 从UDS_Test.xlsx中获取数据
Test_Case_Num = xlrd_import_excel.xlrd_import_excel_info()[0]
Req_Data_Variant = xlrd_import_excel.xlrd_import_excel_info()[1]
Expected_Resp_Data_Variant = xlrd_import_excel.xlrd_import_excel_info()[2]
Actual_Resp_Data_Variant = [[] for i in range(Test_Case_Num)]

print('Test Case Number : %d' % Test_Case_Num)
print('Request Data Variant %s' % str(Req_Data_Variant))
print('Expected Response Data Variant %s' % str(Expected_Resp_Data_Variant))

myLibrary = ctypes.LibraryLoader(ctypes.WinDLL).LoadLibrary(
    "C:\\Program Files (x86)\\Vector CANape 16\\CANapeAPI\\CANapAPI64.dll")

#  句柄 用于传递数据
myHandle = ctypes.c_long(1)
MyXCPMdlHandle = ctypes.c_long(1)
MyDiagMdlHandle = ctypes.c_long(1)

# 变量定义
myWorkingDir = ctypes.c_char_p("D:\\Temp\\Test")
myDebugMode = ctypes.c_bool(True)
myClearDevList = ctypes.c_bool(False)
myModalMode = ctypes.c_bool(False)
myHexMode = ctypes.c_bool(False)
myOnline = ctypes.c_bool(True)
myResponseID = ctypes.c_long(0x7CD)
myDwSize = ctypes.wintypes.DWORD()
myCountResponse = ctypes.c_int(1024)
myServiceState = ctypes.c_int(0)

print('Start Asap3Init5')
ret = myLibrary.Asap3Init5(ctypes.byref(myHandle), ctypes.c_long(120000), myWorkingDir, ctypes.c_long(2048),
                           ctypes.c_long(1024), myDebugMode, myClearDevList, myHexMode, myModalMode)

file_CDD_Dir = "D:\\02_Projects\\02_GWM_ACU\\CANape\\ACU_CANape_ASW_L2_B6\\eAD_ACU.cdd"
MyUDSMdlHandle = ctypes.c_long(1)
myLibrary.Asap3CreateModule2(myHandle, 'Diag', file_CDD_Dir, 70, 2, ctypes.c_bool(True), ctypes.pointer(MyUDSMdlHandle))

myLibrary.Asap3DiagEnableTesterPresent(myHandle, MyUDSMdlHandle, ctypes.c_bool(False))

for l in range(len(Req_Data_Variant)):
    for j in range(len(Req_Data_Variant[l])):
        list_Req = Req_Data_Variant[l][j].split(' ')
        list_req_deal = []
        if Req_Data_Variant[l][j] == 'security_access':
            byteArray = (ctypes.wintypes.BYTE * 2)(*([0x27, 0x01]))
            myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray,
                                                ctypes.c_int(2), ctypes.pointer(MyDiagMdlHandle))
            myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
            time.sleep(2)

            myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(), ctypes.byref(myDwSize),
                                                 myResponseID)
            byteArray_rec = (ctypes.wintypes.BYTE * myDwSize.value)()
            myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.byref(byteArray_rec),
                                                 ctypes.byref(myDwSize), myResponseID)
            string_response = ""
            string_response_2701_rec = ''
            for i in tuple(byteArray_rec):
                if i < 0:
                    temp_string = format(2 ** 8 + int(i), 'x').zfill(2)
                else:
                    temp_string = format(int(i), 'x').zfill(2)
                string_response = string_response + temp_string + " "
            string_response_2701_rec = (str(myDwSize.value).zfill(2) + " " + string_response).upper()

            byteArray_2702 = security_access.security_access(string_response.upper())
            byteArray_ = (ctypes.wintypes.BYTE * 6)(*byteArray_2702)
            myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray_,
                                                ctypes.c_int(6), ctypes.pointer(MyDiagMdlHandle))
            myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
            time.sleep(2)

            myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(), ctypes.byref(myDwSize),
                                                 myResponseID)
            byteArray_rec = (ctypes.wintypes.BYTE * myDwSize.value)()
            myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.byref(byteArray_rec),
                                                 ctypes.byref(myDwSize), myResponseID)
            string_response = ""
            string_response_2702_rec = ""
            for i in tuple(byteArray_rec):
                if i < 0:
                    temp_string = format(2 ** 8 + int(i), 'x').zfill(2)
                else:
                    temp_string = format(int(i), 'x').zfill(2)
                string_response = string_response + temp_string + " "
            string_response_2702_rec = (str(myDwSize.value).zfill(2) + " " + string_response).upper()
            print("string_response_2702_rec %s" % string_response_2702_rec)
            Actual_Resp_Data_Variant[l].append(string_response_2701_rec + "/" + string_response_2702_rec)

        else:
            list_req_deal = function.stringconvert2hexintinlist(list_Req)
            byteArray = (ctypes.wintypes.BYTE * len(list_req_deal))(*list_req_deal)
            myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray,
                                                ctypes.c_int(len(list_req_deal)), ctypes.pointer(MyDiagMdlHandle))
            myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
            time.sleep(2)

            myLibrary.Asap3DiagGetResponseCount(myHandle, MyDiagMdlHandle, ctypes.byref(myCountResponse))

            myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(), ctypes.byref(myDwSize),
                                                 myResponseID)

            byteArray_rec = (ctypes.wintypes.BYTE * myDwSize.value)()
            myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.byref(byteArray_rec),
                                                 ctypes.byref(myDwSize), myResponseID)

            string_response = ""
            for i in tuple(byteArray_rec):
                if i < 0:
                    temp_string = format(2 ** 8 + int(i), 'x').zfill(2)
                else:
                    temp_string = format(int(i), 'x').zfill(2)
                string_response = string_response + temp_string + " "
            print('     %s %s' % (str(myDwSize.value).zfill(2), string_response))
            Actual_Resp_Data_Variant[l].append(str(myDwSize.value).zfill(2) + " " + string_response)

print('Actual Response Data Variant %s' % str(Actual_Resp_Data_Variant))

xlwt_output_excel.xlwt_output_result_to_excel(Actual_Resp_Data_Variant)

'''
file_a2l_Dir = "D:\\02_Projects\\02_GWM_ACU\CANape\\ACU_CANape_ASW_L2_B6\\20201117_GWV_CRB302_CAAA_B1_71.a2l"
print('Start Asap3CreateModule2')
ret = myLibrary.Asap3CreateModule(myHandle, 'GWM_eAD', file_a2l_Dir, 2, 1, ctypes.pointer(MyXCPMdlHandle))

x_Dimension = ctypes.c_int(10)
y_Dimension = ctypes.c_int(10)
print('x_Dimension %d' %(x_Dimension.value))
print('y_Dimension %d' %(y_Dimension.value))
myLibrary.Asap3CalibrationObjectInfo(myHandle,MyXCPMdlHandle,'SicL2_TmHcuMsgCrcErr_cs',ctypes.byref(x_Dimension),ctypes.byref(y_Dimension))
print('x_Dimension %d' %(x_Dimension.value))
print('y_Dimension %d' %(y_Dimension.value))


myLibrary.Asap3ECUOnOffline(myHandle, MyXCPMdlHandle, 0, True)


State = ctypes.c_long(10)
print('State First %d' %State.value)
myLibrary.Asap3IsECUOnline(myHandle,MyXCPMdlHandle,ctypes.pointer(State))
print('State Second %d' %State.value)


maxTaskInfo = 10
ttTaskInfo = (TTaskInfo*10)()
noTasks = ctypes.c_ushort()

myLibrary.Asap3GetEcuTasks(myHandle, MyXCPMdlHandle, ttTaskInfo, ctypes.byref(noTasks), ctypes.c_ushort(maxTaskInfo))
print('no tasks is : %d'%(noTasks.value))

##!!!!taskInfo Define
for i in range(noTasks.value):
    print('Task %d' %i)
    print('   Task Id %i' %ttTaskInfo[i].taskId)

myLibrary.Asap3ResetDataAcquisitionChnls(myHandle)

taskId = ctypes.c_ushort()
downSampling = ctypes.c_ushort()
myLibrary.Asap3GetChnlDefaultRaster(myHandle,MyXCPMdlHandle,'SicL2_TmHcuMsgCrcErr_cs',ctypes.byref(taskId),ctypes.byref(downSampling))
print(taskId.value)
print(downSampling.value)

### taskId 0 for polling mode 10 for 2.5ms task 11 for 5ms task, 12 for 10ms task 13 for 100ms task 14 for 500ms task
myLibrary.Asap3SetupDataAcquisitionChnl(myHandle, MyXCPMdlHandle, 'SicL2_TmHcuMsgCrcErr_cs', 0, 12, 1, True)
myLibrary.Asap3SetupDataAcquisitionChnl(myHandle, MyXCPMdlHandle, 'FsmL2_StBLDCEmgySftG2ToNMont', 0, 12, 1, True)
myLibrary.Asap3SetupDataAcquisitionChnl(myHandle, MyXCPMdlHandle, 'FsmL2_TmBLDCMoveWoReq', 0, 12, 1, True)

myLibrary.Asap3StartDataAcquisition(myHandle)
time.sleep(10)
myValueCalib = TCalibrationObjectValueEx()
print('Asap3ReadCalibrationObject')
ret = myLibrary.Asap3ReadCalibrationObjectEx(myHandle, MyXCPMdlHandle, "SicL2_TmHcuMsgCrcErr_cs", 0, ctypes.byref(myValueCalib))
print('ret Asap3ReadCalibrationObject %d'%ret)
myValue = myValueCalib.value.value
print('SicL2_TmHcuMsgCrcErr_cs Value : %d' %myValue)

time.sleep(1)
myValueCalib.value.value = 200
ret = myLibrary.Asap3WriteCalibrationObject(myHandle, MyXCPMdlHandle, "SicL2_TmHcuMsgCrcErr_cs", 0, ctypes.byref(myValueCalib))

time.sleep(10)

myLibrary.Asap3StopDataAcquisition (myHandle)
time.sleep(5)

print(os.path.exists('D:\\Temp\\Test\\MatlabData.mat'))
if os.path.exists('D:\\Temp\\Test\\MatlabData.mat'):
    os.remove('D:\\Temp\\Test\\MatlabData.mat')
    print('MatlabData.mat file remove!!!!')
    time.sleep(2)

mdfFileName = ctypes.c_char_p('Recorder.MDF')
matlabFileName = ctypes.c_char_p('MatlabData.mat')
myLibrary.Asap3MatlabConversion(myHandle,mdfFileName,matlabFileName)
'''

ret = myLibrary.Asap3Exit(myHandle)
