@echo off
cd %~dp0

@echo ----------------------------------------------------------------
:root_begin
@echo Please root your phone, are you already use *#*#212018#*#* root?(y/n)
set /p root=
if %root% neq y (
  goto root_begin
)

adb wait-for-device
adb devices
adb shell setenforce 0

@echo ----------------------------------------------------------------
:lmk_level_begin
@echo Please input optimize test case number.(case1/case2/case3/case4/case5/case6/case7/case8)
set /p lmk_level=
if %lmk_level% neq case1 (
if %lmk_level% neq case2 (
if %lmk_level% neq case3 (
if %lmk_level% neq case4 (
if %lmk_level% neq case5 (
if %lmk_level% neq case6 (
  goto lmk_level_begin
))))))

if %lmk_level% equ case1 (
  adb shell "echo 14746,18432,22118,28386,48000,82500 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 105625 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  @echo has set LMK and ALMK level to CASE1
)

if %lmk_level% equ case2 (
  adb shell "echo 14746,18432,22118,31224,57600,123750 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 154375 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  @echo has set LMK and ALMK level to CASE2
)

if %lmk_level% equ case3 (
  adb shell "echo 14746,18432,22118,28386,48000,82500 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 105625 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  adb shell "echo 72900 > /proc/sys/vm/extra_free_kbytes"
  adb shell "echo 0 > /sys/module/process_reclaim/parameters/enable_process_reclaim"
  @echo has set LMK and ALMK level to CASE3
)

if %lmk_level% equ case4 (
  adb shell "echo 14746,18432,22118,31224,57600,123750 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 154375 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  adb shell "echo 72900 > /proc/sys/vm/extra_free_kbytes"
  adb shell "echo 0 > /sys/module/process_reclaim/parameters/enable_process_reclaim"
  @echo has set LMK and ALMK level to CASE4
)

if %lmk_level% equ case5 (
  adb shell "echo 14746,18432,22118,28386,48000,82500 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 105625 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  @echo has set LMK and ALMK level to CASE5
)

if %lmk_level% equ case6 (
  adb shell "echo 14746,18432,22118,31224,57600,123750 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 154375 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  @echo has set LMK and ALMK level to CASE6
)

if %lmk_level% equ case7 (
  adb shell "echo 14746,18432,22118,25805,40000,55000 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 81250 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 100 > /proc/sys/vm/swappiness"
  adb shell "echo 24300 > /proc/sys/vm/extra_free_kbytes"
  adb shell "echo 1 > /sys/module/process_reclaim/parameters/enable_process_reclaim"
  @echo has set LMK and ALMK level to CASE7 QCOM
)

if %lmk_level% equ case8 (
  adb shell "echo 27648,41472,48384,59578,71575,109075 > /sys/module/lowmemorykiller/parameters/minfree"
  adb shell "echo 146575 > /sys/module/lowmemorykiller/parameters/vmpressure_file_min"
  adb shell "echo 60 > /proc/sys/vm/swappiness"
  adb shell "echo 72900 > /proc/sys/vm/extra_free_kbytes"
  adb shell "echo 0 > /sys/module/process_reclaim/parameters/enable_process_reclaim"
  @echo has set LMK and ALMK level to CASE8 Fred
)

@echo ----------------------------------------------------------------
pause