SELECT
    leads_result.leads_result_id AS `Result ID`,
    DATE_FORMAT(MAX(leads_result.leads_result_barcode_date), '%m/%d/%Y') AS `DATE`,
    leads.leads_acctno AS `PN`,
    leads.leads_chname AS `NAME`,
    leads.leads_ob AS `OB`,
    dv2.dynamic_value_name AS 'BUCKET',
    leads.leads_endo_date AS `ENDO DATE`,
    "CONCATENATED",
       (SELECT 
            CASE 
		WHEN leads_result.`leads_result_users` = 5505 THEN 'CHARINA ALBAR'
		WHEN leads_result.`leads_result_users` = 5581 THEN 'CHARINA ALBAR'
	     END
            FROM bcrm.leads_result
            INNER JOIN bcrm.users ON leads_result.leads_result_users = users.users_id
            WHERE leads_result.leads_result_lead = leads.leads_id
            AND leads_result.leads_result_hidden <> 1
            AND leads_result.leads_result_barcode_date < CURRENT_DATE()
            ORDER BY leads_result.leads_result_barcode_date DESC
            LIMIT 1
        ) AS `COLLECTOR`,
        (SELECT 
            CASE 
                WHEN leads_substatus.leads_substatus_name IN ('LEFT MESSAGE', 'SMS RESPONSIVE', 'EMAIL RESPONSIVE', 'SMS RESPONSIVE') THEN 'LM' 
                WHEN leads_status.leads_status_name = 'FPTP' THEN 'FPTP'
                WHEN leads_substatus.leads_substatus_name IN ('KOR', 'SMS NO RESPONSE', 'EMAIL NO RESPONSE', 'SOCIAL MEDIA SEARCH_ONLINE SKIPS', 'ADDRESS LOCATED', 'OTHERS') THEN 'NIS_KOR_CBR'
                WHEN leads_status.`leads_status_name` = 'PTP' AND dv2.dynamic_value_name = 'BUCKET 7: 181-360' THEN 'ECA_B7_PTP'
                WHEN leads_status.`leads_status_name` = 'PTP' AND dv2.dynamic_value_name = 'BUCKET 3: 61-90' THEN 'ECA_B3_PTP'
                WHEN leads_status.`leads_status_name` = 'PAYMENT' AND dv2.dynamic_value_name = 'BUCKET 7: 181-360' THEN 'ECA_B7_PTP'
                WHEN leads_status.`leads_status_name` = 'BP' AND dv2.dynamic_value_name = 'BUCKET 7: 181-360' THEN 'ECA_B7_PTP'
                WHEN leads_status.`leads_status_name` = 'PAYMENT' AND dv2.dynamic_value_name = 'BUCKET 3: 61-90' THEN 'ECA_B3_PTP'
                ELSE leads_substatus.leads_substatus_name
            END
        FROM bcrm.leads_result
        INNER JOIN bcrm.leads_status ON leads_result.leads_result_status_id = leads_status.leads_status_id
        INNER JOIN bcrm.leads_substatus ON leads_result.leads_result_substatus_id = leads_substatus.leads_substatus_id
        WHERE leads_result.leads_result_lead = leads.leads_id
        AND leads_result.leads_result_hidden <> 1
        AND leads_substatus.leads_substatus_name NOT IN ('PUSHBACK', 'FLOWED', 'HOLD_TECHNICAL', 'PULLED_OUT')
        AND leads_result.leads_result_barcode_date < CURRENT_DATE()
        ORDER BY leads_result.leads_result_barcode_date DESC
        LIMIT 1
    ) AS `STATUS`,
   
	GROUP_CONCAT(
		DISTINCT UPPER(
		    REPLACE(
			REPLACE(
			    REPLACE(
				CONCAT(DATE_FORMAT(leads_result.leads_result_barcode_date, '%m.%d.%Y'), "-", leads_result.leads_result_comment),
				'- Inserted By API', ''
			    ),
			    '1_', ''
			),
			'0_', ''
		    )
		) 
		ORDER BY leads_result.leads_result_barcode_date DESC SEPARATOR ' | '
	    ) AS `COLLECTION_REMARKS`
,
        
	CASE 
	    -- If the current status is one of the specified positive statuses
	    WHEN leads_status.leads_status_name IN ('PTP', 'POSITIVE CONTACT', 'UNDER NEGO', 'PAYMENT') THEN 
		CASE
		    -- Check if the account was previously marked as 'POSITIVE'
		    WHEN EXISTS (
			SELECT 1
			FROM leads_result AS lr
			INNER JOIN bcrm.leads_status AS ls ON lr.leads_result_status_id = ls.leads_status_id
			WHERE lr.leads_result_lead = leads.leads_id
			AND ls.leads_status_name = 'POSITIVE'
		    ) THEN 'POSITIVE' -- If previously marked as 'POSITIVE', maintain 'POSITIVE'
		    ELSE 'POSITIVE' -- Otherwise, mark as 'POSITIVE'
		END
	    -- If the current status is not one of the specified positive statuses
	    ELSE 
		CASE
		    -- Check if the account was ever marked as 'POSITIVE'
		    WHEN EXISTS (
			SELECT 1
			FROM leads_result AS lr
			INNER JOIN bcrm.leads_status AS ls ON lr.leads_result_status_id = ls.leads_status_id
			WHERE lr.leads_result_lead = leads.leads_id
			AND ls.leads_status_name = 'POSITIVE'
		    ) THEN 'POSITIVE' -- Maintain 'POSITIVE' if it was ever positive
		    ELSE leads_status.leads_status_name -- Otherwise, leave the status as is
		END
	END AS `CLIENT STATUS`,
    CASE 
        WHEN leads_result.`leads_result_reason_delinquency` = "" THEN 
        CASE
            WHEN leads_status.leads_status_name = 'PTP' THEN 'DELAYED SALARY/ CASHFLOW'
            WHEN leads_substatus.leads_substatus_name IN ('NIS_KOR_CBR', 'OCA', 'LM', 'NEGO') THEN 'NO CONTACT/ LEADS'
            WHEN leads_substatus.leads_substatus_name = 'NPL' THEN 'DELAYED SALARY/ CASHFLOW'
            ELSE MAX(leads_result.leads_result_reason_delinquency)
        END
        ELSE leads_result.`leads_result_reason_delinquency`
    END AS `RFD`,

    "SPM" AS `AGENCY`,
    MAX(leads_result.leads_result_barcode_date) AS `Latest Barcode Date`
FROM
    bcrm.leads_result
INNER JOIN
    bcrm.leads ON leads_result.leads_result_lead = leads.leads_id
INNER JOIN
    bcrm.leads_status ON leads_result.leads_result_status_id = leads_status.leads_status_id
INNER JOIN
    bcrm.leads_substatus ON leads_result.leads_result_substatus_id = leads_substatus.leads_substatus_id
INNER JOIN
    bcrm.users ON leads_result.leads_result_users = users.users_id
LEFT JOIN 
    bcrm.dynamic_value AS dv1 ON (dv1.dynamic_value_lead_id = leads.leads_id AND dv1.dynamic_value_dynamic_id = 4902)
LEFT JOIN 
    bcrm.dynamic_value AS dv2 ON (dv2.dynamic_value_lead_id = leads.leads_id AND dv2.dynamic_value_dynamic_id = 4896)
WHERE
    leads_client_id = 191
    AND leads.leads_users_id <> 659
    AND leads_status.`leads_status_name` NOT IN ('RETURNS', 'DNC')
    AND leads.leads_endo_date >= DATE_FORMAT(CURDATE(), '2024-08-01') AND leads.leads_endo_date < DATE_FORMAT(CURDATE() + INTERVAL 1 MONTH, '%Y-%m-01')
    AND leads_result.leads_result_barcode_date BETWEEN DATE_FORMAT(NOW(), '2024-04-01') AND DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 1 DAY), '%Y-%m-%d 23:59:59' )
    AND leads_result.`leads_result_comment` NOT LIKE '%WALKIN%'
    AND leads_result.`leads_result_comment` NOT LIKE '%WALK IN%'
    AND leads_result.`leads_result_comment` NOT LIKE '%WALK-IN%'
    AND leads_result.`leads_result_comment` NOT LIKE '%WALK- IN%'
    AND leads_result.`leads_result_comment` NOT LIKE '%WALK - IN%'
    AND leads_result.`leads_result_comment` NOT LIKE '%WALK -IN%'
    AND leads_result.leads_result_hidden <> 1
GROUP BY leads.leads_chcode
ORDER BY `Latest Barcode Date` DESC;