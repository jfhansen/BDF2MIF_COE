import re
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, help="Type COE to generate COE file, MIF to generate MIF")
    parser.add_argument("filename", type=str, help="Type filename here.")
    args = parser.parse_args()
    mif = ['00'] * int((16384 / 8))
    with open("u_vga16.bdf", 'r') as file:
        lines = file.readlines()
        start_char = False
        cntr = 0
        for line in lines:
            if re.match("ENCODING[\s][\d]*[\s]", line):
                m = re.search("[0-9]+", line)
                enc = int(m.group())
                #print(enc)
                if enc > 127:
                    #exit(0)
                    break
            elif re.match("ENDCHAR", line):
                start_char = False
                cntr = 0
                #exit(0)
            elif start_char:
                byte = re.match("[0-9A-Fa-f][0-9A-Fa-f]", line).group()
                mif[enc*16 + cntr] = byte
                #print(byte)
                cntr += 1
            elif re.match("BITMAP", line):
                start_char = True

    if args.type == "MIF":
        i = 0
        while i < len(mif):
            if mif[i] == '00':
                #for j in range(i, len(mif)-i):
                j = i
                while mif[j] == '00':
                    mif[j] = ''
                    j += 1
                    if j >= len(mif):
                        break
                mif[i] = "[{:<5}-{:>5}]: {:>4};\n".format(i*8, (j-1)*8+7, '00')
                i = j
                #mif[i] = "{:<6}: {:>4}".format(i*8, mif[i])
                #mif[i] = str(i) + ":\t\t" + mif[i]
            else:
                mif[i] = "{:<6}: {:>4};\n".format(i*8, mif[i])  # str(enc*16 + cntr) + ":\t\t" + byte
                i += 1
        with open("rom.mif", 'w') as file:
            file.write("DEPTH = {};\t% Memory Depth is number of addresses %\n".format(16384))
            file.write("WIDTH = {};\t% Memory Width is width of addresses %\n".format(1))
            file.write("ADDRESS_RADIX = DEC;\t% ADDRESS_RADIX specifies base of addresses %\n")
            file.write("DATA_RADIX = HEX;\t% DATA_RADIX specifiec base of data %\n")
            file.write("CONTENT\nBEGIN\n")
            file.write("".join(mif))
            file.write("END;")

    elif args.type == "COE":
        with open("rom.coe", 'w') as file:
            file.write("; This COE file specifies the content of ROM\n")
            file.write("; of depth = 16384 and datawidth = 1.\n")
            file.write("; More precisely it specifies the Font Pattern \n")
            file.write("; extracted from the .bdf file.\n")
            file.write("memory_initialization_radix=16;\n")
            file.write("memory_initialization_vector=\n")
            file.write(",\n".join(mif))
            file.write(";")


if __name__ == "__main__":
    main()