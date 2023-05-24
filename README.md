## python gen wheel
- python 版本為3.9.7

## 步驟解說
1. 資料夾層級如下所示:
   - `__init__.py`文件的作用是將文件夾變為一個Python模組, Python中的每個模塊中都有`__init__.py`文件
   - 通常`__init__.py`的內容是空的
```
   gen_wheel
   ├── setup.py
   ├── MANIFEST.in
   └── self_module
       ├── __init__.py
       ├── main_func.py (預生成.whl之function)
       └── function_ref
           ├── __init__.py
           ├── function_BP.py (會用到的function-1)
           ├── function_LDA.py (會用到的function-2)
```

2. 利用setuptools建立setup.py，以下列出setuptools中各項參數:
    - name: pip install後顯示在conda list的名稱，最好與資料夾同名
    - version: 版本號
    - keywords: 描述版本關鍵字
    - description: 項目簡介
    - author: 作者名
    - author_email: 作者mail
    - url: 想要連結的網址
    - **packages: 預打包項目之python package，setuptools.find_packages() 可自動找出包含的 package**
    - **install_requires: 預生成.whl使用的python module，需一併加入**
    - **include_package_data: 預生成.whl使用的參考檔(如.py file或是.npy的數據檔)，有使用須設為True並同時填寫MANIFEST.in 來將參考檔案納入package中**
    - license: 如 MIT, APACHE, GNU等(這裡使用MIT)
 
3. [手動建立`MANIFEST.in`](https://www.osgeo.cn/python-packaging/guides/using-manifest-in.html), 文件內容入下所示:
```
recursive-include self_module/function_ref *
```

4. 產生wheel檔:
    - 先cd至指定目錄後輸入python setup.py sdist bdist_wheel
    - 輸入完畢後.whl檔便會產生於dist資料夾中
    - 另外可以利用.egg-info中的SOURCES.txt檢查def所引用之module是否都有被納入.whl中

5. 參考文件
   - [Python application 的打包和發布(上)](http://wsfdl.com/python/2015/09/06/Python%E5%BA%94%E7%94%A8%E7%9A%84%E6%89%93%E5%8C%85%E5%92%8C%E5%8F%91%E5%B8%83%E4%B8%8A.html)
   - [Python application 的打包和發布(下)](http://wsfdl.com/python/2015/09/08/Python%E5%BA%94%E7%94%A8%E7%9A%84%E6%89%93%E5%8C%85%E5%92%8C%E5%8F%91%E5%B8%83%E4%B8%8B.html)
   - [打包非.py參考檔](https://stackoverflow.com/questions/54945912/using-setuptools-to-copy-non-py-files)

## 使用流程
1. 先創建虛擬env
```
conda create -n test_env python=3.9.7
conda activate test_env
```
3. 將專案中dist資料夾的self_module-0.1.0-py3-none-any.whl下載下來
4. 下載後安裝於test_env中
```
pip install .../self_module-0.1.0-py3-none-any.whl
```
5. 安裝完後利用conda list檢查是否安裝成功
6. 輸入以下python code進行使用
``` python
from self_module import main_func
import numpy as np
from sklearn import datasets

iris = datasets.load_iris()
data_iris = iris.data[50:,:]
label_iris = iris.target[50:,]
cr_iris = main_func.analysis_lda_loo(data_iris, label_iris, weight_p=1, weight_n=1)

data_time = np.load('test_data/time_series_data.npy')
bp_result = main_func.analysis_bp(data_time, 8, 12, 0, fs=500, bin_hz=10)
```
