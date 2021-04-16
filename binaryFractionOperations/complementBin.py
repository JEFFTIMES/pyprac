
def twos_complement(in_bits):

    """
    :param in_bits: a binary string, 0b prefix allowed
    :return: a binary string prefixed with 0b
    """
    if in_bits[0:2] == '0b':
        in_bits = in_bits[2:]

    out_bits =[]
    for bit in in_bits:
        if bit == '1':
            out_bits.append('0')

        elif bit == '0':
            out_bits.append('1')

    r = bin(int(''.join(out_bits),2)+1)

    #preffix 0 or cut overflow to same sizing the output with the input.
    # remove the '0b'
    r=r[2:]
    diff_len = len(r)-len(in_bits)

    # overflown, remove the overflown bit
    if diff_len == 1:
        return '0b'+ r[1:]

    # the result is shorter than the input
    elif diff_len < 0:
        return '0b' + '0' * -diff_len + r
    # the same size with the input
    else:
        return '0b' + r

