# train_it_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
warnings.filterwarnings('ignore')

class ITInvoicePredictor:
    def __init__(self):
        self.models_loaded = False
        self.dataset_loaded = False
        self.dataset = None
        self.encoders = {}
        
    def load_dataset(self, filename='it_invoice_dataset.csv'):
        """Load the invoice dataset"""
        try:
            self.dataset = pd.read_csv(filename)
            self.dataset_loaded = True
            print(f"✅ Dataset loaded successfully! Shape: {self.dataset.shape}")
            return True
        except FileNotFoundError:
            print("⚠️ Dataset file not found.")
            return False
        except Exception as e:
            print(f"⚠️ Error loading dataset: {e}")
            return False
    
    def prepare_features_for_prediction(self, input_dict):
        """Prepare features for a single prediction"""
        try:
            # Create a DataFrame from the input
            input_df = pd.DataFrame([input_dict])
            
            # Encode categorical variables if encoders are available
            categorical_cols = ['service_category', 'client_industry', 'country', 'project_type']
            
            for col in categorical_cols:
                if col in self.encoders and col in input_df.columns:
                    # Handle unseen categories by using the most common one
                    try:
                        input_df[col] = self.encoders[col].transform([input_dict[col]])[0]
                    except ValueError:
                        # If category not seen during training, use first category
                        input_df[col] = 0
                else:
                    # Default encoding if no encoder available
                    input_df[col] = 0
            
            # Calculate derived features
            input_df['amount_per_hour'] = input_dict['total_amount'] / max(input_dict['total_hours'], 1)
            input_df['is_large_project'] = 1 if input_dict['total_amount'] > 20000 else 0
            input_df['is_enterprise_client'] = 1 if input_dict['client_industry'] in ['Finance', 'Healthcare'] else 0
            
            # Ensure all required columns are present
            required_cols = ['service_category', 'client_industry', 'country', 'project_type', 
                           'total_amount', 'total_hours', 'num_services', 'amount_per_hour', 
                           'is_large_project', 'is_enterprise_client']
            
            for col in required_cols:
                if col not in input_df.columns:
                    input_df[col] = 0
            
            return input_df[required_cols]
            
        except Exception as e:
            print(f"❌ Error preparing features: {e}")
            return None
    
    def train_models(self):
        """Train ML models using the dataset"""
        if not self.load_dataset():
            print("❌ Cannot train models without dataset. Using smart defaults.")
            return False
        
        try:
            # Prepare features
            X = self.dataset.copy()
            
            # Encode categorical variables
            categorical_cols = ['service_category', 'client_industry', 'country', 'project_type']
            for col in categorical_cols:
                self.encoders[col] = LabelEncoder()
                X[col] = self.encoders[col].fit_transform(X[col])
            
            # Feature columns
            feature_cols = categorical_cols + ['total_amount', 'total_hours', 'num_services', 
                                             'amount_per_hour', 'is_large_project', 'is_enterprise_client']
            
            X = X[feature_cols]
            
            # Train models
            self.discount_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
            self.tax_model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=10)
            self.docs_model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=10)
            
            self.discount_model.fit(X, self.dataset['discount'])
            self.tax_model.fit(X, self.dataset['tax_rate'])
            self.docs_model.fit(X, self.dataset['needs_detailed_docs'])
            
            self.models_loaded = True
            print("✅ ML models trained successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error training models: {e}")
            return False
    
    def predict(self, service_category, client_industry, country, project_type, 
                total_amount, total_hours, num_services):
        """Make predictions - FIXED VERSION"""
        try:
            # Always return a dictionary, even if models fail
            if not self.models_loaded:
                # Try to load models first
                if not self.load_models():
                    # If models can't be loaded, use smart defaults
                    return self._get_smart_defaults(service_category, client_industry, project_type, total_amount)
            
            # Prepare input data
            input_dict = {
                'service_category': service_category,
                'client_industry': client_industry,
                'country': country,
                'project_type': project_type,
                'total_amount': total_amount,
                'total_hours': total_hours,
                'num_services': num_services
            }
            
            X_pred = self.prepare_features_for_prediction(input_dict)
            
            if X_pred is not None and self.models_loaded:
                # Use trained models
                discount = float(self.discount_model.predict(X_pred)[0])
                tax_rate = float(self.tax_model.predict(X_pred)[0])
                needs_detailed_docs = int(self.docs_model.predict(X_pred)[0])
                
                # Apply business rules
                discount = max(0, min(20, discount))
                tax_rate = max(0, min(25, tax_rate))
                
                doc_complexity = 'High' if needs_detailed_docs else 'Medium'
                
            else:
                # Fallback to smart defaults
                return self._get_smart_defaults(service_category, client_industry, project_type, total_amount)
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            # Fallback to defaults
            return self._get_smart_defaults(service_category, client_industry, project_type, total_amount)
        
        # Determine outputs
        payment_terms_map = {
            'Fixed Price': '50% Advance, 50% on Completion',
            'Time & Materials': 'Net 30',
            'Retainer': 'Monthly in Advance',
            'Support Contract': 'Quarterly in Advance'
        }
        payment_terms = payment_terms_map.get(project_type, 'Net 30')
        
        service_notes_map = {
            'Software Development': 'Includes code documentation, testing, and deployment support.',
            'Cloud Services': 'Includes architecture design, security configuration, and monitoring.',
            'Cybersecurity': 'Includes security assessment, vulnerability scanning, and compliance reports.',
            'IT Consulting': 'Comprehensive analysis, strategy recommendations, and implementation guidance.'
        }
        service_notes = service_notes_map.get(service_category, 'Professional IT services delivered to industry standards.')
        
        return {
            'discount': round(discount, 2),
            'tax_rate': round(tax_rate, 2),
            'documentation_complexity': doc_complexity,
            'payment_terms': payment_terms,
            'service_notes': service_notes
        }
    
    def _get_smart_defaults(self, service_category, client_industry, project_type, total_amount):
        """Provide reliable smart defaults"""
        # Smart discount calculation
        discount = 0.0
        if total_amount > 20000:
            discount = 10.0
        elif total_amount > 10000:
            discount = 5.0
        elif total_amount > 5000:
            discount = 2.0
        
        # Smart tax rate
        tax_rate = 8.5  # Default US rate
        
        # Documentation complexity
        if total_amount > 15000:
            doc_complexity = 'High'
        elif total_amount > 5000:
            doc_complexity = 'Medium'
        else:
            doc_complexity = 'Low'
        
        # Payment terms
        payment_terms_map = {
            'Fixed Price': '50% Advance, 50% on Completion',
            'Time & Materials': 'Net 30',
            'Retainer': 'Monthly in Advance',
            'Support Contract': 'Quarterly in Advance'
        }
        payment_terms = payment_terms_map.get(project_type, 'Net 30')
        
        # Service notes
        service_notes = f"Professional {service_category} services for {client_industry} sector. Total project value: ${total_amount:,.2f}"
        
        return {
            'discount': discount,
            'tax_rate': tax_rate,
            'documentation_complexity': doc_complexity,
            'payment_terms': payment_terms,
            'service_notes': service_notes
        }
    
    def load_models(self, filename='it_invoice_models.joblib'):
        """Load trained models from file"""
        try:
            model_data = joblib.load(filename)
            self.discount_model = model_data['discount_model']
            self.tax_model = model_data['tax_model']
            self.docs_model = model_data['docs_model']
            self.encoders = model_data.get('encoders', {})
            self.models_loaded = True
            print("✅ ML models loaded successfully!")
            return True
        except FileNotFoundError:
            print("⚠️ Model file not found. Training new models...")
            return self.train_models()
        except Exception as e:
            print(f"⚠️ Error loading models: {e}. Training new models...")
            return self.train_models()
    
    def save_models(self, filename='it_invoice_models.joblib'):
        """Save trained models to file"""
        if not self.models_loaded:
            if not self.train_models():
                print("❌ Cannot save models - training failed")
                return False
        
        try:
            model_data = {
                'discount_model': self.discount_model,
                'tax_model': self.tax_model,
                'docs_model': self.docs_model,
                'encoders': self.encoders
            }
            joblib.dump(model_data, filename)
            print(f"✅ Models saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving models: {e}")
            return False

# Create and save models if run directly
if __name__ == "__main__":
    predictor = ITInvoicePredictor()
    
    # Create dataset if it doesn't exist
    try:
        pd.read_csv('it_invoice_dataset.csv')
        print("✅ Dataset found")
    except FileNotFoundError:
        print("📊 Creating dataset...")
        from create_it_dataset import generate_it_invoice_data
        generate_it_invoice_data(1000)  # Smaller dataset for quick testing
    
    # Train and save models
    if predictor.train_models():
        predictor.save_models()
        print("🎉 ML pipeline completed successfully!")
    else:
        print("⚠️ ML training failed, but smart defaults will work")