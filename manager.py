import models
import db
import users_manager as um
class Manager:
    def __init__(self):
       pass
    def get_meal(self,meal_id):
        with db.connect() as conn:
            if conn is None:
                return False
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM meals WHERE id = ?",(meal_id,))
            row=cursor.fetchone()
            if row is None:
                print("Nu exista!")
                return None
            meal = models.Meal(row['id'],row['category'],row['name'],row['img_url'])
            cursor.execute("""SELECT i.id as ing_id, i.name, i.protein_per_100g, i.calories_per_100g,i.carbo_per_100g, mi.quantity
                                FROM ingredients i
                                JOIN meal_ingredients mi ON i.id = mi.ingredient_id
                                WHERE mi.meal_id = ? """,(meal_id,))
            for ing in cursor.fetchall():
                ing_obj = models.Ingredient(ing['ing_id'],ing['name'],ing['protein_per_100g'],ing['calories_per_100g'],ing['carbo_per_100g'],ing['quantity'])
                meal.add_ingredient(ing_obj)
            return meal
        return False
    

    def add_meal(self,category,name,img_url=None):
        with db.connect() as conn:
            if conn is None: return False
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM meals WHERE name = ?",(name,))
            if cursor.fetchone() is not None:
                print("exista deja!")
                return False
            categories = ["breakfast","lunch","dinner"]
            if category.strip().lower() not in categories:
                print("Nu ai introdus categoria corect!")
                return False
            cursor.execute("INSERT  INTO meals(category,name) VALUES (? , ?)",(category.strip().lower(),name,))

            conn.commit()
            meal_id =cursor.lastrowid
            print("Ai adaugat cu succes!")
            return cursor.lastrowid
        return False
    def  create_ingredient(self,name,protein_per_100g,calories_per_100g,carbo_per_100g):
        with db.connect() as conn:
            if conn is None:
                return False
            cursor=conn.cursor()    
            cursor.execute("SELECT * FROM ingredients WHERE name = ?", (name,))
            if cursor.fetchone() is not None:
                print("Deja exista!")
                return False
            cursor.execute("INSERT INTO ingredients(name,protein_per_100g,calories_per_100g,carbo_per_100g) VALUES(?,?,?,?)",(name,protein_per_100g,calories_per_100g,carbo_per_100g))
            conn.commit()
            print("Ai adaugat cu succes!")  
            return True
        return False
    def add_ingredient(self, meal,ingredient_id,quantity):
        if meal is None:
            print("Nu exista masa!")
            return False
        with db.connect() as conn:
            if conn is None :return False
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM ingredients WHERE id = ?",(ingredient_id,))
            if cursor.fetchone() is None:
                print("Ingredientul nu exista!")
                return False
            cursor.execute("SELECT * FROM meal_ingredients WHERE ingredient_id = ? AND meal_id = ? ",(ingredient_id,meal.meal_id,))
            if cursor.fetchone() is not None:
                print("Deja exista!")
                return False
            cursor.execute("INSERT INTO meal_ingredients(meal_id,ingredient_id,quantity) VALUES (?,?,?)",(meal.meal_id,ingredient_id,quantity,))
            conn.commit()
            print("Ai adaugat cu succes")
            return True
        return False
    def add_img_url(self,img_url,meal):
        if meal is None:
            print("Masa nu exista!")
            return False
        if not isinstance(img_url,str):
            print("Eroare!")
            return False
        with db.connect() as conn:
            if conn is None:return False
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM meals WHERE id = ?", (meal.meal_id,))
            if cursor.fetchone() is None:
                print("Masa nu exista!")
                return False
            cursor.execute("UPDATE meals SET img_url = ? where id = ?",(img_url,meal.meal_id))
            print("Succes!")
            conn.commit()
            return True
        return False
    def add_meal_in_logs(self,user,meal):
        with db.connect() as conn:
            if conn is None : return False
            cursor=conn.cursor()
            if um.verify_if_user_exists(user.id) is None:
                print("Userul nu exista")
                return False
            if meal is None:
                print("Mancarea nu exista!")
                return False
            cursor.execute("INSERT INTO meal_logs(user_id,meal_id,meal_type) VALUES (?,?,?)",(user.id,meal.meal_id,meal.category,))
            conn.commit()
            print("Succes!")
            return True
        return False
    def get_meal_log(self,user):
        with db.connect() as conn:
            if conn is None:
                return False
            cursor=conn.cursor()
            if um.verify_if_user_exists(user.id) is None:
                print("Userul nu exista!")
                return False
            cursor.execute("SELECT * FROM meal_logs WHERE user_id = ? AND date = DATE('now','localtime')",(user.id,))
            logs = cursor.fetchall()
            if len(logs)==0:
                print("Utilizatorul nu are mese pe ziua de astazi!")
                return None
            meal_log_obj = models.MealLog(user.id,logs[0]['date'])
            for item in logs: 
                meal = self.get_meal(item['meal_id'])
                if meal:
                    meal_log_obj.add_meal(meal)
            return meal_log_obj
    def generate_one_meal(self,user,category,last_generated_meal):

        try:
         with db.connect() as conn:
            if conn is None:
                return False
            cursor=conn.cursor()
            if um.verify_if_user_exists(user.id) is None:
                print("Userul nu exista!")
                return False
            cursor.execute("""
                SELECT id FROM meals 
                WHERE category = ? 
                AND id NOT IN (
                    SELECT meal_id FROM meal_logs 
                    WHERE user_id = ? AND date >= DATE('now','localtime', '-1 days')
                  
                ) 
                AND id != ? 
                ORDER BY RANDOM() LIMIT 1
            """, (category.lower().strip(), user.id,last_generated_meal.meal_id if last_generated_meal is not None else -1,))
            row = cursor.fetchone()
            if row:
                return self.get_meal(row['id'])
            return None
        except Exception as e:
            print(f"Eroare la generate_one_meal {e}")
            return None
    def generate_meals(self,user):
        try:
            with db.connect() as conn:
                if conn is None:
                    return False
                cursor=conn.cursor()
                if um.verify_if_user_exists(user.id) is None:
                    print("Userul nu exista!")
                    return False
                categories = ["breakfast","lunch","dinner"]
                meal_log_obj=self.get_meal_log(user)
                logs = meal_log_obj.meals if meal_log_obj is not None else []
                if len(logs)>=3:
                    print("Deja s-au generat 3 mese!")
                    return False
                last_generated_meal=None
                for cat in categories:
                    cursor.execute("SELECT id FROM meal_logs WHERE user_id = ? AND meal_type = ? AND date = DATE('now','localtime')",(user.id,cat,))
                    if cursor.fetchone() is not None:
                        continue
                    accepted = False
                    while not accepted:
                        meal = self.generate_one_meal(user,cat,last_generated_meal)
                        if meal is None:
                            print(f"Nu am gasit nicio masa disponibila!")
                            break 
                        print(f"{meal.name}")
                        choice = input(f"Yes/No : ").strip().lower()
                        if choice == "yes":
                            self.add_meal_in_logs(user,meal)
                            accepted = True
                        elif choice == "no":
                            last_generated_meal=meal
                            print("Refresh...")
            return True
        except Exception as e:
            print(f"Eroare in generate_meals {e}")
    def list_grocery(self,user):
        if user is None:
            print("Trebuie sa fii conectat")
            return False
        if um.verify_if_user_exists(user.id) is None:
            print("Userul nu exista!")
        logs = self.get_meal_log(user)
        if logs is None:
            print("Nu ai meniu pe ziua de astazi!")
            return False
        gorcery_lsit = []
        for meal in logs.meals:
            print(f"--- {meal.category.upper()} ---")
            meal.show_ingredients()
            gorcery_lsit.append(meal)
        return gorcery_lsit
    def add_meal_to_favorite(self,user,meal):
        if user is None:
            print("Nu esti logat!")
            return False
        if um.verify_if_user_exists(user.id) is None:
            print("User nu exista!")
            return False
        if meal is None:
            print("Masa nu exista!")
            return False
        with db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM favorite_meals WHERE meal_id = ? AND user_id = ?",(meal.meal_id,user.id,))
            if cursor.fetchone() is not None:
                print("Ai deja masa adaugata ca favorit!")
                return False
            cursor.execute("INSERT INTO favorite_meals(user_id,meal_id) VALUES (?,?)",(user.id,meal.meal_id,))
            print("Masa a fost salvata ca favorit!")
            conn.commit()
            return True
    def get_favorite_meals(self,user):
        if user is None:
            print("Nu esti logat!")
            return False
        if um.verify_if_user_exists(user.id) is None:
            print("Userul nu exista!")
            return False
        with db.connect() as conn:
            cursor=conn.cursor()
            cursor.execute("SELECT * FROM favorite_meals WHERE user_id = ?",(user.id,))
            rows = cursor.fetchall()
            if len(rows) == 0 :
                print("Nu ai mese favorite")
                return []
            favorite_meals=[]
            for row in rows:
                favorite_meals.append(self.get_meal(row['meal_id']))
            return favorite_meals
    def remove_favorite_meal(self,user,meal):
        if user is None:
            print("trebuie sa fii logat!")
            return False
        if meal is None:
            print("Masa nu exista!")
            return False
        if um.verify_if_user_exists(user.id) is None:
            print("Userul nu exista!")
            return False
        with db.connect() as conn:
            cursor= conn.cursor()
            cursor.execute("SELECT * FROM favorite_meals WHERE user_id = ? AND meal_id = ?",(user.id,meal.meal_id,))
            row = cursor.fetchone()
            if row is None:
                print("Masa nu este adaugata la favorite!")
                return False
            cursor.execute("DELETE FROM favorite_meals WHERE user_id = ? AND meal_id = ?",(user.id,meal.meal_id,))
            print("Ai sters cu succes!")
            conn.commit()
            return True
                               
                    
                 
               
               

