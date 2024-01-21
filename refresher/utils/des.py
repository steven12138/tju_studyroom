def generate_keys(key_byte):
    key = [0] * 56
    keys = [[] for _ in range(16)]
    loop = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    for i in range(7):
        for j in range(8):
            k = 7 - j
            key[i * 8 + j] = key_byte[8 * k + i]

    for i in range(16):
        for j in range(loop[i]):
            temp_left = key[0]
            temp_right = key[28]

            for k in range(27):
                key[k] = key[k + 1]
                key[28 + k] = key[29 + k]

            key[27] = temp_left
            key[55] = temp_right

        temp_key = [0] * 48
        temp_key_positions = [
            13, 16, 10, 23, 0, 4, 2, 27, 14, 5, 20, 9, 22, 18, 11, 3,
            25, 7, 15, 6, 26, 19, 12, 1, 40, 51, 30, 36, 46, 54, 29, 39,
            50, 44, 32, 47, 43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31
        ]

        for m, pos in enumerate(temp_key_positions):
            temp_key[m] = key[pos]

        keys[i] = temp_key

    return keys


def get_box_binary(i):
    binaries = [
        "0000", "0001", "0010", "0011",
        "0100", "0101", "0110", "0111",
        "1000", "1001", "1010", "1011",
        "1100", "1101", "1110", "1111"
    ]
    return binaries[i]


def finally_permute(end_byte):
    fp_byte = [
        end_byte[39], end_byte[7], end_byte[47], end_byte[15], end_byte[55], end_byte[23], end_byte[63], end_byte[31],
        end_byte[38], end_byte[6], end_byte[46], end_byte[14], end_byte[54], end_byte[22], end_byte[62], end_byte[30],
        end_byte[37], end_byte[5], end_byte[45], end_byte[13], end_byte[53], end_byte[21], end_byte[61], end_byte[29],
        end_byte[36], end_byte[4], end_byte[44], end_byte[12], end_byte[52], end_byte[20], end_byte[60], end_byte[28],
        end_byte[35], end_byte[3], end_byte[43], end_byte[11], end_byte[51], end_byte[19], end_byte[59], end_byte[27],
        end_byte[34], end_byte[2], end_byte[42], end_byte[10], end_byte[50], end_byte[18], end_byte[58], end_byte[26],
        end_byte[33], end_byte[1], end_byte[41], end_byte[9], end_byte[49], end_byte[17], end_byte[57], end_byte[25],
        end_byte[32], end_byte[0], end_byte[40], end_byte[8], end_byte[48], end_byte[16], end_byte[56], end_byte[24]
    ]
    return fp_byte


def p_permute(s_box_byte):
    p_box_permute = [
        s_box_byte[15], s_box_byte[6], s_box_byte[19], s_box_byte[20], s_box_byte[28], s_box_byte[11], s_box_byte[27],
        s_box_byte[16],
        s_box_byte[0], s_box_byte[14], s_box_byte[22], s_box_byte[25], s_box_byte[4], s_box_byte[17], s_box_byte[30],
        s_box_byte[9],
        s_box_byte[1], s_box_byte[7], s_box_byte[23], s_box_byte[13], s_box_byte[31], s_box_byte[26], s_box_byte[2],
        s_box_byte[8],
        s_box_byte[18], s_box_byte[12], s_box_byte[29], s_box_byte[5], s_box_byte[21], s_box_byte[10], s_box_byte[3],
        s_box_byte[24]
    ]
    return p_box_permute


def s_box_permute(expand_byte):
    s_box_byte = [0] * 32
    binary = ""
    s1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]]

    s2 = [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]]

    s3 = [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]]

    s4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]]

    s5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]]

    s6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]]

    s7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]]

    s8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]

    for m in range(8):
        i = expand_byte[m * 6 + 0] * 2 + expand_byte[m * 6 + 5]
        j = (expand_byte[m * 6 + 1] * 2 * 2 * 2
             + expand_byte[m * 6 + 2] * 2 * 2
             + expand_byte[m * 6 + 3] * 2
             + expand_byte[m * 6 + 4])

        if m == 0:
            binary = get_box_binary(s1[i][j])
        elif m == 1:
            binary = get_box_binary(s2[i][j])
        elif m == 2:
            binary = get_box_binary(s3[i][j])
        elif m == 3:
            binary = get_box_binary(s4[i][j])
        elif m == 4:
            binary = get_box_binary(s5[i][j])
        elif m == 5:
            binary = get_box_binary(s6[i][j])
        elif m == 6:
            binary = get_box_binary(s7[i][j])
        elif m == 7:
            binary = get_box_binary(s8[i][j])

        for n in range(4):
            s_box_byte[m * 4 + n] = int(binary[n])

    return s_box_byte


def xor(byte_one, byte_two):
    xor_byte = [0] * len(byte_one)
    for i in range(len(byte_one)):
        xor_byte[i] = byte_one[i] ^ byte_two[i]
    return xor_byte


def expand_permute(right_data):
    ep_byte = [0] * 48
    for i in range(8):
        if i == 0:
            ep_byte[i * 6] = right_data[31]
        else:
            ep_byte[i * 6] = right_data[i * 4 - 1]

        ep_byte[i * 6 + 1] = right_data[i * 4]
        ep_byte[i * 6 + 2] = right_data[i * 4 + 1]
        ep_byte[i * 6 + 3] = right_data[i * 4 + 2]
        ep_byte[i * 6 + 4] = right_data[i * 4 + 3]

        if i == 7:
            ep_byte[i * 6 + 5] = right_data[0]
        else:
            ep_byte[i * 6 + 5] = right_data[i * 4 + 4]
    return ep_byte


def dec(data_byte, key_byte):
    keys = generate_keys(key_byte)
    ip_byte = init_permute(data_byte)
    ip_left = [0] * 32
    ip_right = [0] * 32
    temp_left = [0] * 32
    for k in range(32):
        ip_left[k] = ip_byte[k]
        ip_right[k] = ip_byte[32 + k]

    for i in range(15, -1, -1):
        for j in range(32):
            temp_left[j] = ip_left[j]
            ip_left[j] = ip_right[j]

        key = [0] * 48
        for m in range(48):
            key[m] = keys[i][m]

        temp_right = xor(p_permute(s_box_permute(xor(expand_permute(ip_right), key))), temp_left)
        for n in range(32):
            ip_right[n] = temp_right[n]

    final_data = [0] * 64
    for i in range(32):
        final_data[i] = ip_right[i]
        final_data[32 + i] = ip_left[i]

    return finally_permute(final_data)


def init_permute(original_data):
    ip_byte = [0] * 64
    for i in range(4):
        for j in range(7, -1, -1):
            ip_byte[i * 8 + 7 - j] = original_data[j * 8 + i * 2 + 1]
            ip_byte[i * 8 + 7 - j + 32] = original_data[j * 8 + i * 2]
    return ip_byte


def enc(data_byte, key_byte):
    keys = generate_keys(key_byte)
    ip_byte = init_permute(data_byte)
    ip_left = [0] * 32
    ip_right = [0] * 32
    temp_left = [0] * 32
    for k in range(32):
        ip_left[k] = ip_byte[k]
        ip_right[k] = ip_byte[32 + k]

    for i in range(16):
        for j in range(32):
            temp_left[j] = ip_left[j]
            ip_left[j] = ip_right[j]

        key = [0] * 48
        for m in range(48):
            key[m] = keys[i][m]

        temp_right = xor(p_permute(s_box_permute(xor(expand_permute(ip_right), key))), temp_left)
        for n in range(32):
            ip_right[n] = temp_right[n]

    final_data = [0] * 64
    for i in range(32):
        final_data[i] = ip_right[i]
        final_data[32 + i] = ip_left[i]

    return finally_permute(final_data)


def bt4_to_hex(binary):
    switcher = {
        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "A",
        "1011": "B",
        "1100": "C",
        "1101": "D",
        "1110": "E",
        "1111": "F",
    }
    return switcher.get(binary)


def hex_to_bt4(hex_char):
    switcher = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    return switcher.get(hex_char)


def byte_to_string(byte_data):
    string = ""
    for i in range(4):
        count = 0
        for j in range(16):
            pow = 1
            for m in range(15, j, -1):
                pow *= 2
            count += byte_data[16 * i + j] * pow
        if count != 0:
            string += chr(count)
    return string


def bt64_to_hex(byte_data):
    hex_str = ""
    for i in range(16):
        bt = ""
        for j in range(4):
            bt += str(byte_data[i * 4 + j])
        hex_str += bt4_to_hex(bt)
    return hex_str


def hex_to_bt64(hex_str):
    binary = ""
    for i in range(16):
        binary += hex_to_bt4(hex_str[i])
    return binary


def str_to_bt(input_str):
    leng = len(input_str)
    bt = [0] * 64
    if leng < 4:
        for i in range(leng):
            k = ord(input_str[i])
            for j in range(16):
                pow = 1
                for m in range(15, j, -1):
                    pow *= 2
                bt[16 * i + j] = int(k / pow) % 2

        for p in range(leng, 4):
            k = 0
            for q in range(16):
                pow = 1
                for m in range(15, q, -1):
                    pow *= 2
                bt[16 * p + q] = int(k / pow) % 2
    else:
        for i in range(4):
            k = ord(input_str[i])
            for j in range(16):
                pow = 1
                for m in range(15, j, -1):
                    pow *= 2
                bt[16 * i + j] = int(k / pow) % 2
    return bt


def get_key_bytes(key):
    key_bytes = []
    leng = len(key)
    iterator = leng // 4
    remainder = leng % 4
    i = 0

    while i < iterator:
        key_bytes.append(str_to_bt(key[i * 4:i * 4 + 4]))
        i += 1

    if remainder > 0:
        key_bytes.append(str_to_bt(key[i * 4:leng]))

    return key_bytes


def strEnc(data, firstKey, secondKey, thirdKey):
    leng = len(data)
    encData = ""

    if firstKey != None and firstKey != "":
        firstKeyBt = get_key_bytes(firstKey)
        firstLength = len(firstKeyBt)

    if secondKey != None and secondKey != "":
        secondKeyBt = get_key_bytes(secondKey)
        secondLength = len(secondKeyBt)

    if thirdKey != None and thirdKey != "":
        thirdKeyBt = get_key_bytes(thirdKey)
        thirdLength = len(thirdKeyBt)

    if leng > 0:
        if leng < 4:
            bt = str_to_bt(data)
            if firstKey != None and firstKey != "" and secondKey != None and secondKey != "" and thirdKey != None and thirdKey != "":
                tempBt = bt
                for x in range(firstLength):
                    tempBt = enc(tempBt, firstKeyBt[x])
                for y in range(secondLength):
                    tempBt = enc(tempBt, secondKeyBt[y])
                for z in range(thirdLength):
                    tempBt = enc(tempBt, thirdKeyBt[z])
                encByte = tempBt
            elif firstKey != None and firstKey != "" and secondKey != None and secondKey != "":
                tempBt = bt
                for x in range(firstLength):
                    tempBt = enc(tempBt, firstKeyBt[x])
                for y in range(secondLength):
                    tempBt = enc(tempBt, secondKeyBt[y])
                encByte = tempBt
            elif firstKey != None and firstKey != "":
                tempBt = bt
                for x in range(firstLength):
                    tempBt = enc(tempBt, firstKeyBt[x])
                encByte = tempBt
            encData = bt64_to_hex(encByte)
        else:
            iterator = int(leng / 4)
            remainder = leng % 4
            for i in range(iterator):
                tempData = data[i * 4:i * 4 + 4]
                tempByte = str_to_bt(tempData)
                if firstKey != None and firstKey != "" and secondKey != None and secondKey != "" and thirdKey != None and thirdKey != "":
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    for z in range(thirdLength):
                        tempBt = enc(tempBt, thirdKeyBt[z])
                    encByte = tempBt
                elif firstKey != None and firstKey != "" and secondKey != None and secondKey != "":
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    encByte = tempBt
                elif firstKey != None and firstKey != "":
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    encByte = tempBt
                encData += bt64_to_hex(encByte)

            if remainder > 0:
                remainderData = data[iterator * 4:leng]
                tempByte = str_to_bt(remainderData)
                if firstKey != None and firstKey != "" and secondKey != None and secondKey != "" and thirdKey != None and thirdKey != "":
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    for z in range(thirdLength):
                        tempBt = enc(tempBt, thirdKeyBt[z])
                    encByte = tempBt
                elif firstKey != None and firstKey != "" and secondKey != None and secondKey != "":
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    for y in range(secondLength):
                        tempBt = enc(tempBt, secondKeyBt[y])
                    encByte = tempBt
                elif firstKey != None and firstKey != "":
                    tempBt = tempByte
                    for x in range(firstLength):
                        tempBt = enc(tempBt, firstKeyBt[x])
                    encByte = tempBt
                encData += bt64_to_hex(encByte)

    return encData
