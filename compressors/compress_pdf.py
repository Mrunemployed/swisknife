import fitz
from compress_img import ospaths
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class PdfCompress():

    def __init__(self) -> None:
        pass

    def compress(self,filepath,outputpath,quality:int):
        pdf = fitz.open(filepath)
        # with fitz.open(filepath) as pdf:
        quality = int(100-quality)
        pdf.save(outputpath,deflate=True)
        pdf.close()
        return True

    def can(self,session_key,quality:int):
        try:
            osp = ospaths()
            osp.init_paths("pdf_to_be_compressed","pdf_compression_completed")
            files = osp.init_files()
            if files and len(files) > 0:
                files_complete = [os.path.join(osp.input_path,x) for x in files]
                output_files = [os.path.join(osp.output_path,f"cmp_{session_key}{x}") for x in files]
                with ThreadPoolExecutor(max_workers=5) as tread:
                    tasks = [tread.submit(self.compress,file,dest,quality) for file,dest in zip(files_complete,output_files)]

                    for future in concurrent.futures.as_completed(tasks):
                        print(future.result())
            else:
                print("No files found to compress")
        except Exception as err:
            print(err)
            return False
        return True
    
pcmp = PdfCompress()
pcmp.can("213fd",10)