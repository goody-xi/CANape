import xlrd
import xlwt
from xlwt import *
import function


def xlwt_output_result_to_excel(Actual_Resp_Data_Variant):
    filename = "UDS_Test.xlsx"
    work_book_read = xlrd.open_workbook(filename)
    sheet_object = work_book_read.sheet_by_index(0)

    work_book_write = xlwt.Workbook(encoding='utf-8')
    work_sheet_write = work_book_write.add_sheet('sheet1')

    style_Pass = XFStyle()
    pattern_Pass = Pattern()
    pattern_Pass.pattern = Pattern.SOLID_PATTERN
    pattern_Pass.pattern_fore_colour = Style.colour_map['green']
    style_Pass.pattern = pattern_Pass

    style_Fail = XFStyle()
    pattern_Fail = Pattern()
    pattern_Fail.pattern = Pattern.SOLID_PATTERN
    pattern_Fail.pattern_fore_colour = Style.colour_map['red']
    style_Fail.pattern = pattern_Fail

    for i in range(sheet_object.nrows):
        for j in range(4):
            work_sheet_write.write(i, j, sheet_object.cell_value(i, j))

    work_sheet_write.write(0, 4, sheet_object.cell_value(0, 4))
    work_sheet_write.write(0, 5, sheet_object.cell_value(0, 5))

    nrows = 1
    for i in range(len(Actual_Resp_Data_Variant)):
        for j in range(len(Actual_Resp_Data_Variant[i])):
            work_sheet_write.write(nrows, 4, Actual_Resp_Data_Variant[i][j].upper())
            if 'security_access_cboot' in sheet_object.cell_value(nrows, 2):
                print('security_access_cboot')
                print(Actual_Resp_Data_Variant[i][j].split('/'))
                if ('67 35' in Actual_Resp_Data_Variant[i][j].split('/')[0]) and (
                        '67 36' in Actual_Resp_Data_Variant[i][j].split('/')[1]):
                    work_sheet_write.write(nrows, 5, "Pass ", style_Pass)
                else:
                    work_sheet_write.write(nrows, 5, "Fail ", style_Fail)
            elif 'security_access' in sheet_object.cell_value(nrows, 2):
                print('security_access')
                print(Actual_Resp_Data_Variant[i][j].split('/'))
                if ('67 01' in Actual_Resp_Data_Variant[i][j].split('/')[0]) and (
                        '67 02' in Actual_Resp_Data_Variant[i][j].split('/')[1]):
                    work_sheet_write.write(nrows, 5, "Pass ", style_Pass)
                else:
                    work_sheet_write.write(nrows, 5, "Fail ", style_Fail)
            else:
                if 'XX' in sheet_object.cell_value(nrows, 3):
                    list1 = sheet_object.cell_value(nrows, 3).split(' ')
                    list2 = Actual_Resp_Data_Variant[i][j][3:-1].upper().split(' ')
                    if(len(list1) == len(list2)
                       and function.judgestringequalin2list(list1, list2)):
                        work_sheet_write.write(nrows, 5, "Pass ", style_Pass)
                    else:
                        work_sheet_write.write(nrows, 5, "Fail ", style_Fail)
                elif '---' in sheet_object.cell_value(nrows, 3):
                    string1 = sheet_object.cell_value(nrows, 3).replace(' ','').replace('---', '')
                    string2 = Actual_Resp_Data_Variant[i][j][3:-1].upper().replace(' ', '')
                    print(string1 + " : " + string2)
                    if string1 in string2:
                        work_sheet_write.write(nrows, 5, "Pass ", style_Pass)
                    else:
                        work_sheet_write.write(nrows, 5, "Fail ", style_Fail)
                else:
                    if sheet_object.cell_value(nrows, 3) == (Actual_Resp_Data_Variant[i][j][3:-1].upper()):
                        work_sheet_write.write(nrows, 5, "Pass ", style_Pass)
                    else:
                        work_sheet_write.write(nrows, 5, "Fail ", style_Fail)
            nrows = nrows + 1
    work_book_write.save("UDS_Test_Result.xls")
