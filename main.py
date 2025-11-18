from typing import Dict, Tuple
import pyautogui as pag
import keyboard
import time
import pyperclip
from classes.salvaprodutos import SalvaProdutos 

# --- VARIÁVEIS DE CONFIGURAÇÃO ---
TEMPO_AÇÃO = 1.0 # Tempo de espera entre cada ação
TEMPO_AÇÃO_CURTA = 0.5 
LIMITE_SALVAMENTO = 600
# --- VARIÁVEIS DINÂMICAS QUE SERÃO CAPTURADAS ---
COORD_CODBARRA_X: int = 0
COORD_CODBARRA_Y: int = 0

# -------------------------------------------------------------------
# FUNÇÃO COPIAR CAMPO (Inalterada)
# -------------------------------------------------------------------

def copiar_campo(campo_nome: str) -> str:
    """Executa CTRL+C e usa pyperclip para ler o valor."""
    try:
        pyperclip.copy('')
        time.sleep(TEMPO_AÇÃO_CURTA) 
        
        pag.hotkey('ctrl', 'c')
        time.sleep(TEMPO_AÇÃO) 
        
        valor = pyperclip.paste().strip()
        if valor is None:
            return ""
            
        print(f"   [Extraído] {campo_nome}: '{valor}'")
        return valor
        
    except Exception as e:
        print(f"   [ERRO] Falha ao copiar e ler {campo_nome}: {e}")
        return ""

# -------------------------------------------------------------------
# 1. CAPTURA DE PONTO DE REFERÊNCIA (DINÂMICA)
# -------------------------------------------------------------------

print("--- 🗺️ INICIANDO CAPTURA DE PONTO DE REFERÊNCIA ---")
print("[PASSO ÚNICO] Leve o mouse ao centro do campo **CÓDIGO DE BARRAS** e pressione **ENTER**.")

# 🛑 PAUSA para a captura da coordenada
keyboard.wait('enter') 

# Captura X e Y do mouse no momento do ENTER
posicao = pag.position()
COORD_CODBARRA_X = posicao.x
COORD_CODBARRA_Y = posicao.y

print(f"✅ Ponto de Referência (CÓDIGO DE BARRAS) registrado em: ({COORD_CODBARRA_X}, {COORD_CODBARRA_Y})")

# 2. INSTANCIAÇÃO DA CLASSE
gerenciador = SalvaProdutos()
contador_produtos = 0

# 3. MACRO DE EXTRAÇÃO EM LOOP INFINITO (USANDO COORDENADAS CAPTURADAS)
print("\n--- 🤖 MACRO DE EXTRAÇÃO INICIADO (Fluxo AHK) ---")
print(f"Coordenada de Cod.Barras DINÂMICA: ({COORD_CODBARRA_X}, {COORD_CODBARRA_Y})")
print("Iniciando em 5 segundos. Certifique-se de que a aplicação está em foco e o 1º produto selecionado.")
print(f"Para parar o loop, pressione **Ctrl+C** no console.")
time.sleep(5)


try:
    while True:
        contador_produtos += 1
        print(f"\n--- Processando Produto #{contador_produtos} ---")
        dados_temp: Dict[str, str] = {}
        
        # 1. Pressiona Enter para abrir o produto 
        print("1. Abrindo registro com ENTER...")
        pag.press('enter', interval=TEMPO_AÇÃO)
        
        #COPIA DESC
        time.sleep(TEMPO_AÇÃO)
        dados_temp['DESCRICAO'] = copiar_campo("DESCRICAO")

        # 2. Clique duplo no campo de código de barras (USANDO COORDENADAS CAPTURADAS)
        print("2. Focando CODBARRA com duplo clique...")
        pag.doubleClick(COORD_CODBARRA_X, COORD_CODBARRA_Y, duration=0.1)
        time.sleep(TEMPO_AÇÃO) 

        # 3. Copia código de barras 
        print("3. Copiando CODBARRA...")
        dados_temp['CODBARRA'] = copiar_campo("CODBARRA")

        # 4. Pressiona TAB -> PARA PEGAR PRECO
        print("4. Avançando para DESCRIÇÃO com ENTER...")
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        pag.press('TAB')
        
        # 5. Copia descrição do produto 
        print("5. Copiando PRECO...")
        
        
        # (PREÇO não existe no fluxo AHK. Adicionando valor placeholder)
        dados_temp['PRECO'] = copiar_campo("PRECO")
        

        # 6. Ctrl+Tab duas vezes 
        print("6. Mudando ABA com CTRL+TAB (x2)...")
        pag.hotkey('ctrl', 'tab', interval=TEMPO_AÇÃO_CURTA)
        pag.hotkey('ctrl', 'tab', interval=TEMPO_AÇÃO_CURTA)
        time.sleep(TEMPO_AÇÃO)

        # 7. Tab duas vezes -> Navega para NCM
        print("7. Navegando para NCM com TAB (x2)...")
        pag.press('tab', presses=2, interval=TEMPO_AÇÃO_CURTA)
        time.sleep(TEMPO_AÇÃO)

        # 8. Copia NCM 
        print("8. Copiando NCM...")
        dados_temp['NCM'] = copiar_campo("NCM")

        # 9. Monta linha e SALVA na CLASSE
        gerenciador.adicionar_produt(
            codbarra=dados_temp.get('CODBARRA', ''),
            descricao=dados_temp.get('DESCRICAO', ''),
            preco=dados_temp.get('PRECO', ''), 
            ncm=dados_temp.get('NCM', '')
        )
        
        # 10. Fecha o registro com ESC
        print("10. Fechando registro com ESC...")
        pag.press('esc', interval=TEMPO_AÇÃO)

        # 11. Seta para baixo -> Seleciona o próximo
        print("11. Selecionando próximo registro com DOWN...")
        pag.press('down', interval=TEMPO_AÇÃO)
        
        # 12. Lógica de Salvamento
        if contador_produtos % LIMITE_SALVAMENTO == 0:
            print(f"\n📢 ALERTA: Limite de {LIMITE_SALVAMENTO} produtos atingido. Salvando backup...")
            gerenciador.salvarEmPlanilha(nome_arqv=f"Produtos_Backup_{contador_produtos}.xlsx")
            
        time.sleep(TEMPO_AÇÃO) 

except KeyboardInterrupt:
    print("\n\n🛑 Macro de extração interrompido pelo usuário (Ctrl+C).")
except Exception as e:
    print(f"\n\n🚨 Ocorreu um erro inesperado e o macro parou: {e}")

finally:
    # Salvamento final
    print("\n--- FINALIZANDO E SALVANDO OS DADOS FINAIS ---")
    gerenciador.salvarEmPlanilha(nome_arqv="Produtos_Final_Extraidos.xlsx")
    gerenciador.visualisarProdutos()