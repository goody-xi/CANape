#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
from Tkinter import Tk
import tkFileDialog
import os
import Exception_Error
import xlrd_import_excel
import xlwt_output_excel
import ctypes
import ctypes.wintypes
import time
import security_access
import function
import threading

window = Tk()  # type: Tk

window.title('CANapeForUDS')

window.geometry('650x550')

label_main = Label(window, text='UDS On Excel By CANape', font=("Arial", 20)).place(x=80, y=30)

label_Cdd_File = Label(window, text="Cdd File Location : ").place(x=10, y=100)

label_a2l_File = Label(window, text="A2L File Location : ").place(x=10, y=150)

label_Mask = Label(window, text="Security Access Mask : ").place(x=10, y=200)

text_result = Text(window, width=70, height=15)
scroll = Scrollbar(window)

scroll.config(command=text_result.yview)
text_result.config(yscrollcommand=scroll.set)

scroll.pack(side=RIGHT, fill=Y)
text_result.place(x=10, y=250)

Cdd_File_String = StringVar()
Cdd_File_String.set("Default")
Cdd_File_Entry = Entry(window, textvariable=Cdd_File_String, width=30).place(x=150, y=100)


def cmd_cdd():
    filename = tkFileDialog.askopenfilename(title='choose CDD file', filetypes=[('cdd', '*.cdd'), ('All Files', '*')])
    filename_relative = os.path.relpath(filename, os.getcwd())
    Cdd_File_String.set(filename_relative)
    # print(os.getcwd())


BTN_Choose_CDD_File = Button(window, text='choose CDD file', command=cmd_cdd, width=15).place(x=350, y=95)

A2L_File_String = StringVar()
A2L_File_String.set("Default")
A2L_File_Entry = Entry(window, textvariable=A2L_File_String, width=30).place(x=150, y=150)


def cmd_a2l():
    filename = tkFileDialog.askopenfilename(title='choose A2L file', filetypes=[('a2l', '*.a2l'), ('All Files', '*')])
    filename_relative = os.path.relpath(filename, os.getcwd())
    A2L_File_String.set(filename_relative)


BTN_Choose_A2L_File = Button(window, text='choose A2L file', command=cmd_a2l, width=15).place(x=350, y=145)

Mask_Int = StringVar()
Mask_Int.set('0x4d424120')
Mask_Entry = Entry(window, textvariable=Mask_Int, width=30).place(x=150, y=200)


def thread_start():
    T = threading.Thread(target=uds_start, args=())
    T.start()


def uds_start():
    text_result.delete(0.0, END)
    print('a2l file string : %s' % A2L_File_String.get())
    print('cdd file string : %s' % Cdd_File_String.get())
    print('mask string : %s' % Mask_Int.get())
    if '.a2l' not in A2L_File_String.get():
        Exception_Error.a2l_file_error()
    elif '.cdd' not in Cdd_File_String.get():
        Exception_Error.cdd_file_error()
    else:
        xlrd_result = xlrd_import_excel.xlrd_import_excel_info()
        print(xlrd_result)
        text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
        text_result.insert('insert', 'Test Case Num : %i \n' % xlrd_result[0])

        text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
        text_result.insert('insert', 'Import Test Cases Done ! \n')
        myLibrary = ctypes.LibraryLoader(ctypes.WinDLL).LoadLibrary(
            "C:\\Program Files (x86)\\Vector CANape 16\\CANapeAPI\\CANapAPI64.dll")

        #  句柄 用于传递数据
        myHandle = ctypes.c_long(1)
        MyXCPMdlHandle = ctypes.c_long(1)
        MyDiagMdlHandle = ctypes.c_long(1)

        # 变量定义
        myWorkingDir = ctypes.c_char_p("D:\\00_pycharm\\CANape\\Temp")
        myDebugMode = ctypes.c_bool(True)
        myClearDevList = ctypes.c_bool(False)
        myModalMode = ctypes.c_bool(False)
        myHexMode = ctypes.c_bool(False)
        MyUDSMdlHandle = ctypes.c_long(1)
        myOnline = ctypes.c_bool(True)
        # myResponseID = ctypes.c_long(0x7CD)
        myResponseID = ctypes.c_long(0)
        myDwSize = ctypes.wintypes.DWORD()
        myDwSize_2702 = ctypes.wintypes.DWORD()
        myCountResponse = ctypes.c_int(1024)
        myServiceState = ctypes.c_int(0)

        text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
        text_result.insert('insert', 'Start ASAP3 Init\n')
        text_result.see(END)

        myLibrary.Asap3Init5(ctypes.byref(myHandle), ctypes.c_long(120000), myWorkingDir, ctypes.c_long(2048),
                             ctypes.c_long(1024), myDebugMode, myClearDevList, myHexMode, myModalMode)

        text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
        text_result.insert('insert', 'Start ASAP3 DONE\n')
        text_result.see(END)

        cdd_file_relative_path = str(Cdd_File_String.get())

        text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
        text_result.insert('insert', os.path.abspath(cdd_file_relative_path) + '\n')
        text_result.see(END)

        file_CDD_Dir = os.path.abspath(cdd_file_relative_path)

        myLibrary.Asap3CreateModule2(myHandle, 'Diag', file_CDD_Dir, 70, 2, ctypes.c_bool(True),
                                     ctypes.pointer(MyUDSMdlHandle))
        myLibrary.Asap3DiagEnableTesterPresent(myHandle, MyUDSMdlHandle, ctypes.c_bool(False))

        Req_Data_Variant = xlrd_result[1]
        Actual_Resp_Data_Variant = [[] for i in range(xlrd_result[0])]
        for l in range(len(Req_Data_Variant)):
            for j in range(len(Req_Data_Variant[l])):
                list_Req = Req_Data_Variant[l][j].split(' ')
                list_req_deal = []
                if 'wait' in Req_Data_Variant[l][j]:
                    time_wait = float(Req_Data_Variant[l][j].split(" ")[1])
                    time.sleep(time_wait)
                    Actual_Resp_Data_Variant[l].append(" ")
                elif Req_Data_Variant[l][j] == 'security_access_cboot':
                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert',
                                       'request data : %s Done ! \n' % str(Req_Data_Variant[l][j]).ljust(35, ' '))
                    text_result.see(END)
                    byteArray = (ctypes.wintypes.BYTE * 2)(*([0x27, 0x35]))

                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert', '               %s Done ! \n' % str('[27 35]').ljust(35, ' '))
                    text_result.see(END)

                    myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray,
                                                        ctypes.c_int(2), ctypes.pointer(MyDiagMdlHandle))
                    myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
                    time.sleep(1)

                    myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(),
                                                         ctypes.byref(myDwSize),
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
                    string_response_2701_rec = (str(myDwSize.value).zfill(2) + " " + string_response).upper()

                    Mask_Int_Int = int(Mask_Int.get(), 16)

                    byteArray_2702 = security_access.security_access_cboot(string_response.upper(), Mask_Int_Int)
                    byteArray_ = (ctypes.wintypes.BYTE * 6)(*byteArray_2702)

                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert', '               %s Done ! \n' % str(byteArray_2702).ljust(35, ' '))
                    text_result.see(END)

                    myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray_,
                                                        ctypes.c_int(6), ctypes.pointer(MyDiagMdlHandle))
                    myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
                    time.sleep(1)

                    myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(),
                                                         ctypes.byref(myDwSize_2702), myResponseID)

                    byteArray_rec = (ctypes.wintypes.BYTE * myDwSize_2702.value)()
                    myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.byref(byteArray_rec),
                                                         ctypes.byref(myDwSize_2702), myResponseID)
                    tuple_zero = (0, 0)
                    print(tuple(byteArray_rec))

                    string_response = ""
                    for i in tuple(byteArray_rec):
                        if i < 0:
                            temp_string = format(2 ** 8 + int(i), 'x').zfill(2)
                        else:
                            temp_string = format(int(i), 'x').zfill(2)
                        string_response = string_response + temp_string + " "
                    string_response_2702_rec = (str(myDwSize_2702.value).zfill(2) + " " + string_response).upper()
                    print("string_response_2702_rec %s" % string_response_2702_rec)
                    Actual_Resp_Data_Variant[l].append(string_response_2701_rec + "/" + string_response_2702_rec)
                elif Req_Data_Variant[l][j] == 'security_access':
                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert',
                                       'request data : %s Done ! \n' % str(Req_Data_Variant[l][j]).ljust(35, ' '))
                    text_result.see(END)
                    byteArray = (ctypes.wintypes.BYTE * 2)(*([0x27, 0x01]))

                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert', '               %s Done ! \n' % str('[27 01]').ljust(35, ' '))
                    text_result.see(END)

                    myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray,
                                                        ctypes.c_int(2), ctypes.pointer(MyDiagMdlHandle))
                    myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
                    time.sleep(1)

                    myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(),
                                                         ctypes.byref(myDwSize),
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
                    string_response_2701_rec = (str(myDwSize.value).zfill(2) + " " + string_response).upper()

                    Mask_Int_Int = int(Mask_Int.get(), 16)

                    byteArray_2702 = security_access.security_access(string_response.upper(), Mask_Int_Int)
                    byteArray_ = (ctypes.wintypes.BYTE * 6)(*byteArray_2702)

                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert', '               %s Done ! \n' % str(byteArray_2702).ljust(35, ' '))
                    text_result.see(END)

                    myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray_,
                                                        ctypes.c_int(6), ctypes.pointer(MyDiagMdlHandle))
                    myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
                    time.sleep(1)

                    myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(),
                                                         ctypes.byref(myDwSize_2702), myResponseID)

                    byteArray_rec = (ctypes.wintypes.BYTE * myDwSize_2702.value)()
                    myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.byref(byteArray_rec),
                                                         ctypes.byref(myDwSize_2702), myResponseID)
                    tuple_zero = (0, 0)
                    print(tuple(byteArray_rec))

                    string_response = ""
                    for i in tuple(byteArray_rec):
                        if i < 0:
                            temp_string = format(2 ** 8 + int(i), 'x').zfill(2)
                        else:
                            temp_string = format(int(i), 'x').zfill(2)
                        string_response = string_response + temp_string + " "
                    string_response_2702_rec = (str(myDwSize_2702.value).zfill(2) + " " + string_response).upper()
                    print("string_response_2702_rec %s" % string_response_2702_rec)
                    Actual_Resp_Data_Variant[l].append(string_response_2701_rec + "/" + string_response_2702_rec)
                else:
                    list_req_deal = function.stringconvert2hexintinlist(list_Req)
                    print(list_Req)
                    print(list_req_deal)
                    byteArray = (ctypes.wintypes.BYTE * len(list_req_deal))(*list_req_deal)
                    print(tuple(byteArray))
                    myLibrary.Asap3DiagCreateRawRequest(myHandle, MyUDSMdlHandle, byteArray,
                                                        ctypes.c_int(len(list_req_deal)),
                                                        ctypes.pointer(MyDiagMdlHandle))
                    myLibrary.Asap3DiagExecute(myHandle, MyDiagMdlHandle, ctypes.c_bool(False))
                    time.sleep(2)

                    myServiceState = ctypes.c_int(0)
                    myLibrary.Asap3DiagGetServiceState(myHandle, MyDiagMdlHandle, ctypes.byref(myServiceState))
                    print(myServiceState.value)
                    while myServiceState.value < 25:
                        time.sleep(2)
                        myLibrary.Asap3DiagGetServiceState(myHandle, MyDiagMdlHandle, ctypes.byref(myServiceState))
                        print(myServiceState.value)

                    myCountResponse = ctypes.c_int(0)
                    myLibrary.Asap3DiagGetResponseCount(myHandle, MyDiagMdlHandle, ctypes.byref(myCountResponse))
                    print(myCountResponse.value)

                    if myCountResponse.value == 0:
                        Actual_Resp_Data_Variant[l].append(" ")
                    else:
                        myLibrary.Asap3DiagGetResponseStream(myHandle, MyDiagMdlHandle, ctypes.c_void_p(),
                                                             ctypes.byref(myDwSize),
                                                             myResponseID)
                        print(myDwSize.value)

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

                    text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
                    text_result.insert('insert', 'request data : %s Done ! \n' % str(list_req_deal).ljust(35, ' '))
                    text_result.see(END)

                    myLibrary.Asap3DiagReleaseService(myHandle, MyDiagMdlHandle)

        ret = myLibrary.Asap3Exit(myHandle)

        xlwt_output_excel.xlwt_output_result_to_excel(Actual_Resp_Data_Variant)

        text_result.insert('insert', time.strftime("%H:%M:%S", time.localtime()) + '  ')
        text_result.insert('insert', 'Output Test Result Done ! \n')
        text_result.see(END)


BTN_Start = Button(window, text='Start', command=thread_start, width=15, height=1).place(x=350, y=195)
window.mainloop()
