import requests
import os


parameters = {
"project_id" : os.getenv('PROJECT_ID', 'yourgoogleprojectid'), 
"schemaandtable": "storefront_production.order_sent_view", 
"prefix": "test_all/order_sent_view", 
"bucket":"ftp-abinbev",
"source_path_files" : "ftp-abinbev/order_sent_view",
"schemaandtabletoinsert":"storefront_production.order_sent_view_s3_audit",
"schemaandtablegetdates":"storefront_production.order_sent_view",
"process_mode" : "all_objects_no_date",
"timestampcolumn":"timestamp", 
"offset_rework": -99999,
"read_from_s3tobq" : "order_sent_view/",
"drop_or_delete" : "drop",
"query_mode" : "all_in_one",
"read_from_format" : ".json"
}
response = requests.get(f"https://us-central1-{os.getenv('PROJECT_ID', 'project_id_here')}.cloudfunctions.net/s3_to_bq_csvjson", params = parameters)
print(response)