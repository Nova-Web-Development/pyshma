class UserLogin():
    def fromDB(self, user_id, db):
        cur = db.cursor()
        cur.execute('''SELECT * FROM users WHERE id = ?;''', (user_id))
        res = cur.fetchall()
        self.user = res[0]
        return self
    
    def create(self, user):
        self.user = user
        self.basket = {}
        self.dish = []
        self.total_price = 0
        return self

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user['user_id'])
    
    def get_name(self):
        return str(self.user['user_name'])
    
    def get_email(self):
        return str(self.user['email'])
    
    def get_status(self):
        return str(self.user['status'])

    def get_user(self):
        return self.user
    
    def add_to_basket(self, first, second, garnir, salad, drink):
        self.first = first
        self.second = second
        self.garnir = garnir
        self.salad = salad
        self.drink = drink
        self.total_price += 100

        return self
    
    def add_to_checkout(self, dish):
        self.dish.append(dish)
        return self
    
    def get_products(self):
        return self.dish
    
    def get_checkout(self):
        return [self.first, self.second, self.garnir, self.salad, self.drink]
    
    def get_total_price(self):
        return self.total_price
    
    def clear_checkout(self):
        self.dish = ""
        self.first = ''
        self.second = ''
        self.garnir = ''
        self.salad = ''
        self.drink = ''
        
        return self