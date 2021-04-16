import math


def split_bin_fraction(binary):
    """
    receive a dicimal binary in string, split the fractional part from the whole number.
    return a whole number part string with a fractional part string.

    """

    return binary.split('.', 1)[0], binary.split('.', 1)[1]


def fraction_bin2dec(binary_fraction):
    """
    input base2 fraction string, figure out the equal decmal fraction number.
    return a float decimal number.

    """

    # create the dictionay of base10 number corresponding to each bit up to 52bit offset to the dot.
    OFFSETS = {'{:d}'.format(i): pow(2, -i) for i in range(1, 53)}

    dec_result = 0

    if len(binary_fraction) > 52:
        raise ValueError("Input binary Overflow the 52 bits limit.")

    # sum up the base10 value of each bit
    for offset in range(len(binary_fraction)):
        dec_result += int(binary_fraction[offset], 2) * OFFSETS[str(offset + 1)]

    return dec_result


def fraction_dec2bin(fraction):
    """
    input basee10 fraction number, figure out the equal binary fraction number.
    return a string consist of the corresponding bits up to 52 digits.

    """
    # create the dictionay of base10 number corresponding to each bit up to 52bit offset to the dot.
    OFFSETS = {'{:d}'.format(i): pow(2, -i) for i in range(1, 53)}

    if math.isnan(fraction):
        raise TypeError("input is not a number in decimal.")

    bin_result = ''

    for offset in range(52):
        remain = fraction - pow(2, -(offset + 1))

        if remain > 0:
            bin_result += '1'
            fraction = remain

        elif remain < 0:
            bin_result += '0'

        else:
            bin_result += '1'
            break

    return bin_result


def bin2dec(binary):
    if binary.find('.') != -1:
        wn_bin, frc_bin = binary.split('.', 1)

    else:
        wn_bin, frc_bin = binary, '0'

    # print('frc_bin:',frc_bin)

    return int(wn_bin, 2) + fraction_bin2dec(frc_bin)


def dec2bin(dec):
    dec_frc, dec_wn = math.modf(dec)

    return '.'.join([bin(int(dec_wn)), fraction_dec2bin(dec_frc)])


def add(summand, addend):
    return dec2bin(bin2dec(summand) + bin2dec(addend))

def sub(subtractend , subtractor):
    return dec2bin(bin2dec(subtractend) - bin2dec(subtractor))

def multi(multiplicand, multiplier):
    return dec2bin(bin2dec(multiplicand) * bin2dec(multiplier))


def div(dividend, divisor):
    return dec2bin(bin2dec(dividend) / bin2dec(divisor))
