# 1. 소개

## Scikit-learn 설치
```python
!pip install numpy scipy matplotlib scikit-learn pandas pillow # run this code in cmd
```

```python
import numpy as np
x = np.array([[1, 2, 3], [4, 5, 6]])
print("x:\n{}".format(x))

from scipy import sparse
eye = np.eye(4) # 대각선 원소는 1이고 나머지는 0인 2차원 배열생성
print("NumPy 배열:\n{}".format(eye))

sparse_matrix = sparse.csr_matrix(eye) # 배열을 희소 행렬로 변환
print("SciPy의 CSR 행렬:\n{}".format(sparse_matrix))

data = np.ones(4)
row_indices = np.arange(4)
col_indices = np.arange(4)
eye_coo = sparse.coo_matrix((data, (row_indices, col_indices)))
print("COO 표현:\n{}".format(eye_coo))

%matplotlib inline
import matplotlib.pyplot as plt
x = np.linspace(-10,10,100) # -10~10, 100개 간격의 배열
y = np.sin(x) # sin 함수 이용 y 배열 생성
plt.plot(x,y, marker="x")
```

## pandas
```python
import pandas as pd
data = {'Name':["John","Anna","Peter","Linda"],
        'Location':["New York","Paris","Berlin","London"],
        'Age':[24,13,53,33]
       }
data_pandas = pd.DataFrame(data)
display(data_pandas)

# Age 값이 30 이상인 행 선택
display(data_pandas[data_pandas.Age >30])
```

## import packages
```python
!pip install mglearn

from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mglearn

%matplotlib notebook
%matplotlib inline
#plt.show
```

## 버전정보 보기
```python
import sys
print("Python 버전: {}".format(sys.version))
import pandas as pd
print("pandas 버전: {}".format(pd.__version__))
import matplotlib
print("matplotlib 버전: {}".format(matplotlib.__version__))
import numpy as np
print("Numpy 버전: {}".format(np.__version__))
import scipy as sp
print("SciPy 버전: {}".format(sp.__version__))
import IPython
print("IPython 버전: {}".format(IPython.__version__))
import sklearn
print("scikit-learn 버전: {}".format(sklearn.__version__))
```

## iris categorization
```python

```
