from flask import Flask, request, jsonify, g
from contextlib import contextmanager
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE = 'toursync.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database"""
    try:
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(DATABASE)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        # Use direct connection for initialization
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        # Create properties table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create tours table with foreign key
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                property_id INTEGER NOT NULL,
                client_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties (id)
            );
        """)
        
        conn.commit()
        print("Database initialized successfully")
        
        # Check if tables were created
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        print("Created tables:", [table[0] for table in tables])
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

@contextmanager
def get_db_cursor():
    db = get_db()
    cursor = db.cursor()
    try:
        yield cursor
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        cursor.close()

@app.route('/api/properties', methods=['GET'])
def get_properties():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, address
            FROM properties
            ORDER BY address
        """)
        
        properties = [{'id': row[0], 'address': row[1]} for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return jsonify(properties)
    except Exception as e:
        print(f"Database error in get_properties: {str(e)}")
        return jsonify({'error': 'Failed to fetch properties'}), 500

@app.route('/api/properties', methods=['POST'])
def add_property():
    try:
        data = request.json
        if 'address' not in data:
            return jsonify({'error': 'Property address is required'}), 400
            
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO properties (address)
            VALUES (?)
        """, (data['address'],))
        
        property_id = cur.lastrowid
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'id': property_id,
            'address': data['address'],
            'message': 'Property added successfully'
        }), 201
    except Exception as e:
        print(f"Database error in add_property: {str(e)}")
        return jsonify({'error': 'Failed to add property'}), 500

@app.route('/api/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        # Check for existing tours
        cur.execute("SELECT COUNT(*) FROM tours WHERE property_id = ?", (property_id,))
        if cur.fetchone()[0] > 0:
            cur.close()
            conn.close()
            return jsonify({'error': 'Cannot delete property with scheduled tours'}), 400
        
        cur.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        deleted = cur.rowcount > 0
        
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted:
            return jsonify({'message': 'Property deleted successfully'}), 200
        return jsonify({'error': 'Property not found'}), 404
    except Exception as e:
        print(f"Database error in delete_property: {str(e)}")
        return jsonify({'error': 'Failed to delete property'}), 500

@app.route('/api/tours', methods=['GET'])
def get_tours():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        cur.execute("""
            SELECT t.id, t.property_id, t.client_name, t.phone_number, 
                   t.date, t.time, p.address as property_address
            FROM tours t
            JOIN properties p ON t.property_id = p.id
            ORDER BY t.date, t.time
        """)
        
        tours = []
        for row in cur.fetchall():
            tours.append({
                'id': row['id'],
                'property_id': row['property_id'],
                'property_address': row['property_address'],
                'client_name': row['client_name'],
                'phone_number': row['phone_number'],
                'date': row['date'],
                'time': row['time']
            })
        
        cur.close()
        conn.close()
        
        return jsonify(tours)
        
    except Exception as e:
        print(f"Database error in get_tours: {str(e)}")
        return jsonify({'error': 'Failed to fetch tours'}), 500

@app.route('/api/tours', methods=['POST'])
def add_tour():
    try:
        data = request.json
        print("Server received tour data:", data)
        
        # Parse the tour_time into date and time
        if 'tour_time' in data:
            try:
                tour_datetime = datetime.fromisoformat(data['tour_time'])
                data['date'] = tour_datetime.strftime('%Y-%m-%d')
                data['time'] = tour_datetime.strftime('%H:%M')
            except ValueError as e:
                print(f"Error parsing tour_time: {e}")
                return jsonify({'error': 'Invalid tour time format'}), 400
        
        # Validate required fields
        required_fields = ['property_id', 'client_name', 'phone_number']
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        # Get property ID from address
        cur.execute("SELECT id FROM properties WHERE address = ?", (data['property_id'],))
        property_row = cur.fetchone()
        if not property_row:
            print(f"Property not found: {data['property_id']}")
            return jsonify({'error': 'Property not found'}), 404
            
        property_id = property_row[0]
        
        cur.execute("""
            INSERT INTO tours (property_id, client_name, phone_number, date, time)
            VALUES (?, ?, ?, ?, ?)
        """, (property_id, data['client_name'], data['phone_number'], 
              data['date'], data['time']))
        
        tour_id = cur.lastrowid
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'id': tour_id,
            'message': 'Tour scheduled successfully'
        }), 201
        
    except Exception as e:
        print(f"Server error in add_tour: {str(e)}")
        return jsonify({'error': 'Failed to schedule tour'}), 500

@app.route('/api/tours/<int:tour_id>', methods=['DELETE'])
def delete_tour(tour_id):
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        
        cur.execute("DELETE FROM tours WHERE id = ?", (tour_id,))
        deleted = cur.rowcount > 0
        
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted:
            return jsonify({'message': 'Tour cancelled successfully'}), 200
        return jsonify({'error': 'Tour not found'}), 404
    except Exception as e:
        print(f"Database error in delete_tour: {str(e)}")
        return jsonify({'error': 'Failed to cancel tour'}), 500

# Initialize database before running the app
if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        print("Creating new database...")
        init_db()
    app.run(debug=True)
