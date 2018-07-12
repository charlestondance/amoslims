__author__ = 'dmcclymo'

from PIL import Image
import PyPDF2
import re
import os


def get_empty_dict_of_samples(fname):
    filename = open(fname, 'r')
    counter_of_wells = 0
    sample_pages = {}

    for x in filename:
        counter_of_wells += 1
        # create a dict with the key of the line in the file
        sample_pages[x.rstrip()] = 0

    if counter_of_wells != 96:
        print("error")
    else:
        print("96 wells check")

    return sample_pages


def find_page_of_sample(sample_pages):
    total_number_of_pages = pdfReader.numPages
    print(total_number_of_pages)
    keys = sample_pages.keys()
    for x in range(0,total_number_of_pages):
        pageObj = pdfReader.getPage(x)
        page_text = pageObj.extractText()
        extracted_sample_string=re.compile('Sample: (.*?)W').search(page_text)
        if extracted_sample_string:
            print(extracted_sample_string.group(1))
            for y in keys:

                if y == extracted_sample_string.group(1):
                    print(y + " is on page " + str(x))
                    sample_pages[y] = x

    return sample_pages


def save_images_from_page(page_number):
    page0 = pdfReader.getPage(page_number)
    xObject = page0['/Resources']['/XObject'].getObject()

    for obj in xObject:
        if xObject[obj]['/Subtype'] == '/Image':
            size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
            data = xObject[obj].getData()
            if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                mode = "RGB"
            else:
                mode = "P"

            if xObject[obj]['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save(obj[1:] + ".png")
            elif xObject[obj]['/Filter'] == '/DCTDecode':
                img = open(obj[1:] + ".jpg", "wb")
                img.write(data)
                img.close()
            elif xObject[obj]['/Filter'] == '/JPXDecode':
                img = open(obj[1:] + ".jp2", "wb")
                img.write(data)
                img.close()


def save_images_from_page_with_dir(sample_pages):
    newpath = r'pictures'
    if not os.path.exists(newpath):
        os.makedirs(newpath)

    keys = sample_pages.keys()

    for x in keys:
        page0 = pdfReader.getPage(sample_pages[x])
        xObject = page0['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "P"

                if xObject[obj]['/Filter'] == '/FlateDecode':
                    img = Image.frombytes(mode, size, data)
                    img.save(newpath + "//" + x + ".png")
                elif xObject[obj]['/Filter'] == '/DCTDecode':
                    img = open(newpath + "//" + x + ".jpg", "wb")
                    img.write(data)
                    img.close()
                elif xObject[obj]['/Filter'] == '/JPXDecode':
                    img = open(newpath + "//" + x + ".jp2", "wb")
                    img.write(data)
                    img.close()


def old_excecute_set():
    pdfFileObj = open('96-well.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    sample_pages = get_empty_dict_of_samples('P1001J3.txt')
    sample_pages = find_page_of_sample(sample_pages=sample_pages)
    save_images_from_page_with_dir(sample_pages=sample_pages)
