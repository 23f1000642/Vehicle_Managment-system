from celery import current_app as celery_app
from app import db, mail
from app.models import User, Reservation, ParkingLot
from flask_mail import Message
from datetime import datetime, timedelta
import csv
import os
from jinja2 import Template

@celery_app.task
def send_daily_reminders():
    """Send daily reminders to inactive users"""
    try:
        # Find users who haven't made a reservation in the last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        
        # Get all users except admin
        all_users = User.query.filter_by(role='user').all()
        inactive_users = []
        
        for user in all_users:
            recent_reservation = Reservation.query.filter(
                Reservation.user_id == user.id,
                Reservation.created_at >= seven_days_ago
            ).first()
            
            if not recent_reservation:
                inactive_users.append(user)
        
        # Send reminder emails
        sent_count = 0
        for user in inactive_users:
            try:
                send_reminder_email(user)
                sent_count += 1
            except Exception as e:
                print(f"Failed to send reminder to {user.email}: {str(e)}")
        
        return f"Daily reminders sent to {sent_count} users"
    
    except Exception as e:
        return f"Error sending daily reminders: {str(e)}"

@celery_app.task
def send_monthly_reports():
    """Send monthly activity reports to all users"""
    try:
        # Get all users except admin
        users = User.query.filter_by(role='user').all()
        sent_count = 0
        
        for user in users:
            try:
                # Generate and send monthly report
                send_monthly_report_email(user)
                sent_count += 1
            except Exception as e:
                print(f"Failed to send monthly report to {user.email}: {str(e)}")
        
        return f"Monthly reports sent to {sent_count} users"
    
    except Exception as e:
        return f"Error sending monthly reports: {str(e)}"

@celery_app.task
def export_user_data_async(user_id):
    """Async CSV export for user data"""
    try:
        user = User.query.get(user_id)
        if not user:
            return "User not found"
        
        # Get user's reservations
        reservations = Reservation.query.filter_by(user_id=user_id).all()
        
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Create CSV file
        csv_filename = f"parking_history_{user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_path = os.path.join('exports', csv_filename)
        
        # Write CSV data
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Reservation ID', 'Location', 'Spot Number', 'Parking Time', 'Leaving Time', 'Cost', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for reservation in reservations:
                writer.writerow({
                    'Reservation ID': reservation.id,
                    'Location': reservation.parking_spot.parking_lot.prime_location_name if reservation.parking_spot else 'N/A',
                    'Spot Number': reservation.parking_spot.spot_number if reservation.parking_spot else 'N/A',
                    'Parking Time': reservation.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.parking_timestamp else 'N/A',
                    'Leaving Time': reservation.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if reservation.leaving_timestamp else 'Active',
                    'Cost': f"₹{reservation.parking_cost}" if reservation.parking_cost else '₹0',
                    'Status': reservation.status
                })
        
        # Send notification email with CSV attachment
        send_csv_export_email(user, csv_path)
        
        return f"CSV export completed for user {user.username}"
    
    except Exception as e:
        return f"Error exporting CSV: {str(e)}"

def send_reminder_email(user):
    """Send reminder email to inactive user"""
    try:
        # Get available parking lots count
        available_lots = ParkingLot.query.filter(
            ParkingLot.id.in_(
                db.session.query(ParkingLot.id).join(ParkingLot.parking_spots).filter_by(status='A')
            )
        ).count()
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #007bff; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .footer { background-color: #f8f9fa; padding: 10px; text-align: center; color: #6c757d; }
                .btn { background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🚗 Vehicle Parking Management</h2>
            </div>
            <div class="content">
                <h3>Hi {{ username }}!</h3>
                <p>We noticed you haven't booked a parking spot recently. Don't miss out on convenient parking!</p>
                <p><strong>{{ available_lots }}</strong> parking lots have available spots right now.</p>
                <p>Book your parking spot today and enjoy hassle-free parking.</p>
                <p><a href="http://localhost:8080/dashboard" class="btn">Book Parking Now</a></p>
            </div>
            <div class="footer">
                <p>This is an automated reminder. You received this because you're registered with our parking system.</p>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_body = template.render(username=user.username, available_lots=available_lots)
        
        msg = Message(
            subject='🚗 Parking Reminder - Available Spots Waiting!',
            recipients=[user.email],
            html=html_body
        )
        
        mail.send(msg)
        
    except Exception as e:
        raise Exception(f"Failed to send reminder email: {str(e)}")

def send_monthly_report_email(user):
    """Send monthly activity report to user"""
    try:
        # Get current month data
        now = datetime.utcnow()
        first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get user's reservations for this month
        monthly_reservations = Reservation.query.filter(
            Reservation.user_id == user.id,
            Reservation.created_at >= first_day
        ).all()
        
        # Calculate statistics
        total_bookings = len(monthly_reservations)
        total_spent = sum(r.parking_cost or 0 for r in monthly_reservations)
        completed_bookings = len([r for r in monthly_reservations if r.status == 'completed'])
        
        # Most used parking lot
        lot_usage = {}
        for reservation in monthly_reservations:
            if reservation.parking_spot and reservation.parking_spot.parking_lot:
                lot_name = reservation.parking_spot.parking_lot.prime_location_name
                lot_usage[lot_name] = lot_usage.get(lot_name, 0) + 1
        
        most_used_lot = max(lot_usage.items(), key=lambda x: x[1]) if lot_usage else ("None", 0)
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #28a745; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .stats { display: flex; justify-content: space-around; margin: 20px 0; }
                .stat-box { background-color: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; min-width: 120px; }
                .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
                .footer { background-color: #f8f9fa; padding: 10px; text-align: center; color: #6c757d; }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>📊 Monthly Parking Report</h2>
                <p>{{ month_year }}</p>
            </div>
            <div class="content">
                <h3>Hi {{ username }}!</h3>
                <p>Here's your parking activity summary for this month:</p>
                
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-number">{{ total_bookings }}</div>
                        <div>Total Bookings</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{{ completed_bookings }}</div>
                        <div>Completed</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">₹{{ total_spent }}</div>
                        <div>Total Spent</div>
                    </div>
                </div>
                
                <h4>📍 Most Used Parking Lot:</h4>
                <p><strong>{{ most_used_lot_name }}</strong> ({{ most_used_lot_count }} visits)</p>
                
                <p>Thank you for using our parking management system!</p>
            </div>
            <div class="footer">
                <p>Vehicle Parking Management System - Monthly Report</p>
            </div>
        </body>
        </html>
        """
        
        template = Template(html_template)
        html_body = template.render(
            username=user.username,
            month_year=now.strftime('%B %Y'),
            total_bookings=total_bookings,
            completed_bookings=completed_bookings,
            total_spent=total_spent,
            most_used_lot_name=most_used_lot[0],
            most_used_lot_count=most_used_lot[1]
        )
        
        msg = Message(
            subject=f'📊 Your Monthly Parking Report - {now.strftime("%B %Y")}',
            recipients=[user.email],
            html=html_body
        )
        
        mail.send(msg)
        
    except Exception as e:
        raise Exception(f"Failed to send monthly report: {str(e)}")

def send_csv_export_email(user, csv_path):
    """Send email notification when CSV export is complete"""
    try:
        msg = Message(
            subject='📥 Your Parking Data Export is Ready',
            recipients=[user.email],
            body=f'Hi {user.username},\n\nYour parking data export has been completed successfully.\n\nThe CSV file is attached to this email.\n\nBest regards,\nVehicle Parking Management Team'
        )
        
        # Attach the CSV file
        with open(csv_path, 'rb') as f:
            msg.attach(
                filename=os.path.basename(csv_path),
                content_type='text/csv',
                data=f.read()
            )
        
        mail.send(msg)
        
        # Clean up the file after sending
        os.remove(csv_path)
        
    except Exception as e:
        raise Exception(f"Failed to send CSV export email: {str(e)}")