    select
        delivery_addresses_to_state as 'estado',
		avg((julianday(delivery_estimate_date) - julianday(created_at))) as 'estimativa de entrega',
		avg((julianday(delivered_at) - julianday(created_at))) as 'tempo de entrega',
		avg((julianday(delivered_at) - julianday(delivery_estimate_date))) as 'atraso',
		avg((julianday(in_transit_to_local_distribution_at) - julianday(created_at))) as 'em transito para distribuidora local',
		avg((julianday(local_distribution_at) - julianday(created_at))) as ' Chegar na distribuidora Local',
		avg((julianday(in_transit_to_deliver_at) -julianday(local_distribution_at))) as  'em armazen',
		avg((julianday(in_transit_to_deliver_at) - julianday(created_at))) as 'em transito de entrega',

        count(id)
    from logistic
    WHERE (julianday(delivered_at) - julianday(delivery_estimate_date) >= 1)
	GROUP by logistic.delivery_addresses_to_state
	ORDER by avg((julianday(delivered_at) - julianday(created_at)))
		 desc