from cx_Freeze import setup, Executable 

setup(name = "Project VAFM" , 
	version = "1.0" , 
	description = "" , 
	executables = [Executable("app.py",  icon='appicon.ico')]) 
