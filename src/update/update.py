import os
import requests
import zipfile
import psutil

from tqdm import tqdm

def download_update_from_url(update_url, temp_file):
    
    response = requests.get(update_url, stream=True)
    total_size = int(response.headers.get("Content-Length", 0))
    with open(temp_file, "wb") as fileobj:
        with tqdm(total=total_size, unit="B", unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=1024):
                fileobj.write(chunk)
                pbar.update(len(chunk))
            
    # 结束正在运行的程序
    for proc in psutil.process_iter():
            if proc.name() == 'main.exe':
                proc.kill()

    # 解压更新包
    with zipfile.ZipFile(temp_file, "r") as zip_ref:
        zip_ref.extractall(os.path.join(os.getcwd(), 'update'))

