from flask import Flask, render_template_string, request, redirect, url_for
import datetime

app = Flask(__name__)

# In-memory database to store orders for your Admin Panel
orders_db = []

# Complete bundle listings
bundles_data = {
    'data': [
        {'name': '1Gb (11pm - 3pm)', 'price': '19', 'validity': '1 Hour'},
        {'name': '250mbs', 'price': '20', 'validity': '24hours'},
        {'name': '400mbs', 'price': '49', 'validity': 'Valid 7 Days'},
        {'name': '750mbs', 'price': '55', 'validity': '24hrs'},
        {'name': '1GB', 'price': '100', 'validity': 'Valid 24 Hours'},
        {'name': '2gb', 'price': '120', 'validity': '24hrs'},
        {'name': '2.5GB', 'price': '250', 'validity': '30days'},
        {'name': '7GB', 'price': '510', 'validity': '30days'},
        {'name': '21GB', 'price': '1200', 'validity': '30days'},
    ],
    'minutes': [
        {'name': '350 talktime', 'price': '22', 'validity': 'Valid 2 Hours'},
        {'name': '50 Minutes', 'price': '51', 'validity': 'Valid till Midnight'},
        {'name': '100 Minutes', 'price': '118', 'validity': 'Valid till Midnight'},
        {'name': '200 Minutes', 'price': '265', 'validity': 'Valid 7 Days'},
        {'name': '400 Minutes', 'price': '500', 'validity': 'Valid 30 Days'},
        {'name': '300mins', 'price': '502', 'validity': '30days'},
        {'name': '800mins', 'price': '1010', 'validity': '30days'},
    ],
    'sms': [
        {'name': '20 SMS', 'price': '5', 'validity': 'Valid 24 Hours'},
        {'name': '200 SMS', 'price': '10', 'validity': 'Valid 24 Hours'},
        {'name': '1000 SMS', 'price': '30', 'validity': 'Valid 7 Days'},
    ]
}

def trigger_mpesa_stk_push(phone_number, amount):
    print(f"[STK PUSH SENT] Requesting KES {amount} from {phone_number}...")
    return True

def dispatch_bundle_via_api(phone_number, bundle_name):
    print(f"[API DISPATCH] Sending {bundle_name} to {phone_number}...")
    return True

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Safestay Deals</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f5;
            margin: 0; padding: 0; color: #333; padding-bottom: 85px;
        }
        .header-bg {
            background-color: #0b5d2b; color: white; padding: 22px 20px 30px 20px;
            border-bottom-left-radius: 25px; border-bottom-right-radius: 25px;
        }
        .back-btn {
            background: white; border: none; border-radius: 50%; width: 35px; height: 35px;
            font-size: 18px; cursor: pointer; display: flex; align-items: center; justify-content: center;
            color: #0b5d2b; text-decoration: none; margin-bottom: 15px;
        }
        .title { font-size: 24px; font-weight: bold; margin: 0; }
        .subtitle { font-size: 14px; font-style: italic; opacity: 0.9; margin-top: 4px; }
        .container { padding: 15px; }
        .notice-box {
            background-color: #eaf3ed; border: 1px solid #d0e4d6; color: #1b4d2e;
            padding: 12px 15px; border-radius: 12px; font-size: 13px; font-style: italic; margin-bottom: 15px;
        }
        .section-box {
            background: white; border-radius: 18px; padding: 15px; margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }
        .section-title {
            font-size: 15px; font-style: italic; font-weight: bold; color: #333; margin-bottom: 12px;
        }
        .tabs { display: flex; background: white; border-radius: 30px; padding: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 15px; }
        .tab { flex: 1; text-align: center; padding: 10px; border-radius: 25px; cursor: pointer; font-weight: 600; color: #555; text-decoration: none; font-size: 15px; }
        .tab.active { background-color: #0b5d2b; color: white; }
        .card {
            background: white; border-radius: 15px; padding: 15px; margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03); display: flex; justify-content: space-between; align-items: center;
            text-decoration: none; color: inherit;
        }
        .bundle-info h3 { margin: 0 0 5px 0; font-size: 16px; font-weight: bold; }
        .bundle-info p { margin: 0; font-size: 13px; color: #666; font-style: italic; }
        .buy-btn {
            background-color: white; color: #0b5d2b; border: 1.5px solid #0b5d2b;
            padding: 8px 20px; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 14px; text-decoration: none;
        }
        .buy-btn:hover { background-color: #0b5d2b; color: white; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 14px; }
        .form-control { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 10px; font-size: 16px; box-sizing: border-box; }
        .btn-submit { background-color: #0b5d2b; color: white; border: none; width: 100%; padding: 14px; border-radius: 10px; font-size: 16px; font-weight: bold; cursor: pointer; }
        
        .nav-bar { 
            position: fixed; bottom: 0; left: 0; right: 0; background: white; 
            display: flex; justify-content: space-around; padding: 10px 0; 
            box-shadow: 0 -2px 10px rgba(0,0,0,0.06); z-index: 9999; 
        }
        .nav-item { text-align: center; text-decoration: none; color: #777; font-size: 11px; font-style: italic; }
        .nav-item.active { color: #0b5d2b; font-weight: bold; }
        .nav-item div { font-size: 18px; margin-bottom: 2px; }
    </style>
</head>
<body>
    {% block content %}{% endblock %}

    <div class="nav-bar">
        <a href="{{ url_for('other_services', tab='data') }}" class="nav-item"><div>⇄</div>Airtime to Cash</a>
        <a href="{{ url_for('home') }}" class="nav-item active"><div>🏠</div>Home</a>
        <a href="{{ url_for('other_services', tab='data') }}" class="nav-item"><div>⏹️</div>Other Services</a>
        <a href="{{ url_for('admin_panel') }}" class="nav-item"><div>🎧</div>Support</a>
    </div>
</body>
</html>
"""

HOME_TEMPLATE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="header-bg">
        <div style="font-size: 12px; letter-spacing: 1.5px; opacity: 0.9;">SAFESTAY DEALS</div>
        <div class="title" style="font-size: 26px; font-style: italic; margin-top: 4px;">Good Afternoon</div>
        <div class="subtitle">Welcome back</div>
    </div>
    
    <div class="container" style="margin-top: -10px;">
        <div class="section-box">
            <div class="section-title">Airtime to Cash</div>
            <div style="display: flex; gap: 12px;">
                <a href="{{ url_for('other_services', tab='data') }}" style="flex: 1; background: #ffffff; border: 1.5px solid #f0f2f1; padding: 15px 10px; border-radius: 14px; text-align: center; text-decoration: none; color: inherit; display: block;">
                    <div style="width: 42px; height: 42px; background: #28a745; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; font-weight: bold; font-size: 18px;">S</div>
                    <strong style="font-size: 14px; font-style: italic; display: block;">Safaricom</strong>
                    <div style="background: #f4f6f5; border-radius: 20px; padding: 5px; font-size: 11px; margin-top: 8px; color: #555; font-style: italic;">80% cash back</div>
                </a>
                <a href="{{ url_for('other_services', tab='data') }}" style="flex: 1; background: #ffffff; border: 1.5px solid #f0f2f1; padding: 15px 10px; border-radius: 14px; text-align: center; text-decoration: none; color: inherit; display: block;">
                    <div style="width: 42px; height: 42px; background: #dc3545; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; font-weight: bold; font-size: 18px;">A</div>
                    <strong style="font-size: 14px; font-style: italic; display: block;">Airtel</strong>
                    <div style="background: #f4f6f5; border-radius: 20px; padding: 5px; font-size: 11px; margin-top: 8px; color: #555; font-style: italic;">50% cash back</div>
                </a>
            </div>
        </div>

        <div class="section-box">
            <div class="section-title">Bonga Points to Cash</div>
            <a href="{{ url_for('other_services', tab='data') }}" style="display: flex; align-items: center; justify-content: space-between; background: #ffffff; border: 1.5px solid #f0f2f1; padding: 12px 15px; border-radius: 14px; text-decoration: none; color: inherit;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; background: #0b5d2b; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 18px;">🎁</div>
                    <div>
                        <strong style="font-size: 14px; font-style: italic; display: block;">Safaricom Bonga Points</strong>
                        <span style="font-size: 12px; color: #666; font-style: italic;">Convert points to M-Pesa</span>
                    </div>
                </div>
                <span style="color: #aaa; font-size: 18px; font-weight: bold;">›</span>
            </a>
        </div>

        <div class="section-box">
            <div class="section-title">Other Services</div>
            <div style="display: flex; gap: 10px;">
                <a href="{{ url_for('other_services', tab='data') }}" style="flex: 1; background: #ffffff; border: 1.5px solid #f0f2f1; padding: 15px 5px; border-radius: 14px; text-align: center; text-decoration: none; color: inherit; display: block;">
                    <div style="font-size: 22px; margin-bottom: 6px;">📶</div>
                    <span style="font-size: 13px; font-style: italic; font-weight: bold; display: block;">Data</span>
                </a>
                <a href="{{ url_for('other_services', tab='minutes') }}" style="flex: 1; background: #ffffff; border: 1.5px solid #f0f2f1; padding: 15px 5px; border-radius: 14px; text-align: center; text-decoration: none; color: inherit; display: block;">
                    <div style="font-size: 22px; margin-bottom: 6px;">📊</div>
                    <span style="font-size: 13px; font-style: italic; font-weight: bold; display: block;">Minutes</span>
                </a>
                <a href="{{ url_for('other_services', tab='sms') }}" style="flex: 1; background: #ffffff; border: 1.5px solid #f0f2f1; padding: 15px 5px; border-radius: 14px; text-align: center; text-decoration: none; color: inherit; display: block;">
                    <div style="font-size: 22px; margin-bottom: 6px;">💬</div>
                    <span style="font-size: 13px; font-style: italic; font-weight: bold; display: block;">SMS</span>
                </a>
            </div>
        </div>
    </div>
""")

SERVICES_TEMPLATE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="header-bg">
        <a href="{{ url_for('home') }}" class="back-btn">←</a>
        <div class="title">Other Services</div>
        <div class="subtitle">Buy Data, Minutes or SMS bundles</div>
    </div>
    <div class="container">
        <div class="notice-box">You can only purchase one offer per day, per type.</div>
        
        <div class="tabs">
            <a href="{{ url_for('other_services', tab='data') }}" class="tab {% if active_tab == 'data' %}active{% endif %}">Data</a>
            <a href="{{ url_for('other_services', tab='minutes') }}" class="tab {% if active_tab == 'minutes' %}active{% endif %}">Minutes</a>
            <a href="{{ url_for('other_services', tab='sms') }}" class="tab {% if active_tab == 'sms' %}active{% endif %}">SMS</a>
        </div>

        <div>
            {% for item in bundles[active_tab] %}
            <a href="{{ url_for('checkout', name=item.name, price=item.price) }}" class="card">
                <div class="bundle-info">
                    <h3>{{ item.name }}</h3>
                    <p>KES {{ item.price }} &bull; {{ item.validity }}</p>
                </div>
                <span class="buy-btn">Buy</span>
            </a>
            {% endfor %}
        </div>
    </div>
""")

CHECKOUT_TEMPLATE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="header-bg">
        <a href="{{ url_for('other_services') }}" class="back-btn">←</a>
        <div class="title">Complete Purchase</div>
        <div class="subtitle">Secure automated delivery via Method A</div>
    </div>
    <div class="container">
        <div class="section-box">
            <h3 style="margin-top:0; color:#0b5d2b;">{{ bundle_name }}</h3>
            <p style="font-size: 18px; font-weight: bold; margin-bottom: 20px;">Price: KES {{ price }}</p>
            
            <form action="{{ url_for('process_purchase') }}" method="POST">
                <input type="hidden" name="bundle_name" value="{{ bundle_name }}">
                <input type="hidden" name="price" value="{{ price }}">
                
                <div class="form-group">
                    <label>Recipient Phone Number (To receive bundle)</label>
                    <input type="text" name="phone" class="form-control" placeholder="e.g. 0712345678" required>
                </div>
                
                <div style="background: #eaf3ed; padding: 10px; border-radius: 8px; font-size: 12px; color: #1b4d2e; margin-bottom: 20px;">
                    ℹ️ Clicking Pay triggers an M-Pesa prompt on your phone. Funds go to your account, and the bundle is dispatched instantly.
                </div>

                <button type="submit" class="btn-submit">Pay KES {{ price }} & Get Bundle</button>
            </form>
        </div>
    </div>
""")

SUCCESS_TEMPLATE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="header-bg" style="background-color: #28a745;">
        <div class="title">Order Successful!</div>
        <div class="subtitle">Payment received and bundle dispatched</div>
    </div>
    <div class="container">
        <div class="section-box" style="text-align: center; padding: 25px;">
            <div style="font-size: 50px; margin-bottom: 10px;">✅</div>
            <h3>Bundle Sent Successfully</h3>
            <p><strong>{{ bundle }}</strong> was dispatched to <strong>{{ phone }}</strong>.</p>
            <p style="color: #666; font-size: 13px;">Payment of KES {{ price }} successfully routed to your wallet.</p>
            <br>
            <a href="{{ url_for('home') }}" class="buy-btn" style="display: inline-block; padding: 10px 30px;">Back to Home</a>
        </div>
    </div>
""")

ADMIN_TEMPLATE = HTML_TEMPLATE.replace('{% block content %}{% endblock %}', """
    <div class="header-bg">
        <a href="{{ url_for('home') }}" class="back-btn">←</a>
        <div class="title">Support & Admin Panel</div>
        <div class="subtitle">Live Tracking of Paid Orders & Revenue</div>
    </div>
    <div class="container">
        <div class="section-box">
            <h3>Total Orders: {{ orders|length }}</h3>
            <hr style="border:0; border-top:1px solid #eee; margin: 15px 0;">
            {% if orders %}
                {% for o in orders %}
                <div style="background: #f9f9f9; padding: 10px; border-radius: 8px; margin-bottom: 10px; font-size: 13px;">
                    <strong>{{ o.bundle }}</strong> - KES {{ o.price }}<br>
                    <span style="color: #555;">Phone: {{ o.phone }}</span><br>
                    <small style="color: #888;">{{ o.time }}</small>
                </div>
                {% endfor %}
            {% else %}
                <p style="color: #777; font-style: italic;">No orders placed yet. Test your app by buying a bundle!</p>
            {% endif %}
        </div>
    </div>
""")

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/services')
def other_services():
    active_tab = request.args.get('tab', 'data')
    return render_template_string(SERVICES_TEMPLATE, active_tab=active_tab, bundles=bundles_data)

@app.route('/checkout')
def checkout():
    bundle_name = request.args.get('name')
    price = request.args.get('price')
    return render_template_string(CHECKOUT_TEMPLATE, bundle_name=bundle_name, price=price)

@app.route('/process_purchase', methods=['POST'])
def process_purchase():
    bundle_name = request.form.get('bundle_name')
    price = request.form.get('price')
    phone = request.form.get('phone')
    
    trigger_mpesa_stk_push(phone, price)
    dispatch_bundle_via_api(phone, bundle_name)
    
    order_record = {
        'bundle': bundle_name,
        'price': price,
        'phone': phone,
        'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    orders_db.insert(0, order_record)
    
    return render_template_string(SUCCESS_TEMPLATE, bundle=bundle_name, price=price, phone=phone)

@app.route('/admin')
def admin_panel():
    return render_template_string(ADMIN_TEMPLATE, orders=orders_db)

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
