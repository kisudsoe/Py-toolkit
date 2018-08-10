# Py-toolkit

## package note

1. [아톰 파이썬 패키지](https://www.reddit.com/r/Atom/comments/49d97p/can_i_use_atom_as_an_editor_for_r/)
2. [아톰 패키지 추천](http://blog.naver.com/PostView.nhn?blogId=jkikss&logNo=220590070604&categoryNo=44&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView)

## Jupyter notebook/lab 설치

1. R download
2. Python download

3. Jupyter install (in CMD)
```CMD
pip install Jupyter
```

4. CMD 환경변수 설정(R)
* R 위치: Program files/R/버전/bin/x64/
* 시작> 검색: "시스템 환경 변수 편집"
* 환경변수 클릭> 시스템 변수의 Path> Edit>
* `C:\Program Files\R\R-3.4.3\bin\x64` 추가

5. R kernel install (in R)
```r
install.packages('devtools')
devtools::install_github('IRkernel/IRkernel')

#install.packages("stringr") # If 'stringr' error exist
#install.packages("R6") # If 'R6' error exist

# or devtools::install_local('IRkernel-master.tar.gz')
IRkernel::installspec()  # to register the kernel in the current R installation
```
```r
# in R 3.3
IRkernel::installspec(name = 'ir33', displayname = 'R 3.3')
# in R 3.2
IRkernel::installspec(name = 'ir32', displayname = 'R 3.2')
```

## Jupyter update

1. Python update
* Download at https://www.python.org/downloads/

2. jupyter update (in CMD)
```CMD
pip install -U jupyter
```

3. R update & regist IRkernel (in R session)
```r
install.packages("installr")
library(installr)
updateR()

# IRkernel
install.packages('devtools')
devtools::install_github('IRkernel/IRkernel')

#install.packages("stringr") # If 'stringr' error exist
#install.packages("R6") # If 'R6' error exist

# or devtools::install_local('IRkernel-master.tar.gz')
IRkernel::installspec()  # to register the kernel in the current R installation
```

---
Python codes by Seung-Soo Kim. 2016-2018
