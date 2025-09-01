from flask import Flask, request, jsonify, render_template_string
import threading

# إنشاء تطبيق Flask
app = Flask(__name__)

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
        }

        .section-header i {
            color: var(--ios-blue);
            font-size: 20px;
        }

        .section-content {
            max-height: 300px;
            overflow-y: auto;
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
            font-size: 17px;
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
            padding: 16px;
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
            width: 26px;
            height: 26px;
            border: 2px solid var(--ios-gray-2);
            border-radius: 7px;
            margin-right: 14px;
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
            font-size: 16px;
            font-weight: bold;
        }

        .filter-info {
            flex: 1;
        }

        .filter-name {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .filter-details {
            font-size: 15px;
            color: var(--ios-text-secondary);
        }

        .filter-badge {
            background: var(--ios-gray-4);
            color: var(--ios-text-secondary);
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
        }

        .bank-type-info {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }

        .bank-badge {
            background: rgba(0, 122, 255, 0.12);
            color: var(--ios-blue);
            padding: 5px 10px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
        }

        .type-badge {
            background: rgba(52, 199, 89, 0.12);
            color: var(--ios-green);
            padding: 5px 10px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 600;
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

        .ios-footer {
            text-align: center;
            color: var(--ios-text-secondary);
            font-size: 14px;
            margin-top: 24px;
            padding: 16px;
            font-weight: 500;
        }

        .stats-container {
            display: flex;
            justify-content: space-between;
            padding: 16px;
            background: var(--ios-gray-4);
            border-radius: 12px;
            margin: 16px;
        }

        .stat-item {
            text-align: center;
        }

        .stat-number {
            font-size: 20px;
            font-weight: 700;
            color: var(--ios-blue);
        }

        .stat-label {
            font-size: 14px;
            color: var(--ios-text-secondary);
            font-weight: 500;
        }

        .select-all-container {
            padding: 16px;
            border-bottom: 1px solid var(--ios-gray-3);
            background: var(--ios-gray-4);
        }

        .success-animation {
            display: none;
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

        .success-message {
            font-size: 22px;
            font-weight: 700;
            color: var(--ios-green);
            margin-bottom: 10px;
        }

        .success-details {
            font-size: 16px;
            color: var(--ios-text-secondary);
            font-weight: 500;
        }

        .show-more {
            text-align: center;
            padding: 16px;
            color: var(--ios-blue);
            font-weight: 600;
            cursor: pointer;
            background: var(--ios-gray-4);
        }

        .dependency-message {
            padding: 16px;
            background: rgba(255, 149, 0, 0.1);
            color: var(--ios-orange);
            text-align: center;
            font-weight: 500;
            border-radius: 12px;
            margin: 16px;
        }
    </style>
</head>
<body>
    <div class="ios-container">
        <div class="ios-header">
            <h1><i class="fas fa-filter"></i> Advanced Card Filter</h1>
            <p>Filter cards by country, bank, or type</p>
        </div>

        <div class="stats-container">
            <div class="stat-item">
                <div class="stat-number">{{ total_cards }}</div>
                <div class="stat-label">Total Cards</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ total_countries }}</div>
                <div class="stat-label">Countries</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ total_banks }}</div>
                <div class="stat-label">Banks</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{{ total_types }}</div>
                <div class="stat-label">Types</div>
            </div>
        </div>

        <form method="POST" id="filterForm">
            <!-- Countries Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span>Countries <i class="fas fa-globe"></i></span>
                    <span class="filter-badge">{{ countries|length }}</span>
                </div>
                
                <div class="search-container">
                    <input type="text" class="ios-search" id="countrySearch" placeholder="Search countries..." onkeyup="filterItems('country')">
                </div>
                
                <div class="select-all-container">
                    <input type="checkbox" id="selectAllCountries" class="ios-checkbox" onchange="toggleSelectAll('country')">
                    <label for="selectAllCountries" class="ios-checkbox-label">
                        <span class="ios-checkbox-custom"></span>
                        <span class="filter-name">Select All Countries</span>
                    </label>
                </div>
                
                <div class="section-content">
                    <ul class="ios-list" id="countryList">
                        {% for country in countries %}
                        <li class="ios-list-item filter-item country-item">
                            <input type="checkbox" id="country-{{ country.code }}" name="countries" value="{{ country.code }}" class="ios-checkbox country-checkbox" onchange="updateDependencies('country')">
                            <label for="country-{{ country.code }}" class="ios-checkbox-label">
                                <span class="ios-checkbox-custom"></span>
                                <div class="filter-info">
                                    <div class="filter-name">{{ country.name }}</div>
                                    <div class="filter-details">
                                        <span class="filter-badge">{{ country.count }} cards</span>
                                        <span class="filter-badge">{{ country.banks|length }} banks</span>
                                    </div>
                                </div>
                            </label>
                        </li>
                        {% endfor %}
                    </ul>
                    
                    {% if countries|length > 20 %}
                    <div class="show-more" onclick="showAllItems('country')">
                        Show All {{ countries|length }} Countries
                    </div>
                    {% endif %}
                </div>
            </div>

            <!-- Banks Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span>Banks <i class="fas fa-university"></i></span>
                    <span class="filter-badge">{{ banks|length }}</span>
                </div>
                
                <div id="bankDependencyMessage" class="dependency-message" style="display: none;">
                    Please select a country first to see available banks
                </div>
                
                <div id="bankContent" style="display: none;">
                    <div class="search-container">
                        <input type="text" class="ios-search" id="bankSearch" placeholder="Search banks..." onkeyup="filterItems('bank')">
                    </div>
                    
                    <div class="select-all-container">
                        <input type="checkbox" id="selectAllBanks" class="ios-checkbox" onchange="toggleSelectAll('bank')">
                        <label for="selectAllBanks" class="ios-checkbox-label">
                            <span class="ios-checkbox-custom"></span>
                            <span class="filter-name">Select All Banks</span>
                        </label>
                    </div>
                    
                    <div class="section-content">
                        <ul class="ios-list" id="bankList">
                            {% for bank in banks %}
                            <li class="ios-list-item filter-item bank-item" data-countries="{{ bank.countries|join(',') }}">
                                <input type="checkbox" id="bank-{{ bank.id }}" name="banks" value="{{ bank.name }}" class="ios-checkbox bank-checkbox" onchange="updateDependencies('bank')">
                                <label for="bank-{{ bank.id }}" class="ios-checkbox-label">
                                    <span class="ios-checkbox-custom"></span>
                                    <div class="filter-info">
                                        <div class="filter-name">{{ bank.name }}</div>
                                        <div class="filter-details">
                                            <span class="filter-badge">{{ bank.count }} cards</span>
                                            <span class="type-badge">{{ bank.types|join(', ') }}</span>
                                        </div>
                                    </div>
                                </label>
                            </li>
                            {% endfor %}
                        </ul>
                        
                        {% if banks|length > 20 %}
                        <div class="show-more" onclick="showAllItems('bank')">
                            Show All {{ banks|length }} Banks
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Types Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span>Card Types <i class="fas fa-credit-card"></i></span>
                    <span class="filter-badge">{{ types|length }}</span>
                </div>
                
                <div class="search-container">
                    <input type="text" class="ios-search" id="typeSearch" placeholder="Search types..." onkeyup="filterItems('type')">
                </div>
                
                <div class="select-all-container">
                    <input type="checkbox" id="selectAllTypes" class="ios-checkbox" onchange="toggleSelectAll('type')">
                    <label for="selectAllTypes" class="ios-checkbox-label">
                        <span class="ios-checkbox-custom"></span>
                        <span class="filter-name">Select All Types</span>
                    </label>
                </div>
                
                <div class="section-content">
                    <ul class="ios-list" id="typeList">
                        {% for type in types %}
                        <li class="ios-list-item filter-item type-item">
                            <input type="checkbox" id="type-{{ type.id }}" name="types" value="{{ type.name }}" class="ios-checkbox type-checkbox">
                            <label for="type-{{ type.id }}" class="ios-checkbox-label">
                                <span class="ios-checkbox-custom"></span>
                                <div class="filter-info">
                                    <div class="filter-name">{{ type.name }}</div>
                                    <div class="filter-details">
                                        <span class="filter-badge">{{ type.count }} cards</span>
                                        <span class="bank-badge">{{ type.banks|length }} banks</span>
                                    </div>
                                </div>
                            </label>
                        </li>
                        {% endfor %}
                    </ul>
                    
                    {% if types|length > 20 %}
                    <div class="show-more" onclick="showAllItems('type')">
                        Show All {{ types|length }} Types
                    </div>
                    {% endif %}
                </div>
            </div>
        </form>

        <button type="button" class="ios-button" onclick="validateAndSubmit()">
            <i class="fas fa-check"></i> APPLY FILTERS
        </button>

        <div class="success-animation" id="successAnimation">
            <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
            </svg>
            <div class="success-message">Filter Applied!</div>
            <div class="success-details">Return to Telegram to get your results</div>
        </div>

        <div class="ios-footer">
            <p>Advanced filtering with <i class="fas fa-heart" style="color:var(--ios-red)"></i> iOS design</p>
        </div>
    </div>

    <script>
        // Initially show only first 20 items
        document.addEventListener('DOMContentLoaded', function() {
            // Limit to 20 items initially
            limitItems('country', 20);
            limitItems('bank', 20);
            limitItems('type', 20);
            
            // iOS-like smooth animations
            document.body.style.opacity = 0;
            document.body.style.transition = 'opacity 0.5s ease-in-out';
            setTimeout(() => { document.body.style.opacity = 1; }, 100);
        });

        function limitItems(type, limit) {
            const items = document.querySelectorAll(`.${type}-item`);
            items.forEach((item, index) => {
                item.style.display = index < limit ? 'flex' : 'none';
            });
        }

        function showAllItems(type) {
            const items = document.querySelectorAll(`.${type}-item`);
            items.forEach(item => {
                item.style.display = 'flex';
            });
            
            document.querySelector(`.${type}-item`).closest('.section-content').querySelector('.show-more').style.display = 'none';
        }

        function filterItems(type) {
            const searchTerm = document.getElementById(`${type}Search`).value.toLowerCase();
            const items = document.querySelectorAll(`.${type}-item`);
            
            items.forEach(item => {
                const filterName = item.querySelector('.filter-name').textContent.toLowerCase();
                if (filterName.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        }

        function toggleSelectAll(type) {
            const selectAll = document.getElementById(`selectAll${type.charAt(0).toUpperCase() + type.slice(1)}`).checked;
            const checkboxes = document.querySelectorAll(`.${type}-checkbox`);
            
            checkboxes.forEach(checkbox => {
                if (checkbox.closest('.filter-item').style.display !== 'none') {
                    checkbox.checked = selectAll;
                }
            });
            
            if (type === 'country') {
                updateDependencies('country');
            }
        }

        function updateDependencies(type) {
            if (type === 'country') {
                const selectedCountries = Array.from(document.querySelectorAll('.country-checkbox:checked'))
                    .map(cb => cb.value);
                
                const bankItems = document.querySelectorAll('.bank-item');
                const bankContent = document.getElementById('bankContent');
                const bankDependencyMessage = document.getElementById('bankDependencyMessage');
                
                if (selectedCountries.length > 0) {
                    bankDependencyMessage.style.display = 'none';
                    bankContent.style.display = 'block';
                    
                    // Show banks that belong to selected countries
                    bankItems.forEach(item => {
                        const bankCountries = item.getAttribute('data-countries').split(',');
                        const hasMatch = bankCountries.some(country => selectedCountries.includes(country));
                        item.style.display = hasMatch ? 'flex' : 'none';
                    });
                } else {
                    bankDependencyMessage.style.display = 'block';
                    bankContent.style.display = 'none';
                }
            }
        }

        function validateAndSubmit() {
            const selectedCountries = document.querySelectorAll('.country-checkbox:checked').length;
            const selectedBanks = document.querySelectorAll('.bank-checkbox:checked').length;
            const selectedTypes = document.querySelectorAll('.type-checkbox:checked').length;
            
            if (selectedCountries === 0 && selectedBanks === 0 && selectedTypes === 0) {
                alert('Please select at least one filter criteria.');
                return;
            }
            
            showSuccessAnimation();
        }

        function showSuccessAnimation() {
            document.getElementById('successAnimation').style.display = 'block';
            document.querySelector('.ios-button').style.display = 'none';
            
            // Submit form after animation
            setTimeout(() => {
                document.getElementById('filterForm').submit();
            }, 2500);
        }

        // Update select all checkbox when individual checkboxes change
        document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const type = this.className.includes('country') ? 'country' : 
                            this.className.includes('bank') ? 'bank' : 'type';
                
                const allVisibleChecked = Array.from(document.querySelectorAll(`.${type}-checkbox`))
                    .filter(cb => cb.closest('.filter-item').style.display !== 'none')
                    .every(cb => cb.checked);
                    
                document.getElementById(`selectAll${type.charAt(0).toUpperCase() + type.slice(1)}`).checked = allVisibleChecked;
            });
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
                        text-align: center; padding: 80px 20px; color: #8E8E93; background: var(--ios-background); min-height: 100vh;">
                <div style="background: var(--ios-card-bg); padding: 40px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                    <div style="color: #FF3B30; font-size: 60px; margin-bottom: 20px;">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: var(--ios-text-primary);">Session Expired</h2>
                    <p style="font-size: 18px; margin-bottom: 30px;">Please upload your file again in Telegram.</p>
                    <button onclick="window.history.back()" style="background: var(--ios-blue); color: white; border: none; 
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
        
        if not selected_countries and not selected_banks and not selected_types:
            return render_template_string('''
                <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                            text-align: center; padding: 80px 20px; color: #8E8E93; background: var(--ios-background); min-height: 100vh;">
                    <div style="background: var(--ios-card-bg); padding: 40px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                        <div style="color: #FF9500; font-size: 60px; margin-bottom: 20px;">
                            <i class="fas fa-exclamation-circle"></i>
                        </div>
                        <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: var(--ios-text-primary);">No Filters Selected</h2>
                        <p style="font-size: 18px; margin-bottom: 30px;">Please select at least one filter criteria.</p>
                        <button onclick="window.history.back()" style="background: var(--ios-blue); color: white; border: none; 
                                padding: 16px 32px; border-radius: 14px; font-size: 18px; font-weight: 600; cursor: pointer;
                                box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);">
                            Go Back
                        </button>
                    </div>
                </div>
            ''')
        
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
                # إرجاع البطاقة كاملة (مع الشهر والسنة)
                filtered_cards.append(card)
        
        # إرسال النتائج إلى المستخدم عبر البوت (البطاقات كاملة)
        if filtered_cards:
            result = "\n".join(filtered_cards)
            session_data['filtered_result'] = result
        else:
            session_data['filtered_result'] = ""
        
        # إعلام البوت بأن التصفية اكتملت
        session_data['filter_complete'] = True
        
        return render_template_string('''
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                        text-align: center; padding: 80px 20px; background: var(--ios-background); min-height: 100vh;">
                <div style="background: var(--ios-card-bg); padding: 40px; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.1);">
                    <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" style="width: 80px; height: 80px; margin: 0 auto 20px;">
                        <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none" style="stroke-dasharray: 166; stroke-dashoffset: 166; stroke-width: 5; stroke-miterlimit: 10; stroke: #34C759; fill: none; animation: stroke 0.6s cubic-bezier(0.650, 0.000, 0.450, 1.000) forwards;"/>
                        <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" style="transform-origin: 50% 50%; stroke-dasharray: 48; stroke-dashoffset: 48; stroke-width: 5; stroke: #34C759; stroke-miterlimit: 10; animation: stroke 0.3s cubic-bezier(0.650, 0.000, 0.450, 1.000) 0.8s forwards;"/>
                    </svg>
                    <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: #34C759;">Filter Applied Successfully!</h2>
                    <p style="font-size: 18px; color: var(--ios-text-secondary); margin-bottom: 25px;">
                        Found <strong style="color: var(--ios-blue);">{{ filtered_count }}</strong> matching cards
                    </p>
                    <div style="background: var(--ios-gray-4); padding: 20px; border-radius: 14px; margin: 20px 0;">
                        <p style="font-size: 16px; color: var(--ios-text-secondary); font-weight: 500;">
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
                'types': set(),
                'countries': set()
            }
        bank_stats[bank]['count'] += 1
        bank_stats[bank]['types'].add(card_type)
        bank_stats[bank]['countries'].add(country)
        
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
    
    # تحويل المجموعات إلى قوائم
    countries = []
    for country in country_stats.values():
        country['banks'] = list(country['banks'])
        countries.append(country)
    
    banks = []
    for bank in bank_stats.values():
        bank['types'] = list(bank['types'])
        bank['countries'] = list(bank['countries'])
        banks.append(bank)
    
    types = []
    for card_type in type_stats.values():
        card_type['banks'] = list(card_type['banks'])
        types.append(card_type)
    
    # إحصائيات إضافية
    total_cards = len(session_data['cards'])
    total_countries = len(countries)
    total_banks = len(banks)
    total_types = len(types)
    
    return render_template_string(HTML_TEMPLATE, 
                                countries=sorted(countries, key=lambda x: x['count'], reverse=True),
                                banks=sorted(banks, key=lambda x: x['count'], reverse=True),
                                types=sorted(types, key=lambda x: x['count'], reverse=True),
                                total_cards=total_cards,
                                total_countries=total_countries,
                                total_banks=total_banks,
                                total_types=total_types)

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
