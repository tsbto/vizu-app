def get_table_schema(client, project_id, dataset_id, table_id):
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    table = client.get_table(table_ref)

    schema_info = []
    for field in table.schema:
        schema_info.append({
            "name": field.name,
            "type": field.field_type,
            "mode": field.mode,
        })

    return schema_info

def classify_columns(schema_info):
    numeric_types = {"INTEGER", "FLOAT", "NUMERIC", "BIGNUMERIC"}
    temporal_types = {"DATE", "DATETIME", "TIMESTAMP"}
    categorical_types = {"STRING"}
    boolean_types = {"BOOLEAN"}

    classified = {
        "numerical": [],
        "temporal": [],
        "categorical": [],
        "boolean": [],
        "others": []
    }

    for field in schema_info:
        col_type = field["type"]
        name = field["name"]
        if col_type in numeric_types:
            classified["numerical"].append(name)
        elif col_type in temporal_types:
            classified["temporal"].append(name)
        elif col_type in categorical_types:
            classified["categorical"].append(name)
        elif col_type in boolean_types:
            classified["boolean"].append(name)
        else:
            classified["others"].append(name)

    return classified
