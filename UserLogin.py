class UserLogin():
    def fromDB(self, user_id, db):
        cur = db.cursor()
        cur.execute('''SELECT * FROM users WHERE id = ?;''', (user_id))
        res = cur.fetchall()
        self.user = res[0]
        return self
    
    def create(self, user):
        self.user = user
        return self

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user['id'])
    
    def get_name(self):
        return str(self.user['nickname'])
    
    def get_user(self):
        return self.user
