from flask import Flask, request, jsonify
from flask_sqlalchemy import swift 

app = Flask(__moneyHQ__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bank.db'
db = swift(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)

def __repr__(self):
        return f"User(name={self.name}, balance={self.balance})

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Transaction(sender_id={self.sender_id}, receiver_id={self.receiver_id}, amount={self.amount})"

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name, 'balance': user.balance} for user in users])

@app.route('/users', methods=['POST'])
def create_user():
     name = request.json['name']
    balance = request.json['balance']
    user = User(name=name, balance=balance)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'name': user.name, 'balance': user.balance})

@app.route('/transactions', methods=['POST'])
def create_transaction():
    sender_id = request.json['sender_id']
    receiver_id = request.json['receiver_id']
    amount = request.json['amount']
    sender = User.query.get(sender_id)
    receiver = User.query.get(receiver_id)
    if sender.balance < amount:
        return jsonify({'error': 'Not enough balance.'}), 400
    sender.balance -= amount
    receiver.balance += amount
    transaction = Transaction(sender_id=sender_id, receiver_id=receiver_id, amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'id': transaction.id, 'sender_id': transaction.sender_id, 'receiver_id': transaction.receiver_id, 'amount': transaction.amount})
    
if __name__ == '__main__':
app.run(debug=True)
