def security_access(string_response, mask_int):
    seed = string_response.split(' ')[2:6]
    seed_deal = '0x'
    # for i in seed:
    seed_deal = ''.join(seed)
    key = [0, 0, 0, 0]
    # mask = 0x20414355
    mask = mask_int
    wort = eval("0x" + seed_deal + "L")
    i = 0
    for i in range(35):
        if wort & 0x80000000:
            wort = wort << 1
            wort = wort ^ mask
        else:
            wort = wort << 1
    key[0] = (wort & 0xFF000000) >> 24
    key[1] = (wort & 0x00FF0000) >> 16
    key[2] = (wort & 0x0000FF00) >> 8
    key[3] = (wort & 0x000000FF)
    bytearray_2702 = [0x27, 0x02, key[0], key[1], key[2], key[3]]
    return bytearray_2702


def security_access_cboot(string_response, mask_int):
    seed = string_response.split(' ')[2:6]
    seed_deal = '0x'
    # for i in seed:
    seed_deal = ''.join(seed)
    key = [0, 0, 0, 0]
    # mask = 0x20414355
    mask = mask_int
    wort = eval("0x" + seed_deal + "L")
    i = 0
    for i in range(35):
        if wort & 0x80000000:
            wort = wort << 1
            wort = wort ^ mask
        else:
            wort = wort << 1
    key[0] = (wort & 0xFF000000) >> 24
    key[1] = (wort & 0x00FF0000) >> 16
    key[2] = (wort & 0x0000FF00) >> 8
    key[3] = (wort & 0x000000FF)
    bytearray_2702 = [0x27, 0x036, key[0], key[1], key[2], key[3]]
    return bytearray_2702
