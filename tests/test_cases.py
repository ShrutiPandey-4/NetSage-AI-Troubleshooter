import csv
from pathlib import Path
def test_dataset_has_required_fields_and_30_cases():
 rows=list(csv.DictReader(open(Path(__file__).parents[1]/'data'/'cases.csv',encoding='utf-8')))
 assert len(rows)>=30
 required={'case_id','symptom','topology_notes','show_outputs','expected_fault','osi_layer','concept','severity','expected_next_command','expected_fix'}
 assert all(required <= set(x) for x in rows)
