::author:jianhua.he@tcl  2016-3-21 Ext.66051

setlocal enabledelayedexpansion

call:main
pause
goto:eof


:main
call:prompt_root
call:root
call:check_phone_status check_phone_status-begain.txt

:option_again
set /p option=请输入"1"进行状态监控：
if "%option%"=="1" (
    call:monito_phone_status
) else (
    goto:option_again
)

call:check_phone_status check_phone_status-end.txt

echo 所有测试已完成，请pull所有log到本目录
pause
goto:eof


:prompt_root
echo 请先root你的手机(*#*#212018#*#*)
pause
goto:eof

:root
adb shell am start -n com.jrdcom.user2root/.JrdUser2Root
ping -n 3 127.0.0.1>nul
adb shell input tap 180 340
ping -n 4 127.0.0.1>nul
adb shell input keyevent 3
adb shell setprop ro.secure 0
adb shell setprop ro.debuggable 1
adb shell setprop ro.allow.mock.location 1
adb shell setprop persist.sys.usb.config mtp,adb
adb wait-for-device
adb shell /system/bin/setenforce 0
adb remount
adb root
adb remount
adb shell setenforce 0
goto:eof

:update_result_file
echo top > monito_phone_status-top.txt
echo vmstat > monito_phone_status-vmstat.txt
echo cpuinfo > monito_phone_status-cpuinfo.txt
echo meminfo > monito_phone_status-meminfo.txt
goto:eof

:record_date
adb shell date >> monito_phone_status-top.txt
adb shell date >> monito_phone_status-vmstat.txt
adb shell date >> monito_phone_status-cpuinfo.txt
adb shell date >> monito_phone_status-meminfo.txt
goto:eof

:monito_phone_status
echo 1 > stress_test_monitor_flag
call:update_result_file
call:record_date
call:monito_phone_status-real
goto:eof

:monito_phone_status-real
call:monito_phone_status-real-top-vmstat

call:monito_phone_status-real-cpu-men

ping -n 4 127.0.0.1>nul

set /p flag=<stress_test_monitor_flag
if "%flag%"=="1 " (
    goto:monito_phone_status-real
) else (
    call:record_date
    goto:eof
)

:monito_phone_status-real-top-vmstat
echo --------------------- >> monito_phone_status-top.txt
adb shell top -n 2 -d 2 -m 10 -t >> monito_phone_status-top.txt
echo --------------------- >> monito_phone_status-vmstat.txt
adb shell vmstat >> monito_phone_status-vmstat.txt
goto:eof

:monito_phone_status-real-cpu-men
echo --------------------- >> monito_phone_status-cpuinfo.txt
adb shell dumpsys cpuinfo >> monito_phone_status-cpuinfo.txt
echo --------------------- >> monito_phone_status-meminfo.txt
adb shell dumpsys meminfo >> monito_phone_status-meminfo.txt
goto:eof

:check_phone_status
echo adb shell getprop ro.tct.sys.ver : > %1
adb shell getprop ro.tct.sys.ver >> %1

echo adb shell cat /sys/module/lowmemorykiller/parameters/minfree : >> %1
adb shell cat /sys/module/lowmemorykiller/parameters/minfree >> %1

echo adb shell cat /sys/module/lowmemorykiller/parameters/vmpressure_file_min : >> %1
adb shell cat /sys/module/lowmemorykiller/parameters/vmpressure_file_min >> %1

echo adb shell cat /proc/sys/vm/swappiness : >> %1
adb shell cat /proc/sys/vm/swappiness >> %1

echo adb shell cat /proc/swaps : >> %1
adb shell cat /proc/swaps >> %1

echo adb shell cat /sys/module/lowmemorykiller/parameters/enable_adaptive_lmk : >> %1
adb shell cat /sys/module/lowmemorykiller/parameters/enable_adaptive_lmk >> %1

echo adb shell dumpsys battery : >> %1
adb shell dumpsys battery >> %1

echo 状态已经check完成！请运行stress_test.py进行自动压力测试。并在此处按任意键继续监控手机状态！---anything can contacts author:jianhua.he@tcl.com
goto:eof


:eof
