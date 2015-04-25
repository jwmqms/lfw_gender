@echo off
cd src\python
python setup.py install
cd ..\..
REM python C:\Python27\Scripts\epydoc.py --config=epydoc_config.txt lfw_gender