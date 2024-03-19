import mysql.connector
from fastapi import HTTPException
from config.database_config import get_db_connection
from models.user_model import Users
from fastapi.encoders import jsonable_encoder

class UserController():

    def get_user(self):
        try:
            mydb = get_db_connection()
            db = mydb.cursor()
            db.execute("SELECT * FROM users")
            response = db.fetchall()
            payload = []
            content = {} 
            for item in response:
                content={
                    'id':item[0],
                    'name':item[1],
                    'last_name':item[2],
                    'personal_id':item[3],
                    'phone':item[4],
                    'address':item[5],
                    'email':item[6],
                    'user_password':item[7],
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if response:            
                return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")     
        except mysql.connector.Error as err:
            mydb.rollback()
            return {"error": err}
        finally:
            mydb.close()


    def get_patients_user(self):
        try:
            mydb = get_db_connection()
            db = mydb.cursor()
            db.execute("""
                        SELECT u.id, u.name, u.last_name, r.name as role_name, u.personal_id
                        FROM 
                            roles r
                        LEFT JOIN
                            role_users ru ON r.id = ru.role_id
                        LEFT JOIN
                            users u ON ru.user_id = u.id
                        WHERE r.description = 'Role Paciente'
                       """)
            response = db.fetchall()
            payload = []
            content = {} 
            for item in response:
                content={
                    'id': item[0],
                    'name':item[1],
                    'last_name':item[2],
                    'role_name':item[3],
                    'personal_id':item[4]
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)
            if response:            
                return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")     
        except mysql.connector.Error as err:
            mydb.rollback()
            return {"error": err}
        finally:
            mydb.close()


    def get_idpersonal_patients(self, id_p: int):
        try:
            mydb = get_db_connection()
            db = mydb.cursor()
            query = """
                    SELECT u.id, u.name, u.last_name, r.name as role_name, u.personal_id
                    FROM 
                        roles r
                    LEFT JOIN
                        role_users ru ON r.id = ru.role_id
                    LEFT JOIN
                        users u ON ru.user_id = u.id
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
                        'personal_id': item[4]
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


    def insert_user(self, newuser: Users):
        try:
            name = newuser.name
            last_name = newuser.last_name
            personal_id = newuser.personal_id
            phone = newuser.phone
            address = newuser.address
            email = newuser.email
            user_password = newuser.user_password
            mydb = get_db_connection()
            db = mydb.cursor()
            db.execute("""
                        INSERT INTO users(name,last_name,personal_id,phone,address,email,user_password) VALUES(%s,%s,%s,%s,%s,%s,%s)
                    """,(name, last_name, personal_id, phone, address, email, user_password))
            mydb.commit()
            mydb.close()
            return {"info":"User create successfully."}
        except mysql.connector.Error as err:
            mydb.rollback()
            return {"error": err}
        finally:
            mydb.close()


