def stringconvert2hexintinlist(lst_original):
    list_req_deal = []
    for k in lst_original:
        k = int(k, 16)
        list_req_deal.append(k)
    print(list_req_deal)
    return list_req_deal


def judgestringequalin2list(list1, list2):
    result = True
    for i in range(len(list1)):
        if list1[i] <> 'XX':
            if list1[i] <> list2[i]:
                result = False
                break
    return result
