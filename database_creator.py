import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()
cur.execute("CREATE TABLE users(id, firstname, secondname, lastname)")
cur.execute("CREATE TABLE all_dishes(id, name, weight_in_grams, proteins, fats, carbohydrates, price)")

cur.execute("CREATE TABLE today_bl_main_dish(dish_id, count)")
cur.execute("CREATE TABLE today_bl_soups(dish_id, count)")
cur.execute("CREATE TABLE today_bl_snacks(dish_id, count)")
cur.execute("CREATE TABLE today_bl_drinks(dish_id, count)")

cur.execute("CREATE TABLE today_bl_orders(user_id, main_dish_id, soup_id, snack_id, drink_id, hh_time, mm_time)")
cur.execute("CREATE TABLE today_orders(user_id, dish_id, count, hh_time, mm_time)")
