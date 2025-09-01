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

# قالب HTML بتصميم أنيق وألوان متجانسة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Card Filter</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #2563EB;
            --primary-dark: #1D4ED8;
            --secondary: #10B981;
            --danger: #EF4444;
            --warning: #F59E0B;
            --info: #8B5CF6;
            
            --bg-primary: #FFFFFF;
            --bg-secondary: #F8FAFC;
            --bg-tertiary: #F1F5F9;
            
            --text-primary: #1E293B;
            --text-secondary: #64748B;
            --text-muted: #94A3B8;
            
            --border: #E2E8F0;
            --border-hover: #CBD5E1;
            
            --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            
            --radius: 12px;
            --radius-sm: 8px;
            --radius-lg: 16px;
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #0F172A;
                --bg-secondary: #1E293B;
                --bg-tertiary: #334155;
                
                --text-primary: #F1F5F9;
                --text-secondary: #CBD5E1;
                --text-muted: #64748B;
                
                --border: #334155;
                --border-hover: #475569;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 0;
            margin: 0;
            min-height: 100vh;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, var(--primary), var(--info));
            padding: 24px;
            border-radius: var(--radius-lg);
            margin-bottom: 24px;
            text-align: center;
            box-shadow: var(--shadow-lg);
            color: white;
        }

        .header h1 {
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .header p {
            font-size: 16px;
            font-weight: 500;
            opacity: 0.9;
        }

        .filter-section {
            background: var(--bg-primary);
            border-radius: var(--radius);
            margin-bottom: 24px;
            overflow: hidden;
            box-shadow: var(--shadow);
            border: 1px solid var(--border);
        }

        .section-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            font-weight: 600;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--bg-secondary);
            color: var(--text-primary);
        }

        .section-header i {
            color: var(--primary);
            font-size: 20px;
            margin-right: 10px;
        }

        .section-content {
            padding: 20px;
            max-height: 350px;
            overflow-y: auto;
        }

        .countries-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            gap: 12px;
        }

        .country-item {
            background: var(--bg-tertiary);
            padding: 16px;
            border-radius: var(--radius-sm);
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 2px solid transparent;
        }

        .country-item.selected {
            background: linear-gradient(135deg, var(--primary), var(--info));
            border-color: var(--primary);
            color: white;
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .country-item:hover {
            background: var(--bg-secondary);
            border-color: var(--border-hover);
        }

        .country-name {
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            color: inherit;
        }

        .country-count {
            font-size: 12px;
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 8px;
            border-radius: 20px;
            display: inline-block;
            font-weight: 600;
        }

        .country-item.selected .country-count {
            background: rgba(255, 255, 255, 0.3);
        }

        .search-container {
            padding: 16px;
            border-bottom: 1px solid var(--border);
            background: var(--bg-secondary);
        }

        .search-input {
            width: 100%;
            padding: 14px 16px;
            background: var(--bg-primary);
            border: 2px solid var(--border);
            border-radius: var(--radius-sm);
            font-size: 16px;
            font-weight: 500;
            color: var(--text-primary);
            transition: all 0.2s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .search-input:disabled {
            background: var(--bg-tertiary);
            cursor: not-allowed;
        }

        .list {
            list-style: none;
        }

        .list-item {
            display: flex;
            align-items: center;
            padding: 16px;
            border-bottom: 1px solid var(--border);
            transition: background-color 0.2s ease;
        }

        .list-item:hover {
            background: var(--bg-tertiary);
        }

        .list-item:last-child {
            border-bottom: none;
        }

        .checkbox {
            position: absolute;
            opacity: 0;
        }

        .checkbox-label {
            display: flex;
            align-items: center;
            width: 100%;
            cursor: pointer;
        }

        .checkbox-custom {
            width: 24px;
            height: 24px;
            border: 2px solid var(--border);
            border-radius: 6px;
            margin-right: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            background: var(--bg-primary);
        }

        .checkbox:checked + .checkbox-label .checkbox-custom {
            background: var(--primary);
            border-color: var(--primary);
        }

        .checkbox:checked + .checkbox-label .checkbox-custom::after {
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
            margin-bottom: 4px;
            color: var(--text-primary);
        }

        .filter-details {
            font-size: 14px;
            color: var(--text-secondary);
        }

        .badge {
            background: var(--bg-tertiary);
            color: var(--text-secondary);
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin-right: 8px;
        }

        .badge-primary {
            background: rgba(37, 99, 235, 0.1);
            color: var(--primary);
        }

        .badge-secondary {
            background: rgba(16, 185, 129, 0.1);
            color: var(--secondary);
        }

        .select-all-container {
            padding: 16px;
            border-bottom: 1px solid var(--border);
            background: var(--bg-secondary);
        }

        .show-more {
            text-align: center;
            padding: 16px;
            color: var(--primary);
            font-weight: 600;
            cursor: pointer;
            background: var(--bg-secondary);
            transition: background-color 0.2s ease;
        }

        .show-more:hover {
            background: var(--bg-tertiary);
        }

        .hidden {
            display: none;
        }

        .apply-button {
            background: linear-gradient(135deg, var(--primary), var(--info));
            color: white;
            border: none;
            border-radius: var(--radius);
            padding: 18px;
            font-size: 18px;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            margin-top: 24px;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-md);
        }

        .apply-button:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .apply-button:active {
            transform: translateY(0);
        }

        .footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 24px;
            padding: 16px;
        }

        .selection-info {
            background: var(--bg-tertiary);
            padding: 16px;
            border-radius: var(--radius-sm);
            margin: 16px;
            font-size: 14px;
            color: var(--text-secondary);
            border-left: 4px solid var(--primary);
        }

        .selection-info strong {
            color: var(--primary);
        }

        .stats-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            padding: 16px;
            background: var(--bg-secondary);
            border-radius: var(--radius-sm);
            margin: 16px 0;
        }

        .stat-item {
            text-align: center;
            padding: 12px;
            background: var(--bg-primary);
            border-radius: var(--radius-sm);
            box-shadow: var(--shadow);
        }

        .stat-number {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 4px;
        }

        .stat-label {
            font-size: 12px;
            color: var(--text-secondary);
            font-weight: 600;
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
            stroke: var(--secondary);
            stroke-miterlimit: 10;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
            animation: fill .4s ease-in-out .4s forwards, scale .3s ease-in-out .9s both;
            margin: 0 auto 20px;
        }

        .checkmark-circle {
            stroke-dasharray: 166;
            stroke-dashoffset: 166;
            stroke-width: 5;
            stroke-miterlimit: 10;
            stroke: var(--secondary);
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
            color: var(--secondary);
            margin-bottom: 8px;
        }

        .success-details {
            font-size: 16px;
            color: var(--text-secondary);
        }

        @keyframes stroke {
            100% { stroke-dashoffset: 0; }
        }

        @keyframes scale {
            0%, 100% { transform: none; }
            50% { transform: scale3d(1.1, 1.1, 1); }
        }

        @keyframes fill {
            100% { box-shadow: 0 0 30px rgba(16, 185, 129, 0.1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-filter"></i> Advanced Card Filter</h1>
            <p>Filter cards by country, bank, and card type</p>
        </div>

        <form method="POST" id="filterForm">
            <!-- Countries Section -->
            <div class="filter-section">
                <div class="section-header">
                    <span><i class="fas fa-globe"></i> Countries</span>
                    <span class="badge">{{ countries|length }} countries</span>
                </div>
                
                <div class="search-container">
                    <input type="text" class="search-input" id="countrySearch" placeholder="Search countries..." onkeyup="filterItems('country')">
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
                    <span class="badge">{{ banks|length }} banks</span>
                </div>
                
                <div class="selection-info" id="bankSelectionInfo">
                    {% if countries|length > 0 %}
                    Please select countries first to see available banks
                    {% else %}
                    No countries available
                    {% endif %}
                </div>
                
                <div class="search-container">
                    <input type="text" class="search-input" id="bankSearch" placeholder="Search banks..." onkeyup="filterItems('bank')" disabled>
                </div>
                
                <div class="select-all-container">
                    <input type="checkbox" id="selectAllBanks" class="checkbox" onchange="toggleSelectAll('bank')" disabled>
                    <label for="selectAllBanks" class="checkbox-label">
                        <span class="checkbox-custom"></span>
                        <span class="filter-name">Select All Banks</span>
                    </label>
                </div>
                
                <div class="section-content" id="banksContent">
                    <ul class="list">
                        {% for bank in banks %}
                        <li class="list-item filter-item bank-item hidden" data-bank="{{ bank.name }}">
                            <input type="checkbox" id="bank-{{ bank.id }}" name="banks" value="{{ bank.name }}" class="checkbox bank-checkbox" disabled>
                            <label for="bank-{{ bank.id }}" class="checkbox-label">
                                <span class="checkbox-custom"></span>
                                <div class="filter-info">
                                    <div class="filter-name">{{ bank.name }}</div>
                                    <div class="filter-details">
                                        <span class="badge badge-primary">{{ bank.count }} cards</span>
                                        {% if bank.types %}
                                        <span class="badge badge-secondary">{{ bank.types|join(', ') }}</span>
                                        {% endif %}
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
                    <span class="badge">{{ card_types|length }} types</span>
                </div>
                
                <div class="selection-info" id="typeSelectionInfo">
                    {% if countries|length > 0 and banks|length > 0 %}
                    Select countries and banks to see available types
                    {% elif countries|length > 0 %}
                    Select countries first to see available types
                    {% else %}
                    No types available
                    {% endif %}
                </div>
                
                <div class="search-container">
                    <input type="text" class="search-input" id="typeSearch" placeholder="Search types..." onkeyup="filterItems('type')" disabled>
                </div>
                
                <div class="select-all-container">
                    <input type="checkbox" id="selectAllTypes" class="checkbox" onchange="toggleSelectAll('type')" disabled>
                    <label for="selectAllTypes" class="checkbox-label">
                        <span class="checkbox-custom"></span>
                        <span class="filter-name">Select All Types</span>
                    </label>
                </div>
                
                <div class="section-content" id="typesContent">
                    <ul class="list">
                        {% for type in card_types %}
                        <li class="list-item filter-item type-item hidden" data-type="{{ type.name }}">
                            <input type="checkbox" id="type-{{ type.id }}" name="types" value="{{ type.name }}" class="checkbox type-checkbox" disabled>
                            <label for="type-{{ type.id }}" class="checkbox-label">
                                <span class="checkbox-custom"></span>
                                <div class="filter-info">
                                    <div class="filter-name">{{ type.name }}</div>
                                    <div class="filter-details">
                                        <span class="badge badge-primary">{{ type.count }} cards</span>
                                        <span class="badge badge-secondary">{{ type.banks|length }} banks</span>
                                    </div>
                                </div>
                            </label>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <button type="submit" class="apply-button" id="applyButton" onclick="showSuccessAnimation()">
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

        <div class="footer">
            <p>Advanced filtering with <i class="fas fa-heart" style="color:var(--danger)"></i></p>
        </div>
    </div>

    <script>
        let selectedCountries = new Set();
        let selectedBanks = new Set();
        let availableBanks = {{ banks|tojson }};
        let availableTypes = {{ card_types|tojson }};
        let countryBankMap = {{ country_bank_map|tojson }};
        let bankTypeMap = {{ bank_type_map|tojson }};

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
            
            // Update banks and types based on selected countries
            updateAvailableBanks();
            updateAvailableTypes();
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

        function updateAvailableTypes() {
            const typeSearch = document.getElementById('typeSearch');
            const selectAllTypes = document.getElementById('selectAllTypes');
            const typeSelectionInfo = document.getElementById('typeSelectionInfo');
            
            if (selectedCountries.size === 0) {
                typeSearch.disabled = true;
                selectAllTypes.disabled = true;
                typeSelectionInfo.innerHTML = 'Select countries first to see available types';
                
                document.querySelectorAll('.type-item').forEach(item => {
                    item.classList.add('hidden');
                    const checkbox = item.querySelector('.type-checkbox');
                    checkbox.checked = false;
                    checkbox.disabled = true;
                });
                return;
            }
            
            // Enable type search and select all
            typeSearch.disabled = false;
            selectAllTypes.disabled = false;
            typeSelectionInfo.innerHTML = `Showing types for selected criteria`;
            
            // Show all types since we want to display all available types
            document.querySelectorAll('.type-item').forEach(item => {
                item.classList.remove('hidden');
                const checkbox = item.querySelector('.type-checkbox');
                checkbox.disabled = false;
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
            document.body.style.transition = 'opacity 0.3s ease-in-out';
            setTimeout(() => { document.body.style.opacity = 1; }, 100);
            
            // Initial updates
            updateAvailableBanks();
            updateAvailableTypes();
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
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        text-align: center; padding: 80px 20px; color: #64748B; background: #F8FAFC; min-height: 100vh;">
                <div style="background: #FFFFFF; padding: 40px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #E2E8F0;">
                    <div style="color: #EF4444; font-size: 60px; margin-bottom: 20px;">
                        <i class="fas fa-exclamation-triangle"></i>
                    </div>
                    <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: #1E293B;">Session Expired</h2>
                    <p style="font-size: 18px; margin-bottom: 30px;">Please upload your file again in Telegram.</p>
                    <button onclick="window.history.back()" style="background: #2563EB; color: white; border: none; 
                            padding: 16px 32px; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: pointer;
                            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2); transition: all 0.2s ease;">
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
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        text-align: center; padding: 80px 20px; background: #F8FAFC; min-height: 100vh;">
                <div style="background: #FFFFFF; padding: 40px; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border: 1px solid #E2E8F0;">
                    <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52" style="width: 80px; height: 80px; margin: 0 auto 20px;">
                        <circle class="checkmark-circle" cx="26" cy="26" r="25" fill="none" style="stroke-dasharray: 166; stroke-dashoffset: 166; stroke-width: 5; stroke-miterlimit: 10; stroke: #10B981; fill: none; animation: stroke 0.6s cubic-bezier(0.650, 0.000, 0.450, 1.000) forwards;"/>
                        <path class="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" style="transform-origin: 50% 50%; stroke-dasharray: 48; stroke-dashoffset: 48; stroke-width: 5; stroke: #10B981; stroke-miterlimit: 10; animation: stroke 0.3s cubic-bezier(0.650, 0.000, 0.450, 1.000) 0.8s forwards;"/>
                    </svg>
                    <h2 style="font-size: 28px; font-weight: 700; margin-bottom: 15px; color: #10B981;">Filter Applied Successfully!</h2>
                    <p style="font-size: 18px; color: #64748B; margin-bottom: 25px;">
                        Found <strong style="color: #2563EB;">{{ filtered_count }}</strong> matching cards
                    </p>
                    <div style="background: #F1F5F9; padding: 20px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #2563EB;">
                        <p style="font-size: 16px; color: #64748B; font-weight: 600;">
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
    bank_type_map = {}
    
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
        
        # خريطة الأنواع لكل بنك
        if bank not in bank_type_map:
            bank_type_map[bank] = set()
        bank_type_map[bank].add(card_type)
    
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
    
    # تحويل الخرائط إلى قوائم
    country_bank_map_serializable = {}
    for country_code, bank_set in country_bank_map.items():
        country_bank_map_serializable[country_code] = list(bank_set)
    
    bank_type_map_serializable = {}
    for bank_name, type_set in bank_type_map.items():
        bank_type_map_serializable[bank_name] = list(type_set)
    
    # إحصائيات
    total_cards = len(session_data['cards'])
    total_countries = len(countries)
    total_banks = len(banks)
    total_types = len(card_types)
    
    return render_template_string(HTML_TEMPLATE, 
                                countries=sorted(countries, key=lambda x: x['count'], reverse=True),
                                banks=sorted(banks, key=lambda x: x['count'], reverse=True),
                                card_types=sorted(card_types, key=lambda x: x['count'], reverse=True),
                                country_bank_map=country_bank_map_serializable,
                                bank_type_map=bank_type_map_serializable,
                                total_cards=total_cards,
                                total_countries=total_countries,
                                total_banks=total_banks,
                                total_types=total_types)

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
