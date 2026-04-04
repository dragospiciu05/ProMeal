from manager import Manager
from users_manager import UserManager
import db
def main():
    m = Manager()
    um = UserManager()
    current_user = None
    while True:
        try:
            print("\n=== PROMEAL CLIENT -  ===")
            if not current_user:
                print("1. Înregistrare (Create Account)")
                print("2. Autentificare (Login)")
                print("0. Ieșire")
            else:
                print(f"Logat ca: {current_user.f_name} (BMI: {current_user.calculate_bmi()})")
                print("3. Generează Mesele de Azi")
                print("4. Vezi Mesele de Azi & Proteine Totale")
                print("5. Vezi Lista de Cumpărături")
                print("6. Adaugă Masa la Favorite")
                print("7. Vezi Mese Favorite")
                print("8. Sterge Masa Favorita")
                print("9. Logout")
                print("0. Ieșire")

            choice = input("Alege o opțiune: ")

            if choice == "1":
                try:
                    f_name = input("Prenume: ")
                    l_name = input("Nume: ")
                    email = input("Email: ")
                    pw = input("Parola: ")
                    age = int(input("Varsta: "))
                    w = int(input("Greutate (kg): "))
                    h = int(input("Inaltime (cm): "))
                    target = input("Target (lose/maintain/gain): ")
                    gender = input("Gender (m/f): ")
                    um.create_account(f_name, l_name, email, pw, age, w, h, target, gender)
                except ValueError:
                    print("Eroare:Varsta/greutatea trebuie sa fie numere intreegi")
            elif choice == "2":
                email = input("Email: ")
                pw = input("Parola: ")
                user = um.login(email, pw)
                if user:
                    current_user = user

            elif choice == "3" and current_user:
                try:
                    m.generate_meals(current_user)
                except Exception as e:
                    print(f"Eroare {e}")

            elif choice == "4" and current_user:
                log = m.get_meal_log(current_user)
                if log:
                    log.show_meals()
                    log.calculate_all_protein()
                    log.calculate_all_calories()
                    log.calculate_all_carbo()

            elif choice == "5" and current_user:
                m.list_grocery(current_user)

            elif choice == "6" and current_user:
                meal_id = int(input("Introdu ID-ul mesei de adaugat la favorite: "))
                meal = m.get_meal(meal_id)
                m.add_meal_to_favorite(current_user, meal)

            elif choice == "7" and current_user:
                favs = m.get_favorite_meals(current_user)
                for f in favs:
                    print(f"- {f.name} ({f.category})")
            elif choice == "8" and current_user:
                meal_id = int(input("Introdu ID-ul mesei de sters de la favorite: "))
                meal = m.get_meal(meal_id)
                m.remove_favorite_meal(user,meal)
            elif choice == "9":
                current_user = None
                print("Te-ai deconectat.")
        
            elif choice == "0":
                break
            else:
                print("Opțiune invalidă sau nu ești logat!")
        except KeyboardInterrupt:
            print("Intrerupere fortata!")
            break
        except Exception as e:
            print(f"Eroare {e}")
def populare():
    m=Manager()
    db.create_database()
    print("Populam baza de date!")
    ingredients= [
        ("Ou", 13, 155, 1.1),
        ("Pui (Piept)", 31, 165, 0),
        ("Orez", 2.7, 130, 28),
        ("Avocado", 2, 160, 9),
        ("Tofu", 8, 76, 1.9),
        ("Ton Conservă", 25, 116, 0),
        ("Vită", 26, 250, 0),
        ("Broccoli", 2.8, 34, 7),
        ("Pasta (Integrală)", 5.3, 124, 25)
    ]
    for ing in ingredients:
        m.create_ingredient(ing[0],ing[1],ing[2],ing[3])
    meals_data = [
        ("breakfast", "Omletă cu Avocado"),
        ("lunch", "Pui cu Orez și Broccoli"),
        ("dinner", "Salată de Ton"),
        ("lunch", "Paste Bolognese de Vită"),
        ("breakfast", "Tofu"),
        ("dinner","Vită cu Orez si Broccoli")
    ]
    meals_ids={}
    for cat,name in meals_data:
        meal_id=m.add_meal(cat,name) # creeaza masa si returneaza id-ul din baza de date
        if meal_id:
            meals_ids[name]=meal_id # salvam in meals_ids id-ul mesei si numele (pentru a adauga ingrediente mai tarziu)
    if "Omletă cu Avocado" in meals_ids:
        meal_obj =m.get_meal(meals_ids["Omletă cu Avocado"])
        if meal_obj:
            m.add_ingredient(meal_obj,1,150)
            m.add_ingredient(meal_obj,4,80)
    if "Pui cu Orez și Broccoli" in meals_ids:
        meal_obj = m.get_meal(meals_ids["Pui cu Orez și Broccoli"])
        if meal_obj:
            m.add_ingredient(meal_obj,2,200)
            m.add_ingredient(meal_obj,3,150)
            m.add_ingredient(meal_obj,8,100)
    if "Salată de Ton" in meals_ids:
        meal_obj = m.get_meal(meals_ids["Salată de Ton"])
        if meal_obj:
            m.add_ingredient(meal_obj,6,200)
    if "Paste Bolognese de Vită" in meals_ids:
        meal_obj= m.get_meal(meals_ids["Paste Bolognese de Vită"])
        if meal_obj:
            m.add_ingredient(meal_obj,7,150)
            m.add_ingredient(meal_obj,9,100)
    if "Tofu" in meals_ids:
        meal_obj=m.get_meal(meals_ids["Tofu"])
        if meal_obj:
            m.add_ingredient(meal_obj,5,150)
    if "Vită cu Orez si Broccoli" in meals_ids:
        meal_obj = m.get_meal(meals_ids["Vită cu Orez si Broccoli"])
        if meal_obj:
            m.add_ingredient(meal_obj,7,200)
            m.add_ingredient(meal_obj,3,150)
            m.add_ingredient(meal_obj,8,50)
    print("Am populat cu succes baza!")
    
if __name__ == "__main__":
     populare()
     main()