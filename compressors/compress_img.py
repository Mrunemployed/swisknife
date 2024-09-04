from PIL import Image
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class ospaths():
    def __init__(self):
        self.input_path=''
        self.output_path=''

    def init_paths(self,src_dir:str,dest_dir:str):
        try:
            path = os.path.abspath(os.path.dirname(__file__))
            pard = os.path.pardir
            img_to_be_compressed = os.path.join(path,"..",src_dir)
            if not os.path.exists(img_to_be_compressed):
                os.mkdir(img_to_be_compressed)
            img_compression_complete = os.path.join(path,"..",dest_dir)
            if not os.path.exists(img_compression_complete):
                os.mkdir(img_compression_complete)
            self.input_path = img_to_be_compressed
            self.output_path = img_compression_complete
        except Exception as err:
            print(err)
            return False
        return True
        

    def init_files(self):
        try:
            if len(self.input_path) > 0 and len(self.output_path) > 0:
                init_files = os.scandir(self.input_path)
                files = [x.name for x in init_files if x.is_file()]
        except Exception as err:
            # log.error(f"error:{err}")
            print(err)
            return False
        return files


class ImgCompressor():

    def __init__(self) -> None:
        self.input_path = ""
        self.output_path =""
        
    def compress(self,filepath,outputpath,quality:int):
        try:    
            with Image.open(filepath) as img:
                img.save(outputpath,quality=quality)
        except Exception as err:
            print(err)
            return False
        return True
    
    def can(self,session_key:str,quality:int):
        try:
            osp = ospaths()
            osp.init_paths("img_to_be_compressed","img_compression_completed")
            files = osp.init_files()
            files_complete = [os.path.join(osp.input_path,x) for x in files]
            output_files = [os.path.join(osp.output_path,f"cmp_{session_key}{x}") for x in files]
            with ThreadPoolExecutor(max_workers=5) as tread:
                tasks = [tread.submit(self.compress,file,dest,quality) for file,dest in zip(files_complete,output_files)]

                for future in concurrent.futures.as_completed(tasks):
                    print(future.result())
        except Exception as err:
            print(err)
            return False
        return True

    # def main(self):
    #     self.init_img()
    #     self.can()
            

imc = ImgCompressor()
imc.can("abcx123",50)
