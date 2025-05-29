SELECT
`leads`.`leads_id` AS 'LeadID',
IF(UPPER(leads.`leads_type_product`) REGEXP "CARDS",dv2.`dynamic_value_name`,`leads`.`leads_acctno`) AS 'acctNo',
`leads`.`leads_acctno` AS 'Card No',
`leads`.`leads_endo_date` AS 'endoDate',
`leads`.`leads_cycle` AS 'leadsCycle',
leads.`leads_chname` AS 'chName',
`leads`.`leads_chcode` AS 'CHCode',
LEADS_USER.`users_username` AS 'agentCode',
`leads_status`.`leads_status_name` AS 'mainDispo',
`leads_substatus`.`leads_substatus_name` AS 'subDispo',
`leads`.`leads_ob` AS 'LeadOB',
IF(client.client_name="SBC AUTO","AL",UPPER(leads.`leads_type_product`)) AS 'leadsProduct',
UPPER(`leads`.`leads_agency`) AS 'LEVEL / Bucket',
IF(dv1.`dynamic_value_name` IS NULL,IF(leads.`leads_agency` REGEXP '^LEVEL',"RECOVERY","CURING"),dv1.`dynamic_value_name`) AS 'Placement',
dv3.`dynamic_value_name` AS 'Currency',
`leads`.`leads_new_ob`,
`leads`.`leads_pullout` AS 'Pullout date',
`leads`.`leads_full_address`
FROM leads
INNER JOIN `client` ON client.`client_id` = leads.`leads_client_id`
INNER JOIN bcrm.`users` AS LEADS_USER ON LEADS_USER.`users_id` = leads.`leads_users_id`
LEFT JOIN
    (SELECT
      leads_result_lead,
      MAX(leads_result_id) AS leads_result_id
    FROM
      leads_result
      INNER JOIN leads ON leads.`leads_id` = leads_result.`leads_result_lead` AND (UPPER(`leads`.`leads_chcode`) LIKE '%SBCH%')
    WHERE leads.`leads_client_id` = 193
    AND `leads_result`.`leads_result_status_id` = 5159
    GROUP BY leads_result.`leads_result_lead`) latest
    ON latest.leads_result_lead = leads.leads_id
INNER JOIN `users` ON `users`.`users_id` = `leads`.`leads_users_id`
LEFT JOIN leads_result ON latest.leads_result_id = leads_result.leads_result_id
LEFT JOIN leads_status ON (leads_status.leads_status_id = leads_result.leads_result_status_id AND leads_status.leads_status_deleted = '0')
LEFT JOIN leads_substatus ON (leads_substatus.leads_substatus_id = leads_result.leads_result_substatus_id AND leads_substatus.leads_substatus_deleted = '0')
LEFT JOIN `dynamic_value` AS dv1 ON (dv1.`dynamic_value_lead_id`=`leads`.`leads_id` AND dv1.`dynamic_value_dynamic_id`=2566)
LEFT JOIN dynamic_value AS dv2 ON (dv2.dynamic_value_lead_id = `leads`.leads_id AND dv2.`dynamic_value_dynamic_id` = 2330)
LEFT JOIN dynamic_value AS dv3 ON (dv3.dynamic_value_lead_id = `leads`.leads_id AND dv3.`dynamic_value_dynamic_id` = 2356)
WHERE leads.`leads_client_id` IN (193)
AND leads.`leads_deleted` = '0'
AND leads.`leads_users_id` <> 659
AND (UPPER(`leads`.`leads_chcode`) LIKE '%SBCH%')
ORDER BY `leads`.`leads_endo_date` ASC