import db
import bcrypt
import models
class UserManager:
    def create_account(self,f_name,l_name,email,password,age,weight,height,target,gender):
        with db.connect() as conn:
            cursor=conn.cursor()
            email = email.strip().lower()
            cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
            if cursor.fetchone() is not None:
                print("Acest cont exista deja!")
                return False
            if "@" not in email or "." not in email.split("@")[-1]:
                print("email-ul nu este valid!")
                return False
            if len(password)< 5:
                print("Parola trebuie sa aibe minim 5 caractere!")
                return False
            if age <15 or age > 99:
                print("Nu ai varsta necesara!")
                return False 
            if height < 50 or height > 300 :
                print("Nu te poti inscrie!")
                return False
            if weight <10 or weight > 500:
                print("Nu te poti inscrie")
                return False
            valid_genders  = ['m','f']
            if gender.strip().lower() not in valid_genders:
                print("Nu ai introdus corect gender!")
                return False
            valid_target= ['lose','maintain','gain']
            if target.strip().lower() not in valid_target:
                print("Nu ai introdus corect target!")
                return False
            password=bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
            cursor.execute("""INSERT INTO users(f_name,l_name,email,password,age,weight,height,target,gender)
                           VALUES(?,?,?,?,?,?,?,?,?)""",(f_name.strip().title(),l_name.strip().title(),email,password,age,\
                                                           weight,height,target,gender))
            print("Succes!")
            conn.commit()
            return True
        return False
    def get_user_info(self,userid):
        with db.connect() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?",(userid,))
            row = cursor.fetchone()
            if row is None:
                print("Nu exista!")
                return False
            return models.User(row['id'],row['f_name'],row['l_name'],row['email'],row['password'],\
                               row['age'],row['weight'],row['height'],row['target'],\
                                row['gender'])
        return False
    def login(self,email,password):
        with db.connect() as conn:
            cursor=conn.cursor()
            if "@" not in email or "." not in email.split("@")[-1]:
                print("email-ul nu este valid!")
                return False
            email=email.lower()
            cursor.execute("SELECT * FROM users WHERE email = ?",(email,))
            row = cursor.fetchone()
            if row is None:
                print("Contul nu exista!")
                return False
            stored_hash = row['password']
            password_bytes = password.encode("utf-8")
            if bcrypt.checkpw(password_bytes,stored_hash):
                print(f"Te-ai logat cu succes! Salut {row['f_name']} {row['l_name']}")
                return models.User(row['id'],row['f_name'],row['l_name'],row['email'],row['password'],\
                               row['age'],row['weight'],row['height'],row['target'],\
                                row['gender']) # salvez aici sesiunea curenta 
            else :
                print("Parola gresita!")

                return False
        return 
def verify_if_user_exists(userid):
        with db.connect() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?",(userid,))
            return cursor.fetchone()
        return False
            
           
