
import PyPDF2
 
# creating a pdf file object
pdfFileObj = open('c.pdf', 'rb')
 
# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
# creating a page object
pageObj = pdfReader.getPage(1)
 
# extracting text from page
x = pageObj.extractText()
#print(pageObj.extractText())
x = x.split()
print(x)
 
# closing the pdf file object
pdfFileObj.close()