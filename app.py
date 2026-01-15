import os
import csv
import io
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'incident-management-secret-key-2024')

import sqlite3

DATABASE = 'incidents.db'

SEVERITY_LEVELS = ['Low', 'Medium', 'High', 'Critical']
STATUS_OPTIONS = ['Open', 'In Progress', 'Pending', 'Resolved', 'Closed']
CATEGORY_OPTIONS = ['Hardware', 'Software', 'Network', 'Security', 'Database', 'Application', 'Other']

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            reported_by TEXT,
            assigned_to TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            downtime_minutes INTEGER DEFAULT 0,
            root_cause TEXT,
            resolution TEXT,
            sla_target_hours INTEGER DEFAULT 24,
            sla_breached INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            flash(f'Terjadi kesalahan. Silakan coba lagi.', 'error')
            return redirect(url_for('dashboard'))
    return decorated_function

def validate_incident_input(data):
    errors = []
    if not data.get('title') or len(data.get('title', '').strip()) < 3:
        errors.append('Judul harus minimal 3 karakter')
    if data.get('severity') not in SEVERITY_LEVELS:
        errors.append('Severity tidak valid')
    if data.get('status') not in STATUS_OPTIONS:
        errors.append('Status tidak valid')
    if data.get('category') not in CATEGORY_OPTIONS:
        errors.append('Kategori tidak valid')
    return errors

def calculate_sla_status(incident):
    if incident['status'] in ['Resolved', 'Closed']:
        if incident['resolved_at']:
            created = datetime.strptime(incident['created_at'], '%Y-%m-%d %H:%M:%S')
            resolved = datetime.strptime(incident['resolved_at'], '%Y-%m-%d %H:%M:%S')
            hours_taken = (resolved - created).total_seconds() / 3600
            return hours_taken <= incident['sla_target_hours']
    else:
        created = datetime.strptime(incident['created_at'], '%Y-%m-%d %H:%M:%S')
        hours_elapsed = (datetime.now() - created).total_seconds() / 3600
        return hours_elapsed <= incident['sla_target_hours']
    return True

@app.route('/')
@handle_errors
def dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM incidents')
    total = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE status = 'Open'")
    open_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE status = 'In Progress'")
    in_progress = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE status IN ('Resolved', 'Closed')")
    resolved = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE severity = 'Critical' AND status NOT IN ('Resolved', 'Closed')")
    critical = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM incidents WHERE sla_breached = 1")
    sla_breached = cursor.fetchone()['count']
    
    cursor.execute('SELECT * FROM incidents ORDER BY created_at DESC LIMIT 5')
    recent_incidents = cursor.fetchall()
    
    cursor.execute('''
        SELECT category, COUNT(*) as count 
        FROM incidents 
        GROUP BY category 
        ORDER BY count DESC
    ''')
    by_category = cursor.fetchall()
    
    cursor.execute('''
        SELECT severity, COUNT(*) as count 
        FROM incidents 
        GROUP BY severity
    ''')
    by_severity = cursor.fetchall()
    
    conn.close()
    
    stats = {
        'total': total,
        'open': open_count,
        'in_progress': in_progress,
        'resolved': resolved,
        'critical': critical,
        'sla_breached': sla_breached,
        'sla_compliance': round((1 - sla_breached / total) * 100, 1) if total > 0 else 100
    }
    
    return render_template('dashboard.html', 
                         stats=stats, 
                         recent_incidents=recent_incidents,
                         by_category=by_category,
                         by_severity=by_severity)

@app.route('/incidents')
@handle_errors
def incidents_list():
    conn = get_db()
    cursor = conn.cursor()
    
    status_filter = request.args.get('status', '')
    severity_filter = request.args.get('severity', '')
    search = request.args.get('search', '')
    
    query = 'SELECT * FROM incidents WHERE 1=1'
    params = []
    
    if status_filter and status_filter in STATUS_OPTIONS:
        query += ' AND status = ?'
        params.append(status_filter)
    
    if severity_filter and severity_filter in SEVERITY_LEVELS:
        query += ' AND severity = ?'
        params.append(severity_filter)
    
    if search:
        query += ' AND (title LIKE ? OR description LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    incidents = cursor.fetchall()
    conn.close()
    
    return render_template('incidents.html', 
                         incidents=incidents,
                         status_options=STATUS_OPTIONS,
                         severity_levels=SEVERITY_LEVELS,
                         current_status=status_filter,
                         current_severity=severity_filter,
                         search=search)

@app.route('/incidents/new', methods=['GET', 'POST'])
@handle_errors
def create_incident():
    if request.method == 'POST':
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'category': request.form.get('category', 'Other'),
            'severity': request.form.get('severity', 'Medium'),
            'status': 'Open',
            'reported_by': request.form.get('reported_by', '').strip(),
            'assigned_to': request.form.get('assigned_to', '').strip(),
            'sla_target_hours': int(request.form.get('sla_target_hours', 24))
        }
        
        errors = validate_incident_input(data)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('incident_form.html', 
                                 incident=data, 
                                 mode='create',
                                 severity_levels=SEVERITY_LEVELS,
                                 status_options=STATUS_OPTIONS,
                                 category_options=CATEGORY_OPTIONS)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO incidents (title, description, category, severity, status, 
                                 reported_by, assigned_to, sla_target_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['title'], data['description'], data['category'], data['severity'],
              data['status'], data['reported_by'], data['assigned_to'], data['sla_target_hours']))
        conn.commit()
        incident_id = cursor.lastrowid
        conn.close()
        
        flash('Insiden berhasil dibuat!', 'success')
        return redirect(url_for('incident_detail', id=incident_id))
    
    return render_template('incident_form.html', 
                         incident=None, 
                         mode='create',
                         severity_levels=SEVERITY_LEVELS,
                         status_options=STATUS_OPTIONS,
                         category_options=CATEGORY_OPTIONS)

@app.route('/incidents/<int:id>')
@handle_errors
def incident_detail(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM incidents WHERE id = ?', (id,))
    incident = cursor.fetchone()
    conn.close()
    
    if not incident:
        flash('Insiden tidak ditemukan', 'error')
        return redirect(url_for('incidents_list'))
    
    sla_met = calculate_sla_status(dict(incident))
    
    return render_template('incident_detail.html', 
                         incident=incident,
                         sla_met=sla_met,
                         severity_levels=SEVERITY_LEVELS,
                         status_options=STATUS_OPTIONS)

@app.route('/incidents/<int:id>/edit', methods=['GET', 'POST'])
@handle_errors
def edit_incident(id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        old_status = request.form.get('old_status', '')
        new_status = request.form.get('status', 'Open')
        
        data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'category': request.form.get('category', 'Other'),
            'severity': request.form.get('severity', 'Medium'),
            'status': new_status,
            'assigned_to': request.form.get('assigned_to', '').strip(),
            'downtime_minutes': int(request.form.get('downtime_minutes', 0)),
            'root_cause': request.form.get('root_cause', '').strip(),
            'resolution': request.form.get('resolution', '').strip(),
            'sla_target_hours': int(request.form.get('sla_target_hours', 24))
        }
        
        errors = validate_incident_input(data)
        if errors:
            for error in errors:
                flash(error, 'error')
            cursor.execute('SELECT * FROM incidents WHERE id = ?', (id,))
            incident = cursor.fetchone()
            conn.close()
            return render_template('incident_form.html', 
                                 incident=incident, 
                                 mode='edit',
                                 severity_levels=SEVERITY_LEVELS,
                                 status_options=STATUS_OPTIONS,
                                 category_options=CATEGORY_OPTIONS)
        
        resolved_at = None
        sla_breached = 0
        
        if new_status in ['Resolved', 'Closed'] and old_status not in ['Resolved', 'Closed']:
            resolved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('SELECT created_at, sla_target_hours FROM incidents WHERE id = ?', (id,))
            incident_data = cursor.fetchone()
            if incident_data:
                created = datetime.strptime(incident_data['created_at'], '%Y-%m-%d %H:%M:%S')
                hours_taken = (datetime.now() - created).total_seconds() / 3600
                sla_breached = 1 if hours_taken > incident_data['sla_target_hours'] else 0
        
        if resolved_at:
            cursor.execute('''
                UPDATE incidents SET 
                    title = ?, description = ?, category = ?, severity = ?, status = ?,
                    assigned_to = ?, downtime_minutes = ?, root_cause = ?, resolution = ?,
                    sla_target_hours = ?, updated_at = ?, resolved_at = ?, sla_breached = ?
                WHERE id = ?
            ''', (data['title'], data['description'], data['category'], data['severity'],
                  data['status'], data['assigned_to'], data['downtime_minutes'], 
                  data['root_cause'], data['resolution'], data['sla_target_hours'],
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'), resolved_at, sla_breached, id))
        else:
            cursor.execute('''
                UPDATE incidents SET 
                    title = ?, description = ?, category = ?, severity = ?, status = ?,
                    assigned_to = ?, downtime_minutes = ?, root_cause = ?, resolution = ?,
                    sla_target_hours = ?, updated_at = ?
                WHERE id = ?
            ''', (data['title'], data['description'], data['category'], data['severity'],
                  data['status'], data['assigned_to'], data['downtime_minutes'], 
                  data['root_cause'], data['resolution'], data['sla_target_hours'],
                  datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id))
        
        conn.commit()
        conn.close()
        
        flash('Insiden berhasil diperbarui!', 'success')
        return redirect(url_for('incident_detail', id=id))
    
    cursor.execute('SELECT * FROM incidents WHERE id = ?', (id,))
    incident = cursor.fetchone()
    conn.close()
    
    if not incident:
        flash('Insiden tidak ditemukan', 'error')
        return redirect(url_for('incidents_list'))
    
    return render_template('incident_form.html', 
                         incident=incident, 
                         mode='edit',
                         severity_levels=SEVERITY_LEVELS,
                         status_options=STATUS_OPTIONS,
                         category_options=CATEGORY_OPTIONS)

@app.route('/incidents/<int:id>/update-status', methods=['POST'])
@handle_errors
def update_status(id):
    new_status = request.form.get('status')
    if new_status not in STATUS_OPTIONS:
        flash('Status tidak valid', 'error')
        return redirect(url_for('incident_detail', id=id))
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT status, created_at, sla_target_hours FROM incidents WHERE id = ?', (id,))
    incident = cursor.fetchone()
    
    if not incident:
        conn.close()
        flash('Insiden tidak ditemukan', 'error')
        return redirect(url_for('incidents_list'))
    
    old_status = incident['status']
    resolved_at = None
    sla_breached = 0
    
    if new_status in ['Resolved', 'Closed'] and old_status not in ['Resolved', 'Closed']:
        resolved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        created = datetime.strptime(incident['created_at'], '%Y-%m-%d %H:%M:%S')
        hours_taken = (datetime.now() - created).total_seconds() / 3600
        sla_breached = 1 if hours_taken > incident['sla_target_hours'] else 0
    
    if resolved_at:
        cursor.execute('''
            UPDATE incidents SET status = ?, updated_at = ?, resolved_at = ?, sla_breached = ?
            WHERE id = ?
        ''', (new_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), resolved_at, sla_breached, id))
    else:
        cursor.execute('''
            UPDATE incidents SET status = ?, updated_at = ? WHERE id = ?
        ''', (new_status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id))
    
    conn.commit()
    conn.close()
    
    flash(f'Status berhasil diubah menjadi {new_status}', 'success')
    return redirect(url_for('incident_detail', id=id))

@app.route('/export/csv')
@handle_errors
def export_csv():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM incidents ORDER BY created_at DESC')
    incidents = cursor.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Title', 'Description', 'Category', 'Severity', 'Status',
                    'Reported By', 'Assigned To', 'Created At', 'Updated At', 
                    'Resolved At', 'Downtime (min)', 'Root Cause', 'Resolution',
                    'SLA Target (hrs)', 'SLA Breached'])
    
    for incident in incidents:
        writer.writerow([
            incident['id'], incident['title'], incident['description'],
            incident['category'], incident['severity'], incident['status'],
            incident['reported_by'], incident['assigned_to'], incident['created_at'],
            incident['updated_at'], incident['resolved_at'], incident['downtime_minutes'],
            incident['root_cause'], incident['resolution'], incident['sla_target_hours'],
            'Yes' if incident['sla_breached'] else 'No'
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment;filename=incidents_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'}
    )

@app.route('/how-to-use')
def how_to_use():
    return render_template('how_to_use.html')

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
