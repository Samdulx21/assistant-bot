import mysql.connector
from fastapi import HTTPException
from config.database_config import get_db_connection
from models.user_model import LoginModel
from fastapi.encoders import jsonable_encoder

class LoginController():

    def login_user(self, userlogin: LoginModel):
        try:
            email = userlogin.email
            user_password = userlogin.user_password
            mydb = get_db_connection()
            db = mydb.cursor()
            db.execute(""" 
                        SELECT u.id, u.name, u.last_name, r.description as role, u.email, u.personal_id as cc
                        FROM 
                            users u
                        JOIN
                            role_users ru ON u.id = ru.user_id
                        JOIN
                            roles r ON ru.role_id = r.id
                        WHERE 
                            u.email = %s AND u.user_password = %s
                        """, (email, user_password))
            response = db.fetchall()
            payload = []
            content = {}
            for item in response:
                content = {
                    "id": item[0],
                    "name": item[1],
                    "last_name": item[2],
                    "role": item[3],
                    "email": item[4],
                    "cc": item[5],
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            return {"result": json_data}
        except mysql.connector.Error as err:
            mydb.rollback()
            return {"error": err + "no aparece en la base de datos" }
        finally:
            mydb.close()