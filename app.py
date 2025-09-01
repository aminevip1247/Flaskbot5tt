from flask import Flask, request, jsonify, render_template_string
import threading

# إنشاء تطبيق Flask
app = Flask(__name__)

# قالب HTML لعرض واجهة الفلترة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Filter Cards by Country</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .country-list {
            max-height: 300px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .country-item {
            margin: 8px 0;
            padding: 8px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #45a049;
        }
        .count {
            font-weight: bold;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Filter Cards by Country</h1>
        <p>Found <span class="count">{{ countries|length }}</span> unique countries in your cards.</p>
        
        <div class="country-list">
            <h3>Select countries to filter:</h3>
            <form method="POST">
                {% for country in countries %}
                <div class="country-item">
                    <input type="checkbox" id="{{ country.code }}" name="countries" value="{{ country.code }}">
                    <label for="{{ country.code }}">{{ country.name }} ({{ country.code }}) - {{ country.count }} cards</label>
                </div>
                {% endfor %}
                <br>
                <button type="submit">DONE</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

# بيانات مؤقتة (في تطبيق حقيقي، استخدم قاعدة بيانات)
user_sessions = {}

@app.route('/filter/<user_id>', methods=['GET', 'POST'])
def filter_cards(user_id):
    if user_id not in user_sessions:
        return "Session expired or invalid request. Please upload your file again in Telegram."
    
    session_data = user_sessions[user_id]
    
    if request.method == 'POST':
        selected_countries = request.form.getlist('countries')
        if not selected_countries:
            return "No countries selected. Please go back and select at least one country."
        
        # تصفية البطاقات حسب الدول المختارة
        filtered_cards = []
        for card in session_data['cards']:
            bin_code = card.split('|')[0][:6]
            country = session_data['bin_data'].get(bin_code, {}).get('country', 'Unknown')
            if country in selected_countries:
                filtered_cards.append(card)
        
        # إرسال النتائج إلى المستخدم عبر البوت
        if filtered_cards:
            result = "\n".join(filtered_cards[:50])  # إرسال أول 50 بطاقة فقط لتجنب حدود الرسائل
            message = f"✅ Found {len(filtered_cards)} cards for selected countries:\n\n{result}"
            if len(filtered_cards) > 50:
                message += f"\n\n... and {len(filtered_cards) - 50} more cards."
            
            # هنا تحتاج إلى طريقة لإرسال الرسالة إلى البوت
            # في تطبيق حقيقي، قد تستخدم طابور رسائل أو تخزين مؤقت
            session_data['filtered_result'] = message
        else:
            session_data['filtered_result'] = "❌ No cards found for the selected countries."
        
        # إعلام البوت بأن التصفية اكتملت
        session_data['filter_complete'] = True
        
        return "Filtering completed! You can return to Telegram to see the results."
    
    # تجميع قائمة الدول مع عدد البطاقات لكل دولة
    country_stats = {}
    for card in session_data['cards']:
        bin_code = card.split('|')[0][:6]
        country = session_data['bin_data'].get(bin_code, {}).get('country', 'Unknown')
        country_name = session_data['bin_data'].get(bin_code, {}).get('country_name', 'Unknown')
        
        if country not in country_stats:
            country_stats[country] = {
                'code': country,
                'name': country_name,
                'count': 0
            }
        country_stats[country]['count'] += 1
    
    return render_template_string(HTML_TEMPLATE, countries=country_stats.values())

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
    
    # هنا يمكنك تشغيل بوت التيليجرام أيضاً إذا أردت
    # bot.infinity_polling()
