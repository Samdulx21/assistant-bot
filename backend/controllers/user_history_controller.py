import mysql.connector
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from config.database_config import get_db_connection
from models.history_report_model import History

class HistoryController():

    def get_history(self, id_p: int):
        try:
            mydb = get_db_connection()
            db = mydb.cursor()
            query = """
                    SELECT u.id, u.name, u.last_name, r.name as role_name, u.personal_id, h.description as history, h.date as exact_date 
                    FROM 
                        roles r
                    JOIN
                        role_users ru ON r.id = ru.role_id
                    JOIN
                        users u ON ru.user_id = u.id
                    JOIN
                        history_users hu ON u.id = hu.user_id
                    JOIN
                        history h ON hu.history_id = h.id
                    WHERE u.personal_id = %s AND r.description = 'Role Paciente'
                    """
            db.execute(query, (id_p,)) 
            response = db.fetchall()
            if response:
                payload = []
                for item in response:
                    content = {
                        'id': item[0],
                        'name': item[1],
                        'last_name': item[2],
                        'role_name': item[3],
                        'personal_id': item[4],
                        'history': item[5],
                        'exact_date': item[6]
                    }
                    payload.append(content)
                json_data = jsonable_encoder(payload)
                return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")     
        except mysql.connector.Error as err:
            mydb.rollback()
            return {"error": err}
        finally:
            mydb.close()


    # def insert_history(newhistory: History):
    #     try:
    #         history = newhistory.description
    #         date = newhistory.date


