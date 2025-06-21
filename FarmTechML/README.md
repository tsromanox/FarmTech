
# Projeto FarmTech Solutions - Fase 4 🌱
Bem-vindo ao repositório do projeto FarmTech Solutions.

Este projeto acadêmico tem como objetivo desenvolver um sistema de monitoramento inteligente para prever a necessidade de irrigação em lavouras com base em dados simulados de sensore, integrando hardware (ESP32), modelagem preditiva com Machine Learning e um dashboard interativo para visualização de dados.


**Entregas e Arquivos Gerados**

O script modelagem_ml.py foi desenvolvido para automatizar todo o pipeline deste módulo. Ao ser executado, ele produz os seguintes artefatos essenciais para o projeto:

- sensores_data.csv: Um arquivo CSV com 1000 amostras de dados artificiais de sensores (umidade do solo, temperatura, etc.), utilizado para treinar e validar o modelo.

- modelo_irrigacao.pkl: O modelo de Machine Learning (RandomForestClassifier) treinado e exportado. Este arquivo contém a lógica preditiva e está pronto para ser consumido por outras partes do sistema (como o dashboard).

- farmtech.db: Um banco de dados SQLite leve que contém duas tabelas:

- dados_treinamento: Um registro completo dos dados usados para treinar o modelo, garantindo rastreabilidade.

- previsoes_irrigacao: Uma tabela para armazenar as leituras de sensores em tempo real e os resultados (previsões) gerados pelo modelo.

**Como Executar**

Para replicar os resultados e gerar os arquivos, siga os passos abaixo.

1. Pré-requisitos:

- Certifique-se de ter o Python 3 instalado.
- Em seguida, instale as bibliotecas necessárias:

```pip install pandas scikit-learn joblib ```

2. Execução do Script:

Navegue até o diretório do projeto e execute o script principal deste módulo:

``` python modelagem_ml.py ```

Após a execução, todos os arquivos (.csv, .pkl, e .db) estarão disponíveis no diretório.

**Detalhes do Modelo**

- Algoritmo: RandomForestClassifier do Scikit-learn.
- Features Utilizadas: umidade_solo, temperatura, nutrientes_N.
- Variável Alvo: acao_irrigacao (0 para "Não Irrigar", 1 para "Irrigar").

*Performance*

O modelo alcançou uma acurácia superior a 95% no conjunto de testes, demonstrando alta capacidade de prever a ação correta com base nos dados dos sensores.
