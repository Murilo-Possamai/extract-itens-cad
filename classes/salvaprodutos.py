import pandas as pd
from typing import List, Dict, Any

class SalvaProdutos:
    """
    Classe para armazenamento dos produtos em planilha.
    """
    
    def __init__(self):
        self.produtos: List[Dict[str, Any]] = []
        
    def _validar_dados(self, codbarra: str, descricao: str, preco: float, ncm: str) -> None:
        """
        valida os dados do produto.
        """
        erros = []

        if not codbarra or not codbarra.strip():
            erros.append("CODBARRA não pode ser nulo ou vazio.")

        if not descricao or not descricao.strip():
            erros.append("DESCRICAO não pode ser nula ou vazia.")

        if preco is None:
            erros.append("PRECO não pode ser nulo.")

        if not ncm or not ncm.strip():
            erros.append("NCM não pode ser nulo ou vazio.")

        if len(ncm) != 8:
            erros.append(f"NCM deve ter exatamente 8 caracteres (Atualmente: {len(ncm)}).")
        
        if codbarra and len(codbarra) <= 5:
            erros.append(f"CODBARRA deve ter mais de 5 caracteres (Atualmente: {len(codbarra)}).")
        
        if descricao and len(descricao) <= 5:
            erros.append(f"DESCRICAO deve ter mais de 5 caracteres (Atualmente: {len(descricao)}).")
            
        if preco is not None and preco <= 0:
            erros.append("PRECO não pode ser zero ou negativo.")

        if erros:
            raise ValueError("\n".join(erros))
        
    def adicionar_produt(self, codbarra: str, descricao: str, preco: float, ncm: str):
        """Adiciona Produto"""  
        try:
                self._validar_dados(codbarra, descricao, preco, ncm)
                
                produto = {
                    "CODBARRA": codbarra,
                    "DESCRICAO": descricao,
                    "PRECO": preco,
                    "NCM": ncm
                }
                self.produtos.append(produto)
                print(f"✅ Produto '{descricao}' adicionado com sucesso.")
                
        except ValueError as e:
            print(f"\nProduto INVÁLIDO{descricao}). Erros:")
            print("  - " + e.args[0].replace("\n", "\n  - "))
            
    def salvarEmPlanilha(self, nome_arqv: str = "Produtos"):
        if not self.produtos:
            print("Não há produtos para salvar")        
            return
        try:
            df = pd.DataFrame(self.produtos)
                
            df.to_excel(nome_arqv, index=False) 
            print(f"\nDados salvos com sucesso no arquivo: **{nome_arqv}**")

        except Exception as e:
            print(f"Ocorreu um erro ao salvar o arquivo: {e}")
        
    def visualisarProdutos(self):
        if not self.produtos:
            print("Não há produtos para visualizar")
            return
        df = pd.DataFrame(self.produtos)
        print("\n--- Produtos Atuais ---")
        print(df.to_string(index=False))
        print("-----------------------")
        
