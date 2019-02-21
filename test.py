passcode = ''
class pote():
    def one(self):
        global passcode
        passcode += '1'
        self.prints()
    def two(self):
        global passcode
        passcode += '2'
        self.prints()
    def prints(self):
        global passcode
        print(passcode)
    self.one()
# pote().one()
# pote().two()
