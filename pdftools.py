import tabula
import tempfile
import fitz
import os
from  PIL import Image
import json

class tools():

    def __init__(self,pdfpath) -> None:
        self.pdf = pdfpath
        self.pdf_doc = fitz.open(self.pdf)
        # self.temp_file_path = ''

    def temp_pdf(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False,mode='wb')
        temp_file.write(self.pdf)
        temp_file.close()
        self.temp_file_path = temp_file.name
        print(self.temp_file_path)
        print(self.pdf)

    def pdf_to_mages(self):
        pagespng=[]
        pdf_doc = self.pdf_doc
        name = pdf_doc.name
        for idx in range(len(pdf_doc)):
            page = pdf_doc.load_page(idx)
            pixmap = page.get_pixmap()
            path = os.path.abspath(os.path.dirname(__file__))

            if name.find(" ") > -1:
                remove_whitespace = pdf_doc.name.split(' ')
                name ="".join(remove_whitespace)

            path = os.path.join(path,"uploads",f"{name}_{idx}.png")
            page_img = Image.frombytes("RGB",[pixmap.width,pixmap.height],pixmap.samples)
            page_img.save(path,"PNG")
            pagespng.append(path)
        pdf_doc.close()
        return pagespng
    
    def extract_text(self,page:int,extype:str):
         if self.pdf_doc is not None:
            pdf_doc = self.pdf_doc.load_page(page)
            page_data = pdf_doc.get_textpage()
            if extype in "json":
                return page_data.extractJSON()
            elif extype in "text":
                doc_name = self.pdf_doc.name.split("\\")
                text_data = page_data.extractText()
                lines = ""
                for line in text_data.splitlines():
                    if not line.startswith(u"\u2022"):
                        lines+=line+"\n"
                    else:
                        pass
                data = {
                    "name": f"{doc_name[len(doc_name)-1]}",
                    "page": f"{page}",
                    "page_data": f"{lines}"
                }
                data = json.dumps(data)
                return data
            else:
                msg = {"msg":"Specify Extraction Type"}
                msg = json.dumps(msg)
                return msg
            # return page_data.extractJSON()
         else:
            return self.pdf_doc

        

    def read_pdfs(self):
            dfs = tabula.read_pdf(self.pdf)
            print(dfs)


# with open(r"D:\swisknife\swisknife\uploads\Rudradip Khan-cv.pdf",'rb') as file:
# tt = tools(r"D:\swisknife\swisknife\uploads\Rudradip Khan-cv.pdf")
# data = tt.extract_text(0,"text")
# print(data)
# print(data.extractTEXT())