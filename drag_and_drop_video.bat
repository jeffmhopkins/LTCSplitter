@echo off
rem ===========================================================================
rem  LTC Splitter – Drag & Drop (multi-file)
rem  Portable version – just edit the two paths below and commit to GitHub
rem ===========================================================================

rem === EDIT THESE TWO LINES FOR YOUR SYSTEM ===================================
set "CONDA_ROOT=C:\Users\username\miniconda3"
set "SCRIPT_PATH=C:\code\ltc_split\ltc_split.py"
rem ===========================================================================

rem Activate conda environment (base by default – change if you use another env)
call "%CONDA_ROOT%\Scripts\activate.bat" base

rem If no files were dropped, show helpful message
if "%~1"=="" (
    echo.
    echo  *** Drag one or more video/audio files onto this .bat file ***
    echo.
    pause
    exit /b
)

echo.
echo  LTC Splitter – Processing dropped files...
echo.

rem Loop through every dropped file
:loop
if "%~1"=="" goto :done

echo  ==================================================
echo  Processing: %~nx1
echo  ==================================================

"%CONDA_ROOT%\python.exe" "%SCRIPT_PATH%" "%~1"

echo.
shift
goto :loop

:done
echo.
echo  All files processed successfully!
echo.
pause
