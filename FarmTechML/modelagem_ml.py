# -*- coding: utf-8 -*-
"""
modelagem_ml.py

Este script executa as seguintes tarefas em sequência:

1.  Gera um dataset artificial ('sensores_data.csv') para treinamento.

2.  Cria um banco de dados SQLite ('farmtech.db') com duas tabelas:
    - 'dados_treinamento': Armazena o dataset inicial.
    - 'previsoes_irrigacao': Registra novas leituras e as previsões do modelo.

3.  Treina um modelo de classificação (RandomForestClassifier) para prever a necessidade de irrigação.

4.  Avalia o modelo e o salva como 'modelo_irrigacao.pkl'.

5.  Simula uma nova leitura de sensor, faz uma previsão e a registra no banco de dados,
    demonstrando a integração completa do pipeline.

"""

import pandas as pd
import numpy as np
import sqlite3
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from datetime import datetime

# --- PARTE 1: GERAÇÃO DO DATASET ARTIFICIAL ---

def gerar_dataset(filename="sensores_data.csv", num_samples=1000):
    """
    Gera um dataset artificial com dados de sensores e salva em um arquivo CSV.
    A regra de negócio para irrigação é simples: irrigar se a umidade do solo for < 40.
    """
    print(f"--- [1/5] Gerando dataset artificial com {num_samples} amostras... ---")
    data = {
        'umidade_solo': np.random.uniform(15, 95, num_samples).round(2),
        'temperatura': np.random.uniform(10, 40, num_samples).round(2),
        'nutrientes_N': np.random.uniform(40, 250, num_samples).round(2), # Nível de Nitrogênio (ppm)
    }
    df = pd.DataFrame(data)

    # Lógica para a variável alvo: 1 = Irrigar, 0 = Não Irrigar
    # Adicionamos um pouco de ruído para não ser uma regra perfeita e simular a realidade.
    noise = np.random.normal(0, 5, num_samples)
    df['acao_irrigacao'] = np.where((df['umidade_solo'] + noise) < 40, 1, 0)
    
    df.to_csv(filename, index=False)
    print(f"✅ Dataset '{filename}' criado com sucesso.\n")
    return filename

# --- PARTE 2: GUIA E CRIAÇÃO DO BANCO DE DADOS ---

def configurar_banco_de_dados(db_name="farmtech.db", training_data_csv="sensores_data.csv"):
    """
    Cria e configura o banco de dados SQLite.
    1. Cria a tabela 'dados_treinamento' para o dataset inicial.
    2. Cria a tabela 'previsoes_irrigacao' para registrar novas previsões.
    3. Popula 'dados_treinamento' com os dados do CSV.
    """
    print(f"--- [2/5] Configurando o banco de dados '{db_name}'... ---")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Tabela 1: Armazena os dados que foram usados para treinar o modelo.
    # É uma boa prática para rastreabilidade e auditoria do modelo.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dados_treinamento (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        umidade_solo REAL NOT NULL,
        temperatura REAL NOT NULL,
        nutrientes_N REAL NOT NULL,
        acao_irrigacao INTEGER NOT NULL
    );
    """)

    # Tabela 2: Armazena as leituras em tempo real e as previsões do modelo.
    # Esta tabela será usada pelo dashboard do Thiago (Pessoa 3).
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS previsoes_irrigacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        umidade_solo REAL NOT NULL,
        temperatura REAL NOT NULL,
        nutrientes_N REAL NOT NULL,
        previsao_modelo INTEGER NOT NULL,
        status_previsao TEXT NOT NULL
    );
    """)

    # Popula a tabela de treinamento com os dados do CSV
    df_training = pd.read_csv(training_data_csv)
    # 'replace' apaga dados antigos, útil para re-execuções do script
    df_training.to_sql('dados_treinamento', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    print("✅ Banco de dados configurado com as tabelas 'dados_treinamento' e 'previsoes_irrigacao'.")
    print("✅ Tabela 'dados_treinamento' populada.\n")

# --- PARTE 3: TREINAMENTO E EXPORTAÇÃO DO MODELO ---

def treinar_e_salvar_modelo(data_csv="sensores_data.csv", model_filename="modelo_irrigacao.pkl"):
    """
    Carrega os dados, treina um modelo RandomForestClassifier, avalia e salva em .pkl.
    """
    print("--- [3/5] Iniciando treinamento do modelo... ---")
    df = pd.read_csv(data_csv)

    # Definindo features (X) e alvo (y)
    X = df[['umidade_solo', 'temperatura', 'nutrientes_N']]
    y = df['acao_irrigacao']

    # Divisão em treino e teste (70% treino, 30% teste)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Treinamento do modelo RandomForest
    # random_state=42 garante que o resultado seja sempre o mesmo
    model = RandomForestClassifier(n_estimators=100, random_state=42, oob_score=True)
    model.fit(X_train, y_train)

    # Avaliação do modelo
    print("--- [4/5] Avaliando o modelo treinado... ---")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Acurácia do modelo no conjunto de teste: {accuracy:.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred, target_names=['Não Irrigar (0)', 'Irrigar (1)']))
    print("\nMatriz de Confusão:")
    print(confusion_matrix(y_test, y_pred))

    # Salvando o modelo treinado
    joblib.dump(model, model_filename)
    print(f"\n✅ Modelo treinado e salvo com sucesso como '{model_filename}'.\n")
    return model

# --- PARTE 4: INTEGRAÇÃO COM BANCO E SIMULAÇÃO ---

def executar_previsao_e_salvar(dados_novos, db_name="farmtech.db", model_filename="modelo_irrigacao.pkl"):
    """
    Carrega o modelo, faz uma previsão para novos dados e salva no banco de dados.
    Esta função simula o que o sistema fará em produção.
    """
    print("--- [5/5] Executando simulação de integração... ---")
    
    # Carregar o modelo que foi salvo anteriormente
    model = joblib.load(model_filename)
    
    # Preparar os novos dados para previsão
    df_novo = pd.DataFrame([dados_novos])
    
    # Fazer a previsão
    previsao = model.predict(df_novo)[0]
    status_texto = "IRRIGAR" if previsao == 1 else "NÃO IRRIGAR"
    
    print(f"  > Dados do sensor: {dados_novos}")
    print(f"  > Previsão do modelo: {previsao} ({status_texto})")

    # Salvar a leitura e a previsão no banco de dados
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
    INSERT INTO previsoes_irrigacao (timestamp, umidade_solo, temperatura, nutrientes_N, previsao_modelo, status_previsao)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, dados_novos['umidade_solo'], dados_novos['temperatura'], dados_novos['nutrientes_N'], int(previsao), status_texto))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Leitura e previsão registradas com sucesso na tabela 'previsoes_irrigacao' do banco '{db_name}'.")

# --- BLOCO PRINCIPAL DE EXECUÇÃO ---

if __name__ == "__main__":
    # Define os nomes dos arquivos para fácil manutenção
    NOME_ARQUIVO_DADOS = "sensores_data.csv"
    NOME_ARQUIVO_DB = "farmtech.db"
    NOME_ARQUIVO_MODELO = "modelo_irrigacao.pkl"

    # 1. Gerar o dataset
    gerar_dataset(filename=NOME_ARQUIVO_DADOS)

    # 2. Criar e popular o banco de dados
    configurar_banco_de_dados(db_name=NOME_ARQUIVO_DB, training_data_csv=NOME_ARQUIVO_DADOS)

    # 3. Treinar e salvar o modelo
    treinar_e_salvar_modelo(data_csv=NOME_ARQUIVO_DADOS, model_filename=NOME_ARQUIVO_MODELO)

    # 4. Simular uma nova leitura de sensor e registrar a previsão
    # Cenário 1: Umidade baixa, deve prever "IRRIGAR"
    novo_dado_irrigar = {
        'umidade_solo': 25.5,
        'temperatura': 28.1,
        'nutrientes_N': 150.7
    }
    executar_previsao_e_salvar(novo_dado_irrigar, db_name=NOME_ARQUIVO_DB, model_filename=NOME_ARQUIVO_MODELO)
    
    print("-" * 20)

    # Cenário 2: Umidade alta, deve prever "NÃO IRRIGAR"
    novo_dado_nao_irrigar = {
        'umidade_solo': 80.2,
        'temperatura': 22.5,
        'nutrientes_N': 180.3
    }
    executar_previsao_e_salvar(novo_dado_nao_irrigar, db_name=NOME_ARQUIVO_DB, model_filename=NOME_ARQUIVO_MODELO)
    
    print("\n\nPipeline completo executado com sucesso!")
    print("Arquivos gerados: 'sensores_data.csv', 'farmtech.db', 'modelo_irrigacao.pkl'.")
    print("Você pode inspecionar o 'farmtech.db' com um visualizador de SQLite para ver as tabelas e os dados.")