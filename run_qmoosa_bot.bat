@echo off
title Qmoosa Bot - Autonomous Agentic OS Launcher
color 0A
echo ===============================================================================
echo                QMOOSA BOT - AUTONOMOUS AGENTIC SUPER-MACHINE
echo   Conway Automaton ^| Multi-Model AI ^| Screen Controller ^| x402 ^| PQC ^| QR
echo ===============================================================================
echo.

cd /d "%~dp0"

echo [1/3] Running Comprehensive Subsystem Verification Tests...
python tests\run_all_tests.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Verification tests failed. Aborting launch.
    pause
    exit /b 1
)

echo.
echo [2/3] Launching Live Proof-of-Agent Demonstration...
python marketing\proof_of_agent_demo.py

echo.
echo [3/3] Synchronizing and Booting Qmoosa Bot Master Machine...
python qmoosa_bot_launcher.py

echo.
echo ===============================================================================
echo [SUCCESS] QMOOSA BOT IS RUNNING FULLY SYNCHRONIZED AND AUTONOMOUS!
echo ===============================================================================
pause
