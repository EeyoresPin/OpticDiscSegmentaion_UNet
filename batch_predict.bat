


@echo off
setlocal enabledelayedexpansion

echo Starting batch processing of PNG images...
echo.

REM Set the folder containing PNG images
set "IMAGE_FOLDER=Final data/Final data/New folder/Original"

REM Check if the folder exists
if not exist "%IMAGE_FOLDER%" (
    echo Error: Image folder "%IMAGE_FOLDER%" does not exist!
    pause
    exit /b 1
)

REM Counter for processed images
set count=0

REM Loop through all PNG files in the folder
for %%f in ("%IMAGE_FOLDER%\*.png") do (
    set /a count+=1
    echo Processing image !count!: %%~nxf
    
    python PaddleSeg/tools/predict.py --config cellSeg_config2.yml --model_path output/best_model/model.pdparams --image_path "%%f" --save_dir output_Blood/results
    
    if !errorlevel! neq 0 (
        echo Error processing %%~nxf
    ) else (
        echo Successfully processed %%~nxf
    )
    echo.
)

echo.
echo Batch processing completed!
echo Total images processed: %count%
pause