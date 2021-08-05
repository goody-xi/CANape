import xlrd
import xlwt


def xlrd_import_excel_info():
    work_book = xlrd.open_workbook('UDS_Test.xlsx')
    #sheet_names = work_book.sheet_names()
    sheet_object = work_book.sheet_by_index(0)

# ----------initial parameter----------
    Test_Case_Num = 0
    Test_Case_Array = []
# ----------initial parameter end------

# ----------Analyze Num Of Test Case----------
    for i in range(1, sheet_object.nrows):
        if sheet_object.cell_value(i, 0) != '':
            Test_Case_Num = Test_Case_Num + 1
            Test_Case_Array.append(i)
    Test_Case_Array.append(sheet_object.nrows)
# ----------Analyze Num Of Test Case End------

# ----------Initial List For Parameter Input----------
    Req_Data_Variant = [[] for i in range(Test_Case_Num)]
    Expected_Resp_Data_Variant = [[] for i in range(Test_Case_Num)]


# ----------Initial List For Parameter Input End------

# ----------Set Value from Excel to Each Patameters---------------
    for i in range(Test_Case_Num):
        for j in range(Test_Case_Array[i], Test_Case_Array[i + 1]):
            Req_Data_Variant[i].append(sheet_object.cell_value(j, 2))
            Expected_Resp_Data_Variant[i].append(sheet_object.cell_value(j, 3))
# ----------Set Value from Excel to Each Patameters End-----------

    return Test_Case_Num, Req_Data_Variant, Expected_Resp_Data_Variant