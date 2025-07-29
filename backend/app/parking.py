from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import User, ParkingLot, ParkingSpot, Reservation
from datetime import datetime
import json

parking_bp = Blueprint('parking', __name__)

def admin_required():
    """Check if current user is admin"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    return user and user.role == 'admin'

@parking_bp.route('/lots', methods=['GET'])
@jwt_required()
def get_parking_lots():
    """Get all parking lots with Redis caching"""
    try:
        # Try to get from cache first
        cache_key = 'parking_lots_all'
        
        if current_app.redis:
            try:
                cached_data = current_app.redis.get(cache_key)
                if cached_data:
                    return jsonify({
                        'parking_lots': json.loads(cached_data),
                        'from_cache': True
                    }), 200
            except:
                pass  # Continue without cache if Redis fails
        
        # Get from database
        lots = ParkingLot.query.all()
        lots_data = [lot.to_dict() for lot in lots]
        
        # Cache the result for 5 minutes
        if current_app.redis:
            try:
                current_app.redis.setex(cache_key, 300, json.dumps(lots_data))
            except:
                pass  # Continue without caching if Redis fails
        
        return jsonify({
            'parking_lots': lots_data,
            'from_cache': False
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/test-daily-reminder', methods=['POST'])
@jwt_required()
def test_daily_reminder():
    """Test daily reminder functionality (Admin only)"""
    try:
        if not admin_required():
            return jsonify({'error': 'Admin access required'}), 403
        
        # Import and run the task synchronously for testing
        from app.tasks import send_daily_reminders
        
        # Call the function directly (not as Celery task)
        result = send_daily_reminders()
        
        return jsonify({
            'message': 'Daily reminder test completed',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/test-monthly-report', methods=['POST'])
@jwt_required()
def test_monthly_report():
    """Test monthly report functionality (Admin only)"""
    try:
        if not admin_required():
            return jsonify({'error': 'Admin access required'}), 403
        
        # Import and run the task synchronously for testing
        from app.tasks import send_monthly_reports
        
        # Call the function directly (not as Celery task)
        result = send_monthly_reports()
        
        return jsonify({
            'message': 'Monthly report test completed',
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots', methods=['POST'])
@jwt_required()
def create_parking_lot():
    """Create a new parking lot (Admin only)"""
    try:
        if not admin_required():
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['prime_location_name', 'price', 'address', 'pin_code', 'number_of_spots']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate data types
        try:
            price = float(data['price'])
            number_of_spots = int(data['number_of_spots'])
        except ValueError:
            return jsonify({'error': 'Price must be a number and number_of_spots must be an integer'}), 400
        
        if number_of_spots <= 0:
            return jsonify({'error': 'Number of spots must be greater than 0'}), 400
        
        # Create parking lot
        parking_lot = ParkingLot(
            prime_location_name=data['prime_location_name'].strip(),
            price=price,
            address=data['address'].strip(),
            pin_code=data['pin_code'].strip(),
            number_of_spots=number_of_spots
        )
        
        db.session.add(parking_lot)
        db.session.flush()  # Get the ID
        
        # Create parking spots automatically
        for i in range(1, number_of_spots + 1):
            spot = ParkingSpot(
                lot_id=parking_lot.id,
                spot_number=i,
                status='A'  # Available
            )
            db.session.add(spot)

        db.session.commit()
        
        # Clear cache when new lot is created
        if current_app.redis:
            try:
                current_app.redis.delete('parking_lots_all')
            except:
                pass
        
        return jsonify({
            'message': 'Parking lot created successfully',
            'parking_lot': parking_lot.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@jwt_required()
def update_parking_lot(lot_id):
    """Update parking lot (Admin only)"""
    try:
        if not admin_required():
            return jsonify({'error': 'Admin access required'}), 403
        
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify({'error': 'Parking lot not found'}), 404
        
        data = request.get_json()
        
        # Update basic fields
        if 'prime_location_name' in data:
            lot.prime_location_name = data['prime_location_name'].strip()
        if 'price' in data:
            try:
                lot.price = float(data['price'])
            except ValueError:
                return jsonify({'error': 'Price must be a number'}), 400
        if 'address' in data:
            lot.address = data['address'].strip()
        if 'pin_code' in data:
            lot.pin_code = data['pin_code'].strip()
        
        # Handle number_of_spots change
        if 'number_of_spots' in data:
            try:
                new_spots = int(data['number_of_spots'])
            except ValueError:
                return jsonify({'error': 'Number of spots must be an integer'}), 400
            
            if new_spots <= 0:
                return jsonify({'error': 'Number of spots must be greater than 0'}), 400
            
            current_spots = len(lot.parking_spots)
            
            if new_spots < current_spots:
                # Check if we can reduce spots (no occupied spots beyond new limit)
                spots_to_remove = ParkingSpot.query.filter(
                    ParkingSpot.lot_id == lot_id,
                    ParkingSpot.spot_number > new_spots
                ).all()
                
                occupied_spots = [s for s in spots_to_remove if s.status == 'O']
                if occupied_spots:
                    return jsonify({
                        'error': f'Cannot reduce spots. Spots {[s.spot_number for s in occupied_spots]} are currently occupied'
                    }), 400
                
                # Remove extra spots
                for spot in spots_to_remove:
                    db.session.delete(spot)
            
            elif new_spots > current_spots:
                # Add new spots
                for i in range(current_spots + 1, new_spots + 1):
                    new_spot = ParkingSpot(
                        lot_id=lot_id,
                        spot_number=i,
                        status='A'
                    )
                    db.session.add(new_spot)
            
            lot.number_of_spots = new_spots
        
        db.session.commit()
        
        return jsonify({
            'message': 'Parking lot updated successfully',
            'parking_lot': lot.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@jwt_required()
def delete_parking_lot(lot_id):
    """Delete parking lot (Admin only, only if all spots are empty)"""
    try:
        if not admin_required():
            return jsonify({'error': 'Admin access required'}), 403
        
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify({'error': 'Parking lot not found'}), 404
        
        # Check if any spots are occupied
        occupied_spots = ParkingSpot.query.filter(
            ParkingSpot.lot_id == lot_id,
            ParkingSpot.status == 'O'
        ).count()
        
        if occupied_spots > 0:
            return jsonify({
                'error': f'Cannot delete parking lot. {occupied_spots} spots are currently occupied'
            }), 400
        
        # Delete all spots and the lot
        ParkingSpot.query.filter_by(lot_id=lot_id).delete()
        db.session.delete(lot)
        db.session.commit()
        
        return jsonify({'message': 'Parking lot deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/lots/<int:lot_id>/spots', methods=['GET'])
@jwt_required()
def get_parking_spots(lot_id):
    """Get all spots in a parking lot"""
    try:
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify({'error': 'Parking lot not found'}), 404
        
        spots = ParkingSpot.query.filter_by(lot_id=lot_id).order_by(ParkingSpot.spot_number).all()
        
        spots_data = []
        for spot in spots:
            spot_data = spot.to_dict()
            
            # If spot is occupied, get reservation details
            if spot.status == 'O':
                active_reservation = Reservation.query.filter_by(
                    spot_id=spot.id, 
                    status='active'
                ).first()
                
                if active_reservation:
                    spot_data['reservation'] = {
                        'user_id': active_reservation.user_id,
                        'username': active_reservation.user.username,
                        'parking_timestamp': active_reservation.parking_timestamp.isoformat(),
                        'parking_cost': active_reservation.parking_cost
                    }
            
            spots_data.append(spot_data)
        
        return jsonify({
            'parking_lot': lot.to_dict(),
            'spots': spots_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/book', methods=['POST'])
@jwt_required()
def book_parking_spot():
    """Book a parking spot (User) - automatically allocates first available spot"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        if not data.get('lot_id'):
            return jsonify({'error': 'lot_id is required'}), 400
        
        lot_id = data['lot_id']
        
        # Check if lot exists
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify({'error': 'Parking lot not found'}), 404
        
        # Check if user already has an active reservation
        active_reservation = Reservation.query.filter_by(
            user_id=user_id,
            status='active'
        ).first()
        
        if active_reservation:
            return jsonify({'error': 'You already have an active reservation'}), 400
        
        # Find first available spot
        available_spot = ParkingSpot.query.filter_by(
            lot_id=lot_id,
            status='A'
        ).order_by(ParkingSpot.spot_number).first()
        
        if not available_spot:
            return jsonify({'error': 'No available spots in this parking lot'}), 400
        
        # Create reservation
        reservation = Reservation(
            spot_id=available_spot.id,
            user_id=user_id,
            parking_timestamp=datetime.utcnow(),
            parking_cost=lot.price,
            status='active'
        )
        
        # Update spot status
        available_spot.status = 'O'
        
        db.session.add(reservation)
        db.session.commit()
        
        return jsonify({
            'message': 'Parking spot booked successfully',
            'reservation': reservation.to_dict(),
            'spot': available_spot.to_dict(),
            'parking_lot': lot.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/release/<int:reservation_id>', methods=['POST'])
@jwt_required()
def release_parking_spot(reservation_id):
    """Release/vacate a parking spot"""
    try:
        user_id = int(get_jwt_identity())
        
        reservation = Reservation.query.get(reservation_id)
        if not reservation:
            return jsonify({'error': 'Reservation not found'}), 404
        
        # Check if user owns this reservation or is admin
        user = User.query.get(user_id)
        if reservation.user_id != user_id and user.role != 'admin':
            return jsonify({'error': 'Access denied'}), 403
        
        if reservation.status != 'active':
            return jsonify({'error': 'Reservation is not active'}), 400
        
        # Calculate final cost based on time spent
        leaving_time = datetime.utcnow()
        time_spent = leaving_time - reservation.parking_timestamp
        hours_spent = max(1, time_spent.total_seconds() / 3600)  # Minimum 1 hour
        
        final_cost = round(hours_spent * reservation.parking_spot.parking_lot.price, 2)
        
        # Update reservation
        reservation.leaving_timestamp = leaving_time
        reservation.parking_cost = final_cost
        reservation.status = 'completed'
        
        # Update spot status
        reservation.parking_spot.status = 'A'
        
        db.session.commit()
        
        return jsonify({
            'message': 'Parking spot released successfully',
            'reservation': reservation.to_dict(),
            'final_cost': final_cost,
            'hours_spent': round(hours_spent, 2)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/my-reservations', methods=['GET'])
@jwt_required()
def get_my_reservations():
    """Get current user's reservations"""
    try:
        user_id = int(get_jwt_identity())
        
        reservations = Reservation.query.filter_by(user_id=user_id).order_by(
            Reservation.created_at.desc()
        ).all()
        
        return jsonify({
            'reservations': [reservation.to_dict() for reservation in reservations]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/export-csv', methods=['POST'])
@jwt_required()
def export_csv_async():
    """Trigger async CSV export for user data"""
    try:
        user_id = int(get_jwt_identity())
        print(f"Starting CSV export for user ID: {user_id}")
        
        # Check if user exists
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        print(f"User found: {user.username}")
        
        # Import the task here to avoid circular imports
        try:
            from app.tasks import export_user_data_async
            print("Task imported successfully")
        except ImportError as e:
            print(f"Failed to import task: {e}")
            return jsonify({'error': 'Task import failed'}), 500
        
        # Start async task
        try:
            task = export_user_data_async.delay(user_id)
            print(f"Task started with ID: {task.id}")
        except Exception as e:
            print(f"Failed to start task: {e}")
            return jsonify({'error': f'Task start failed: {str(e)}'}), 500
        
        return jsonify({
            'message': 'CSV export started! You will receive an email when it\'s ready.',
            'task_id': task.id
        }), 200
        
    except Exception as e:
        print(f"Error in export_csv_async: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@parking_bp.route('/export-csv-sync', methods=['POST'])
@jwt_required()
def export_csv_sync():
    """Synchronous CSV export (temporary fix)"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user's reservations
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        
        # Create CSV data
        import csv
        from io import StringIO
        
        output = StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Reservation ID', 'Location', 'Spot Number', 'Parking Time', 'Leaving Time', 'Cost', 'Status'])
        
        # Write data
        for reservation in reservations:
            writer.writerow([
                reservation.id,
                reservation.parking_spot.parking_lot.prime_location_name if reservation.parking_spot else 'N/A',
                reservation.parking_spot.spot_number if reservation.parking_spot else 'N/A',
                reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_timestamp else 'N/A',
                reservation.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_timestamp else 'Active',
                f"₹{reservation.parking_cost}" if reservation.parking_cost else '₹0',
                reservation.status
            ])
        
        # Get CSV content
        csv_content = output.getvalue()
        output.close()
        
        # Return CSV as response
        from flask import Response
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=parking_history_{user.username}.csv'}
        )
        
    except Exception as e:
        print(f"Error in sync CSV export: {e}")
        return jsonify({'error': str(e)}), 500