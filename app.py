import pandas as pd
import re

ARQUIVO_CSV = 'scorpius.csv'
COLUNAS_DESEJADAS = [
    'Cidade Rem.', 'Destinatário', 'Cidade Dest.',
    'Status Rastreio', 'Data Emissao', 'Data Prev. Entrega', 'Data Entrega', 'Nota Fiscal'
]

def carregar_dados_csv(arquivo, colunas):
    return pd.read_csv(arquivo, usecols=colunas, encoding='utf-8')

def normalize_cnpj_cpf(cnpj_cpf):
    """Remove caracteres não numéricos de um CNPJ ou CPF."""
    return re.sub(r'\D', '', cnpj_cpf)

def extract_cnpj_cpf(destinatario):
    """Extrai e normaliza o CNPJ ou CPF do campo 'Destinatário'."""
    match = re.search(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{3}\.\d{3}\.\d{3}-\d{2}', str(destinatario))
    return normalize_cnpj_cpf(match.group()) if match else ''

def adicionar_coluna_cnpj_cpf_normalizado(df):
    """Adiciona a coluna 'CNPJ_CPF_Normalizado' ao DataFrame."""
    df['CNPJ_CPF_Normalizado'] = df['Destinatário'].apply(extract_cnpj_cpf)
    return df

def buscar_encomenda(df, cnpj_cpf_normalizado, nota_fiscal):
    """Filtra o DataFrame pelo CNPJ/CPF normalizado e Nota Fiscal."""
    df['Notas_Fiscais'] = df['Nota Fiscal'].apply(lambda x: re.split(r'[,\s]+', str(x).strip()))
    df_explodido = df.explode('Notas_Fiscais')
    return df_explodido[
        (df_explodido['CNPJ_CPF_Normalizado'] == cnpj_cpf_normalizado) &
        (df_explodido['Notas_Fiscais'].str.strip() == nota_fiscal.strip())
    ]

def exibir_encomendas(encomendas_cliente, nota_fiscal):
    if not encomendas_cliente.empty:
        nome_empresa = encomendas_cliente.iloc[0]['Destinatário'].split('/')[0].strip()
        print(f"\nEncomendas para o '{nome_empresa}' com a Nota Fiscal '{nota_fiscal}':")
        for _, row in encomendas_cliente.iterrows():
            print(f"Número da Nota Fiscal: {row['Notas_Fiscais']}")
            print(f"Cidade de origem: {row['Cidade Rem.']}")
            print(f"Data de emissão: {row['Data Emissao']}")
            print(f"Status da encomenda: {row['Status Rastreio']}")
            print(f"Cidade de destino: {row['Cidade Dest.']}")
            print(f"Previsão de entrega: {row['Data Prev. Entrega']}")
            print(f"Data de entrega: {row['Data Entrega']}")
            print("-" * 20)
    else:
        print(f"Nenhuma encomenda encontrada para a Nota Fiscal '{nota_fiscal}'.")

def main():
    # Carregar dados do CSV
    df = carregar_dados_csv(ARQUIVO_CSV, COLUNAS_DESEJADAS)
    
    # Adicionar a coluna 'CNPJ_CPF_Normalizado'
    df = adicionar_coluna_cnpj_cpf_normalizado(df)
    
    cnpj_cpf = input("Digite os números do CNPJ ou CPF: ")
    cnpj_cpf_normalizado = normalize_cnpj_cpf(cnpj_cpf)
    
    nota_fiscal = input("Digite o número da Nota Fiscal: ")
    
    # Filtrar o DataFrame pelo CNPJ/CPF normalizado e Nota Fiscal
    encomenda = buscar_encomenda(df, cnpj_cpf_normalizado, nota_fiscal)
    
    # Exibir as encomendas encontradas
    exibir_encomendas(encomenda, nota_fiscal)

if __name__ == "__main__":
    main()