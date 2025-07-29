from app import db
from datetime import datetime
from sqlalchemy import func

class User(db.Model):
    """User model for both admin and regular users"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationship with reservations
    reservations = db.relationship('Reservation', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class ParkingLot(db.Model):
    """Parking lot model"""
    __tablename__ = 'parking_lots'
    
    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price per hour/day
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    number_of_spots = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with parking spots
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ParkingLot {self.prime_location_name}>'
    
    def to_dict(self):
        available_spots = len([spot for spot in self.parking_spots if spot.status == 'A'])
        occupied_spots = len([spot for spot in self.parking_spots if spot.status == 'O'])
        
        return {
            'id': self.id,
            'prime_location_name': self.prime_location_name,
            'price': self.price,
            'address': self.address,
            'pin_code': self.pin_code,
            'number_of_spots': self.number_of_spots,
            'available_spots': available_spots,
            'occupied_spots': occupied_spots,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ParkingSpot(db.Model):
    """Parking spot model"""
    __tablename__ = 'parking_spots'
    
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    status = db.Column(db.String(1), nullable=False, default='A')  # 'A' = Available, 'O' = Occupied
    spot_number = db.Column(db.Integer, nullable=False)  # Sequential spot number within lot
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with reservations
    reservations = db.relationship('Reservation', backref='parking_spot', lazy=True)
    
    def __repr__(self):
        return f'<ParkingSpot {self.id} - {self.status}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'lot_id': self.lot_id,
            'status': self.status,
            'spot_number': self.spot_number,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Reservation(db.Model):
    """Reservation model for tracking parking bookings"""
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parking_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # 'active', 'completed', 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Reservation {self.id} - User {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'spot_id': self.spot_id,
            'user_id': self.user_id,
            'parking_timestamp': self.parking_timestamp.isoformat() if self.parking_timestamp else None,
            'leaving_timestamp': self.leaving_timestamp.isoformat() if self.leaving_timestamp else None,
            'parking_cost': self.parking_cost,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            # Include related data
            'spot_number': self.parking_spot.spot_number if self.parking_spot else None,
            'lot_name': self.parking_spot.parking_lot.prime_location_name if self.parking_spot and self.parking_spot.parking_lot else None
        }