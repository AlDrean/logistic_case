import os
from datetime import datetime

import numpy as np
import pandas as pd
from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt

BADCOLOR = '#B22222'
GOODCOLOR = '#3D59AB'

# Press the green button in the gutter to run the script.
parse_dates = [
    'created_at',
    'in_transit_to_local_distribution_at',
    'local_distribution_at',
    'in_transit_to_deliver_at',
    'delivered_at',
    'delivery_estimate_date',
]


def create_db():
    if os.path.isfile('logistic.db'):
        return 0
    Path("./logistic.db").touch()
    con = sqlite3.connect("logistic.db")

    data = pd.read_csv('logistic_case/logistics-case-v3.csv', parse_dates=parse_dates)
    data.to_sql("logistic", con, if_exists='fail', index=False)
    con.close()


querry1 = """    select
        delivery_addresses_to_state as 'estado',
		avg((julianday(delivery_estimate_date) - julianday(created_at))) as 'estimativa de entrega',
		avg((julianday(delivered_at) - julianday(created_at))) as 'tempo de entrega',
		avg((julianday(delivered_at) - julianday(delivery_estimate_date))) as 'atraso',
		avg((julianday(in_transit_to_local_distribution_at) - julianday(created_at))) as 'em transito para distribuidora local',
		avg((julianday(local_distribution_at) - julianday(created_at))) as 'chegar na distribuidora Local',
		avg((julianday(in_transit_to_deliver_at) -julianday(local_distribution_at))) as  'em armazen',
		avg((julianday(in_transit_to_deliver_at) - julianday())) as 'em transito de entrega',

        count(id)
    from logistic
    WHERE ('atraso' >= 1)
	GROUP by logistic.delivery_addresses_to_state
	ORDER by 'tempo de entrega'
		 desc"""

# df = pd.read_sql_query(querry1,con)


if __name__ == '__main__':
    create_db()
    con = sqlite3.connect("logistic.db")

    data = pd.read_csv('logistic_case/logistics-case-v3.csv', parse_dates=parse_dates)
    con = sqlite3.connect("logistic.db")
    cur = con.cursor()

    df_late = pd.read_csv('sql/em_atraso.csv')
    df_late = df_late.sort_values(by='count(id)')
    df_onDay = pd.read_csv('sql/em_dia.csv')
    df_onDay = df_onDay.sort_values(by='count(id)')

    df_plot = pd.DataFrame

    q1 = """    select
        delivery_addresses_to_state as 'state',
		avg((julianday(delivery_estimate_date) - julianday(created_at))) as 'delivery__',
		avg((julianday(delivered_at) - julianday(created_at))) as 'delivery_time',
		avg((julianday(delivered_at) - julianday(delivery_estimate_date))) as 'lateness',

        count(id)
    from logistic
  	GROUP by logistic.delivery_addresses_to_state
	ORDER by count(id)
		 desc"""

    df_ = pd.read_sql_query(q1, con)

    df = pd.DataFrame({
        'state': df_['state'],
        'lateness': df_['lateness'],
        'delivery_time': df_['delivery_time']

    })

    ax = df.plot.bar(x='state', y=['lateness', 'delivery_time'], rot=0, figsize=(20, 15), stacked=False,
                     title="Deliveries: average per State")
    ax.set_xlabel("States")
    ax.set_ylabel("Days")
    fig = ax.get_figure()
    fig.savefig('graph/avg_delivery_time.png')
    df.to_csv('graph/avg_delivery_time.csv')

    #
    # Fist, we need to find anomalies. As its a  delivery system, we should star by looking  at thhe average times between
    # the checkpoints and thedelivery, and copare it to the stimated  date.  We can split the data between brazil's states and see what do we got
    #

    df = pd.DataFrame({
        'States': df_late['estado'],
        'Late': df_late['atraso'],
        'OnDay': df_onDay['atraso']
    })

    ax = df.plot.bar(x='States', rot=0, figsize=(20, 15), stacked=True, color=[BADCOLOR, GOODCOLOR],
                     title="Deliveries: on day x late comparison")
    ax.set_xlabel("States")
    ax.set_ylabel("Days")
    fig = ax.get_figure()
    fig.savefig('graph/comparison_late_on_day.png')
    df.to_csv('graph/comparison_late_on_day.csv')

    df = pd.DataFrame({
        'States': df_late['estado'],

        'late': df_late['chegar na distribuidora Local'],
        'OnDay': df_onDay['chegar na distribuidora Local'],
    })

    # - sor
    ax = df.plot.bar(x='States', rot=0, figsize=(20, 15), stacked=False, color=[BADCOLOR, GOODCOLOR],
                     title="Comparison: Time until reach local distributor, between late and on day deliveries")
    ax.set_xlabel("States")
    ax.set_ylabel("days")
    fig = ax.get_figure()
    fig.savefig('graph/comparison_local_distributor.png')

    df = pd.DataFrame({
        'States': df_late['estado'],
        'late': df_late['em armazen'],
        'onDay': df_onDay['em armazen'],

    })

    # - sor
    ax = df.plot.bar(x='States', rot=0, figsize=(20, 15), stacked=False, color=[BADCOLOR, GOODCOLOR],
                     title="Comparison: storage time in local distributor, between late and on day deliveries")
    ax.set_xlabel("States")
    ax.set_ylabel("Days")
    fig = ax.get_figure()
    fig.savefig('graph/comparison_onStorage.png')

    df = pd.DataFrame({
        'States': df_late['estado'],

        'late': df_late['em transito de entrega'],
        'onDay': df_onDay['em transito de entrega']

    })

    # - sor
    ax = df.plot.bar(x='States', rot=0, figsize=(20, 15), stacked=False, color=[BADCOLOR, GOODCOLOR],
                     title="Comparison: in transit between late and on day deliveries")
    ax.set_xlabel("States")
    ax.set_ylabel("Days")
    fig = ax.get_figure()
    fig.savefig('graph/comparison_in_transit.png')

    # as we have the higher impacts, we want to see the size of those

    df = pd.DataFrame({
        'States': df_late['estado'],

        'late delivers(days)': df_late['atraso'],
        'delivers': df_late['count(id)']
    })

    # - sor
    ax = df.plot.bar(x='States', rot=0, figsize=(20, 15), stacked=False, color=[BADCOLOR, BADCOLOR],
                     title="Comparison: lateness x count per state",
                     subplots=True)

    df = pd.DataFrame({
        'States': df_onDay['estado'],
        'Early delivery(days)': df_onDay['atraso'],
        'number deliveries': df_onDay['count(id)'],
    })

    # - sor
    ax = df.plot.bar(x='States', rot=0, figsize=(20, 15), stacked=False, color=[GOODCOLOR, GOODCOLOR],
                     title="Comparison: good deliveries x count per state",
                     subplots=True)

    #
    # By now, we can see that the avg  delivery time is higher than the avg on time delivery; when looking at this data, we can find in wich steps
    # are taking  more days.  This way, we can find what is taking more time.
    # we can see, as well that SP and  RJ account for the  majority of the late deliveres, whichh means, that the avg time will be dictated by those centers
    #

    df = pd.DataFrame({
        'States': df_late['estado'],

        'Late_delivers': df_late['count(id)'],
        'Late_delivers(days)': df_late['tempo de entrega'],
        'late_percenagt': df_late['count(id)'] / df_late['count(id)'].sum() * 100,

        'onDay_delivers': df_onDay['count(id)'],
        'onDays_delivers(days)': df_onDay['tempo de entrega'],
        'onDay_percent': df_onDay['count(id)'] / df_onDay['count(id)'].sum() * 100,

    })

    plt.show()
    con.close()
