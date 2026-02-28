"""
GL Auto-Coding Engine - Using Scikit-Learn
==========================================
Production-ready ML pipeline for automatic GL code assignment
Using RandomForest + TF-IDF + Static Rules + Feedback Loop
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import pickle
import json
from datetime import datetime
import re

MISTRAL_API_KEY = "zuq8I57aSASX5O066kZbjMsCPHWzkb2u"

# ============================================================
# MODULE 1: STATIC MAPPING RULE ENGINE
# ============================================================

class StaticMappingEngine:
    """
    Procedural Memory - if-then rules for known recurring invoices
    100% accuracy for fixed vendors (rent, utilities, telecom)
    """
    
    def __init__(self):
        self.vendor_to_gl = {}
        self.vendor_category = {}
        
    def add_mapping(self, vendor_id, gl_code, category=None):
        self.vendor_to_gl[vendor_id] = (gl_code, 1.0)
        if category:
            self.vendor_category[vendor_id] = category
            
    def load_from_dataframe(self, df, vendor_col, gl_col, category_col=None):
        for _, row in df.iterrows():
            vendor = str(row[vendor_col])
            gl = str(row[gl_col])
            cat = str(row[category_col]) if category_col and category_col in df.columns else None
            if vendor not in self.vendor_to_gl:
                self.add_mapping(vendor, gl, cat)
                
    def predict(self, vendor_id):
        vendor_id = str(vendor_id)
        if vendor_id in self.vendor_to_gl:
            gl, conf = self.vendor_to_gl[vendor_id]
            return {'gl_code': gl, 'confidence': conf, 'source': 'static', 'auto_post': True}
        return None
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({'vendor_to_gl': self.vendor_to_gl, 'vendor_category': self.vendor_category}, f)
            
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.vendor_to_gl = data['vendor_to_gl']
            self.vendor_category = data.get('vendor_category', {})


# ============================================================
# MODULE 2: FEATURE ENGINEERING
# ============================================================

class FeatureEngine:
    """
    Converts: Vendor ID + Invoice Description + Cost Center + Category
    Into: Numerical feature matrix for ML
    """
    
    def __init__(self):
        self.vendor_encoder = LabelEncoder()
        self.cc_encoder = LabelEncoder()
        self.cat_encoder = LabelEncoder()
        self.gl_encoder = LabelEncoder()
        self.tfidf = TfidfVectorizer(max_features=300, ngram_range=(1,2), stop_words='english')
        self.tfidf_fitted = False
        self.keywords = {
            'software': r'software|license|subscription|saas|cloud|adobe|microsoft',
            'hardware': r'laptop|computer|server|printer|keyboard|mouse|monitor',
            'travel': r'flight|hotel|taxi|uber|railway|airbnb|travel|boarding',
            'marketing': r'advertisement|marketing|promo|branding|event|exhibition',
            'rent': r'rent|lease|property|monthly rent|building',
            'utility': r'electricity|water|gas|internet|phone|mobile|bill',
            'maintenance': r'repair|maintenance|amc|service|fix|installation',
            'legal': r'legal|advocate|attorney|court|legal fees|consultation',
            'consulting': r'consulting|consultant|advisory|strategy|audit',
            'logistics': r'logistics|shipping|transport|freight|courier|delivery',
            'food': r'food|ingredients|raw material|dairy|spices|vegetables',
            'packaging': r'packaging|box|carton|container|wrapper|paper',
            'labor': r'labor|wages|staff|manpower|contractor',
            'security': r'security|guard|safety|cctv',
            'cleaning': r'cleaning|housekeeping|janitor|pest control'
        }
        
    def _extract_keywords(self, text):
        text = str(text).lower()
        found = []
        for kw, pattern in self.keywords.items():
            if re.search(pattern, text):
                found.append(kw)
        return found
    
    def fit(self, df, vendor_col, desc_col, cc_col, cat_col, gl_col):
        self.tfidf.fit(df[desc_col].fillna('').astype(str))
        self.tfidf_fitted = True
        
        self.vendor_encoder.fit(df[vendor_col].fillna('UNK').astype(str))
        self.cc_encoder.fit(df[cc_col].fillna('UNK').astype(str))
        self.cat_encoder.fit(df[cat_col].fillna('UNK').astype(str))
        self.gl_encoder.fit(df[gl_col].fillna('UNK').astype(str))
        
        print(f"TF-IDF vocab: {len(self.tfidf.vocabulary_)}")
        print(f"GL codes: {len(self.gl_encoder.classes_)}")
        
    def transform(self, df, vendor_col, desc_col, cc_col, cat_col):
        vendor_enc = self._encode(self.vendor_encoder, df[vendor_col], 'vendor')
        cc_enc = self._encode(self.cc_encoder, df[cc_col], 'cost_center')
        cat_enc = self._encode(self.cat_encoder, df[cat_col], 'category')
        
        tfidf_mat = self.tfidf.transform(df[desc_col].fillna('').astype(str)).toarray()
        
        kw_features = []
        for desc in df[desc_col].fillna(''):
            vec = np.zeros(len(self.keywords))
            found = self._extract_keywords(desc)
            for i, kw in enumerate(self.keywords.keys()):
                vec[i] = 1 if kw in found else 0
            kw_features.append(vec)
        kw_features = np.array(kw_features)
        
        X = np.column_stack([vendor_enc, cc_enc, cat_enc, tfidf_mat, kw_features])
        return X
    
    def _encode(self, encoder, series, name):
        result = []
        for val in series.fillna('UNK').astype(str):
            if val in encoder.classes_:
                result.append(encoder.transform([val])[0])
            else:
                result.append(-1)
        return np.array(result)
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'vendor_encoder': self.vendor_encoder,
                'cc_encoder': self.cc_encoder,
                'cat_encoder': self.cat_encoder,
                'gl_encoder': self.gl_encoder,
                'tfidf': self.tfidf,
                'keywords': self.keywords
            }, f)
    
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.vendor_encoder = data['vendor_encoder']
            self.cc_encoder = data['cc_encoder']
            self.cat_encoder = data['cat_encoder']
            self.gl_encoder = data['gl_encoder']
            self.tfidf = data['tfidf']
            self.keywords = data['keywords']
            self.tfidf_fitted = True


# ============================================================
# MODULE 3: ML CLASSIFIER
# ============================================================

class GLClassifier:
    """
    ML Model: RandomForest for GL Classification
    Outputs probability distribution -> confidence score
    """
    
    def __init__(self, confidence_threshold=0.85):
        self.model = None
        self.feature_engine = FeatureEngine()
        self.static_mapping = StaticMappingEngine()
        self.confidence_threshold = confidence_threshold
        self.is_trained = False
        
    def train(self, df, vendor_col, desc_col, cc_col, cat_col, gl_col):
        print("=== Training GL Classifier ===")
        
        vendor_gl_counts = df.groupby(vendor_col)[gl_col].nunique()
        recurring = vendor_gl_counts[vendor_gl_counts == 1].index
        static_df = df[df[vendor_col].isin(recurring)]
        
        for vendor in static_df[vendor_col].unique():
            gl = static_df[static_df[vendor_col] == vendor][gl_col].iloc[0]
            self.static_mapping.add_mapping(vendor, gl)
        print(f"Static mappings: {len(self.static_mapping.vendor_to_gl)}")
        
        self.feature_engine.fit(df, vendor_col, desc_col, cc_col, cat_col, gl_col)
        
        X = self.feature_engine.transform(df, vendor_col, desc_col, cc_col, cat_col)
        y = self.feature_engine.gl_encoder.transform(df[gl_col].astype(str))
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy:.2%}")
        
        self.is_trained = True
        return accuracy
    
    def predict(self, vendor_id, description, cc, category):
        static = self.static_mapping.predict(vendor_id)
        if static:
            static['reason'] = f"Static mapping for vendor {vendor_id}"
            return static
        
        if not self.is_trained:
            return {'gl_code': None, 'confidence': 0, 'source': 'none', 'auto_post': False, 'reason': 'Not trained'}
        
        df = pd.DataFrame({
            'vendor': [str(vendor_id)],
            'desc': [str(description)],
            'cc': [str(cc)],
            'cat': [str(category)]
        })
        
        X = self.feature_engine.transform(df, 'vendor', 'desc', 'cc', 'cat')
        proba = self.model.predict_proba(X)[0]
        
        pred_idx = np.argmax(proba)
        confidence = proba[pred_idx]
        
        gl = self.feature_engine.gl_encoder.inverse_transform([pred_idx])[0]
        auto_post = confidence >= self.confidence_threshold
        
        return {
            'gl_code': gl,
            'confidence': float(confidence),
            'source': 'ml',
            'auto_post': auto_post,
            'reason': f"ML (threshold: {self.confidence_threshold})"
        }
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_engine': self.feature_engine,
                'static_mapping': self.static_mapping,
                'confidence_threshold': self.confidence_threshold,
                'is_trained': self.is_trained
            }, f)
    
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.feature_engine = data['feature_engine']
            self.static_mapping = data['static_mapping']
            self.confidence_threshold = data['confidence_threshold']
            self.is_trained = data['is_trained']


# ============================================================
# MODULE 4: FEEDBACK LOOP
# ============================================================

class FeedbackLoop:
    """
    Records human corrections -> triggers retraining
    """
    
    def __init__(self, classifier, retrain_threshold=100):
        self.classifier = classifier
        self.corrections = []
        self.retrain_threshold = retrain_threshold
        
    def record(self, vendor_id, description, cc, category, predicted, corrected):
        correction = {
            'timestamp': datetime.now().isoformat(),
            'vendor': str(vendor_id),
            'desc': str(description),
            'cc': str(cc),
            'cat': str(category),
            'predicted': str(predicted),
            'corrected': str(corrected)
        }
        self.corrections.append(correction)
        
        vendor_corr = [c for c in self.corrections if c['vendor'] == str(vendor_id)]
        if len(vendor_corr) >= 3:
            gls = [c['corrected'] for c in vendor_corr]
            if len(set(gls)) == 1:
                self.classifier.static_mapping.add_mapping(vendor_id, gls[0])
                print(f"[Feedback] New static mapping: {vendor_id} -> {gls[0]}")
        
        if len(self.corrections) >= self.retrain_threshold:
            print(f"[Feedback] {self.retrain_threshold} corrections - trigger retrain")
            self.corrections = []
    
    def stats(self):
        return {
            'total': len(self.corrections),
            'vendors': len(set(c['vendor'] for c in self.corrections))
        }


# ============================================================
# MODULE 5: MISTRAL LLM ENHANCEMENT
# ============================================================

class LLMEnhancer:
    """
    Uses Mistral LLM for complex cases where ML confidence is low
    """
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = "https://api.mistral.ai/v1/chat/completions"
        
    def explain_and_suggest(self, vendor_id, description, cc, category, ml_prediction):
        prompt = f"""You are a GL code classification assistant for a finance team.

Invoice Details:
- Vendor ID: {vendor_id}
- Description: {description}
- Cost Center: {cc}
- Category: {category}

ML Model Prediction: {ml_prediction['gl_code']} (confidence: {ml_prediction['confidence']:.2%})

If confidence is low, analyze the description and suggest the correct GL code from these categories:
- Software/IT: GL5100500
- Hardware: GL5100300
- Travel: GL5200100
- Rent: GL5300100
- Utilities: GL5300200
- Marketing: GL5200200
- Maintenance: GL5100400
- Legal: GL5100600
- Consulting: GL5100700
- Logistics: GL5100800

Respond in format:
GL_CODE: <code>
REASON: <2-3 sentence explanation>
"""
        
        import requests
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200
        }
        
        try:
            resp = requests.post(self.endpoint, headers=headers, json=data, timeout=30)
            if resp.status_code == 200:
                result = resp.json()
                content = result['choices'][0]['message']['content']
                
                gl_code = None
                reason = ""
                for line in content.split('\n'):
                    if line.startswith('GL_CODE:'):
                        gl_code = line.replace('GL_CODE:', '').strip()
                    elif line.startswith('REASON:'):
                        reason = line.replace('REASON:', '').strip()
                
                return {'gl_code': gl_code, 'reason': reason, 'llm_used': True}
        except Exception as e:
            print(f"LLM error: {e}")
        
        return {'llm_used': False}


# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

class GLAutoCodingEngine:
    """
    Main pipeline:
    1. Static mapping check (instant)
    2. ML prediction
    3. Confidence threshold
    4. LLM for edge cases
    5. Feedback recording
    """
    
    def __init__(self, model_path=None, confidence_threshold=0.85, use_llm=True):
        self.classifier = GLClassifier(confidence_threshold)
        self.feedback = None
        self.llm = LLMEnhancer(MISTRAL_API_KEY) if use_llm else None
        
        if model_path:
            self.load(model_path)
            
    def train(self, df, vendor_col, desc_col, cc_col, cat_col, gl_col):
        acc = self.classifier.train(df, vendor_col, desc_col, cc_col, cat_col, gl_col)
        self.feedback = FeedbackLoop(self.classifier)
        return acc
    
    def predict(self, vendor_id, description, cc, category):
        result = self.classifier.predict(vendor_id, description, cc, category)
        
        if not result['auto_post'] and self.llm and result['confidence'] < 0.95:
            llm_result = self.llm.explain_and_suggest(
                vendor_id, description, cc, category, result
            )
            if llm_result.get('llm_used'):
                result['llm_suggestion'] = llm_result['gl_code']
                result['llm_reason'] = llm_result.get('reason', '')
        
        return result
    
    def process(self, vendor_id, description, cc, category, manual_gl=None):
        result = self.predict(vendor_id, description, cc, category)
        
        if manual_gl and manual_gl != result.get('gl_code'):
            self.feedback.record(vendor_id, description, cc, category, 
                               result.get('gl_code'), manual_gl)
        
        return result
    
    def save(self, filepath):
        self.classifier.save(filepath)
    
    def load(self, filepath):
        self.classifier.load(filepath)
        self.feedback = FeedbackLoop(self.classifier)


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    # Sample training data - 150 records
    records = []
    
    # Software vendors
    for i in range(30):
        records.append({
            'vendor_id': 'V001' if i < 15 else 'V002',
            'description': 'Software Microsoft 365 subscription' if i % 3 == 0 else 'Adobe license renewal annual' if i % 3 == 1 else 'Cloud AWS hosting charges',
            'cost_center': 'CC001',
            'category': 'IT',
            'gl_code': 'GL5100500'
        })
    
    # Travel vendors
    for i in range(30):
        records.append({
            'vendor_id': 'V003' if i < 10 else 'V004',
            'description': 'Hotel Taj Delhi booking' if i % 3 == 0 else 'Flight Indigo Mumbai Bangalore' if i % 3 == 1 else 'Uber taxi client meeting',
            'cost_center': 'CC002',
            'category': 'Travel',
            'gl_code': 'GL5200100'
        })
    
    # Hardware vendors
    for i in range(30):
        records.append({
            'vendor_id': 'V005' if i < 15 else 'V006',
            'description': 'Dell laptop purchase' if i % 3 == 0 else 'HP printer office use' if i % 3 == 1 else 'Server hardware upgrade',
            'cost_center': 'CC001',
            'category': 'Hardware',
            'gl_code': 'GL5100300'
        })
    
    # Rent vendors
    for i in range(30):
        records.append({
            'vendor_id': 'V007' if i < 15 else 'V008',
            'description': 'Monthly office rent' if i % 3 == 0 else 'Building lease payment' if i % 3 == 1 else 'Property rent monthly',
            'cost_center': 'CC003',
            'category': 'Rent',
            'gl_code': 'GL5300100'
        })
    
    # Utilities vendors
    for i in range(30):
        records.append({
            'vendor_id': 'V009' if i < 15 else 'V010',
            'description': 'Electricity bill payment' if i % 3 == 0 else 'Water supply charges' if i % 3 == 1 else 'Internet broadband monthly',
            'cost_center': 'CC004',
            'category': 'Utilities',
            'gl_code': 'GL5300200'
        })
    
    df = pd.DataFrame(records)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print("=== GL Auto-Coding Engine Demo ===\n")
    
    engine = GLAutoCodingEngine(confidence_threshold=0.80)
    
    accuracy = engine.train(df, 'vendor_id', 'description', 'cost_center', 'category', 'gl_code')
    
    print("\n" + "="*50)
    print("TEST PREDICTIONS")
    print("="*50)
    
    tests = [
        ('V001', 'Microsoft Office 365 renewal', 'CC001', 'IT'),
        ('V002', 'Hotel stay Bangalore client', 'CC002', 'Travel'),
        ('V999', 'Unknown vendor new invoice', 'CC003', 'Office'),
        ('V003', 'Server purchase for data center', 'CC001', 'Hardware'),
        ('V004', 'Monthly electricity bill', 'CC002', 'Utilities'),
    ]
    
    for vendor, desc, cc, cat in tests:
        result = engine.predict(vendor, desc, cc, cat)
        print(f"\nVendor: {vendor}")
        print(f"  Description: {desc}")
        print(f"  GL Code: {result['gl_code']}")
        print(f"  Confidence: {result['confidence']:.1%}")
        print(f"  Auto-Post: {result['auto_post']}")
        print(f"  Source: {result['source']}")
        if 'llm_suggestion' in result:
            print(f"  LLM Suggestion: {result['llm_suggestion']}")
    
    engine.save('gl_model.pkl')
    print("\n\nModel saved to gl_model.pkl")
    print("\n=== COMPLETE ===")
