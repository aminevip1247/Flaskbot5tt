from flask import Flask, request, jsonify, render_template_string, Response
import threading
import json
from datetime import datetime, date

# إنشاء تطبيق Flask
app = Flask(__name__)

# إضافة encoder مخصص للتعامل مع الكائنات غير القابلة للتسلسل
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, set):
            return list(obj)
        else:
            return str(obj)

app.json_encoder = CustomJSONEncoder

# دالة مساعدة لتحويل الكائنات إلى JSON بشكل آمن
def safe_jsonify(data):
    return app.response_class(
        json.dumps(data, cls=CustomJSONEncoder, indent=2),
        mimetype='application/json'
    )

# قالب HTML بتصميم iOS متقدم مع أقسام متعددة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Card Filter • iOS Style</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --ios-blue: #007AFF;
            --ios-green: #34C759;
            --ios-red: #FF3B30;
            --ios-orange: #FF9500;
            --ios-purple: #AF52DE;
            --ios-gray-1: #8E8E93;
            --ios-gray-2: #C7C7CC;
            --ios-gray-3: #E5E5EA;
            --ios-gray-4: #F2F2F7;
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
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .ios-header h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 6px;
            background: linear-gradient(135deg, var(--ios-blue), var(--ios-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .ios-header p {
            color: var(--ios-text-secondary);
            font-size: 16px;
            font-weight: 500;
        }

        .filter-section {
            background: var(--ios-card-bg);
            border-radius: 16px;
            margin-bottom: 20px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .section-header {
            padding: 18px;
            border-bottom: 1px solid var(--ios-gray-3);
            font-weight: 700;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--ios-gray-4);
        }

        .section-header i {
            color: var(--ios-blue);
            font-size: 20px;
        }

        .section-content {
            padding: 16px;
            max-height: 300px;
            overflow-y: auto;
        }

        .countries-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
        }

        .country-item {
            background: var(--ios-gray-4);
            padding: 12px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .country-item.selected {
            background: rgba(0, 122, 255, 0.1);
            border-color: var(--ios-blue);
            transform: scale(1.05);
        }

        .country-item:hover {
            background: var(--ios-gray-3);
        }

        .country-name {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .country-count {
            font-size: 12px;
            color: var(--ios-text-secondary);
            background: var(--ios-card-bg);
            padding: 2px 8px;
            border-radius: 10px;
            display: inline-block;
        }

        .search-container {
            padding: 16px;
            border-bottom: 1px solid var(--ios-gray-3);
        }

        .ios-search {
            width: 100%;
            padding: 14px 18px;
            background: var(--ios-gray-4);
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 500;
        }

        .ios-search:focus {
            outline: none;
            background: var(--ios-gray-3);
        }

        .ios-list {
            list-style: none;
        }

        .ios-list-item {
            display: flex;
            align-items: center;
            padding: 14px;
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
            transition: all 0.3s ease;
        }

        .ios-checkbox:checked + .ios-checkbox-label .ios-checkbox-custom {
            background-color: var(--ios-blue);
            border-color: var(--ios-blue);
            transform: scale(1.1);
        }

        .ios-checkbox:checked + .ios-checkbox-label .ios-checkbox-custom::after {
            content: '✓';
            color: white;
            font-size: 14px;
            font-weight: bold;
        }

        .filter-info {
            flex: 1;
        }

        .filter-name {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 2px;
        }

        .filter-details {
            font-size: 14px;
            color: var(--ios-text-secondary);
        }

        .filter-badge {
            background: var(--ios-gray-4);
            color: var(--ios-text-secondary);
            padding: 4px 8px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
        }

        .select-all-container {
            padding: 14px;
            border-bottom: 1px solid var(--ios-gray-3);
            background: var(--ios-gray-4);
        }

        .show-more {
            text-align: center;
            padding: 12px;
            color: var(--ios-blue);
            font-weight: 600;
            cursor: pointer;
            background: var(--ios-gray-4);
        }

        .show-more:hover {
            background: var(--ios-gray-3);
        }

        .hidden {
            display: none;
        }

        .ios-button {
            background: var(--ios-blue);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 18px;
            font-size: 18px;
            font-weight: 700;
            width: 100%;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
        }

        .ios-button:hover {
            background: #0062CC;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0, 122, 255, 0.4);
        }

        .ios-button:active {
            background: #0052B3;
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3);
        }

        .ios-button:disabled {
            background: var(--ios-gray-2);
            cursor: not-allowed;
            box-shadow: none;
        }

        .success-animation {
            text-align: center;
            padding: 40px 20px;
        }

        .checkmark {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: block;
            stroke-width: 5;
            stroke: #34C759;
            stroke-miterlimit: 10;
            box-shadow: 0 0 20px rgba(52, 199, 89, 0.3);
            animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
            margin: 0 auto 20px;
        }

        .checkmark-circle {
            stroke-dasharray: 166;
            stroke-dashoffset: 166;
            stroke-width: 5;
            stroke-miterlimit: 10;
            stroke: #34C759;
            fill: none;
            animation: stroke .6s cubic-bezier(0.650, 0.000, 0.450, 1.000) forwards;
        }

        .checkmark-check {
            transform-origin: 50% 50%;
            stroke-dasharray: 48;
            stroke-dashoffset: 48;
            animation: stroke .3s cubic-bezier(0.650, 0.000, 0.450, 1.000) .8s forwards;
        }

        .success-message {
            font-size: 24px;
            font-weight: 700;
            color: var(--ios-green);
            margin-bottom: 10px;
        }

        .success-details {
            font-size: 16px;
            color: var(--ios-text-secondary);
            font-weight: 500;
        }

        .selection-info {
            background: var(--ios-gray-4);
            padding: 12px 16px;
            border-radius: 12px;
            margin: 12px 0;
            font-size: 14px;
            color: var(--ios-text-secondary);
        }

        .selection-info strong {
            color: var(--ios-blue);
        }

        @keyframes stroke {
            100% { stroke-dashoffset: 0; }
        }

        @keyframes scale {
            0%, 100% { transform: none; }
            50% { transform: scale3d(1.1, 1.1, 1); }
        }

        @keyframes fill {
            100% { box-shadow: 0 0 30px rgba(52, 199, 89, 0.2); }
        }
    </style>
</head>
<body>
    <div class="ios-container">
        <div class="ios-header">
            <h1><i class="fas fa-filter"></i> Advanced Card Filter</h1>
            <p>Select countries, banks, and card types to filter</p>
        </div>

        <form method="POST" id="filterForm">
            <!-- Countries Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span><i class="fas fa-globe"></i> Countries</span>
                    <span class="filter-badge">{{ countries|length }} countries</span>
                </div>
                
                <div class="search-container">
                    <input type="text" class="ios-search" id="countrySearch" placeholder="Search countries..." onkeyup="filterItems('country')">
                </div>
                
                <div class="section-content">
                    <div class="countries-grid" id="countriesGrid">
                        {% for country in countries[:20] %}
                        <div class="country-item" data-country="{{ country.code }}" onclick="toggleCountry('{{ country.code }}')">
                            <div class="country-name">{{ country.name }}</div>
                            <div class="country-count">{{ country.count }} cards</div>
                        </div>
                        {% endfor %}
                    </div>
                    
                    {% if countries|length > 20 %}
                    <div id="moreCountries" class="hidden">
                        {% for country in countries[20:] %}
                        <div class="country-item" data-country="{{ country.code }}" onclick="toggleCountry('{{ country.code }}')">
                            <div class="country-name">{{ country.name }}</div>
                            <div class="country-count">{{ country.count }} cards</div>
                        </div>
                        {% endfor %}
                    </div>
                    
                    <div class="show-more" onclick="showMore('moreCountries', this)">
                        Show All {{ countries|length }} Countries
                    </div>
                    {% endif %}
                </div>
                
                <input type="hidden" name="selected_countries" id="selectedCountries" value="">
            </div>

            <!-- Banks Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span><i class="fas fa-university"></i> Banks</span>
                    <span class="filter-badge">{{ banks|length }} banks</span>
                </div>
                
                <div class="selection-info" id="bankSelectionInfo">
                    {% if countries|length > 0 %}
                    Please select countries first to see available banks
                    {% else %}
                    No countries available
                    {% endif %}
                </div>
                
                <div class="search-container">
                    <input type="text" class="ios-search" id="bankSearch" placeholder="Search banks..." onkeyup="filterItems('bank')" disabled>
                </div>
                
                <div class="select-all-container">
                    <input type="checkbox" id="selectAllBanks" class="ios-checkbox" onchange="toggleSelectAll('bank')" disabled>
                    <label for="selectAllBanks" class="ios-checkbox-label">
                        <span class="ios-checkbox-custom"></span>
                        <span class="filter-name">Select All Banks</span>
                    </label>
                </div>
                
                <div class="section-content" id="banksContent">
                    <ul class="ios-list">
                        {% for bank in banks %}
                        <li class="ios-list-item filter-item bank-item hidden" data-bank="{{ bank.name }}">
                            <input type="checkbox" id="bank-{{ bank.id }}" name="banks" value="{{ bank.name }}" class="ios-checkbox bank-checkbox" disabled>
                            <label for="bank-{{ bank.id }}" class="ios-checkbox-label">
                                <span class="ios-checkbox-custom"></span>
                                <div class="filter-info">
                                    <div class="filter-name">{{ bank.name }}</div>
                                    <div class="filter-details">
                                        <span class="filter-badge">{{ bank.count }} cards</span>
                                        <span class="filter-badge">{{ bank.types|join(', ') }}</span>
                                    </div>
                                </div>
                            </label>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <!-- Card Types Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span><i class="fas fa-credit-card"></i> Card Types</span>
                    <span class="filter-badge">{{ card_types|length }} types</span>
                </div>
                
                <div class="select-all-container">
                    <input type="checkbox" id="selectAllTypes" class="ios-checkbox" onchange="toggleSelectAll('type')">
                    <label for="selectAllTypes" class="ios-checkbox-label">
                        <span class="ios-checkbox-custom"></span>
                        <span class="filter-name">Select All Types</span>
                    </label>
                </div>
                
                <div class="section-content">
                    <ul class="ios-list">
                        {% for type in card_types %}
                        <li class="ios-list-item filter-item">
                            <input type="checkbox" id="type-{{ type.id }}" name="types" value="{{ type.name }}" class="ios-checkbox type-checkbox">
                            <label for="type-{{ type.id }}" class="ios-checkbox-label">
                                <span class="ios-checkbox-custom"></span>
                                <div class="filter-info">
                                    <div class="filter-name">{{ type.name }}</div>
                                    <div class="filter-details">
                                        <span class="filter-badge">{{ type.count }} cards</span>
                                        <span class="filter-badge">{{ type.banks|length }} banks</span>
                                    </div>
                                </div>
                            </label>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button type="submit" class="ios-button" id="applyButton" onclick="showSuccessAnimation()">
                <i class="fas fa-check"></i> APPLY FILTERS
            </button>
        </form>

        <div class="success-animation" id="successAnimation" style="display: none;">
            <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
            <div class="success-message">Filter Applied!</div>
            <div class="success-details">Return to Telegram to get your results</div>
        </div>
    </div>

    <script>
        let selectedCountries = new Set();
        let availableBanks = {{ banks|tojson }};
        let countryBankMap = {{ country_bank_map|tojson }};

        function toggleCountry(countryCode) {
            const countryItem = document.querySelector(`.country-item[data-country="${countryCode}"]`);
            
            if (selectedCountries.has(countryCode)) {
                selectedCountries.delete(countryCode);
                countryItem.classList.remove('selected');
            } else {
                selectedCountries.add(countryCode);
                countryItem.classList.add('selected');
            }
            
            // Update hidden input
            document.getElementById('selectedCountries').value = Array.from(selectedCountries).join(',');
            
            // Update banks based on selected countries
            updateAvailableBanks();
        }

        function updateAvailableBanks() {
            const bankSearch = document.getElementById('bankSearch');
            const selectAllBanks = document.getElementById('selectAllBanks');
            const bankSelectionInfo = document.getElementById('bankSelectionInfo');
            
            if (selectedCountries.size === 0) {
                // No countries selected
                bankSearch.disabled = true;
                selectAllBanks.disabled = true;
                bankSelectionInfo.innerHTML = 'Please select countries first to see available banks';
                
                // Hide all banks
                document.querySelectorAll('.bank-item').forEach(item => {
                    item.classList.add('hidden');
                    const checkbox = item.querySelector('.bank-checkbox');
                    checkbox.checked = false;
                    checkbox.disabled = true;
                });
                
                return;
            }
            
            // Enable bank search and select all
            bankSearch.disabled = false;
            selectAllBanks.disabled = false;
            
            // Get banks available in selected countries
            let availableBankNames = new Set();
            selectedCountries.forEach(countryCode => {
                const banksInCountry = countryBankMap[countryCode] || [];
                banksInCountry.forEach(bank => availableBankNames.add(bank));
            });
            
            // Update bank selection info
            bankSelectionInfo.innerHTML = `Showing banks for <strong>${selectedCountries.size}</strong> selected countries`;
            
            // Show/hide banks based on availability
            document.querySelectorAll('.bank-item').forEach(item => {
                const bankName = item.dataset.bank;
                const checkbox = item.querySelector('.bank-checkbox');
                
                if (availableBankNames.has(bankName)) {
                    item.classList.remove('hidden');
                    checkbox.disabled = false;
                } else {
                    item.classList.add('hidden');
                    checkbox.checked = false;
                    checkbox.disabled = true;
                }
            });
        }

        function showMore(elementId, button) {
            const element = document.getElementById(elementId);
            element.classList.remove('hidden');
            button.style.display = 'none';
        }

        function filterItems(type) {
            const searchTerm = document.getElementById(type + 'Search').value.toLowerCase();
            const items = document.querySelectorAll('.' + type + '-item');
            
            items.forEach(item => {
                if (item.classList.contains('hidden')) return;
                
                const name = item.querySelector('.filter-name')?.textContent.toLowerCase() || 
                            item.querySelector('.country-name')?.textContent.toLowerCase() || '';
                
                if (name.includes(searchTerm)) {
                    item.style.display = type === 'country' ? 'block' : 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function toggleSelectAll(type) {
            const selectAll = document.getElementById('selectAll' + type.charAt(0).toUpperCase() + type.slice(1));
            const checkboxes = document.querySelectorAll('.' + type + '-checkbox:not(:disabled)');
            
            checkboxes.forEach(checkbox => {
                checkbox.checked = selectAll.checked;
            });
        }

        function showSuccessAnimation() {
            document.getElementById('successAnimation').style.display = 'block';
            document.getElementById('applyButton').style.display = 'none';
            
            // Submit form after animation
            setTimeout(() => {
                document.getElementById('filterForm').submit();
            }, 2500);
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            document.body.style.opacity = 0;
            document.body.style.transition = 'opacity 0.5s ease-in-out';
            setTimeout(() => { document.body.style.opacity = 1; }, 100);
            
            // Initial bank update
            updateAvailableBanks();
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
                        text-align: center; padding: 80px 20px; color: #8E8E93; background: #F2F2F7; min-height: 100vh;">
                <div style="background: #FFFFFF; padding: 40px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                    <div style="color: #FF3B30; font-size: 60px; margin-bottom: 20px;">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: #000000;">Session Expired</h2>
                    <p style="font-size: 18px; margin-bottom: 30px;">Please upload your file again in Telegram.</p>
                    <button onclick="window.history.back()" style="background: #007AFF; color: white; border: none; 
                            padding: 16px 32px; border-radius: 14px; font-size: 18px; font-weight: 600; cursor: pointer;
                            box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3); transition: all 0.3s ease;">
                        Go Back
                    </button>
                </div>
            </div>
        ''')
    
    session_data = user_sessions[user_id]
    
    if request.method == 'POST':
        selected_countries = request.form.getlist('countries')
        selected_banks = request.form.getlist('banks')
        selected_types = request.form.getlist('types')
        
        # تصفية البطاقات حسب المعايير المختارة
        filtered_cards = []
        for card in session_data['cards']:
            bin_code = card.split('|')[0][:6]
            bin_info = session_data['bin_data'].get(bin_code, {})
            country = bin_info.get('country', 'Unknown')
            bank = bin_info.get('bank', 'Unknown Bank')
            card_type = bin_info.get('type', 'Unknown Type')
            
            # التحقق من تطابق المعايير
            country_match = not selected_countries or country in selected_countries
            bank_match = not selected_banks or bank in selected_banks
            type_match = not selected_types or card_type in selected_types
            
            if country_match and bank_match and type_match:
                # إرجاع البطاقة كاملة (رقم + تاريخ + CVV)
                filtered_cards.append(card)
        
        # إرسال النتائج إلى المستخدم عبر البوت (البطاقات كاملة)
        session_data['filtered_result'] = "\n".join(filtered_cards) if filtered_cards else ""
        
        # إعلام البوت بأن التصفية اكتملت
        session_data['filter_complete'] = True
        
        return render_template_string('''
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                        text-align: center; padding: 80px 20px; background: #F2F2F7; min-height: 100vh;">
                <div style="background: #FFFFFF; padding: 40px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                    <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" style="width: 80px; height: 80px; margin: 0 auto 20px;">
                        <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none" style="stroke-dasharray: 166; stroke-dashoffset: 166; stroke-width: 5; stroke-miterlimit: 10; stroke: #34C759; fill: none; animation: stroke 0.6s cubic-bezier(0.650, 0.000, 0.450, 1.000) forwards;"/>
                        <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" style="transform-origin: 50% 50%; stroke-dasharray: 48; stroke-dashoffset: 48; stroke-width: 5; stroke: #34C759; stroke-miterlimit: 10; animation: stroke 0.3s cubic-bezier(0.650, 0.000, 0.450, 1.000) 0.8s forwards;"/>
                    </svg>
                    <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: #34C759;">Filter Applied Successfully!</h2>
                    <p style="font-size: 18px; color: #8E8E93; margin-bottom: 25px;">
                        Found <strong style="color: #007AFF;">{{ filtered_count }}</strong> matching cards
                    </p>
                    <div style="background: #F2F2F7; padding: 20px; border-radius: 14px; margin: 20px 0;">
                        <p style="font-size: 16px; color: #8E8E93; font-weight: 500;">
                            Return to Telegram to download your filtered cards file
                        </p>
                    </div>
                </div>
                <style>
                    @keyframes stroke {
                        100% { stroke-dashoffset: 0; }
                    }
                    .checkmark { animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both; }
                </style>
            </div>
        ''', filtered_count=len(filtered_cards))
    
    # تجميع بيانات التصفية
    country_stats = {}
    bank_stats = {}
    type_stats = {}
    country_bank_map = {}
    
    for card in session_data['cards']:
        bin_code = card.split('|')[0][:6]
        bin_info = session_data['bin_data'].get(bin_code, {})
        country = bin_info.get('country', 'Unknown')
        country_name = bin_info.get('country_name', 'Unknown Country')
        bank = bin_info.get('bank', 'Unknown Bank')
        card_type = bin_info.get('type', 'Unknown Type')
        
        # إحصاءات الدول
        if country not in country_stats:
            country_stats[country] = {
                'code': country,
                'name': country_name,
                'count': 0,
                'banks': set()
            }
        country_stats[country]['count'] += 1
        country_stats[country]['banks'].add(bank)
        
        # إحصاءات البنوك
        if bank not in bank_stats:
            bank_stats[bank] = {
                'id': len(bank_stats),
                'name': bank,
                'count': 0,
                'types': set()
            }
        bank_stats[bank]['count'] += 1
        bank_stats[bank]['types'].add(card_type)
        
        # إحصاءات الأنواع
        if card_type not in type_stats:
            type_stats[card_type] = {
                'id': len(type_stats),
                'name': card_type,
                'count': 0,
                'banks': set()
            }
        type_stats[card_type]['count'] += 1
        type_stats[card_type]['banks'].add(bank)
        
        # خريطة البنوك لكل دولة
        if country not in country_bank_map:
            country_bank_map[country] = set()
        country_bank_map[country].add(bank)
    
    # تحويل المجموعات إلى قوائم
    countries = []
    for country in country_stats.values():
        country['banks'] = list(country['banks'])
        countries.append(country)
    
    banks = []
    for bank in bank_stats.values():
        bank['types'] = list(bank['types'])
        banks.append(bank)
    
    card_types = []
    for card_type in type_stats.values():
        card_type['banks'] = list(card_type['banks'])
        card_types.append(card_type)
    
    # تحويل country_bank_map إلى قاموس عادي مع قوائم بدلاً من مجموعات
    country_bank_map_serializable = {}
    for country_code, bank_set in country_bank_map.items():
        country_bank_map_serializable[country_code] = list(bank_set)
    
    return render_template_string(HTML_TEMPLATE, 
                                countries=sorted(countries, key=lambda x: x['count'], reverse=True),
                                banks=sorted(banks, key=lambda x: x['count'], reverse=True),
                                card_types=sorted(card_types, key=lambda x: x['count'], reverse=True),
                                country_bank_map=country_bank_map_serializable)

@app.route('/api/set_session/<user_id>', methods=['POST'])
def set_session_data(user_id):
    """واجهة برمجية لوضع بيانات الجلسة من البوت"""
    try:
        data = request.get_json()
        if data is None:
            return safe_jsonify({"status": "error", "message": "Invalid JSON data"})
        
        user_sessions[user_id] = data
        return safe_jsonify({"status": "success", "message": "Session data stored"})
    
    except Exception as e:
        return safe_jsonify({"status": "error", "message": str(e)})

@app.route('/api/get_result/<user_id>', methods=['GET'])
def get_filter_result(user_id):
    """واجهة برمجية للحصول على نتيجة التصفية"""
    try:
        if user_id not in user_sessions:
            return safe_jsonify({"status": "error", "message": "Session not found"})
        
        session_data = user_sessions[user_id]
        
        if 'filtered_result' in session_data:
            result = session_data['filtered_result']
            # حذف الجلسة بعد استرجاع النتيجة
            del user_sessions[user_id]
            return safe_jsonify({"status": "success", "result": result})
        else:
            return safe_jsonify({"status": "pending", "message": "Filter not complete yet"})
    
    except Exception as e:
        return safe_jsonify({"status": "error", "message": str(e)})

def run_web_server():
    """تشغيل خادم الويب"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # تشغيل الخادم في خيط منفصل
    server_thread = threading.Thread(target=run_web_server)
    server_thread.daemon = True
    server_thread.start()
    print("Web server started on http://0.0.0.0:5000")
