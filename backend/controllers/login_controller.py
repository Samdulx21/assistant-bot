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
                        SELECT 
                            u.email as email, 
                            u.user_password as u_pass
                        FROM users as u
                        WHERE u.email = %s AND u.user_password = %s
                        """, (email, user_password))
            response = db.fetchall()
            payload = []
            content = {}
            for item in response:
                content = {
                    "email": item[0],
                    "u_pass": item[1],
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