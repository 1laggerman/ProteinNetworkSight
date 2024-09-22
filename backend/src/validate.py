from src.common.configuration import close_db_conn, open_db_conn

ID_NOT_FOUND = "id not found"

def get_id_by_name(conn, name, organism) -> str:
    sql = """ 
            SELECT protein_id 
            FROM items.proteins
            WHERE preferred_name = %s and species_id =  %s
            """
    
    cur = conn.cursor()
    cur.execute(sql, (name, organism))

    if cur.rowcount == 0:
        return ID_NOT_FOUND

    rows = cur.fetchall()
    return rows[0][0]


def cal_string_id(name, organism):
    conn = open_db_conn()
    if conn is None:
        return

    id =  get_id_by_name(conn, name, organism)
    close_db_conn(conn) 

    return {"match_id" : id}