import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from datetime import datetime, timedelta

# Função para ler dados de um arquivo de texto
def ler_dados_arquivo(caminho_arquivo):
    # Lê o arquivo de texto, assumindo que cada linha é um ponto de dado
    dados = pd.read_csv(caminho_arquivo, header=None, squeeze=True)
    return dados

# Caminho para o arquivo de dados
caminho_arquivo = r"C:\TIAGO_Backup\UFSM\DOUTORADO\Projeto_Python_Mestrado_yearly_COM_ESS\load_shape_abril.txt"

# Carregar os dados do arquivo
dados = ler_dados_arquivo(caminho_arquivo)
print(dados.head())  # Exibe os primeiros dados para verificação

# Criar um índice de datas, assumindo que os dados são horários consecutivos
data_inicio = datetime(2023, 1, 1)  # Substitua pela data de início correta
datas = [data_inicio + timedelta(minutes=15 * i) for i in range(len(dados))]

# Criar a série temporal com frequência definida
serie_temporal = pd.Series(dados.values, index=pd.DatetimeIndex(datas, freq='15T'))

# Dividir os dados em treino e teste
train_size = int(len(serie_temporal) * 0.75)  # Ajustado para 75% de treino
train, test = serie_temporal[:train_size], serie_temporal[train_size:]

# Encontrar o melhor modelo ARIMA usando auto_arima
modelo_auto = auto_arima(train, seasonal=False, trace=True, stepwise=True)
print(modelo_auto.summary())

# Ajustar o modelo ARIMA
modelo = ARIMA(train, order=modelo_auto.order)
modelo_ajustado = modelo.fit()

# Fazer previsões
previsao = modelo_ajustado.forecast(steps=len(test))

# Previsão além do período de teste (se desejar)
steps_a_longo_praz = 100  # Por exemplo, prever 100 períodos além do período de teste
previsao_longo_praz = modelo_ajustado.get_forecast(steps=steps_a_longo_praz).predicted_mean

# Criar índices de datas para previsões além do período de teste
data_fim_teste = serie_temporal.index[-1] + timedelta(minutes=15)
datas_longo_praz = [data_fim_teste + timedelta(minutes=15 * i) for i in range(len(previsao_longo_praz))]

# Criar séries para previsões
previsao_series = pd.Series(previsao, index=test.index)
previsao_longo_praz_series = pd.Series(previsao_longo_praz, index=pd.DatetimeIndex(datas_longo_praz, freq='15T'))

# Criar subplots para gráficos separados
fig, axs = plt.subplots(3, 1, figsize=(14, 18), sharex=True)

# Gráfico da Série Temporal Completa
axs[0].plot(serie_temporal.index, serie_temporal, color='gray', linestyle='--')
axs[0].set_title('Série Temporal Completa')
axs[0].set_ylabel('Valor')

# Gráfico dos Dados de Treinamento
axs[1].plot(train.index, train, color='blue')
axs[1].set_title('Dados de Treinamento')
axs[1].set_ylabel('Valor')

# Gráfico dos Dados de Teste e Previsões
axs[2].plot(serie_temporal.index, serie_temporal, color='gray', linestyle='--', label='Série Temporal Completa')
axs[2].plot(train.index, train, color='blue', label='Treinamento')
axs[2].plot(test.index, test, color='green', label='Teste')
axs[2].plot(previsao_series.index, previsao_series, color='red', label='Previsão ARIMA')
axs[2].plot(previsao_longo_praz_series.index, previsao_longo_praz_series, color='orange', linestyle='--', label='Previsão Longo Prazo')
axs[2].set_title('Dados de Teste e Previsões')
axs[2].set_xlabel('Data')
axs[2].set_ylabel('Valor')
axs[2].legend()

# Ajustar o layout para evitar sobreposição
plt.tight_layout()
plt.show()

# Exibir o resumo do modelo
print(modelo_ajustado.summary())
