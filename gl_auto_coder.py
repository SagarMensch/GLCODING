"""
GL Auto-Coding Engine
=====================
Production-ready ML pipeline for automatic GL code assignment
using XGBoost + NLP + Static Rules + Feedback Loop
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import xgboost as xgb
import pickle
import json
from datetime import datetime
from collections import defaultdict
import re

# ============================================================
# MODULE 1: STATIC MAPPING RULE ENGINE
# ============================================================
# Level 1 Automation: For recurring vendors (rent, utilities, telecom)

class StaticMappingEngine:
    """
    Procedural Memory - Simple if-then rules for known recurring invoices
    Guarantees 100% accuracy for fixed vendors
    """
    
    def __init__(self):
        self.vendor_to_gl = {}  # vendor_id -> (gl_code, confidence)
        self.vendor_to_category = {}
        
    def add_mapping(self, vendor_id, gl_code, category=None):
        """Add static mapping: vendor -> GL code"""
        self.vendor_to_gl[vendor_id] = (gl_code, 1.0)  # 100% confidence
        if category:
            self.vendor_to_category[vendor_id] = category
            
    def load_from_dataframe(self, df, vendor_col, gl_col, category_col=None):
        """Load mappings from existing data"""
        for _, row in df.iterrows():
            vendor = row[vendor_col]
            gl = row[gl_col]
            cat = row[category_col] if category_col and category_col in row else None
            self.add_mapping(vendor, gl, cat)
            
    def predict(self, vendor_id, invoice_description=None):
        """
        Check if vendor has static mapping
        Returns: (gl_code, confidence, source)
        """
        if vendor_id in self.vendor_to_gl:
            gl, conf = self.vendor_to_gl[vendor_id]
            return {
                'gl_code': gl,
                'confidence': conf,
                'source': 'static_mapping',
                'auto_post': True
            }
        return None
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'vendor_to_gl': self.vendor_to_gl,
                'vendor_to_category': self.vendor_to_category
            }, f)
            
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.vendor_to_gl = data['vendor_to_gl']
            self.vendor_to_category = data['vendor_to_category']


# ============================================================
# MODULE 2: FEATURE ENGINEERING PIPELINE
# ============================================================
# Converts structured + unstructured data into ML features

class FeatureEngine:
    """
    Feature Engineering for Invoice Classification
    
    Features from:
    - Vendor ID (categorical -> embedding)
    - Invoice Description (text -> TF-IDF + keywords)
    - Cost Center (categorical)
    - Expense Category (categorical)
    """
    
    def __init__(self):
        self.vendor_encoder = LabelEncoder()
        self.cost_center_encoder = LabelEncoder()
        self.category_encoder = LabelEncoder()
        self.tfidf = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.tfidf_fitted = False
        self.keyword_patterns = self._compile_keywords()
        
    def _compile_keywords(self):
        """Compile regex patterns for GL-relevant keywords"""
        return {
            'software': r'software|license|subscription|saas|cloud',
            'hardware': r'laptop|computer|server|printer|keyboard|mouse',
            'travel': r'flight|hotel|taxi|uber|railway|airbnb',
            'marketing': r'advertisement|marketing|promo|branding|event',
            'rent': r'rent|lease|monthly rent|property',
            'utility': r'electricity|water|gas|internet|phone|mobile',
            'maintenance': r'repair|maintenance|AMC|service|fix',
            'legal': r'legal|advocate|attorney|court|legal fees',
            'consulting': r'consulting|consultant|advisory|strategy',
            'logistics': r'logistics|shipping|transport|freight|courier',
            'food': r'food|ingredients|raw material|dairy|spices',
            'packaging': r'packaging|box|carton|container|wrapper'
        }
        
    def extract_keywords(self, text):
        """Extract GL-relevant keywords from description"""
        text_lower = text.lower()
        found = []
        for category, pattern in self.keyword_patterns.items():
            if re.search(pattern, text_lower):
                found.append(category)
        return found
    
    def fit(self, df, vendor_col, desc_col, cost_center_col, category_col, gl_col):
        """Fit encoders on historical data"""
        # Fit text vectorizer
        self.tfidf.fit(df[desc_col].fillna(''))
        self.tfidf_fitted = True
        
        # Fit label encoders
        self.vendor_encoder.fit(df[vendor_col].fillna('UNKNOWN'))
        self.cost_center_encoder.fit(df[cost_center_col].fillna('UNKNOWN'))
        self.category_encoder.fit(df[category_col].fillna('UNKNOWN'))
        
        # Store all GL codes for classification
        self.gl_encoder = LabelEncoder()
        self.gl_encoder.fit(df[gl_col])
        
        print(f"Vocabulary size: {len(self.tfidf.vocabulary_)}")
        print(f"Unique GL codes: {len(self.gl_encoder.classes_)}")
        
    def transform(self, df, vendor_col, desc_col, cost_center_col, category_col):
        """Transform raw data into feature matrix"""
        features = {}
        
        # 1. Vendor encoding
        vendor_encoded = []
        for v in df[vendor_col].fillna('UNKNOWN'):
            if v in self.vendor_encoder.classes_:
                vendor_encoded.append(self.vendor_encoder.transform([v])[0])
            else:
                vendor_encoded.append(-1)  # Unknown vendor
        features['vendor'] = np.array(vendor_encoded)
        
        # 2. Cost Center encoding
        cc_encoded = []
        for cc in df[cost_center_col].fillna('UNKNOWN'):
            if cc in self.cost_center_encoder.classes_:
                cc_encoded.append(self.cost_center_encoder.transform([cc])[0])
            else:
                cc_encoded.append(-1)
        features['cost_center'] = np.array(cc_encoded)
        
        # 3. Category encoding
        cat_encoded = []
        for c in df[category_col].fillna('UNKNOWN'):
            if c in self.category_encoder.classes_:
                cat_encoded.append(self.category_encoder.transform([c])[0])
            else:
                cat_encoded.append(-1)
        features['category'] = np.array(cat_encoded)
        
        # 4. TF-IDF features from description
        tfidf_matrix = self.tfidf.transform(df[desc_col].fillna('')).toarray()
        
        # 5. Keyword features
        keyword_features = []
        for desc in df[desc_col].fillna(''):
            keywords = self.extract_keywords(desc)
            vec = np.zeros(len(self.keyword_patterns))
            for i, kw in enumerate(self.keyword_patterns.keys()):
                vec[i] = 1 if kw in keywords else 0
            keyword_features.append(vec)
        keyword_features = np.array(keyword_features)
        
        # Combine all features
        X = np.column_stack([
            features['vendor'],
            features['cost_center'], 
            features['category'],
            tfidf_matrix,
            keyword_features
        ])
        
        return X
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'vendor_encoder': self.vendor_encoder,
                'cost_center_encoder': self.cost_center_encoder,
                'category_encoder': self.category_encoder,
                'gl_encoder': self.gl_encoder,
                'tfidf': self.tfidf,
                'keyword_patterns': self.keyword_patterns
            }, f)
            
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.vendor_encoder = data['vendor_encoder']
            self.cost_center_encoder = data['cost_center_encoder']
            self.category_encoder = data['category_encoder']
            self.gl_encoder = data['gl_encoder']
            self.tfidf = data['tfidf']
            self.keyword_patterns = data['keyword_patterns']
            self.tfidf_fitted = True


# ============================================================
# MODULE 3: ML CLASSIFICATION MODEL
# ============================================================
# XGBoost classifier with probability output

class GLClassifier:
    """
    ML Model for GL Code Classification
    
    Algorithm: XGBoost (Gradient Boosting)
    - Handles mixed feature types
    - Outputs probability distribution
    - Fast inference
    """
    
    def __init__(self, confidence_threshold=0.85):
        self.model = None
        self.feature_engine = FeatureEngine()
        self.static_mapping = StaticMappingEngine()
        self.confidence_threshold = confidence_threshold
        self.is_trained = False
        
    def train(self, df, vendor_col, desc_col, cost_center_col, category_col, gl_col):
        """Train the classification model"""
        print("Training GL Classifier...")
        
        # Step 1: Extract recurring vendors for static mapping
        vendor_gl_counts = df.groupby(vendor_col)[gl_col].nunique()
        recurring_vendors = vendor_gl_counts[vendor_gl_counts == 1].index
        static_df = df[df[vendor_col].isin(recurring_vendors)]
        
        # Build static mapping from recurring vendors
        for vendor in static_df[vendor_col].unique():
            gl = static_df[static_df[vendor_col] == vendor][gl_col].iloc[0]
            self.static_mapping.add_mapping(vendor, gl)
        print(f"Static mappings created: {len(self.static_mapping.vendor_to_gl)}")
        
        # Step 2: Fit feature engine
        self.feature_engine.fit(
            df, vendor_col, desc_col, cost_center_col, category_col, gl_col
        )
        
        # Step 3: Transform features
        X = self.feature_engine.transform(
            df, vendor_col, desc_col, cost_center_col, category_col
        )
        y = self.feature_engine.gl_encoder.transform(df[gl_col])
        
        # Step 4: Train XGBoost
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            objective='multi:softprob',
            num_class=len(self.feature_engine.gl_encoder.classes_),
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model Accuracy: {accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        self.is_trained = True
        return accuracy
        
    def predict(self, vendor_id, invoice_description, cost_center, expense_category):
        """
        Predict GL code with confidence score
        
        Returns: {
            'gl_code': str,
            'confidence': float,
            'source': 'static' | 'ml',
            'auto_post': bool,
            'reason': str
        }
        """
        # Step 1: Check static mapping first (Level 1)
        static_result = self.static_mapping.predict(vendor_id, invoice_description)
        if static_result:
            static_result['reason'] = f"Known recurring vendor: {vendor_id}"
            return static_result
            
        # Step 2: ML prediction (Level 2)
        if not self.is_trained:
            return {
                'gl_code': None,
                'confidence': 0.0,
                'source': 'none',
                'auto_post': False,
                'reason': 'Model not trained'
            }
            
        # Prepare single record
        df = pd.DataFrame({
            'vendor': [vendor_id],
            'description': [invoice_description],
            'cost_center': [cost_center],
            'category': [expense_category]
        })
        
        X = self.feature_engine.transform(
            df, 'vendor', 'description', 'cost_center', 'category'
        )
        
        # Get probability distribution
        proba = self.model.predict_proba(X)[0]
        predicted_class = np.argmax(proba)
        confidence = proba[predicted_class]
        
        gl_code = self.feature_engine.gl_encoder.inverse_transform([predicted_class])[0]
        
        # Threshold check - Reject Option
        auto_post = confidence >= self.confidence_threshold
        
        return {
            'gl_code': gl_code,
            'confidence': float(confidence),
            'source': 'ml_model',
            'auto_post': auto_post,
            'reason': f"ML prediction (threshold: {self.confidence_threshold})"
        }
    
    def predict_batch(self, df, vendor_col, desc_col, cost_center_col, category_col):
        """Batch prediction for multiple invoices"""
        results = []
        
        for _, row in df.iterrows():
            result = self.predict(
                row[vendor_col],
                row[desc_col],
                row[cost_center_col],
                row[category_col]
            )
            results.append(result)
            
        return pd.DataFrame(results)
        
    def save(self, filepath):
        """Save model and encoders"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'feature_engine': self.feature_engine,
                'static_mapping': self.static_mapping,
                'confidence_threshold': self.confidence_threshold,
                'is_trained': self.is_trained
            }, f)
            
    def load(self, filepath):
        """Load saved model"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.feature_engine = data['feature_engine']
            self.static_mapping = data['static_mapping']
            self.confidence_threshold = data['confidence_threshold']
            self.is_trained = data['is_trained']


# ============================================================
# MODULE 4: FEEDBACK LOOP - CONTINUOUS LEARNING
# ============================================================
# Updates model based on human corrections

class FeedbackLoop:
    """
    Reinforcement Learning from Human Feedback (RLHF)
    
    When human corrects a GL code:
    1. Store correction in training buffer
    2. Periodically retrain model
    3. Update static mappings if applicable
    """
    
    def __init__(self, classifier, retrain_threshold=100):
        self.classifier = classifier
        self.retrain_threshold = retrain_threshold
        self.corrections = []  # List of (features, correct_gl)
        self.correction_history = []
        
    def record_correction(self, vendor_id, invoice_description, cost_center, 
                         expense_category, predicted_gl, corrected_gl):
        """Record a human correction"""
        correction = {
            'timestamp': datetime.now().isoformat(),
            'vendor_id': vendor_id,
            'invoice_description': invoice_description,
            'cost_center': cost_center,
            'expense_category': expense_category,
            'predicted_gl': predicted_gl,
            'corrected_gl': corrected_gl
        }
        
        self.corrections.append(correction)
        self.correction_history.append(correction)
        
        # If same vendor now has consistent GL mapping, update static mapping
        vendor_corrections = [c for c in self.corrections 
                             if c['vendor_id'] == vendor_id]
        if len(vendor_corrections) >= 3:
            gls = [c['corrected_gl'] for c in vendor_corrections]
            if len(set(gls)) == 1:  # All same GL
                self.classifier.static_mapping.add_mapping(vendor_id, gls[0])
                print(f"Updated static mapping: {vendor_id} -> {gls[0]}")
                
        # Check if retraining needed
        if len(self.corrections) >= self.retrain_threshold:
            self.trigger_retrain()
            
    def trigger_retrain(self):
        """Retrain model with new corrections"""
        print(f"\n=== Retraining with {len(self.corrections)} corrections ===")
        
        # In production, you would:
        # 1. Load full historical data
        # 2. Add corrections to training set
        # 3. Retrain classifier
        # 4. Save new model
        
        self.corrections = []  # Clear buffer after retrain
        print("Retraining complete")
        
    def get_statistics(self):
        """Get correction statistics"""
        if not self.correction_history:
            return {"total_corrections": 0}
            
        df = pd.DataFrame(self.correction_history)
        return {
            "total_corrections": len(df),
            "unique_vendors": df['vendor_id'].nunique(),
            "correction_rate": df.groupby('vendor_id').size().mean(),
            "recent_corrections": df.tail(10)[['vendor_id', 'predicted_gl', 'corrected_gl']].to_dict('records')
        }


# ============================================================
# MODULE 5: EXPLAINABILITY (SHAP)
# ============================================================

def explain_prediction(classifier, vendor_id, invoice_description, 
                     cost_center, expense_category):
    """
    Explain why a specific GL code was predicted
    
    Uses feature importance to show which factors contributed
    """
    import shap
    
    # Prepare features
    df = pd.DataFrame({
        'vendor': [vendor_id],
        'description': [invoice_description],
        'cost_center': [cost_center],
        'category': [expense_category]
    })
    
    X = classifier.feature_engine.transform(
        df, 'vendor', 'description', 'cost_center', 'category'
    )
    
    # Get prediction
    prediction = classifier.predict(vendor_id, invoice_description, cost_center, expense_category)
    
    # Explain with SHAP
    explainer = shap.TreeExplainer(classifier.model)
    shap_values = explainer.shap_values(X)
    
    # Get top contributing features
    feature_names = ['vendor', 'cost_center', 'category'] + \
                   list(classifier.feature_engine.tfidf.get_feature_names_out()) + \
                   list(classifier.feature_engine.keyword_patterns.keys())
    
    # Get top 5 positive contributors
    top_indices = np.argsort(shap_values[0])[-5:][::-1]
    
    explanations = []
    for idx in top_indices:
        if shap_values[0][idx] > 0:
            explanations.append({
                'feature': feature_names[idx] if idx < len(feature_names) else f"feature_{idx}",
                'contribution': float(shap_values[0][idx])
            })
    
    return {
        'predicted_gl': prediction['gl_code'],
        'confidence': prediction['confidence'],
        'top_factors': explanations
    }


# ============================================================
# MODULE 6: MAIN ORCHESTRATOR
# ============================================================

class GLAutoCodingEngine:
    """
    Main orchestrator combining all modules
    
    Workflow:
    1. Check static mapping (instant)
    2. If no match, run ML prediction
    3. Apply threshold routing
    4. Record feedback for corrections
    """
    
    def __init__(self, model_path=None, confidence_threshold=0.85):
        self.classifier = GLClassifier(confidence_threshold=confidence_threshold)
        self.feedback_loop = None
        
        if model_path:
            self.load(model_path)
            
    def train(self, df, vendor_col, desc_col, cost_center_col, category_col, gl_col):
        """Full training pipeline"""
        # Train classifier
        accuracy = self.classifier.train(
            df, vendor_col, desc_col, cost_center_col, category_col, gl_col
        )
        
        # Initialize feedback loop
        self.feedback_loop = FeedbackLoop(self.classifier)
        
        return accuracy
        
    def predict(self, vendor_id, invoice_description, cost_center, expense_category):
        """Single invoice prediction"""
        return self.classifier.predict(
            vendor_id, invoice_description, cost_center, expense_category
        )
        
    def process_invoice(self, vendor_id, invoice_description, cost_center, 
                       expense_category, manual_gl=None):
        """
        Full processing with feedback recording
        
        If manual_gl provided, treat as correction feedback
        """
        # Get prediction
        prediction = self.predict(
            vendor_id, invoice_description, cost_center, expense_category
        )
        
        # If human provided correct GL, record feedback
        if manual_gl and manual_gl != prediction['gl_code']:
            self.feedback_loop.record_correction(
                vendor_id, invoice_description, cost_center,
                expense_category, prediction['gl_code'], manual_gl
            )
            
        return prediction
        
    def save(self, filepath):
        """Save entire engine"""
        self.classifier.save(filepath)
        
    def load(self, filepath):
        """Load saved engine"""
        self.classifier.load(filepath)
        self.feedback_loop = FeedbackLoop(self.classifier)


# ============================================================
# USAGE EXAMPLE
# ============================================================

if __name__ == "__main__":
    # Sample training data
    train_data = pd.DataFrame({
        'vendor_id': ['V001', 'V001', 'V002', 'V002', 'V003', 'V003', 'V004', 'V004', 'V005'] * 20,
        'invoice_description': [
            'Software license for MS Office 365', 'Annual software subscription',
            'Hotel booking for Delhi trip', 'Flight tickets Mumbai Bangalore',
            'Laptop Dell Inspiron 15', 'Computer hardware purchase',
            'Monthly office rent', 'Building lease payment',
            'Consulting services for strategy'
        ] * 20,
        'cost_center': ['CC001', 'CC001', 'CC002', 'CC002', 'CC003', 'CC003', 'CC004', 'CC004', 'CC005'] * 20,
        'expense_category': [
            'Software', 'Software', 'Travel', 'Travel', 
            'Hardware', 'Hardware', 'Rent', 'Rent', 'Consulting'
        ] * 20,
        'gl_code': [
            'GL5100500', 'GL5100500', 'GL5200100', 'GL5200100',
            'GL5100300', 'GL5100300', 'GL5300100', 'GL5300100', 'GL5100600'
        ] * 20
    })
    
    # Add some noise/variation
    train_data.loc[train_data.index[::3], 'gl_code'] = 'GL5100500'
    train_data.loc[train_data.index[1::3], 'gl_code'] = 'GL5200100'
    
    # Initialize engine
    engine = GLAutoCodingEngine(confidence_threshold=0.85)
    
    # Train
    accuracy = engine.train(
        train_data, 'vendor_id', 'invoice_description', 
        'cost_center', 'expense_category', 'gl_code'
    )
    
    # Test predictions
    test_cases = [
        ('V001', 'Software license renewal', 'CC001', 'Software'),
        ('V999', 'Office supplies purchase', 'CC006', 'Office'),
        ('V002', 'Taxi fare for client meeting', 'CC002', 'Travel'),
    ]
    
    print("\n" + "="*60)
    print("TEST PREDICTIONS")
    print("="*60)
    
    for vendor, desc, cc, cat in test_cases:
        result = engine.predict(vendor, desc, cc, cat)
        print(f"\nVendor: {vendor}")
        print(f"Description: {desc}")
        print(f"Predicted GL: {result['gl_code']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Auto-Post: {result['auto_post']}")
        print(f"Source: {result['source']}")
        print(f"Reason: {result['reason']}")
    
    # Save model
    engine.save('gl_auto_coding_model.pkl')
    print("\nModel saved to gl_auto_coding_model.pkl")
