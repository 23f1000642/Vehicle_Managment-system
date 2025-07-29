from app import create_app, db, create_admin_user

# Create Flask app
app = create_app()

# Simple test route to check if everything is working
@app.route('/')
def home():
    return {
        'message': 'Vehicle Parking Management System API',
        'status': 'running',
        'version': '1.0'
    }

@app.route('/api/test')
def test_api():
    return {
        'message': 'API is working!',
        'database': 'connected' if db else 'not connected',
        'redis': 'connected' if app.redis else 'not connected'
    }

# Shell context for Flask CLI
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'app': app
    }

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create admin user
        create_admin_user()
        
    print("🚀 Starting Flask development server...")
    print("📍 API will be available at: http://localhost:5000")
    print("🧪 Test endpoint: http://localhost:5000/api/test")
    
    app.run(debug=True, host='0.0.0.0', port=5000)