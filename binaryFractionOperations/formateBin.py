import binaryFractionOperations.operatorBin as operatorBin

def add_whitespace(binary):

    """
    :param binary: a binary string, '0b' allowed
    :return:
    """

    if binary.find(' ') !=-1:
        binary = remove_whitespace(binary)

    out_wn = []
    out_frc = []
    i = 0

    wn, frc = operatorBin.split_bin_fraction(binary)

    if wn[0:2] == '0b':
        wn = wn[2:]
    # add ws in whole number part
    for bit in reversed(wn):

        out_wn.append(bit)
        i += 1
        if i % 4 == 0:
            out_wn.append(' ')

    # add ws in fractional part
    i=0
    for bit in frc:
        out_frc.append(bit)
        i += 1
        if i % 4 == 0:
            out_frc.append(' ')

    return '0b'+ ''.join(reversed(out_wn)).lstrip() + '.' + ''.join(out_frc).rstrip()



def remove_whitespace(binary):

    return binary.replace(' ','')

#def check_prefix(binary):

