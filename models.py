from datetime import datetime
class Ingredient:
    def __init__(self,ing_id, name,protein_per_100g,calories_per_100g,carbo_per_100g,quantity):
        self.ing_id=ing_id
        self.name=name
        self.protein_per_100g=protein_per_100g
        self.calories_per_100g=calories_per_100g
        self.carbo_per_100g=carbo_per_100g
        self.quantity=quantity
        
class Meal:
    def __init__(self,meal_id,category,name,img_url=None):
        self.meal_id=meal_id
        self.category=category
        self.name=name
        self.img_url=img_url
        self.ingredients=[]
    def add_ingredient(self,meal_ingredient):
        self.ingredients.append(meal_ingredient)
    def calculate_protein(self):
        total =0
        for item in self.ingredients:
            total += (item.protein_per_100g/100)*item.quantity
        return total
    def calculate_calories(self):
        total =0
        for item in self.ingredients:
            total+=(item.calories_per_100g/100)*item.quantity
        return total
    def calculate_carbo(self):
        total =0
        for item in self.ingredients:
            total+=(item.carbo_per_100g/100)*item.quantity
        return total
    def show_ingredients(self):
        for item in self.ingredients:
            print(f"ID: {item.ing_id}, Name: {item.name}, Qty: {item.quantity}g")
        return self.ingredients
        
class User:
    def __init__(self,id, f_name,l_name,email,password,age,weight,height,target,gender):
        self.id=id
        self.f_name=f_name
        self.l_name=l_name
        self.email=email
        self.password=password
        self.age=age
        self.weight=weight
        self.height=height
        self.target=target
        self.gender=gender
    def calculate_bmi(self):
        height_in_meters = self.height / 100
        bmi = self.weight / (height_in_meters ** 2)
        return round(bmi, 2)
            
class MealLog:
    def __init__(self,user_id,date):
        self.user_id=user_id
        self.meals=[] # Meal()
        if isinstance(date, str):
            self.date = datetime.strptime(date, "%Y-%m-%d").date()
        else:
            self.date = date
    def add_meal(self,meals_obj):
        self.meals.append(meals_obj)
        return True
    def calculate_all_protein(self):
        if not self.meals:
            print(f"Nu exista mese pentru data {self.date}")
            return None
        total =0
        for item in self.meals:
            total+=item.calculate_protein()
        print(f"Total proteine {round(total,2)}g")
        return total
    def calculate_all_calories(self):
        if not self.meals:
            print("Nu ai mese pentru data {self.date}")
        total =0
        for item in self.meals:
            total+= item.calculate_calories()
        print (f"Total calorii {round(total,2)}kcal")
        return total
    def calculate_all_carbo(self):
        if not self.meals:
            print("Nu ai mese pentru data {self.date}")
        total =0
        for item in self.meals:
            total+=item.calculate_carbo()
        print(f"Total carbohidrati {round(total,2)}g")
        return total
    def show_meals(self):
        if  not self.meals:
            print(f"Nu exista mese pentru data {self.date}")
        for  item in self.meals:
            ingredients = ", ".join([ing.name for ing in item.ingredients])
            print(f"Category: {item.category}, Name: {item.name} , Ingredients: {ingredients}")
        return self.meals