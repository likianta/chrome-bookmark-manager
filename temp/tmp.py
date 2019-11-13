from lk_utils import read_and_write_basic
from lk_utils.excel_reader import ExcelReader
from lk_utils.excel_writer import ExcelWriter


def txt_2_txt():
    ifile = 'in.txt'
    ofile = 'out.txt'
    
    reader = read_and_write_basic.read_file_by_line(ifile, 1)
    writer = []

    # ------------------------------------------------

    for index, i in enumerate(reader):
        pass

    # ------------------------------------------------

    read_and_write_basic.write_file(writer, ofile)


def excel_2_excel():
    ifile = '../temp/in.xlsx'
    ofile = '../temp/out.xls'
    
    reader = ExcelReader(ifile)
    writer = ExcelWriter(ofile)

    # ------------------------------------------------
    
    pass

    # ------------------------------------------------
    
    writer.save()


def excel_2_txt():
    ifile = '../temp/in.xlsx'
    ofile = '../temp/out.txt'
    
    reader = ExcelReader(ifile)
    writer = []
    
    # ------------------------------------------------
    
    for i, j in reader.zip_cols(0, 1):
        pass
    
    # ------------------------------------------------
    
    read_and_write_basic.write_file(writer, ofile)


if __name__ == '__main__':
    # txt_2_txt()
    # excel_2_excel()
    excel_2_txt()
    pass
