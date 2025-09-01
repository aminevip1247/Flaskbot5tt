from flask import Flask, request, jsonify, render_template_string
import os
import csv

app = Flask(__name__)

# قالب HTML مع تصميم يشبه iOS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Card Filter</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }
        
        body {
            background-color: #f2f2f7;
            color: #000;
            padding: 16px;
            max-width: 500px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 24px;
            padding-top: 20px;
        }
        
        .header h1 {
            font-size: 28px;
            font-weight: 600;
            color: #000;
        }
        
        .filters-section {
            background-color: #fff;
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        
        .section-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #000;
        }
        
        .filter-group {
            margin-bottom: 20px;
        }
        
        .filter-label {
            display: block;
            font-size: 16px;
            font-weight: 500;
            margin-bottom: 8px;
            color: #000;
        }
        
        .checkbox-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 12px;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
        }
        
        .ios-checkbox {
            appearance: none;
            -webkit-appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid #c7c7cc;
            margin-right: 8px;
            position: relative;
            cursor: pointer;
        }
        
        .ios-checkbox:checked {
            background-color: #007AFF;
            border-color: #007AFF;
        }
        
        .ios-checkbox:checked::after {
            content: "✓";
            position: absolute;
            color: white;
            font-size: 12px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        
        .card-type-selector {
            display: flex;
            background-color: #e5e5ea;
            border-radius: 8px;
            padding: 4px;
            margin-bottom: 16px;
        }
        
        .card-type-btn {
            flex: 1;
            padding: 8px 12px;
            text-align: center;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            background: transparent;
            border: none;
            color: #3c3c43;
        }
        
        .card-type-btn.active {
            background-color: #fff;
            color: #000;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .action-buttons {
            display: flex;
            gap: 12px;
            margin-top: 24px;
        }
        
        .ios-button {
            flex: 1;
            padding: 14px 20px;
            border-radius: 12px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s;
        }
        
        .ios-button.primary {
            background-color: #007AFF;
            color: white;
        }
        
        .ios-button.secondary {
            background-color: #e5e5ea;
            color: #000;
        }
        
        .ios-button:active {
            opacity: 0.8;
            transform: scale(0.98);
        }
        
        .results-section {
            background-color: #fff;
            border-radius: 14px;
            padding: 16px;
            margin-top: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            display: none;
        }
        
        .card-item {
            padding: 12px;
            border-bottom: 1px solid #f2f2f7;
        }
        
        .card-item:last-child {
            border-bottom: none;
        }
        
        .card-number {
            font-weight: 500;
            margin-bottom: 4px;
        }
        
        .card-details {
            font-size: 14px;
            color: #8e8e93;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Card Filter</h1>
    </div>
    
    <div class="filters-section">
        <div class="section-title">Filter Options</div>
        
        <div class="filter-group">
            <span class="filter-label">Card Type</span>
            <div class="card-type-selector">
                <button class="card-type-btn active" data-type="all">All</button>
                <button class="card-type-btn" data-type="credit">Credit</button>
                <button class="card-type-btn" data-type="debit">Debit</button>
            </div>
        </div>
        
        <div class="filter-group">
            <span class="filter-label">Countries</span>
            <div class="checkbox-grid" id="countries-container">
                <!-- سيتم ملء هذا القسم بالدول المتاحة -->
            </div>
        </div>
        
        <div class="filter-group">
            <span class="filter-label">Banks</span>
            <div class="checkbox-grid" id="banks-container">
                <!-- سيتم ملء هذا القسم بالبنوك المتاحة -->
            </div>
        </div>
        
        <div class="action-buttons">
            <button class="ios-button secondary" id="reset-btn">Reset</button>
            <button class="ios-button primary" id="filter-btn">Apply Filters</button>
        </div>
    </div>
    
    <div class="results-section" id="results-section">
        <div class="section-title">Filtered Cards</div>
        <div id="cards-container">
            <!-- سيتم ملء هذا القسم بالبطاقات التي تطابق الفلتر -->
        </div>
    </div>

    <script>
        // بيانات التطبيق
        const appData = {
            cards: {{ cards_data|tojson }},
            countries: {{ countries|tojson }},
            banks: {{ banks|tojson }},
            cardTypes: ['CREDIT', 'DEBIT']
        };
        
        // تهيئة واجهة المستخدم
        function initializeUI() {
            // تعبئة قائمة الدول
            const countriesContainer = document.getElementById('countries-container');
            appData.countries.forEach(country => {
                const checkboxItem = document.createElement('div');
                checkboxItem.className = 'checkbox-item';
                checkboxItem.innerHTML = `
                    <input type="checkbox" class="ios-checkbox" id="country-${country}" data-value="${country}">
                    <label for="country-${country}">${country}</label>
                `;
                countriesContainer.appendChild(checkboxItem);
            });
            
            // تعبئة قائمة البنوك
            const banksContainer = document.getElementById('banks-container');
            appData.banks.forEach(bank => {
                const checkboxItem = document.createElement('div');
                checkboxItem.className = 'checkbox-item';
                checkboxItem.innerHTML = `
                    <input type="checkbox" class="ios-checkbox" id="bank-${bank}" data-value="${bank}">
                    <label for="bank-${bank}">${bank}</label>
                `;
                banksContainer.appendChild(checkboxItem);
            });
            
            // إضافة أحداث لأزرار نوع البطاقة
            document.querySelectorAll('.card-type-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    document.querySelectorAll('.card-type-btn').forEach(b => b.classList.remove('active'));
                    this.classList.add('active');
                });
            });
            
            // حدث لزر التصفية
            document.getElementById('filter-btn').addEventListener('click', applyFilters);
            
            // حدث لزر إعادة الضبط
            document.getElementById('reset-btn').addEventListener('click', resetFilters);
        }
        
        // تطبيق الفلاتر
        function applyFilters() {
            // الحصول على نوع البطاقة المحدد
            const selectedType = document.querySelector('.card-type-btn.active').dataset.type;
            
            // الحصول على الدول المحددة
            const selectedCountries = [];
            document.querySelectorAll('#countries-container .ios-checkbox:checked').forEach(checkbox => {
                selectedCountries.push(checkbox.dataset.value);
            });
            
            // الحصول على البنوك المحددة
            const selectedBanks = [];
            document.querySelectorAll('#banks-container .ios-checkbox:checked').forEach(checkbox => {
                selectedBanks.push(checkbox.dataset.value);
            });
            
            // تصفية البطاقات
            const filteredCards = appData.cards.filter(card => {
                // تصفية حسب النوع
                if (selectedType !== 'all') {
                    const cardType = card.details && card.details[2] ? card.details[2].toLowerCase() : '';
                    if (selectedType !== cardType) return false;
                }
                
                // تصفية حسب الدولة
                if (selectedCountries.length > 0) {
                    const cardCountry = card.details && card.details[8] ? card.details[8] : '';
                    if (!selectedCountries.includes(cardCountry)) return false;
                }
                
                // تصفية حسب البنك
                if (selectedBanks.length > 0) {
                    const cardBank = card.details && card.details[4] ? card.details[4] : '';
                    if (!selectedBanks.includes(cardBank)) return false;
                }
                
                return true;
            });
            
            // عرض النتائج
            displayResults(filteredCards);
        }
        
        // عرض النتائج
        function displayResults(cards) {
            const resultsSection = document.getElementById('results-section');
            const cardsContainer = document.getElementById('cards-container');
            
            // إظهار قسم النتائج
            resultsSection.style.display = 'block';
            
            // مسح المحتوى القديم
            cardsContainer.innerHTML = '';
            
            // إضافة البطاقات المصفاة
            if (cards.length === 0) {
                cardsContainer.innerHTML = '<div class="card-item">No cards match your filters</div>';
            } else {
                cards.forEach(card => {
                    const cardItem = document.createElement('div');
                    cardItem.className = 'card-item';
                    
                    const cardNumber = document.createElement('div');
                    cardNumber.className = 'card-number';
                    cardNumber.textContent = card.full_data.split('|')[0];
                    
                    const cardDetails = document.createElement('div');
                    cardDetails.className = 'card-details';
                    
                    let detailsText = '';
                    if (card.details) {
                        detailsText = `${card.details[1] || ''} • ${card.details[2] || ''} • ${card.details[4] || ''} • ${card.details[8] || ''}`;
                    }
                    cardDetails.textContent = detailsText;
                    
                    cardItem.appendChild(cardNumber);
                    cardItem.appendChild(cardDetails);
                    cardsContainer.appendChild(cardItem);
                });
            }
            
            // التمرير إلى قسم النتائج
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        // إعادة ضبط الفلاتر
        function resetFilters() {
            // إلغاء تحديد جميع checkboxes
            document.querySelectorAll('.ios-checkbox').forEach(checkbox => {
                checkbox.checked = false;
            });
            
            // إعادة تعيين نوع البطاقة إلى "الكل"
            document.querySelectorAll('.card-type-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.dataset.type === 'all') {
                    btn.classList.add('active');
                }
            });
            
            // إخفاء قسم النتائج
            document.getElementById('results-section').style.display = 'none';
        }
        
        // تهيئة التطبيق عند تحميل الصفحة
        document.addEventListener('DOMContentLoaded', initializeUI);
    </script>
</body>
</html>
"""

@app.route('/webapp')
def webapp():
    # الحصول على بيانات البطاقات من الطلب
    cards_data = request.args.get('cards', '[]')
    countries = request.args.get('countries', '[]')
    banks = request.args.get('banks', '[]')
    
    # تحويل البيانات من JSON strings إلى كائنات Python
    import json
    cards_data = json.loads(cards_data)
    countries = json.loads(countries)
    banks = json.loads(banks)
    
    # تقديم القالب مع البيانات
    return render_template_string(HTML_TEMPLATE, cards_data=cards_data, countries=countries, banks=banks)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
