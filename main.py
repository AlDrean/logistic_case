# @TODO: mudar o nome do csv importado para o nome original
# @TODO: Mais gráficos

from datetime import datetime

import numpy as np
import pandas as pd
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt


# Press the green button in the gutter to run the script.
parse_dates = [
    'created_at',
    'in_transit_to_local_distribution_at',
    'local_distribution_at',
    'in_transit_to_deliver_at',
    'delivered_at',
    'delivery_estimate_date',
]


def create_db(value: int):
    if value == 1:
        return 0

    Path("./logistic.db").touch()
    con = sqlite3.connect("logistic.db")

    data = pd.read_csv('logistic_case/logistics-case-v3.csv', parse_dates=parse_dates)
    data.to_sql("logistic", con, if_exists='append', index=False)


#
# process_datas = {
#     'id': [],
#     'v_data_entrega': [],
#     'estado_destino': []
# }
#
# process_data = {
#     'id': int,
#     'v_data_entrega': datetime,
#     'estado_destino': str
# }
#
#
# def insert_process_datas(dataset, i):
#     dataset['id'].append(i['id'])
#     dataset['v_data_entrega'].append(i['v_data_entrega'])
#     dataset['estado_destino'].append(i['estado_destino'])
#


if __name__ == '__main__':
    create_db(0)
    data = pd.read_csv('logistic_case/logistics-case-v3.csv', parse_dates=parse_dates)

    df_atraso = pd.read_csv('sql/em_atraso')
    df_em_dia = pd.read_csv('sql/em_dia')

    # df_atraso.plot(kind='scatter', x='estado', y='atraso',color='red')

    df_plot =pd.DataFrame

    df_atraso = df_atraso.sort_values(by='estado')
    df_em_dia = df_em_dia.sort_values(by='estado')

    #
    df =  pd.DataFrame({
        'estados': df_atraso['estado'],
        'atrasos': df_atraso['atraso'],
        'adiantamentos': df_em_dia['atraso']
    })

    df = df.sort_values(by='estados')
    ax = df.plot.bar(x='estados', rot=0, figsize=(20, 15), stacked=True,
                     title="Entregas: Comparação atrasos e adiantamentos por Estado")
    ax.set_xlabel("Estados")
    ax.set_ylabel("Dias")
    fig = ax.get_figure()
    fig.savefig('atrasos_adiantamentos.png')

    df = df.sort_values(by='estados')
    ax = df.plot.bar(x='estados', rot=0, figsize=(20, 15), stacked=True,
                     title="2Entregas: Comparação atrasos e adiantamentos por Estado")
    ax.set_xlabel("Estados")
    ax.set_ylabel("Dias")
    fig = ax.get_figure()
    fig.savefig('teste.png')


    plt.show()


    # plt.bar(df_atraso['estado'], df_atraso['atraso'],color = 'r')
    # plt.bar(df_atraso['estado'], df_em_dia['atraso'], color = 'b')
    # plt.title("Entregas: Comparação  atraso x  adiantamento por estado")
    # plt.xlabel('Estados')
    # plt.ylabel('em dias')
    # plt.figure
    # plt.savefig("Entregas.png",dpi=100)
    #
    #
    #
    # plt.show()
    #
    #
    #
    # plt.bar(df_atraso['estado'], df_atraso['em armazen'],color = 'r')
    # plt.bar(df_atraso['estado'], df_em_dia['em armazen'], color = 'b')
    # plt.title("Espera no armazen local: Comparação  atraso x  adiantamento por estado")
    # plt.xlabel('Estados')
    # plt.ylabel('em dias')
    #
    #
    # plt.show()
    # plt.savefig("armazen.png",dpi=100)
    #

    # data["delivery_time_error"] = data['delivery_estimate_date'] - data["delivered_at"]
    # print(data.groupby(data["delivery_addresses_to_state"])['delivery_time_error'].mean(), "estado")
