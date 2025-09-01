from flask import Flask, request, jsonify, render_template_string
import threading

# إنشاء تطبيق Flask
app = Flask(__name__)

# قالب HTML بتصميم iOS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Filter • iOS Style</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --ios-blue: #007AFF;
            --ios-gray-1: #8E8E93;
            --ios-gray-2: #C7C7CC;
            --ios-gray-3: #E5E5EA;
            --ios-gray-4: #F2F2F7;
            --ios-green: #34C759;
            --ios-red: #FF3B30;
            --ios-background: #F2F2F7;
            --ios-card-bg: #FFFFFF;
            --ios-text-primary: #000000;
            --ios-text-secondary: #8E8E93;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --ios-background: #000000;
                --ios-card-bg: #1C1C1E;
                --ios-text-primary: #FFFFFF;
                --ios-text-secondary: #8E8E93;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--ios-background);
            color: var(--ios-text-primary);
            line-height: 1.4;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }

        .ios-container {
            max-width: 600px;
            margin: 0 auto;
            padding: 16px;
        }

        .ios-header {
            background: var(--ios-card-bg);
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 16px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .ios-header h1 {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .ios-header p {
            color: var(--ios-text-secondary);
            font-size: 15px;
        }

        .ios-card {
            background: var(--ios-card-bg);
            border-radius: 12px;
            margin-bottom: 16px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .ios-card-header {
            padding: 16px;
            border-bottom: 1px solid var(--ios-gray-3);
            font-weight: 600;
            font-size: 17px;
        }

        .ios-list {
            list-style: none;
        }

        .ios-list-item {
            display: flex;
            align-items: center;
            padding: 14px 16px;
            border-bottom: 1px solid var(--ios-gray-3);
            position: relative;
        }

        .ios-list-item:last-child {
            border-bottom: none;
        }

        .ios-checkbox {
            position: absolute;
            opacity: 0;
        }

        .ios-checkbox-label {
            display: flex;
            align-items: center;
            width: 100%;
            cursor: pointer;
        }

        .ios-checkbox-custom {
            width: 24px;
            height: 24px;
            border: 2px solid var(--ios-gray-2);
            border-radius: 6px;
            margin-right: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }

        .ios-checkbox:checked + .ios-checkbox-label .ios-checkbox-custom {
            background-color: var(--ios-blue);
            border-color: var(--ios-blue);
        }

        .ios-checkbox:checked + .ios-checkbox-label .ios-checkbox-custom::after {
            content: '✓';
            color: white;
            font-size: 14px;
            font-weight: bold;
        }

        .country-info {
            flex: 1;
        }

        .country-name {
            font-size: 17px;
            font-weight: 500;
            margin-bottom: 2px;
        }

        .country-details {
            font-size: 14px;
            color: var(--ios-text-secondary);
        }

        .country-badge {
            background: var(--ios-gray-4);
            color: var(--ios-text-secondary);
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 13px;
            font-weight: 500;
        }

        .bank-type-info {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 6px;
        }

        .bank-badge {
            background: rgba(0, 122, 255, 0.1);
            color: var(--ios-blue);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
        }

        .type-badge {
            background: rgba(52, 199, 89, 0.1);
            color: var(--ios-green);
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 12px;
        }

        .ios-button {
            background: var(--ios-blue);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 16px;
            font-size: 17px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            margin-top: 16px;
            transition: background 0.2s;
        }

        .ios-button:hover {
            background: #0062CC;
        }

        .ios-button:active {
            background: #0052B3;
        }

        .ios-footer {
            text-align: center;
            color: var(--ios-text-secondary);
            font-size: 13px;
            margin-top: 20px;
            padding: 16px;
        }

        .select-all-container {
            padding: 12px 16px;
            border-bottom: 1px solid var(--ios-gray-3);
        }

        .search-container {
            padding: 12px 16px;
            border-bottom: 1px solid var(--ios-gray-3);
        }

        .ios-search {
            width: 100%;
            padding: 10px 16px;
            background: var(--ios-gray-4);
            border: none;
            border-radius: 10px;
            font-size: 16px;
        }

        .ios-search:focus {
            outline: none;
            background: var(--ios-gray-3);
        }

        .stats-container {
            display: flex;
            justify-content: space-between;
            padding: 12px 16px;
            background: var(--ios-gray-4);
            border-radius: 8px;
            margin: 12px 0;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 18px;
            font-weight: 600;
            color: var(--ios-blue);
        }

        .stat-label {
            font-size: 13px;
            color: var(--ios-text-secondary);
        }
    </style>
</head>
<body>
    <div class="ios-container">
        <div class="ios-header">
            <h1><i class="fas fa-credit-card"></i> Card Filter</h1>
            <p>Select countries to filter your cards</p>
        </div>

        <div class="ios-card">
            <div class="stats-container">
                <div class="stat-item">
                    <div class="stat-number">{{ total_cards }}</div>
                    <div class="stat-label">Total Cards</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ countries|length }}</div>
                    <div class="stat-label">Countries</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{{ total_bins }}</div>
                    <div class="stat-label">BINs</div>
                </div>
            </div>

            <div class="search-container">
                <input type="text" class="ios-search" id="searchInput" placeholder="Search countries..." onkeyup="filterCountries()">
            </div>

            <div class="select-all-container">
                <input type="checkbox" id="selectAll" class="ios-checkbox" onchange="toggleSelectAll()">
                <label for="selectAll" class="ios-checkbox-label">
                    <span class="ios-checkbox-custom"></span>
                    <span class="country-name">Select All Countries</span>
                </label>
            </div>

            <form method="POST" id="filterForm">
                <ul class="ios-list">
                    {% for country in countries %}
                    <li class="ios-list-item country-item">
                        <input type="checkbox" id="country-{{ country.code }}" name="countries" value="{{ country.code }}" class="ios-checkbox country-checkbox">
                        <label for="country-{{ country.code }}" class="ios-checkbox-label">
                            <span class="ios-checkbox-custom"></span>
                            <div class="country-info">
                                <div class="country-name">{{ country.name }} ({{ country.code }})</div>
                                <div class="country-details">
                                    <span class="country-badge">{{ country.count }} cards</span>
                                    <div class="bank-type-info">
                                        {% for bank in country.banks[:3] %}
                                        <span class="bank-badge">{{ bank }}</span>
                                        {% endfor %}
                                        {% if country.banks|length > 3 %}
                                        <span class="bank-badge">+{{ country.banks|length - 3 }} more</span>
                                        {% endif %}
                                        {% if country.types %}
                                        <span class="type-badge">{{ country.types|join(', ') }}</span>
                                        {% endif %}
                                    </div>
                                </div>
                            </div>
                        </label>
                    </li>
                    {% endfor %}
                </ul>
            </form>
        </div>

        <button type="submit" form="filterForm" class="ios-button">
            <i class="fas fa-check"></i> DONE
        </button>

        <div class="ios-footer">
            <p>Processed with <i class="fas fa-heart" style="color:var(--ios-red)"></i> using iOS design</p>
        </div>
    </div>

    <script>
        function filterCountries() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const countryItems = document.querySelectorAll('.country-item');
            
            countryItems.forEach(item => {
                const countryName = item.querySelector('.country-name').textContent.toLowerCase();
                if (countryName.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function toggleSelectAll() {
            const selectAll = document.getElementById('selectAll').checked;
            const countryCheckboxes = document.querySelectorAll('.country-checkbox');
            
            countryCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAll;
            });
        }

        // Update select all checkbox when individual checkboxes change
        document.querySelectorAll('.country-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const allChecked = Array.from(document.querySelectorAll('.country-checkbox'))
                    .every(cb => cb.checked);
                document.getElementById('selectAll').checked = allChecked;
            });
        });

        // Add iOS-like smooth scrolling
        document.addEventListener('DOMContentLoaded', function() {
            document.body.style.opacity = 1;
            document.body.style.transition = 'opacity 0.3s ease-in-out';
        });
    </script>
</body>
</html>
"""

# بيانات مؤقتة
user_sessions = {}

@app.route('/filter/<user_id>', methods=['GET', 'POST'])
def filter_cards(user_id):
    if user_id not in user_sessions:
        return render_template_string('''
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                        text-align: center; padding: 50px; color: #8E8E93;">
                <h1 style="color: #FF3B30;"><i class="fas fa-exclamation-triangle"></i></h1>
                <h2>Session Expired</h2>
                <p>Please upload your file again in Telegram.</p>
            </div>
        ''')
    
    session_data = user_sessions[user_id]
    
    if request.method == 'POST':
        selected_countries = request.form.getlist('countries')
        if not selected_countries:
            return render_template_string('''
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                            text-align: center; padding: 50px; color: #8E8E93;">
                    <h1 style="color: #FF3B30;"><i class="fas fa-exclamation-circle"></i></h1>
                    <h2>No Countries Selected</h2>
                    <p>Please go back and select at least one country.</p>
                    <button onclick="window.history.back()" style="background: #007AFF; color: white; border: none; 
                            padding: 12px 24px; border-radius: 12px; margin-top: 20px; cursor: pointer;">
                        Go Back
                    </button>
                </div>
            ''')
        
        # تصفية البطاقات حسب الدول المختارة
        filtered_cards = []
        for card in session_data['cards']:
            bin_code = card.split('|')[0][:6]
            country = session_data['bin_data'].get(bin_code, {}).get('country', 'Unknown')
            if country in selected_countries:
                # إضافة معلومات البنك والنوع إلى البطاقة
                bank = session_data['bin_data'].get(bin_code, {}).get('bank', 'Unknown Bank')
                card_type = session_data['bin_data'].get(bin_code, {}).get('type', 'Unknown Type')
                filtered_cards.append(f"{card} | {bank} | {card_type}")
        
        # إرسال النتائج إلى المستخدم عبر البوت
        if filtered_cards:
            result = "\n".join(filtered_cards)
            session_data['filtered_result'] = f"✅ Found {len(filtered_cards)} cards for selected countries:\n\n{result}"
        else:
            session_data['filtered_result'] = "❌ No cards found for the selected countries."
        
        # إعلام البوت بأن التصفية اكتملت
        session_data['filter_complete'] = True
        
        return render_template_string('''
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                        text-align: center; padding: 50px;">
                <h1 style="color: #34C759;"><i class="fas fa-check-circle"></i></h1>
                <h2>Filtering Completed!</h2>
                <p style="color: #8E8E93;">You can return to Telegram to see the results.</p>
                <div style="margin-top: 30px; padding: 16px; background: #F2F2F7; border-radius: 12px;">
                    <p style="font-size: 15px; color: #8E8E93;">Found <strong>{{ filtered_count }}</strong> cards in <strong>{{ country_count }}</strong> selected countries</p>
                </div>
            </div>
        ''', filtered_count=len(filtered_cards), country_count=len(selected_countries))
    
    # تجميع قائمة الدول مع إحصائيات
    country_stats = {}
    for card in session_data['cards']:
        bin_code = card.split('|')[0][:6]
        bin_info = session_data['bin_data'].get(bin_code, {})
        country = bin_info.get('country', 'Unknown')
        country_name = bin_info.get('country_name', 'Unknown Country')
        bank = bin_info.get('bank', 'Unknown Bank')
        card_type = bin_info.get('type', 'Unknown Type')
        
        if country not in country_stats:
            country_stats[country] = {
                'code': country,
                'name': country_name,
                'count': 0,
                'banks': set(),
                'types': set()
            }
        
        country_stats[country]['count'] += 1
        country_stats[country]['banks'].add(bank)
        country_stats[country]['types'].add(card_type)
    
    # تحويل المجموعات إلى قوائم
    for country in country_stats.values():
        country['banks'] = list(country['banks'])
        country['types'] = list(country['types'])
    
    # إحصائيات إضافية
    total_cards = len(session_data['cards'])
    total_bins = len(session_data['bin_data'])
    
    return render_template_string(HTML_TEMPLATE, 
                                countries=sorted(country_stats.values(), key=lambda x: x['count'], reverse=True),
                                total_cards=total_cards,
                                total_bins=total_bins)

@app.route('/api/set_session/<user_id>', methods=['POST'])
def set_session_data(user_id):
    """واجهة برمجية لوضع بيانات الجلسة من البوت"""
    data = request.json
    user_sessions[user_id] = data
    return jsonify({"status": "success", "message": "Session data stored"})

@app.route('/api/get_result/<user_id>', methods=['GET'])
def get_filter_result(user_id):
    """واجهة برمجية للحصول على نتيجة التصفية"""
    if user_id not in user_sessions:
        return jsonify({"status": "error", "message": "Session not found"})
    
    session_data = user_sessions[user_id]
    
    if 'filtered_result' in session_data:
        result = session_data['filtered_result']
        # حذف الجلسة بعد استرجاع النتيجة
        del user_sessions[user_id]
        return jsonify({"status": "success", "result": result})
    else:
        return jsonify({"status": "pending", "message": "Filter not complete yet"})

def run_web_server():
    """تشغيل خادم الويب"""
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    # تشغيل الخادم في خيط منفصل
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    print("Web server started on http://0.0.0.0:5000")
