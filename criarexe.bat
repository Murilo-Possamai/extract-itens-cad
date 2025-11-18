@echo off
echo =======================================================
echo Iniciando o processo de criacao do executavel com PyInstaller
echo =======================================================

REM Limpa o build anterior para garantir uma construcao limpa
if exist build rd /s /q build
if exist dist rd /s /q dist

REM Comando PyInstaller
REM -F ou --onefile: Cria um unico arquivo executavel.
REM --name: Define o nome do executavel de saida (sem a extensao .exe).
REM --hidden-import: Garante que o modulo 'salvaprodutos' dentro da pasta 'classes' seja incluido, 
REM                 mesmo que o PyInstaller nao o detecte automaticamente.

pyinstaller --onefile ^
            --name "MacroExtratorProdutos" ^
            --hidden-import "classes.salvaprodutos" ^
            "main.py"

REM Verifica se a construcao foi bem-sucedida
if exist dist\MacroExtratorProdutos.exe (
    echo.
    echo =======================================================
    echo ✅ Sucesso! O executavel foi criado:
    echo    dist\MacroExtratorProdutos.exe
    echo =======================================================
) else (
    echo.
    echo =======================================================
    echo ❌ ERRO: Falha ao criar o executavel. Verifique a saida acima.
    echo =======================================================
)

pause