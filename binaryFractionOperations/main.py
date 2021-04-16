import binaryFractionOperations.formateBin as formateBin
import binaryFractionOperations.complementBin as complementBin
import binaryFractionOperations.operatorBin as operatorBin
def main():


    a = '00000011.1'
    b = '010'
    c = '1101000101111.000101'


    print(complementBin.twos_complement(b))

    print(formateBin.add_whitespace(c))

    print(operatorBin.add(b,b))

    print(operatorBin.sub(c,b))

    print(operatorBin.multi(a,b))

    print(operatorBin.div(a,b))

main()