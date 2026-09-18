from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for contacts/leads
CONTACTS = [
    {"id": 1, "name": "Jane Doe", "phone": "0712345678", "email": "jane@example.com", "notes": "Interested in bulk printing services."}
]

@app.route('/')
def crm_home():
    contact_html = ""
    for c in CONTACTS:
        contact_html += f'''
        <div style="background: #1b2230; border-radius: 8px; padding: 12px; margin-bottom: 10px; border: 1px solid #2a3447;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 14px; font-weight: bold; color: #fff;">{c['name']}</span>
                <span style="font-size: 11px; color: #38bdf8;">{c['phone']}</span>
            </div>
            <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Email: {c['email']}</div>
            <div style="font-size: 11px; color: #cbd5e1; background: #121824; padding: 6px; border-radius: 4px; margin-top: 6px;">Notes: {c['notes']}</div>
        </div>
        '''

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contact Directory & CRM</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{ font-family: sans-serif; background: #121824; color: #fff; margin: 0; padding: 12px; }}
            h2 {{ color: #38bdf8; border-bottom: 2px solid #38bdf8; padding-bottom: 6px; }}
            .card {{ background: #1b2230; padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid #2a3447; }}
            input, textarea {{ width: 100%; padding: 10px; margin: 6px 0 12px 0; background: #121824; border: 1px solid #334155; color: #fff; border-radius: 6px; box-sizing: border-box; font-family: sans-serif; }}
            button {{ width: 100%; padding: 12px; background: #0284c7; color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h2>Contact Directory & CRM</h2>
        <div class="card">
            <h3 style="margin-top:0; color:#38bdf8; font-size:15px;">Add New Contact</h3>
            <form action="/add_contact" method="POST">
                <input type="text" name="name" placeholder="Full Name" required>
                <input type="text" name="phone" placeholder="Phone Number" required>
                <input type="email" name="email" placeholder="Email Address">
                <textarea name="notes" rows="2" placeholder="Interaction notes..."></textarea>
                <button type="submit">+ Save Contact</button>
            </form>
        </div>
        <h3 style="color: #38bdf8; margin-top: 20px;">Contact Ledger</h3>
        {contact_html}
    </body>
    </html>
    '''

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    notes = request.form.get('notes')
    if name and phone:
        CONTACTS.insert(0, {"id": len(CONTACTS) + 1, "name": name, "phone": phone, "email": email, "notes": notes})
    return redirect(url_for('crm_home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5012, debug=True)
