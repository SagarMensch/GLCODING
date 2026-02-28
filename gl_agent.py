"""
GL Auto-Coding Engine - Agentic AI Architecture
================================================
Using: Embeddings + RAG + ML + LLM
No regex - pure semantic AI
"""

import os
import json
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any

# Supabase
from supabase import create_client, Client

# ML/AI
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# LLM
import requests

# ============================================================
# CONFIGURATION
# ============================================================

MISTRAL_API_KEY = "zuo8I57aSASX5O066kZbjMsCPHWzkb2u"

SUPABASE_URL = "https://ysrsniznvwionmzcrzeh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InlzcnNuaXpudndpb25temNyemVoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3OTk1NjcsImV4cCI6MjA4NzM3NTU2N30.e8MRaKHJALMnXOHToWsvc2KojqrFIIz6pQ_YxP6rXLQ"
POSTGRES_PASSWORD = "Messiejfnvjrbgbndfg"

# ============================================================
# MODULE 1: SEMANTIC EMBEDDINGS (RAG)
# ============================================================

class SemanticSearchEngine:
    """
    Uses semantic embeddings instead of regex for keyword matching
    RAG-based approach for understanding invoice descriptions
    """
    
    def __init__(self):
        self.embeddings = {}
        self.gl_categories = {}
        self.dimension = 384  # Default for sentence-transformers
        
    def initialize_categories(self):
        """Initialize GL categories with semantic descriptions"""
        self.gl_categories = {
            'GL5100500': {
                'name': 'Software/IT Expenses',
                'description': 'Software licenses, subscriptions, cloud services, IT support, SaaS products, technology costs',
                'examples': ['microsoft office', 'adobe license', 'aws hosting', 'software subscription', 'cloud services']
            },
            'GL5200100': {
                'name': 'Travel Expenses', 
                'description': 'Travel bookings, hotels, flights, taxi, uber, railway, boarding, lodging',
                'examples': ['hotel booking', 'flight ticket', 'taxi fare', 'uber ride', 'railway ticket']
            },
            'GL5100300': {
                'name': 'Hardware Expenses',
                'description': 'Computer hardware, laptops, servers, printers, keyboards, monitors, IT equipment',
                'examples': ['laptop purchase', 'server hardware', 'printer', 'computer', 'monitor']
            },
            'GL5300100': {
                'name': 'Rent Expenses',
                'description': 'Office rent, building lease, property rental, monthly rent payments',
                'examples': ['office rent', 'building lease', 'property rent', 'monthly rent']
            },
            'GL5300200': {
                'name': 'Utility Expenses',
                'description': 'Electricity, water, gas, internet, phone bills, utility payments',
                'examples': ['electricity bill', 'water charges', 'internet broadband', 'phone bill']
            },
            'GL5200200': {
                'name': 'Marketing Expenses',
                'description': 'Advertising, promotions, branding, marketing campaigns, event sponsorship',
                'examples': ['advertisement', 'marketing campaign', 'event sponsorship', 'brand promotion']
            },
            'GL5100400': {
                'name': 'Maintenance Expenses',
                'description': 'Equipment repair, AMC, service contracts, maintenance work, installation',
                'examples': ['repair service', 'maintenance AMC', 'equipment service', 'installation']
            },
            'GL5100600': {
                'name': 'Legal Expenses',
                'description': 'Legal services, advocate fees, attorney, legal consultation, court matters',
                'examples': ['legal fees', 'advocate charges', 'legal consultation', 'attorney fees']
            },
            'GL5100700': {
                'name': 'Consulting Expenses',
                'description': 'Consulting services, management advisory, strategy consulting, audit services',
                'examples': ['consulting services', 'management advisory', 'strategy consulting', 'audit']
            },
            'GL5100800': {
                'name': 'Logistics Expenses',
                'description': 'Shipping, freight, courier, transport, logistics services, delivery charges',
                'examples': ['shipping charges', 'courier service', 'freight charges', 'transport']
            }
        }
        
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding for text using sentence-transformers
        Falls back to simple hash-based embedding if not available
        """
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = model.encode([text])[0]
            return embedding
        except ImportError:
            # Fallback: simple hash-based pseudo-embedding
            return self._pseudo_embedding(text)
            
    def _pseudo_embedding(self, text: str) -> np.ndarray:
        """Simple hash-based embedding as fallback"""
        text = text.lower()
        vec = np.zeros(384)
        for i, char in enumerate(text):
            vec[i % 384] += ord(char) * (i + 1)
        vec = vec / (np.linalg.norm(vec) + 1e-8)
        return vec
        
    def build_index(self, historical_data: pd.DataFrame):
        """Build embedding index from historical data"""
        print("Building semantic index...")
        self.initialize_categories()
        
        # Build embeddings for GL categories
        for gl_code, info in self.gl_categories.items():
            # Use description + examples for rich embedding
            combined_text = f"{info['description']} {' '.join(info['examples'])}"
            self.embeddings[gl_code] = self.get_embedding(combined_text)
            
        print(f"Built semantic index for {len(self.gl_categories)} GL codes")
        
    def find_similar_gl(self, description: str, top_k: int = 3) -> List[Dict]:
        """Find similar GL codes using semantic search"""
        query_embedding = self.get_embedding(description)
        
        similarities = []
        for gl_code, gl_embedding in self.embeddings.items():
            # Cosine similarity
            sim = np.dot(query_embedding, gl_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(gl_embedding) + 1e-8
            )
            similarities.append({
                'gl_code': gl_code,
                'name': self.gl_categories[gl_code]['name'],
                'similarity': float(sim),
                'description': self.gl_categories[gl_code]['description']
            })
        
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        return similarities[:top_k]


# ============================================================
# MODULE 2: STATIC MAPPING (RECURRING VENDORS)
# ============================================================

class StaticMappingEngine:
    """Static mapping for recurring vendors - no ML needed"""
    
    def __init__(self, supabase_client: Client = None):
        self.vendor_gl_map = {}
        self.supabase = supabase_client
        
    def load_from_database(self):
        """Load static mappings from Supabase"""
        if self.supabase:
            try:
                response = self.supabase.table('vendor_gl_mapping').select('*').execute()
                for row in response.data:
                    self.vendor_gl_map[row['vendor_id']] = {
                        'gl_code': row['gl_code'],
                        'confidence': 1.0,
                        'category': row.get('category', '')
                    }
                print(f"Loaded {len(self.vendor_gl_map)} static mappings from database")
            except Exception as e:
                print(f"Could not load from database: {e}")
                
    def add_mapping(self, vendor_id: str, gl_code: str, category: str = ''):
        self.vendor_gl_map[vendor_id] = {
            'gl_code': gl_code,
            'confidence': 1.0,
            'category': category
        }
        
    def predict(self, vendor_id: str) -> Optional[Dict]:
        vendor_id = str(vendor_id).upper()
        if vendor_id in self.vendor_gl_map:
            return {
                'gl_code': self.vendor_gl_map[vendor_id]['gl_code'],
                'confidence': self.vendor_gl_map[vendor_id]['confidence'],
                'source': 'static_mapping',
                'auto_post': True,
                'reason': f'Known recurring vendor: {vendor_id}'
            }
        return None
    
    def save_to_database(self):
        """Save mappings to Supabase"""
        if not self.supabase:
            return
            
        for vendor_id, data in self.vendor_gl_map.items():
            self.supabase.table('vendor_gl_mapping').upsert({
                'vendor_id': vendor_id,
                'gl_code': data['gl_code'],
                'category': data.get('category', ''),
                'updated_at': datetime.now().isoformat()
            }).execute()


# ============================================================
# MODULE 3: ML CLASSIFIER (TRAINABLE)
# ============================================================

class MLClassifier:
    """RandomForest classifier for GL prediction"""
    
    def __init__(self):
        self.model = None
        self.vendor_encoder = LabelEncoder()
        self.cc_encoder = LabelEncoder()
        self.cat_encoder = LabelEncoder()
        self.gl_encoder = LabelEncoder()
        self.is_trained = False
        
    def train(self, df: pd.DataFrame, vendor_col, desc_col, cc_col, cat_col, gl_col):
        """Train ML model on historical data"""
        print("Training ML Classifier...")
        
        # Encode categorical features
        all_vendors = df[vendor_col].fillna('UNKNOWN').astype(str).unique()
        all_cc = df[cc_col].fillna('UNKNOWN').astype(str).unique()
        all_cats = df[cat_col].fillna('UNKNOWN').astype(str).unique()
        all_gls = df[gl_col].fillna('UNKNOWN').astype(str).unique()
        
        self.vendor_encoder.fit(list(all_vendors) + ['UNK'])
        self.cc_encoder.fit(list(all_cc) + ['UNK'])
        self.cat_encoder.fit(list(all_cats) + ['UNK'])
        self.gl_encoder.fit(list(all_gls))
        
        # Simple feature matrix (in production, use embeddings)
        def encode_series(encoder, series, default='UNK'):
            return [encoder.transform([str(v) if v in encoder.classes_ else default])[0] 
                    for v in series]
        
        X = np.column_stack([
            encode_series(self.vendor_encoder, df[vendor_col]),
            encode_series(self.cc_encoder, df[cc_col]),
            encode_series(self.cat_encoder, df[cat_col])
        ])
        
        y = self.gl_encoder.transform(df[gl_col].astype(str))
        
        # Train
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"ML Model Accuracy: {accuracy:.2%}")
        
        self.is_trained = True
        return accuracy
    
    def predict(self, vendor_id: str, cost_center: str, category: str) -> Dict:
        if not self.is_trained:
            return {'gl_code': None, 'confidence': 0, 'source': 'ml', 'auto_post': False}
        
        try:
            v_enc = self.vendor_encoder.transform([vendor_id])[0] if vendor_id in self.vendor_encoder.classes_ else -1
            cc_enc = self.cc_encoder.transform([cost_center])[0] if cost_center in self.cc_encoder.classes_ else -1
            cat_enc = self.cat_encoder.transform([category])[0] if category in self.cat_encoder.classes_ else -1
            
            X = np.array([[v_enc, cc_enc, cat_enc]])
            proba = self.model.predict_proba(X)[0]
            
            pred_idx = np.argmax(proba)
            confidence = proba[pred_idx]
            
            gl_code = self.gl_encoder.inverse_transform([pred_idx])[0]
            
            return {
                'gl_code': gl_code,
                'confidence': float(confidence),
                'source': 'ml',
                'auto_post': confidence >= 0.85
            }
        except Exception as e:
            return {'gl_code': None, 'confidence': 0, 'source': 'ml', 'error': str(e)}


# ============================================================
# MODULE 4: LLM REASONING ENGINE
# ============================================================

class LLMReasoningEngine:
    """Mistral LLM for complex reasoning and edge cases"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://api.mistral.ai/v1/chat/completions"
        
    def analyze_invoice(self, vendor_id: str, description: str, cost_center: str, 
                       category: str, ml_prediction: Dict = None, 
                       semantic_results: List[Dict] = None) -> Dict:
        """
        Use LLM to analyze and suggest GL code for complex cases
        """
        
        # Build context
        context = f"""You are a GL code classification expert for a finance team.

Invoice Details:
- Vendor ID: {vendor_id}
- Description: {description}
- Cost Center: {cost_center}
- Category: {category}
"""

        if ml_prediction and ml_prediction.get('confidence', 0) < 0.85:
            context += f"\nML Model Prediction: {ml_prediction.get('gl_code', 'N/A')} (confidence: {ml_prediction.get('confidence', 0):.1%})"

        if semantic_results:
            context += "\nSemantic Search Results (similar GL categories):\n"
            for i, r in enumerate(semantic_results[:3], 1):
                context += f"{i}. {r['gl_code']} - {r['name']} (similarity: {r['similarity']:.2%})\n"

        context += """

Based on the invoice description and semantic analysis, determine the correct GL code.

Available GL Codes:
- GL5100500: Software/IT (licenses, subscriptions, cloud)
- GL5200100: Travel (hotels, flights, taxi)
- GL5100300: Hardware (computers, servers, printers)
- GL5300100: Rent (office, building, property)
- GL5300200: Utilities (electricity, water, internet)
- GL5200200: Marketing (ads, promotions, events)
- GL5100400: Maintenance (repairs, AMC, service)
- GL5100600: Legal (advocate, attorney, legal fees)
- GL5100700: Consulting (advisory, strategy, audit)
- GL5100800: Logistics (shipping, freight, courier)

Respond in JSON format:
{
    "gl_code": "GLXXXXXXX",
    "confidence": 0.XX,
    "reasoning": "2-3 sentence explanation"
}
"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "mistral-small-latest",
            "messages": [{"role": "user", "content": context}],
            "response_format": {"type": "json_object"},
            "max_tokens": 300
        }
        
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return json.loads(content)
        except Exception as e:
            print(f"LLM Error: {e}")
            
        return {"gl_code": None, "confidence": 0, "reasoning": "LLM unavailable"}


# ============================================================
# MAIN ORCHESTRATOR
# ============================================================

class GLAutoCodingAgent:
    """
    Agentic AI Orchestrator:
    1. Static Mapping (instant) -> Recurring vendors
    2. Semantic Search (RAG) -> Similar categories  
    3. ML Classifier -> Pattern learning
    4. LLM Reasoning -> Complex cases
    """
    
    def __init__(self, supabase_client: Client = None):
        self.supabase = supabase_client
        self.static_mapping = StaticMappingEngine(supabase_client)
        self.semantic = SemanticSearchEngine()
        self.ml = MLClassifier()
        self.llm = LLMReasoningEngine(MISTRAL_API_KEY)
        self.threshold = 0.85
        
    def initialize(self, historical_data: pd.DataFrame = None):
        """Initialize all components"""
        print("Initializing GL Auto-Coding Agent...")
        
        # Load static mappings
        self.static_mapping.load_from_database()
        
        # Build semantic index
        self.semantic.build_index(historical_data or pd.DataFrame())
        
        print("Agent initialized successfully")
        
    def train(self, df: pd.DataFrame, vendor_col, desc_col, cc_col, cat_col, gl_col):
        """Train the ML component"""
        accuracy = self.ml.train(df, vendor_col, desc_col, cc_col, cat_col, gl_col)
        
        # Extract and save static mappings for recurring vendors
        vendor_gl_counts = df.groupby(vendor_col)[gl_col].nunique()
        recurring = vendor_gl_counts[vendor_gl_counts == 1]
        
        for vendor in recurring.index:
            gl = df[df[vendor_col] == vendor][gl_col].iloc[0]
            cat = df[df[vendor_col] == vendor][cat_col].iloc[0]
            self.static_mapping.add_mapping(str(vendor), str(gl), str(cat))
            
        self.static_mapping.save_to_database()
        return accuracy
        
    def predict(self, vendor_id: str, description: str, cost_center: str, 
                category: str, use_llm: bool = True) -> Dict:
        """
        Full prediction pipeline
        """
        # Step 1: Static mapping (fastest)
        static_result = self.static_mapping.predict(vendor_id)
        if static_result:
            return static_result
            
        # Step 2: Semantic search (RAG)
        semantic_results = self.semantic.find_similar_gl(description)
        
        # Step 3: ML prediction
        ml_result = self.ml.predict(vendor_id, cost_center, category)
        
        # Step 4: Decision based on ML confidence
        if ml_result.get('confidence', 0) >= self.threshold:
            ml_result['semantic_context'] = semantic_results[:2]
            ml_result['reasoning'] = f"ML model confident ({ml_result['confidence']:.1%})"
            return ml_result
            
        # Step 5: LLM for low confidence cases
        if use_llm:
            llm_result = self.llm.analyze_invoice(
                vendor_id, description, cost_center, category,
                ml_result, semantic_results
            )
            
            if llm_result.get('gl_code'):
                return {
                    'gl_code': llm_result['gl_code'],
                    'confidence': llm_result.get('confidence', 0.7),
                    'source': 'llm',
                    'auto_post': llm_result.get('confidence', 0.7) >= self.threshold,
                    'reasoning': llm_result.get('reasoning', ''),
                    'semantic_context': semantic_results[:2],
                    'ml_confidence': ml_result.get('confidence', 0)
                }
        
        # Fallback to ML
        ml_result['semantic_context'] = semantic_results[:2]
        ml_result['reasoning'] = "Low confidence - using ML prediction"
        return ml_result
        
    def process_feedback(self, vendor_id: str, description: str, cost_center: str,
                        category: str, predicted_gl: str, corrected_gl: str):
        """Process human feedback for continuous learning"""
        # Save feedback to database
        if self.supabase:
            self.supabase.table('gl_corrections').insert({
                'vendor_id': vendor_id,
                'description': description,
                'cost_center': cost_center,
                'category': category,
                'predicted_gl': predicted_gl,
                'corrected_gl': corrected_gl,
                'created_at': datetime.now().isoformat()
            }).execute()
            
        # If same vendor corrected multiple times with same GL, update static mapping
        response = self.supabase.table('gl_corrections').select('*').eq('vendor_id', vendor_id).execute()
        if len(response.data) >= 3:
            gls = [r['corrected_gl'] for r in response.data]
            if len(set(gls)) == 1:
                self.static_mapping.add_mapping(vendor_id, gls[0], category)
                self.static_mapping.save_to_database()
                print(f"Updated static mapping for {vendor_id}")


# ============================================================
# DATABASE SETUP
# ============================================================

def setup_database(client: Client):
    """Create tables in Supabase"""
    
    # Vendor to GL mapping
    client.table('vendor_gl_mapping').create(
        Column('vendor_id', 'text', primary_key=True),
        Column('gl_code', 'text'),
        Column('category', 'text'),
        Column('updated_at', 'timestamp')
    ).execute()
    
    # Corrections for feedback loop
    client.table('gl_corrections').create(
        Column('id', 'bigint', identity=True, primary_key=True),
        Column('vendor_id', 'text'),
        Column('description', 'text'),
        Column('cost_center', 'text'),
        Column('category', 'text'),
        Column('predicted_gl', 'text'),
        Column('corrected_gl', 'text'),
        Column('created_at', 'timestamp')
    ).execute()
    
    # Invoice predictions log
    client.table('invoice_predictions').create(
        Column('id', 'bigint', identity=True, primary_key=True),
        Column('vendor_id', 'text'),
        Column('description', 'text'),
        Column('cost_center', 'text'),
        Column('category', 'text'),
        Column('predicted_gl', 'text'),
        Column('confidence', 'float'),
        Column('source', 'text'),
        Column('auto_post', 'bool'),
        Column('created_at', 'timestamp')
    ).execute()
    
    print("Database tables created")


if __name__ == "__main__":
    # Initialize Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Setup database
    try:
        setup_database(supabase)
    except:
        print("Tables may already exist")
    
    # Initialize agent
    agent = GLAutoCodingAgent(supabase)
    agent.initialize()
    
    # Demo predictions
    test_cases = [
        ('V001', 'Microsoft Office 365 subscription', 'CC001', 'IT'),
        ('V002', 'Hotel Taj Delhi booking', 'CC002', 'Travel'),
        ('V999', 'New vendor invoice for consulting services', 'CC003', 'Consulting'),
    ]
    
    print("\n=== DEMO PREDICTIONS ===")
    for vendor, desc, cc, cat in test_cases:
        result = agent.predict(vendor, desc, cc, cat)
        print(f"\nVendor: {vendor}")
        print(f"Description: {desc}")
        print(f"GL Code: {result.get('gl_code')}")
        print(f"Confidence: {result.get('confidence', 0):.1%}")
        print(f"Source: {result.get('source')}")
        print(f"Auto-Post: {result.get('auto_post')}")
