from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
import json
import requests
import pandas as pd
from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from PIL import Image as PILImage
from collections import Counter

# Serve normal static from ./static and allow serving images placed in ./image
app = Flask(__name__, static_folder='static', template_folder='templates')
# For dev only; set FLASK_SECRET env var in production
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# Backend API configuration
BACKEND_API_BASE = os.environ.get('BACKEND_API_BASE', 'http://192.168.1.4:8000/')

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('user_id') or user_data.get('email')
        self.email = user_data.get('email')
        self.full_name = user_data.get('full_name', '')
        self.designation = user_data.get('designation', '')
        self.phone = user_data.get('phone', '')
        self.role = user_data.get('role', '')
        self._is_active = user_data.get('is_active', True)  # Use private variable
        self.user_id = user_data.get('user_id', '')
        self.company_id = user_data.get('company_id', '')
        self.company = user_data.get('company', {})
        self.token = user_data.get('token', '')
        self.username = user_data.get('username', '')
        self.auto_proposal_access_end_date = user_data.get('auto_proposal_access_end_date', '')
    
    @property
    def is_active(self):
        """Override Flask-Login's is_active property"""
        return self._is_active
        
    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    # Load user from session
    user_data = session.get('user')
    print(f"[load_user] Looking for user_id: {user_id}")
    print(f"[load_user] Session user data: {user_data.get('user_id') if user_data else 'No session'}")
    
    if user_data:
        # Check if user_id matches either user_id or email in session
        stored_id = user_data.get('user_id') or user_data.get('email')
        print(f"[load_user] Stored ID: {stored_id}, Match: {str(stored_id) == str(user_id)}")
        if str(stored_id) == str(user_id):
            return User(user_data)
    return None

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Image folder for logos
IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), 'image')
os.makedirs(IMAGE_FOLDER, exist_ok=True)

FORMS_PATH = os.path.join(os.path.dirname(__file__), 'data', 'forms.json')
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'data', 'config.json')
BOQ_PATH = os.path.join(os.path.dirname(__file__), 'data', 'boq_items.json')


def load_forms():
    try:
        with open(FORMS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_form(entry):
    forms = load_forms()
    entry['id'] = (max([f.get('id', 0) for f in forms]) + 1) if forms else 1
    forms.append(entry)
    os.makedirs(os.path.dirname(FORMS_PATH), exist_ok=True)
    with open(FORMS_PATH, 'w', encoding='utf-8') as f:
        json.dump(forms, f, indent=2)


def load_config():
    # Default flags if no file exists
    default_cfg = {
        "feature_flags": {
            "gpt5_mini_enabled": True,
            "scope": "all_clients",
        }
    }
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_cfg


def load_boq_items():
    try:
        with open(BOQ_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_boq_item(item):
    items = load_boq_items()
    item['id'] = (max([i.get('id', 0) for i in items]) + 1) if items else 1
    items.append(item)
    with open(BOQ_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)


def download_and_save_logo(s3_url, company_name, company_id):
    """Download logo from S3 and save it locally in the image folder"""
    try:
        if not s3_url or not s3_url.startswith('http'):
            return None
        
        # Sanitize company name for filename
        safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_company_name = safe_company_name.replace(' ', '_')
        
        # Get file extension from S3 URL
        file_ext = os.path.splitext(s3_url.split('?')[0])[1]
        if not file_ext:
            file_ext = '.png'
        
        # Create filename: CompanyName_CompanyID.ext
        logo_filename = f"{safe_company_name}_{company_id}{file_ext}"
        logo_path = os.path.join(IMAGE_FOLDER, logo_filename)
        
        # Check if already downloaded
        if os.path.exists(logo_path):
            print(f"Logo already exists locally: {logo_filename}")
            return f'/image/{logo_filename}'
        
        # Download from S3
        print(f"Downloading logo from: {s3_url}")
        response = requests.get(s3_url, timeout=10)
        response.raise_for_status()
        
        # Save to local image folder
        with open(logo_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Logo saved locally: {logo_filename}")
        return f'/image/{logo_filename}'
        
    except Exception as e:
        print(f"Error downloading logo: {str(e)}")
        return None


def extract_dominant_color_from_logo(logo_path):
    """Extract the dominant color from a logo image"""
    try:
        # Open image
        img = PILImage.open(logo_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to speed up processing
        img = img.resize((150, 150))
        
        # Get all pixels
        pixels = list(img.getdata())
        
        # Filter out very light colors (close to white) and very dark (close to black)
        filtered_pixels = []
        for r, g, b in pixels:
            # Skip if too light (background)
            if r > 240 and g > 240 and b > 240:
                continue
            # Skip if too dark (shadows)
            if r < 20 and g < 20 and b < 20:
                continue
            filtered_pixels.append((r, g, b))
        
        if not filtered_pixels:
            # If all pixels filtered, return default color
            return '#3D2B1F'
        
        # Count color occurrences
        color_counter = Counter(filtered_pixels)
        
        # Get most common color
        dominant_color = color_counter.most_common(1)[0][0]
        
        # Convert RGB to hex
        hex_color = '#{:02x}{:02x}{:02x}'.format(dominant_color[0], dominant_color[1], dominant_color[2])
        
        print(f"Extracted dominant color from logo: {hex_color}")
        return hex_color
        
    except Exception as e:
        print(f"Error extracting color from logo: {str(e)}")
        # Return default color on error
        return '#3D2B1F'


def update_boq_item(item_id, updated_item):
    items = load_boq_items()
    for i, item in enumerate(items):
        if item.get('id') == item_id:
            updated_item['id'] = item_id
            updated_item['updated_at'] = datetime.utcnow().isoformat()
            items[i] = updated_item
            break
    with open(BOQ_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)


def delete_boq_item(item_id):
    items = load_boq_items()
    items = [item for item in items if item.get('id') != item_id]
    with open(BOQ_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Load config at startup and expose to templates
app.config['FEATURE_FLAGS'] = load_config().get('feature_flags', {})


@app.context_processor
def inject_globals():
    return {
        'feature_flags': app.config.get('FEATURE_FLAGS', {}),
        'current_year': datetime.now().year,
    }


@app.route('/')
def root():
    # Redirect root to login page if not authenticated, otherwise to profile
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))


@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files (PDFs, etc.)"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/proposals', methods=['GET', 'POST'])
@login_required
def index():
    # Mustard and green brand palette
    colors = {
        # Header color requested: #a88c7b (warm muted brown)
        'mustard': '#a88c7b',        # header / primary
        'mustard_light': '#d6c6bd',  # lighter outline/accent
        'green': '#90EE90',          # Light green (for underlines/accents)
    }

    if request.method == 'POST':
        # Save the submitted proposal form to the JSON store
        client = request.form.get('client', '').strip()
        title = request.form.get('title', '').strip()
        scope = request.form.get('scope', '').strip()
        if not client and not title and not scope:
            flash('Please provide at least one field before submitting.', 'warning')
            return render_template('index.html', colors=colors, current_year=datetime.now().year)

        entry = {
            'client': client,
            'title': title,
            'scope': scope,
            'created_at': datetime.utcnow().isoformat()
        }
        save_form(entry)
        flash('Proposal saved.', 'success')
        return redirect(url_for('users'))

    return render_template('index.html', colors=colors, current_year=datetime.now().year, user=session.get('user'))


@app.route('/image/<path:filename>')
def image_file(filename):
    # Serve files placed in the repository's image/ folder (e.g. image/logo.png)
    root = os.path.join(os.path.dirname(__file__), 'image')
    return send_from_directory(root, filename)


@app.route('/proposals/view/<int:proposal_id>')
@login_required
def view_proposal(proposal_id):
    user = session.get('user')
    
    print(f"\n=== Viewing Proposal ID: {proposal_id} ===")
    
    company_id = user.get('company_id')
    if not company_id and user.get('company'):
        # Handle both dict and string company values
        company = user.get('company')
        if isinstance(company, dict):
            company_id = company.get('id')
    print(f"Company ID: {company_id}")
    
    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    
    # Load proposal from API
    proposal = None
    proposal_items = []
    
    try:
        # Get proposal details
        api_url = f'{BACKEND_API_BASE}/api/proposals/{proposal_id}'
        print(f"Fetching proposal from: {api_url}")
        response = requests.get(api_url, timeout=5)
        print(f"Proposal response status: {response.status_code}")
        if response.status_code == 200:
            proposal = response.json()
            print(f"Proposal data: {proposal}")
            
            # Get client name from clients API
            if proposal.get('client_id'):
                try:
                    client_url = f'{BACKEND_API_BASE}/api/clients/{proposal["client_id"]}'
                    print(f"Fetching client from: {client_url}")
                    client_response = requests.get(client_url, timeout=5)
                    print(f"Client response status: {client_response.status_code}")
                    if client_response.status_code == 200:
                        client = client_response.json()
                        proposal['client_name'] = client.get('client_name', 'Unknown Client')
                        print(f"Client name: {proposal['client_name']}")
                except Exception as e:
                    print(f"Error loading client name: {e}")
                    proposal['client_name'] = 'Unknown Client'
        else:
            print(f"Proposal not found - Status: {response.status_code}")
            flash(f'Proposal not found', 'danger')
            return redirect(url_for('users'))
    except Exception as e:
        print(f"Error loading proposal: {str(e)}")
        flash(f'Error loading proposal: {str(e)}', 'danger')
        return redirect(url_for('users'))
    
    # Load proposal items (BOQ items)
    try:
        items_url = f'{BACKEND_API_BASE}/api/proposal-items/proposal/{proposal_id}'
        print(f"Loading BOQ items from: {items_url}")
        items_response = requests.get(items_url, timeout=5)
        print(f"BOQ items response status: {items_response.status_code}")
        if items_response.status_code == 200:
            proposal_items = items_response.json()
            print(f"Loaded {len(proposal_items)} BOQ items")
        else:
            print(f"Failed to load BOQ items: {items_response.status_code}")
            print(f"Response: {items_response.text}")
    except Exception as e:
        print(f"Error loading proposal items: {e}")
    
    # Load clients for display
    clients_json = '[]'
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/clients/company/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                clients = response.json()
                clients_json = json.dumps(clients)
        except Exception as e:
            print(f"Error loading clients: {e}")
    
    # Load project types
    project_types = []
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/boq-items/project-types/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                project_types = response.json()
        except Exception as e:
            print(f"Error loading project types: {e}")
            project_types = ['Office', 'Residential', 'Commercial', 'Saloon', 'Other']
    
    print(f"\n=== Rendering Template ===")
    print(f"Proposal: {proposal}")
    print(f"Proposal Items count: {len(proposal_items)}")
    print(f"Readonly: True")
    print(f"=========================\n")
    
    return render_template('view_proposal.html', 
                         user=user,
                         colors=colors,
                         clients_json=clients_json, 
                         project_types=project_types,
                         proposal=proposal,
                         proposal_items=proposal_items)


@app.route('/proposals/edit/<int:proposal_id>', methods=['GET', 'POST'])
@login_required
def edit_proposal(proposal_id):
    user = session.get('user')
    
    print(f"\n=== Editing Proposal ID: {proposal_id} ===")
    
    company_id = user.get('company_id')
    if not company_id and user.get('company'):
        # Handle both dict and string company values
        company = user.get('company')
        if isinstance(company, dict):
            company_id = company.get('id')
    print(f"Company ID: {company_id}")
    
    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        print("=== Processing Edit Form Submission ===")
        
        # Get form data
        proposal_data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'amount': float(request.form.get('amount', 0) or 0),
            'status': request.form.get('status', 'Draft').strip(),
            'project_type': request.form.get('project_type', '').strip(),
            'area': request.form.get('area', '').strip(),
            'material_preferences': request.form.get('material_preferences', '').strip(),
            'special_requirement': request.form.get('special_requirement', '').strip(),
        }
        
        # Client data
        client_id = request.form.get('client_id', '').strip()
        client_data = {
            'client_name': request.form.get('client_name', '').strip(),
            'email_address': request.form.get('email_address', '').strip(),
            'mobile_number': request.form.get('mobile_number', '').strip(),
            'contact_address': request.form.get('contact_address', '').strip(),
        }
        
        # Update client if client_id exists
        if client_id:
            try:
                client_payload = {
                    'client_name': client_data['client_name'],
                    'email_address': client_data['email_address'],
                    'mobile_number': client_data['mobile_number'],
                    'contact_address': client_data['contact_address'],
                    'company_id': int(company_id),
                    'is_active': True
                }
                
                api_response = requests.put(
                    f'{BACKEND_API_BASE}/api/clients/{client_id}',
                    json=client_payload,
                    timeout=5
                )
                
                if api_response.status_code == 200:
                    print(f"Client {client_id} updated successfully")
                else:
                    print(f"Failed to update client: {api_response.status_code}")
            except Exception as e:
                print(f"Error updating client: {e}")
        
        # Update proposal
        try:
            proposal_payload = {
                'title': proposal_data['title'],
                'description': proposal_data['description'],
                'amount': proposal_data['amount'],
                'status': proposal_data['status'],
                'project_type': proposal_data['project_type'],
                'area': proposal_data['area'],
                'material_preferences': proposal_data['material_preferences'],
                'special_requirement': proposal_data['special_requirement'],
                'client_id': int(client_id) if client_id else None,
                'company_id': int(company_id),
                'user_id': user.get('id')
            }
            
            api_response = requests.put(
                f'{BACKEND_API_BASE}/api/proposals/{proposal_id}',
                json=proposal_payload,
                timeout=5
            )
            
            if api_response.status_code == 200:
                print(f"Proposal {proposal_id} updated successfully")
                
                # Update BOQ items
                boq_items_json = request.form.get('boq_items_json', '[]')
                try:
                    boq_items = json.loads(boq_items_json)
                    
                    # Get existing proposal items from API
                    existing_items_response = requests.get(
                        f'{BACKEND_API_BASE}/api/proposal-items/proposal/{proposal_id}',
                        timeout=5
                    )
                    existing_items = existing_items_response.json() if existing_items_response.status_code == 200 else []
                    existing_item_ids = {item['id'] for item in existing_items}
                    
                    # Track which items are being kept/updated
                    updated_item_ids = set()
                    
                    # Process BOQ items - update existing or create new
                    for item in boq_items:
                        item_id = item.get('id')  # This will be the proposal_item id, not boq_item_id
                        
                        item_payload = {
                            'proposal_id': proposal_id,
                            'boq_item_id': item.get('boq_item_id'),
                            'item_name': item.get('item_name', ''),
                            'description': item.get('description', ''),
                            'unit': item.get('unit', ''),
                            'qty': float(item.get('qty', 0)),
                            'unit_price': float(item.get('unit_price', 0))
                        }
                        
                        if item_id and int(item_id) in existing_item_ids:
                            # Update existing item
                            updated_item_ids.add(int(item_id))
                            item_response = requests.put(
                                f'{BACKEND_API_BASE}/api/proposal-items/{item_id}',
                                json=item_payload,
                                timeout=5
                            )
                            
                            if item_response.status_code == 200:
                                print(f"Updated BOQ item {item_id}: {item.get('item_name')}")
                            else:
                                print(f"Failed to update BOQ item {item_id}: {item_response.status_code}")
                        else:
                            # Create new item
                            item_response = requests.post(
                                f'{BACKEND_API_BASE}/api/proposal-items/',
                                json=item_payload,
                                timeout=5
                            )
                            
                            if item_response.status_code in [200, 201]:
                                new_item = item_response.json()
                                print(f"Created new BOQ item: {item.get('item_name')}")
                                if isinstance(new_item, dict) and 'id' in new_item:
                                    updated_item_ids.add(new_item['id'])
                            else:
                                print(f"Failed to create BOQ item: {item_response.status_code}")
                    
                    # Delete items that were removed (exist in DB but not in submitted form)
                    items_to_delete = existing_item_ids - updated_item_ids
                    for item_id_to_delete in items_to_delete:
                        try:
                            delete_response = requests.delete(
                                f'{BACKEND_API_BASE}/api/proposal-items/{item_id_to_delete}',
                                timeout=5
                            )
                            if delete_response.status_code in [200, 204]:
                                print(f"Deleted BOQ item {item_id_to_delete}")
                            else:
                                print(f"Failed to delete BOQ item {item_id_to_delete}: {delete_response.status_code}")
                        except Exception as e:
                            print(f"Error deleting BOQ item {item_id_to_delete}: {e}")
                    
                    flash('Proposal updated successfully!', 'success')
                    return redirect(url_for('view_proposal', proposal_id=proposal_id))
                    
                except Exception as e:
                    print(f"Error processing BOQ items: {e}")
                    flash(f'Proposal updated but error with BOQ items: {str(e)}', 'warning')
                    return redirect(url_for('view_proposal', proposal_id=proposal_id))
            else:
                print(f"Failed to update proposal: {api_response.status_code}")
                flash(f'Error updating proposal: {api_response.text}', 'danger')
                
        except Exception as e:
            print(f"Error updating proposal: {e}")
            flash(f'Error updating proposal: {str(e)}', 'danger')
    
    # Handle GET request (load proposal for editing)
    proposal = None
    proposal_items = []
    
    try:
        # Get proposal details
        api_url = f'{BACKEND_API_BASE}/api/proposals/{proposal_id}'
        print(f"Fetching proposal from: {api_url}")
        response = requests.get(api_url, timeout=5)
        print(f"Proposal response status: {response.status_code}")
        if response.status_code == 200:
            proposal = response.json()
            print(f"Proposal data: {proposal}")
            
            # Get client details
            if proposal.get('client_id'):
                try:
                    client_url = f'{BACKEND_API_BASE}/api/clients/{proposal["client_id"]}'
                    print(f"Fetching client from: {client_url}")
                    client_response = requests.get(client_url, timeout=5)
                    print(f"Client response status: {client_response.status_code}")
                    if client_response.status_code == 200:
                        client = client_response.json()
                        proposal['client_name'] = client.get('client_name', 'Unknown Client')
                        proposal['email_address'] = client.get('email_address', '')
                        proposal['mobile_number'] = client.get('mobile_number', '')
                        proposal['contact_address'] = client.get('contact_address', '')
                        print(f"Client name: {proposal['client_name']}")
                except Exception as e:
                    print(f"Error loading client details: {e}")
        else:
            print(f"Proposal not found - Status: {response.status_code}")
            flash(f'Proposal not found', 'danger')
            return redirect(url_for('users'))
    except Exception as e:
        print(f"Error loading proposal: {str(e)}")
        flash(f'Error loading proposal: {str(e)}', 'danger')
        return redirect(url_for('users'))
    
    # Load proposal items (BOQ items)
    try:
        items_url = f'{BACKEND_API_BASE}/api/proposal-items/proposal/{proposal_id}'
        print(f"Loading BOQ items from: {items_url}")
        items_response = requests.get(items_url, timeout=5)
        print(f"BOQ items response status: {items_response.status_code}")
        if items_response.status_code == 200:
            proposal_items = items_response.json()
            print(f"Loaded {len(proposal_items)} BOQ items")
        else:
            print(f"Failed to load BOQ items: {items_response.status_code}")
    except Exception as e:
        print(f"Error loading proposal items: {e}")
    
    # Load clients for display
    clients = []
    clients_json = '[]'
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/clients/company/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                clients = response.json()
                clients_json = json.dumps(clients)
        except Exception as e:
            print(f"Error loading clients: {e}")
    
    # Load project types
    project_types = []
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/boq-items/project-types/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                project_types = response.json()
        except Exception as e:
            print(f"Error loading project types: {e}")
            project_types = ['Office', 'Residential', 'Commercial', 'Saloon', 'Other']
    
    print(f"\n=== Rendering Edit Template ===")
    print(f"Proposal: {proposal}")
    print(f"Proposal Items count: {len(proposal_items)}")
    print(f"=========================\n")
    
    return render_template('new_proposal.html', 
                         user=user,
                         colors=colors,
                         clients=clients,
                         clients_json=clients_json, 
                         project_types=project_types,
                         proposal=proposal,
                         proposal_items=proposal_items,
                         edit_mode=True)


@app.route('/proposals/<int:proposal_id>/check-pdf', methods=['GET'])
@login_required
def check_proposal_pdf(proposal_id):
    """Check if PDF exists for a proposal"""
    try:
        import re
        # Get proposal details to generate filename
        api_url = f'{BACKEND_API_BASE}/api/proposals/{proposal_id}'
        response = requests.get(api_url, timeout=5)
        if response.status_code != 200:
            return jsonify({'exists': False}), 200
        
        proposal = response.json()
        proposal_title = proposal.get('title', 'Proposal')
        sanitized_title = re.sub(r'[^\w\s-]', '', proposal_title)
        sanitized_title = re.sub(r'[-\s]+', '_', sanitized_title)
        
        pdf_filename = f'{sanitized_title}_{proposal_id}.pdf'
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        
        if os.path.exists(pdf_path):
            pdf_url = f'/uploads/{pdf_filename}'
            return jsonify({'exists': True, 'pdf_url': pdf_url, 'filename': pdf_filename}), 200
        else:
            return jsonify({'exists': False}), 200
            
    except Exception as e:
        print(f"Error checking PDF: {str(e)}")
        return jsonify({'exists': False}), 200


@app.route('/proposals/<int:proposal_id>/generate-pdf', methods=['POST'])
@login_required
def generate_proposal_pdf(proposal_id):
    """Generate PDF for a proposal"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.units import inch, cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
    from io import BytesIO
    import re
    
    user = session.get('user')
    
    try:
        # Get proposal details
        api_url = f'{BACKEND_API_BASE}/api/proposals/{proposal_id}'
        response = requests.get(api_url, timeout=5)
        if response.status_code != 200:
            return {'error': 'Proposal not found'}, 404
        
        proposal = response.json()
        
        # Create sanitized filename from proposal title
        proposal_title = proposal.get('title', 'Proposal')
        # Remove special characters and replace spaces with underscores
        sanitized_title = re.sub(r'[^\w\s-]', '', proposal_title)
        sanitized_title = re.sub(r'[-\s]+', '_', sanitized_title)
        
        # Create consistent PDF filename: ProposalName_ProposalID.pdf
        pdf_filename = f'{sanitized_title}_{proposal_id}.pdf'
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        
        # Check if PDF already exists and force regenerate flag
        force_regenerate = request.get_json().get('force_regenerate', False) if request.is_json else False
        
        if os.path.exists(pdf_path) and not force_regenerate:
            # PDF already exists, return existing file
            pdf_url = f'/uploads/{pdf_filename}'
            return {'pdf_url': pdf_url, 'filename': pdf_filename, 'already_exists': True}, 200
        
        # Get client details
        client = None
        if proposal.get('client_id'):
            client_url = f'{BACKEND_API_BASE}/api/clients/{proposal["client_id"]}'
            client_response = requests.get(client_url, timeout=5)
            if client_response.status_code == 200:
                client = client_response.json()
        
        # Get proposal items
        items_url = f'{BACKEND_API_BASE}/api/proposal-items/proposal/{proposal_id}'
        items_response = requests.get(items_url, timeout=5)
        proposal_items = items_response.json() if items_response.status_code == 200 else []
        
        # Get company details from session
        company = user.get('company', {}) if isinstance(user.get('company'), dict) else {}
        
        # Create PDF
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4, 
            topMargin=0.5*inch, 
            bottomMargin=0.5*inch,
            leftMargin=0.5*inch,
            rightMargin=0.5*inch
        )
        story = []
        styles = getSampleStyleSheet()
        
        # Page width for calculations
        page_width = A4[0] - 1*inch  # Account for margins
        
        # Default brand color
        brand_color = '#3D2B1F'
        
        # ==================== HEADER SECTION ====================
        # Company Logo and Details in header
        header_data = []
        
        # Try to load company logo and extract color
        logo_img = None
        logo_path_for_color = None
        if company.get('logo_url'):
            logo_path_candidates = [
                os.path.join(IMAGE_FOLDER, os.path.basename(company['logo_url'])),
                os.path.join(os.path.dirname(__file__), company['logo_url'].lstrip('/')),
            ]
            for logo_path in logo_path_candidates:
                if os.path.exists(logo_path):
                    try:
                        logo_img = Image(logo_path, width=1.2*inch, height=1.2*inch, kind='proportional')
                        logo_path_for_color = logo_path
                        break
                    except:
                        pass
        
        # Extract dominant color from logo
        if logo_path_for_color:
            brand_color = extract_dominant_color_from_logo(logo_path_for_color)
            print(f"Using logo brand color: {brand_color}")
        else:
            print(f"Using default brand color: {brand_color}")
        
        # Company info paragraph
        company_info = []
        if company.get('company_name'):
            company_info.append(f"<b><font size=14>{company.get('company_name')}</font></b>")
        if company.get('contact_address'):
            company_info.append(f"{company.get('contact_address')}")
        if company.get('city') or company.get('state') or company.get('pincode'):
            location = f"{company.get('city', '')}, {company.get('state', '')} - {company.get('pincode', '')}"
            company_info.append(location.strip(', -'))
        if company.get('contact_email'):
            company_info.append(f"Email: {company.get('contact_email')}")
        if company.get('contact_phone'):
            company_info.append(f"Phone: {company.get('contact_phone')}")
        if company.get('gstin'):
            company_info.append(f"<b>GSTIN:</b> {company.get('gstin')}")
        
        company_para_style = ParagraphStyle(
            'CompanyInfo',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=rl_colors.HexColor(brand_color)
        )
        company_para = Paragraph('<br/>'.join(company_info), company_para_style) if company_info else Paragraph('', company_para_style)
        
        # Create header table with logo and company info
        if logo_img:
            header_data = [[logo_img, company_para]]
            header_table = Table(header_data, colWidths=[1.5*inch, page_width - 1.5*inch])
        else:
            header_data = [[company_para]]
            header_table = Table(header_data, colWidths=[page_width])
        
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Horizontal line with brand color
        line_table = Table([['']], colWidths=[page_width])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, rl_colors.HexColor(brand_color)),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 0.15*inch))
        
        # ==================== QUOTATION TITLE ====================
        title_style = ParagraphStyle(
            'QuotationTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=rl_colors.HexColor(brand_color),
            spaceAfter=15,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph("QUOTATION", title_style))
        story.append(Spacer(1, 0.15*inch))
        
        # ==================== CLIENT & PROJECT DETAILS GRID ====================
        # Create a grid with client details on left and project details on right
        grid_cell_style = ParagraphStyle(
            'GridCell',
            parent=styles['Normal'],
            fontSize=9,
            leading=11,
            textColor=rl_colors.black
        )
        
        # Client details
        client_details = []
        client_details.append(Paragraph("<b><font size=10>CLIENT DETAILS</font></b>", grid_cell_style))
        if client:
            if client.get('client_name'):
                client_details.append(Paragraph(f"<b>Name:</b> {client.get('client_name')}", grid_cell_style))
            if client.get('mobile_number'):
                client_details.append(Paragraph(f"<b>Mobile:</b> {client.get('mobile_number')}", grid_cell_style))
            if client.get('email_address'):
                client_details.append(Paragraph(f"<b>Email:</b> {client.get('email_address')}", grid_cell_style))
            if client.get('contact_address'):
                client_details.append(Paragraph(f"<b>Address:</b> {client.get('contact_address')}", grid_cell_style))
        
        # Project details
        project_details = []
        project_details.append(Paragraph("<b><font size=10>PROJECT DETAILS</font></b>", grid_cell_style))
        if proposal.get('title'):
            project_details.append(Paragraph(f"<b>Project:</b> {proposal.get('title')}", grid_cell_style))
        if proposal.get('project_type'):
            project_details.append(Paragraph(f"<b>Type:</b> {proposal.get('project_type')}", grid_cell_style))
        if proposal.get('area'):
            project_details.append(Paragraph(f"<b>Area:</b> {proposal.get('area')} sq.ft", grid_cell_style))
        if proposal.get('description'):
            project_details.append(Paragraph(f"<b>Description:</b> {proposal.get('description')}", grid_cell_style))
        if proposal.get('material_preferences'):
            project_details.append(Paragraph(f"<b>Materials:</b> {proposal.get('material_preferences')}", grid_cell_style))
        if proposal.get('special_requirement'):
            project_details.append(Paragraph(f"<b>Special Req:</b> {proposal.get('special_requirement')}", grid_cell_style))
        
        # Date
        from datetime import datetime
        current_date = datetime.now().strftime('%d-%b-%Y')
        project_details.append(Paragraph(f"<b>Date:</b> {current_date}", grid_cell_style))
        
        # Create grid table
        grid_data = [[client_details, project_details]]
        grid_table = Table(grid_data, colWidths=[page_width/2 - 0.1*inch, page_width/2 - 0.1*inch])
        grid_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), rl_colors.HexColor('#f8f8f8')),
            ('BOX', (0, 0), (-1, -1), 1, rl_colors.HexColor(brand_color)),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, rl_colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(grid_table)
        story.append(Spacer(1, 0.25*inch))
        
        # ==================== BOQ ITEMS TABLE ====================
        if proposal_items:
            # BOQ Heading
            boq_heading_style = ParagraphStyle(
                'BOQHeading',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=rl_colors.HexColor(brand_color),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph("BILL OF QUANTITIES", boq_heading_style))
            
            # BOQ Table Header
            boq_data = [[
                Paragraph('<b>S.No</b>', grid_cell_style),
                Paragraph('<b>Item Description</b>', grid_cell_style),
                Paragraph('<b>Qty</b>', grid_cell_style),
                Paragraph('<b>Unit Price (₹)</b>', grid_cell_style),
                Paragraph('<b>Amount (₹)</b>', grid_cell_style)
            ]]
            
            total_amount = 0
            
            for idx, item in enumerate(proposal_items, 1):
                item_qty = item.get('qty', 0)
                unit_price = item.get('unit_price', 0)
                item_total = item_qty * unit_price
                total_amount += item_total
                
                # Item description with name and details
                item_name = item.get('item_name', 'N/A')
                desc = item.get('description', '')
                
                item_text = f"<b>{item_name}</b>"
                if desc:
                    item_text += f"<br/><font size=8>{desc}</font>"
                
                item_para = Paragraph(item_text, grid_cell_style)
                
                boq_data.append([
                    Paragraph(str(idx), grid_cell_style),
                    item_para,
                    Paragraph(str(item_qty), grid_cell_style),
                    Paragraph(f"{unit_price:,.2f}", grid_cell_style),
                    Paragraph(f"<b>{item_total:,.2f}</b>", grid_cell_style)
                ])
            
            # BOQ Table
            boq_table = Table(
                boq_data, 
                colWidths=[0.5*inch, 3.2*inch, 0.6*inch, 1.2*inch, 1.3*inch]
            )
            boq_table.setStyle(TableStyle([
                # Header row styling with logo brand color
                ('BACKGROUND', (0, 0), (-1, 0), rl_colors.HexColor(brand_color)),
                ('TEXTCOLOR', (0, 0), (-1, 0), rl_colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                
                # Data rows styling
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # S.No center
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),  # Qty center
                ('ALIGN', (3, 1), (3, -1), 'LEFT'),    # Unit Price left align
                ('ALIGN', (4, 1), (4, -1), 'LEFT'),    # Amount left align
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                
                # Grid and borders with logo brand color
                ('GRID', (0, 0), (-1, -1), 0.5, rl_colors.grey),
                ('BOX', (0, 0), (-1, -1), 1.5, rl_colors.HexColor(brand_color)),
                
                # Padding
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                
                # Alternate row colors for better readability
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [rl_colors.white, rl_colors.HexColor('#f9f9f9')])
            ]))
            story.append(boq_table)
            story.append(Spacer(1, 0.1*inch))
            
            # ==================== TOTAL SECTION ====================
            # Create total table aligned with BOQ amount column
            # BOQ columns: [0.5, 3.2, 0.6, 1.2, 1.3] inches
            # Total should align with last column (1.3 inch for amount)
            
            total_data = [
                ['Subtotal:', f"₹ {total_amount:,.2f}"],
            ]
            
            # Add GST if available in company details
            gst_amount = 0
            if company.get('gstin'):
                gst_rate = 18  # Default GST rate
                gst_amount = total_amount * gst_rate / 100
                total_data.append([f'GST ({gst_rate}%):', f"₹ {gst_amount:,.2f}"])
            
            grand_total = total_amount + gst_amount
            total_data.append(['', ''])  # Empty row for spacing
            total_data.append(['GRAND TOTAL:', f"₹ {grand_total:,.2f}"])
            
            # Create total table - match BOQ table width structure
            # Empty space + label + amount columns
            empty_space_width = 0.5*inch + 3.2*inch + 0.6*inch  # S.No + Description + Qty columns
            label_width = 1.2*inch  # Unit Price column width
            amount_width = 1.3*inch  # Amount column width
            
            total_table = Table(total_data, colWidths=[label_width, amount_width])
            total_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),  # Left align amounts to match BOQ
                ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -2), 10),
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, -1), (-1, -1), 14),
                ('TEXTCOLOR', (0, -1), (-1, -1), rl_colors.HexColor(brand_color)),
                ('LINEABOVE', (0, -1), (-1, -1), 2, rl_colors.HexColor(brand_color)),
                ('TOPPADDING', (0, -1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -2), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),  # Match BOQ padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            # Wrapper to position total table aligned with BOQ columns
            # Create empty spacer and total table side by side
            total_wrapper = Table([[Spacer(empty_space_width, 0), total_table]], colWidths=[empty_space_width, label_width + amount_width])
            total_wrapper.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(total_wrapper)
            story.append(Spacer(1, 0.3*inch))
        else:
            total_amount = 0
        
        # ==================== FOOTER SECTION ====================
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=rl_colors.grey,
            alignment=TA_CENTER
        )
        
        terms_style = ParagraphStyle(
            'Terms',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            textColor=rl_colors.black
        )
        
        # Terms and conditions
        story.append(Paragraph("<b>Terms & Conditions:</b>", terms_style))
        terms = [
            "1. The above quotation is valid for 30 days from the date of issue.",
            "2. Payment terms: 50% advance, 30% on material delivery, 20% on completion.",
            "3. GST as applicable will be charged extra.",
            "4. Any changes to the scope of work will be charged separately.",
        ]
        for term in terms:
            story.append(Paragraph(term, terms_style))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Company signature area
        signature_text = f"""
        <br/><br/>
        <b>For {company.get('company_name', 'Company Name')}</b><br/>
        <br/><br/><br/>
        Authorized Signatory
        """
        story.append(Paragraph(signature_text, terms_style))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF URL
        pdf_url = f'/uploads/{pdf_filename}'
        return {'pdf_url': pdf_url, 'filename': pdf_filename}, 200
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'error': str(e)}, 500


@app.route('/proposals/<int:proposal_id>/send-email', methods=['POST'])
@login_required
def send_proposal_email(proposal_id):
    """Send proposal PDF via email"""
    user = session.get('user')
    
    try:
        data = request.get_json()
        recipient_email = data.get('email')
        pdf_filename = data.get('pdf_filename')
        
        if not recipient_email:
            return jsonify({'error': 'Email address is required'}), 400
        
        # Get proposal details
        api_url = f'{BACKEND_API_BASE}/api/proposals/{proposal_id}'
        response = requests.get(api_url, timeout=5)
        if response.status_code != 200:
            return jsonify({'error': 'Proposal not found'}), 404
        
        proposal = response.json()
        
        # Get client details
        client = None
        if proposal.get('client_id'):
            client_url = f'{BACKEND_API_BASE}/api/clients/{proposal["client_id"]}'
            client_response = requests.get(client_url, timeout=5)
            if client_response.status_code == 200:
                client = client_response.json()
        
        # Email configuration (you should set these as environment variables)
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        sender_email = os.environ.get('SENDER_EMAIL', '')
        sender_password = os.environ.get('SENDER_PASSWORD', '').replace(' ', '')  # Remove spaces from app password
        
        # Check if email is configured
        if not sender_email or not sender_password:
            print(f"Email not configured. Would send to: {recipient_email}")
            print(f"Proposal: {proposal.get('title')}")
            print(f"PDF: {pdf_filename}")
            return jsonify({'message': 'Email configuration not set. Email would be sent in production.', 'warning': True}), 200
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Proposal: {proposal.get('title', 'Your Proposal')}"
        
        # Email body
        client_name = client.get('client_name', 'Valued Client') if client else 'Valued Client'
        body = f"""
Dear {client_name},

Please find attached the proposal for your project: {proposal.get('title', 'N/A')}

Project Details:
- Project Type: {proposal.get('project_type', 'N/A')}
- Area: {proposal.get('area', 'N/A')} sq.ft
- Total Amount: ₹{proposal.get('amount', 0):,.2f}

{proposal.get('description', '')}

If you have any questions, please feel free to contact us.

Best regards,
Your Company Name
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF if provided
        if pdf_filename:
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
                    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                    msg.attach(pdf_attachment)
            else:
                return jsonify({'error': 'PDF file not found'}), 404
        
        # Send email
        try:
            print(f"Attempting to send email to {recipient_email}")
            print(f"SMTP Server: {smtp_server}:{smtp_port}")
            print(f"Sender Email: {sender_email}")
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.set_debuglevel(1)  # Enable debug output
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            
            print(f"✓ Email sent successfully to {recipient_email}")
            return jsonify({'message': 'Email sent successfully'}), 200
            
        except smtplib.SMTPAuthenticationError as auth_error:
            print(f"✗ Authentication failed: {str(auth_error)}")
            return jsonify({'error': 'Email authentication failed. Check your App Password.'}), 500
        except smtplib.SMTPException as smtp_error:
            print(f"✗ SMTP error: {str(smtp_error)}")
            return jsonify({'error': f'SMTP error: {str(smtp_error)}'}), 500
        except Exception as email_error:
            print(f"Error sending email: {str(email_error)}")
            return jsonify({'error': f'Failed to send email: {str(email_error)}'}), 500
        
    except Exception as e:
        print(f"Error in send_proposal_email: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/proposals/new', methods=['GET', 'POST'])
@login_required
def new_proposal():
    user = session.get('user')

    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    
    # Get company_id from user session
    company_id = user.get('company_id') or user.get('company', {}).get('id')
    
    # Load clients from API
    clients = []
    clients_json = '[]'
    
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/clients/company/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                clients = response.json()
                clients_json = json.dumps(clients)
        except Exception as e:
            flash(f'Could not load clients: {str(e)}', 'warning')
            print(f"Error loading clients: {e}")
    
    # Load project types from API
    project_types = []
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/boq-items/project-types/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                project_types = response.json()
        except Exception as e:
            print(f"Error loading project types: {e}")
            # Fallback to some default types if API fails
            project_types = ['Office', 'Residential', 'Commercial', 'Saloon', 'Other']
    
    if request.method == 'POST':
        is_new_client = request.form.get('is_new_client') == 'true'
        client_id = request.form.get('client_id', '').strip()
        
        # Client data
        client_data = {
            'client_name': request.form.get('client_name', '').strip(),
            'email_address': request.form.get('email_address', '').strip(),
            'mobile_number': request.form.get('mobile_number', '').strip(),
            'contact_address': request.form.get('contact_address', '').strip(),
        }
        
        # Project/Proposal data
        proposal_data = {
            'title': request.form.get('title', '').strip(),
            'description': request.form.get('description', '').strip(),
            'amount': float(request.form.get('amount', 0) or 0),
            'status': request.form.get('status', 'Draft').strip(),
            'project_type': request.form.get('project_type', '').strip(),
            'area': request.form.get('area', '').strip(),
            'material_preferences': request.form.get('material_preferences', '').strip(),
            'special_requirement': request.form.get('special_requirement', '').strip(),
        }
        
        # BOQ items data
        boq_items_json = request.form.get('boq_items_json', '[]')
        try:
            boq_items = json.loads(boq_items_json)
        except:
            boq_items = []
        
        # If new client, create client first (check if client already exists by email)
        if is_new_client and company_id:
            try:
                # Check if client already exists
                check_url = f'{BACKEND_API_BASE}/api/clients/company/{company_id}'
                check_response = requests.get(check_url, timeout=5)
                
                if check_response.status_code == 200:
                    existing_clients = check_response.json()
                    existing_client = next(
                        (c for c in existing_clients if c.get('email_address', '').lower() == client_data['email_address'].lower()),
                        None
                    )
                    
                    if existing_client:
                        flash(f'Client with email "{client_data["email_address"]}" already exists. Using existing client.', 'warning')
                        client_id = existing_client.get('id')
                        is_new_client = False
                    else:
                        # Create new client
                        client_payload = {
                            'company_id': int(company_id),
                            'client_name': client_data['client_name'],
                            'email_address': client_data['email_address'],
                            'mobile_number': client_data['mobile_number'],
                            'contact_address': client_data['contact_address'],
                            'is_active': True
                        }
                        
                        api_response = requests.post(
                            f'{BACKEND_API_BASE}/api/clients/',
                            json=client_payload,
                            timeout=5
                        )
                        
                        if api_response.status_code in [200, 201]:
                            created_client = api_response.json()
                            client_id = created_client.get('id')
                            flash(f'New client "{client_data["client_name"]}" created successfully', 'success')
                        else:
                            error_detail = api_response.json() if api_response.text else {}
                            flash(f'Error creating client: {api_response.status_code} - {error_detail}', 'danger')
                            return redirect(url_for('new_proposal'))
                else:
                    flash('Could not verify existing clients', 'warning')
                    
            except Exception as e:
                flash(f'Error creating client: {str(e)}', 'danger')
                return redirect(url_for('new_proposal'))
        
        # Validate client_id exists
        if not client_id:
            flash('Please select or create a client before submitting', 'danger')
            return redirect(url_for('new_proposal'))
        
        # Create proposal via API
        if company_id and client_id:
            try:
                proposal_payload = {
                    'company_id': int(company_id),
                    'client_id': int(client_id),
                    'title': proposal_data['title'],
                    'description': proposal_data['description'],
                    'amount': proposal_data['amount'],
                    'status': proposal_data['status'],
                    'project_type': proposal_data['project_type'],
                    'area': proposal_data['area'],
                    'material_preferences': proposal_data['material_preferences'],
                    'special_requirement': proposal_data['special_requirement']
                }
                
                api_response = requests.post(
                    f'{BACKEND_API_BASE}/api/proposals/',
                    json=proposal_payload,
                    timeout=5
                )
                
                if api_response.status_code in [200, 201]:
                    created_proposal = api_response.json()
                    proposal_id = created_proposal.get('id')
                    flash(f'Proposal "{proposal_data["title"]}" created successfully in database', 'success')
                    
                    # Save BOQ items to API if proposal created successfully
                    if proposal_id and boq_items:
                        saved_items = 0
                        failed_items = 0
                        
                        for item in boq_items:
                            try:
                                item_payload = {
                                    'item_name': item.get('item_name', ''),
                                    'description': item.get('description', ''),
                                    'qty': item.get('qty', 0),
                                    'unit_price': item.get('unit_price', 0),
                                    'proposal_id': proposal_id
                                }
                                
                                item_response = requests.post(
                                    f'{BACKEND_API_BASE}/api/proposal-items/',
                                    json=item_payload,
                                    timeout=5
                                )
                                
                                if item_response.status_code in [200, 201]:
                                    saved_items += 1
                                else:
                                    failed_items += 1
                                    print(f"Failed to save item: {item_response.status_code}")
                                    
                            except Exception as item_error:
                                failed_items += 1
                                print(f"Error saving BOQ item: {str(item_error)}")
                        
                        if saved_items > 0:
                            flash(f'{saved_items} BOQ item(s) saved successfully', 'success')
                        if failed_items > 0:
                            flash(f'{failed_items} BOQ item(s) failed to save', 'warning')
                    
                else:
                    error_detail = api_response.json() if api_response.text else {}
                    flash(f'Proposal saved locally, but API returned: {api_response.status_code} - {error_detail}', 'warning')
                    
            except Exception as e:
                flash(f'Proposal saved locally, but API error: {str(e)}', 'warning')
        
        # Save proposal locally as backup
        entry = {
            'client': client_data['client_name'],
            'title': proposal_data['title'],
            'scope': proposal_data['description'],
            'client_id': client_id,
            'project_type': proposal_data['project_type'],
            'amount': proposal_data['amount'],
            'status': proposal_data['status'],
            'created_at': datetime.utcnow().isoformat()
        }
        save_form(entry)
        
        flash('Proposal created successfully', 'success')
        return redirect(url_for('users'))
    
    return render_template('new_proposal.html', colors=colors, user=user, clients=clients, clients_json=clients_json, project_types=project_types)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If already logged in, redirect to profile
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    
    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    if request.method == 'POST':
        company = request.form.get('company', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Simple validation for demo: require fields non-empty
        if not email or not password:
            flash('Enter email and password', 'danger')
            return render_template('login.html', colors=colors)

        # Call backend API for authentication
        try:
            api_url = f'{BACKEND_API_BASE}/api/auth/login'
            payload = {
                'company_name': company,
                'email': email,
                'password': password
            }
            
            print(f"\n=== Login Attempt ===")
            print(f"API URL: {api_url}")
            print(f"Payload: {payload}")
            
            response = requests.post(api_url, json=payload, timeout=5)
            
            print(f"Response Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            
            if response.status_code == 200:
                # Successful login
                api_data = response.json()
                user_data = api_data.get('user', {})
                company_data = user_data.get('company', {})
                
                # Store user data in session
                session['user'] = {
                    'email': user_data.get('email', email),
                    'full_name': user_data.get('full_name', ''),
                    'designation': user_data.get('designation', ''),
                    'phone': user_data.get('phone', ''),
                    'role': user_data.get('role', ''),
                    'is_active': user_data.get('is_active', True),
                    'user_id': user_data.get('id', ''),
                    'company_id': user_data.get('company_id', ''),
                    'auto_proposal_access_end_date': user_data.get('auto_proposal_access_end_date', ''),
                    'created_at': user_data.get('created_at', ''),
                    'updated_at': user_data.get('updated_at', ''),
                    'company': company_data,
                    'token': api_data.get('token', ''),
                    'username': user_data.get('full_name', email.split('@')[0])
                }
                
                # Make session permanent
                session.permanent = True
                
                # Create User object and login
                user = User(session['user'])
                login_user(user, remember=True)
                
                print(f"[Login] User logged in: {user.get_id()}")
                print(f"[Login] Session user_id: {session['user'].get('user_id')}")
                
                flash(f'Welcome, {user_data.get("full_name", email)}', 'success')
                
                # Redirect to next page or profile
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('profile'))
            else:
                # Login failed
                print(f"Login failed - Status: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"Error data: {error_data}")
                    error_msg = error_data.get('message', 'Invalid credentials')
                except:
                    error_msg = f'Login failed with status {response.status_code}'
                flash(error_msg, 'danger')
                return render_template('login.html', colors=colors)
                
        except requests.exceptions.RequestException as e:
            # API connection error
            print(f"API Connection Error: {str(e)}")
            flash(f'Unable to connect to authentication service. Please try again later.', 'danger')
            print(f'Login API Error: {str(e)}')
            return render_template('login.html', colors=colors)

    return render_template('login.html', colors=colors)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))


@app.route('/users')
@login_required
def users():
    user = session.get('user')

    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    
    # Get company_id from user session
    company_id = user.get('company_id')
    if not company_id and user.get('company'):
        # Handle both dict and string company values
        company = user.get('company')
        if isinstance(company, dict):
            company_id = company.get('id')
        # If it's a string (fallback auth), we don't have company_id
    
    # Load proposals from API
    proposals = []
    if company_id:
        try:
            api_url = f'{BACKEND_API_BASE}/api/proposals/company/{company_id}'
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                proposals = response.json()
                
                # Load all clients to map client names
                clients = []
                try:
                    clients_url = f'{BACKEND_API_BASE}/api/clients/company/{company_id}'
                    clients_response = requests.get(clients_url, timeout=5)
                    if clients_response.status_code == 200:
                        clients = clients_response.json()
                except Exception as e:
                    print(f"Error loading clients: {e}")
                
                # Add client names to proposals
                for proposal in proposals:
                    client_id = proposal.get('client_id')
                    if client_id:
                        client = next((c for c in clients if c['id'] == client_id), None)
                        if client:
                            proposal['client_name'] = client.get('client_name', 'Unknown')
                        else:
                            proposal['client_name'] = 'Unknown'
                    else:
                        proposal['client_name'] = 'N/A'
                
                # Sort by created date (most recent first)
                proposals = sorted(proposals, key=lambda p: p.get('created_at', ''), reverse=True)
            else:
                flash(f'Could not load proposals from API: {response.status_code}', 'warning')
        except Exception as e:
            flash(f'Error loading proposals: {str(e)}', 'warning')
            print(f"Error loading proposals: {e}")
    
    # Also load local forms as backup
    forms = load_forms()
    forms = sorted(forms, key=lambda f: f.get('created_at', ''), reverse=True)
    
    return render_template('users.html', colors=colors, forms=forms, proposals=proposals, user=user)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = session.get('user')

    if request.method == 'POST':
        # Update user profile
        try:
            user_id = user.get('user_id')
            company_id = user.get('company_id')
            
            print(f"Updating profile - User ID: {user_id}, Company ID: {company_id}")
            
            # Handle logo upload
            logo_url = user.get('company', {}).get('logo_url') if isinstance(user.get('company'), dict) else None
            if 'logo' in request.files:
                logo_file = request.files['logo']
                if logo_file and logo_file.filename:
                    # Get file extension
                    file_ext = os.path.splitext(logo_file.filename)[1]
                    if not file_ext:
                        file_ext = '.png'  # Default extension
                    
                    # Get company name and ID
                    company_name = request.form.get('company_name', 'Company').strip()
                    # Sanitize company name for filename
                    safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
                    safe_company_name = safe_company_name.replace(' ', '_')
                    
                    # Create filename: CompanyName_CompanyID.ext
                    logo_filename = f"{safe_company_name}_{company_id}{file_ext}"
                    logo_path = os.path.join(IMAGE_FOLDER, logo_filename)
                    
                    # Save logo file to image folder
                    logo_file.save(logo_path)
                    logo_url = f'/image/{logo_filename}'
                    print(f"Logo uploaded: {logo_url} for Company: {company_name} (ID: {company_id})")
            
            # Prepare user data for API
            user_data = {
                'email': user.get('email'),  # Required
                'full_name': request.form.get('full_name', '').strip(),
                'phone': request.form.get('phone', '').strip(),
                'designation': request.form.get('designation', '').strip(),
                'role': user.get('role', 'User'),  # Keep existing role
                'is_active': user.get('is_active', True),  # Keep existing status
                'company_id': company_id or 0
            }
            
            # Update user via API
            user_updated = False
            if user_id:
                api_url = f'{BACKEND_API_BASE}/api/users/{user_id}'
                print(f"Calling PUT {api_url}")
                print(f"User data: {user_data}")
                
                response = requests.put(api_url, json=user_data, timeout=5)
                print(f"User update response: {response.status_code}")
                
                if response.status_code == 200:
                    # Update session with new data
                    user['full_name'] = user_data['full_name']
                    user['phone'] = user_data['phone']
                    user['designation'] = user_data['designation']
                    user_updated = True
                else:
                    print(f"Failed to update user: {response.text}")
            
            # Update company data if exists
            company_updated = False
            if company_id and isinstance(user.get('company'), dict):
                company_data = {
                    'company_name': request.form.get('company_name', '').strip(),
                    'industry_type': request.form.get('industry_type', '').strip(),
                    'contact_person': request.form.get('contact_person', '').strip(),
                    'email': request.form.get('company_email', '').strip(),
                    'phone': request.form.get('company_phone', '').strip(),
                    'alternate_phone': request.form.get('alternate_phone', '').strip(),
                    'address_line1': request.form.get('address_line1', '').strip(),
                    'address_line2': request.form.get('address_line2', '').strip(),
                    'city': request.form.get('city', '').strip(),
                    'state': request.form.get('state', '').strip(),
                    'postal_code': request.form.get('postal_code', '').strip(),
                    'country': request.form.get('country', '').strip(),
                    'website': request.form.get('website', '').strip(),
                    'gst_number': request.form.get('gst_number', '').strip(),
                    'pan_number': request.form.get('pan_number', '').strip(),
                    'logo_url': logo_url,
                    'subscription_type': user.get('company', {}).get('subscription_type', 'Free'),
                    'subscription_start_date': user.get('company', {}).get('subscription_start_date'),
                    'subscription_end_date': user.get('company', {}).get('subscription_end_date')
                }
                
                # Update company via API
                api_url = f'{BACKEND_API_BASE}/api/companies/{company_id}'
                print(f"Calling PUT {api_url}")
                print(f"Company data: {company_data}")
                
                response = requests.put(api_url, json=company_data, timeout=5)
                print(f"Company update response: {response.status_code}")
                
                if response.status_code == 200:
                    # Update session company data
                    user['company'].update(company_data)
                    company_updated = True
                else:
                    print(f"Failed to update company: {response.text}")
            
            # Update session
            if user_updated or company_updated:
                session['user'] = user
                return jsonify({
                    'success': True,
                    'message': 'Profile updated successfully!',
                    'user_updated': user_updated,
                    'company_updated': company_updated
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'error': 'Failed to update profile'
                }), 400
                    
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    
    # Download and save S3 logo locally if it exists
    if user.get('company') and isinstance(user.get('company'), dict):
        company = user['company']
        s3_logo_url = company.get('logo_url')
        
        # If logo is from S3, download and save it locally
        if s3_logo_url and 's3.amazonaws.com' in s3_logo_url:
            company_name = company.get('company_name', 'Company')
            company_id = user.get('company_id')
            
            local_logo_url = download_and_save_logo(s3_logo_url, company_name, company_id)
            if local_logo_url:
                # Update the logo URL to point to local file
                user['company']['logo_url'] = local_logo_url
                session['user'] = user
                print(f"Logo URL updated to local: {local_logo_url}")
    
    return render_template('profile.html', colors=colors, user=user)


@app.route('/boq', methods=['GET', 'POST'])
@login_required
def boq():
    user = session.get('user')

    colors = {
        'mustard': '#DAA520',
        'mustard_light': '#F4C430',
        'green': '#90EE90',
    }
    
    # Get preview data from session if exists
    preview_items = session.get('boq_preview', [])

    if request.method == 'POST':
        # Get company_id from user session
        company_id = user.get('company_id') or user.get('company', {}).get('id')
        
        # Check if it's saving preview items to database
        if 'save_preview' in request.form:
            preview_items = session.get('boq_preview', [])
            if preview_items:
                items_added = 0
                api_added = 0
                
                for item in preview_items:
                    # Save to local JSON
                    save_boq_item(item)
                    items_added += 1
                    
                    # Also save to backend API if company_id is available
                    if company_id:
                        try:
                            api_payload = {
                                'company_id': int(company_id),
                                'project_type': item['project_type'],
                                'title': item['title'],
                                'description': item['description'],
                                'unit': item['unit'],
                                'basic_rate': item['basic_rate'],
                                'premium_rate': item['premium_rate']
                            }
                            api_response = requests.post(
                                f'{BACKEND_API_BASE}/api/boq-items/',
                                json=api_payload,
                                timeout=5
                            )
                            if api_response.status_code in [200, 201]:
                                api_added += 1
                        except Exception as api_err:
                            print(f"API error for item {item['title']}: {api_err}")
                
                # Clear preview from session
                session.pop('boq_preview', None)
                
                if api_added > 0:
                    flash(f'Successfully saved {items_added} BOQ items ({api_added} saved to database)', 'success')
                else:
                    flash(f'Successfully saved {items_added} BOQ items (saved locally only)', 'success')
            else:
                flash('No preview items to save', 'warning')
            
            return redirect(url_for('boq'))
        
        # Check if it's canceling the preview
        elif 'cancel_preview' in request.form:
            session.pop('boq_preview', None)
            flash('Preview cancelled', 'info')
            return redirect(url_for('boq'))
        
        # Check if it's a file upload for preview
        elif 'excel_file' in request.files:
            file = request.files['excel_file']
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Read Excel file
                    df = pd.read_excel(file, sheet_name='Sheet1')
                    
                    # Expected columns
                    expected_cols = ['S.no', 'Project Type', 'Title', 'Description', 'Unit', 'Basic Rate', 'Premium Rate']
                    
                    # Check if all columns exist
                    if all(col in df.columns for col in expected_cols):
                        preview_data = []
                        for idx, row in df.iterrows():
                            item = {
                                's_no': str(row['S.no']),
                                'project_type': str(row['Project Type']),
                                'title': str(row['Title']),
                                'description': str(row['Description']),
                                'unit': str(row['Unit']),
                                'basic_rate': float(row['Basic Rate']) if pd.notna(row['Basic Rate']) else 0.0,
                                'premium_rate': float(row['Premium Rate']) if pd.notna(row['Premium Rate']) else 0.0,
                                'created_at': datetime.utcnow().isoformat(),
                                'preview_index': idx
                            }
                            preview_data.append(item)
                        
                        # Store in session for preview
                        session['boq_preview'] = preview_data
                        flash(f'Excel file loaded successfully. Preview {len(preview_data)} items below. Click "Save All to Database" to save.', 'info')
                    else:
                        flash('Excel file must contain columns: S.no, Project Type, Title, Description, Unit, Basic Rate, Premium Rate', 'danger')
                
                except Exception as e:
                    flash(f'Error reading Excel file: {str(e)}', 'danger')
            else:
                flash('Please upload a valid Excel file (.xlsx or .xls)', 'danger')
            
            return redirect(url_for('boq'))
        
        else:
            # Manual entry
            item = {
                's_no': request.form.get('s_no', '').strip(),
                'project_type': request.form.get('project_type', '').strip(),
                'title': request.form.get('title', '').strip(),
                'description': request.form.get('description', '').strip(),
                'unit': request.form.get('unit', '').strip(),
                'basic_rate': float(request.form.get('basic_rate', 0)),
                'premium_rate': float(request.form.get('premium_rate', 0)),
                'created_at': datetime.utcnow().isoformat()
            }
            
            if item['title']:
                # Save to local JSON
                save_boq_item(item)
                
                # Also save to backend API if company_id is available
                saved_to_api = False
                if company_id:
                    try:
                        api_payload = {
                            'company_id': int(company_id),
                            'project_type': item['project_type'],
                            'title': item['title'],
                            'description': item['description'],
                            'unit': item['unit'],
                            'basic_rate': item['basic_rate'],
                            'premium_rate': item['premium_rate']
                        }
                        api_response = requests.post(
                            f'{BACKEND_API_BASE}/api/boq-items/',
                            json=api_payload,
                            timeout=5
                        )
                        if api_response.status_code in [200, 201]:
                            saved_to_api = True
                            flash('BOQ item added successfully and saved to database', 'success')
                        else:
                            flash(f'BOQ item added locally, but API returned: {api_response.status_code}', 'warning')
                    except Exception as api_err:
                        flash(f'BOQ item added locally, but API error: {str(api_err)}', 'warning')
                
                if not saved_to_api and not company_id:
                    flash('BOQ item added successfully (saved locally only)', 'success')
            else:
                flash('Title is required', 'danger')
        
        return redirect(url_for('boq'))
    
    # GET request - show all BOQ items and preview items
    boq_items = load_boq_items()
    return render_template('boq.html', colors=colors, user=user, boq_items=boq_items, preview_items=preview_items)


@app.route('/boq/edit/<int:item_id>', methods=['POST'])
@login_required
def boq_edit(item_id):
    updated_item = {
        's_no': request.form.get('s_no', '').strip(),
        'project_type': request.form.get('project_type', '').strip(),
        'title': request.form.get('title', '').strip(),
        'description': request.form.get('description', '').strip(),
        'unit': request.form.get('unit', '').strip(),
        'basic_rate': float(request.form.get('basic_rate', 0)),
        'premium_rate': float(request.form.get('premium_rate', 0)),
    }
    
    update_boq_item(item_id, updated_item)
    flash('BOQ item updated successfully', 'success')
    return redirect(url_for('boq'))


@app.route('/boq/delete/<int:item_id>', methods=['POST'])
@login_required
def boq_delete(item_id):
    delete_boq_item(item_id)
    flash('BOQ item deleted successfully', 'success')
    return redirect(url_for('boq'))


@app.route('/boq/bulk-delete', methods=['POST'])
@login_required
def boq_bulk_delete():
    import json
    item_ids_json = request.form.get('item_ids', '[]')
    item_ids = json.loads(item_ids_json)
    
    if not item_ids:
        flash('No items selected for deletion', 'warning')
        return redirect(url_for('boq'))
    
    # Delete each item
    deleted_count = 0
    for item_id in item_ids:
        try:
            delete_boq_item(int(item_id))
            deleted_count += 1
        except Exception as e:
            print(f"Error deleting item {item_id}: {e}")
    
    flash(f'{deleted_count} BOQ item(s) deleted successfully', 'success')
    return redirect(url_for('boq'))


if __name__ == '__main__':
    app.run(debug=True)
