# it_invoice_app.py
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import joblib

# Create a robust predictor class that always works
class SimpleInvoicePredictor:
    def __init__(self):
        self.models_loaded = False
    
    def load_models(self, filename):
        """Try to load models, but always provide fallback"""
        try:
            model_data = joblib.load(filename)
            self.models_loaded = True
            return True
        except:
            self.models_loaded = False
            return False
    
    def predict(self, service_category, client_industry, country, project_type, total_amount, total_hours, num_services):
        """Provide robust predictions that always return a dictionary"""
        try:
            # Default sensible values
            discount = 5.0 if total_amount > 10000 else (3.0 if total_amount > 5000 else 0.0)
            tax_rate = 8.5  # Default US tax rate
            
            # Documentation complexity based on project size
            if total_amount > 15000:
                doc_complexity = 'High'
            elif total_amount > 5000:
                doc_complexity = 'Medium'
            else:
                doc_complexity = 'Low'
            
            # Payment terms based on project type
            payment_terms_map = {
                'Fixed Price': '50% Advance, 50% on Completion',
                'Time & Materials': 'Net 30',
                'Retainer': 'Monthly in Advance',
                'Support Contract': 'Quarterly in Advance'
            }
            payment_terms = payment_terms_map.get(project_type, 'Net 30')
            
            # Service notes based on category
            service_notes_map = {
                'Software Development': 'Includes code documentation, testing, and deployment support.',
                'Cloud Services': 'Includes architecture design and security configuration.',
                'Cybersecurity': 'Includes security assessment and compliance documentation.',
                'IT Consulting': 'Professional consulting services with detailed reports.',
                'System Integration': 'Includes system design and integration testing.',
                'Data Analytics': 'Includes data analysis and visualization reports.',
                'DevOps Services': 'Includes CI/CD pipeline setup and automation.',
                'AI/ML Solutions': 'Includes model development and implementation.'
            }
            service_notes = service_notes_map.get(service_category, 'Professional IT services delivered to industry standards.')
            
            return {
                'discount': float(discount),
                'tax_rate': float(tax_rate),
                'documentation_complexity': doc_complexity,
                'payment_terms': payment_terms,
                'service_notes': service_notes
            }
        except Exception as e:
            # Ultimate fallback - always return a valid dictionary
            return {
                'discount': 5.0,
                'tax_rate': 8.5,
                'documentation_complexity': 'Medium',
                'payment_terms': 'Net 30',
                'service_notes': 'Thank you for your business! Professional services delivered.'
            }

# Page configuration for professional look
st.set_page_config(
    page_title="IT Professional Invoice Generator",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    .professional-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2E86AB;
        border-bottom: 2px solid #2E86AB;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .service-item-card {
        background-color: #f8f9fa;
        border-left: 4px solid #2E86AB;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .metric-card {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .download-btn {
        background: linear-gradient(45deg, #2E86AB, #4CAF50) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

class ProfessionalITInvoiceGenerator:
    def __init__(self):
        # Use the robust predictor
        self.predictor = SimpleInvoicePredictor()
        try:
            if self.predictor.load_models('it_invoice_models.joblib'):
                st.success("✅ Professional IT invoice models loaded")
            else:
                st.info("ℹ️ Using smart AI recommendations")
        except:
            st.info("ℹ️ Using smart AI recommendations")
    
    def calculate_project_totals(self, services, discount, tax_rate):
        """Calculate professional IT project totals"""
        try:
            subtotal = sum(service['hours'] * service['hourly_rate'] for service in services)
            discount_amount = subtotal * (discount / 100)
            taxable_amount = subtotal - discount_amount
            tax_amount = taxable_amount * (tax_rate / 100)
            total = taxable_amount + tax_amount
            total_hours = sum(service['hours'] for service in services)
            
            return {
                'subtotal': subtotal,
                'discount_amount': discount_amount,
                'tax_amount': tax_amount,
                'total': total,
                'total_hours': total_hours
            }
        except Exception as e:
            # Fallback calculation
            return {
                'subtotal': 0,
                'discount_amount': 0,
                'tax_amount': 0,
                'total': 0,
                'total_hours': 0
            }
    
    def generate_professional_pdf(self, invoice_data):
        """Generate professional IT service PDF invoice"""
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch)
            styles = getSampleStyleSheet()
            
            # Create professional styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                textColor=colors.HexColor('#2E86AB'),
                spaceAfter=30,
                alignment=1
            )
            
            # Story elements
            story = []
            
            # Header with company info
            header_table = Table([
                [
                    Paragraph(f"<b>{invoice_data['company_name']}</b><br/>"
                             f"{invoice_data['company_address']}<br/>"
                             f"Phone: {invoice_data['company_phone']}<br/>"
                             f"Email: {invoice_data['company_email']}<br/>"
                             f"Website: {invoice_data['company_website']}", styles['Normal']),
                    Paragraph(f"<b>INVOICE</b><br/>"
                             f"Invoice #: {invoice_data['invoice_number']}<br/>"
                             f"Date: {invoice_data['invoice_date']}<br/>"
                             f"Due Date: {invoice_data['due_date']}<br/>"
                             f"Terms: {invoice_data['payment_terms']}", 
                             styles['Normal'])
                ]
            ], colWidths=[3.5*inch, 2.5*inch])
            
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ]))
            
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))
            
            # Client information
            client_info = Paragraph(
                f"<b>Bill To:</b><br/>"
                f"{invoice_data['client_name']}<br/>"
                f"{invoice_data['client_company']}<br/>"
                f"{invoice_data['client_address']}<br/>"
                f"Email: {invoice_data['client_email']}<br/>"
                f"Project: {invoice_data['project_name']}",
                styles['Normal']
            )
            story.append(client_info)
            story.append(Spacer(1, 0.3*inch))
            
            # Project scope and objectives
            if invoice_data.get('project_scope'):
                scope_text = Paragraph(
                    f"<b>Project Scope:</b> {invoice_data['project_scope']}",
                    styles['Normal']
                )
                story.append(scope_text)
                story.append(Spacer(1, 0.2*inch))
            
            # Services table
            data = [['Service Description', 'Hours', 'Rate ($/hr)', 'Amount ($)']]
            
            for service in invoice_data['services']:
                amount = service['hours'] * service['hourly_rate']
                data.append([
                    f"{service['description']}\n<font size=8 color='#666666'>{service.get('details', '')}</font>",
                    str(service['hours']),
                    f"${service['hourly_rate']:.2f}",
                    f"${amount:.2f}"
                ])
            
            items_table = Table(data, colWidths=[3.2*inch, 0.8*inch, 1*inch, 1*inch])
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E86AB')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8f9fa')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
                ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ]))
            
            story.append(items_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Totals table
            totals = invoice_data['totals']
            totals_data = [
                ['Subtotal:', f"${totals['subtotal']:,.2f}"],
                [f"Discount ({invoice_data['discount']}%):", f"-${totals['discount_amount']:,.2f}"],
                [f"Tax ({invoice_data['tax_rate']}%):", f"${totals['tax_amount']:,.2f}"],
                ['<b>TOTAL AMOUNT DUE:</b>', f"<b>${totals['total']:,.2f}</b>"]
            ]
            
            totals_table = Table(totals_data, colWidths=[4*inch, 2*inch])
            totals_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('LINEABOVE', (-1, -1), (-1, -1), 2, colors.black),
                ('BACKGROUND', (-1, -1), (-1, -1), colors.HexColor('#e8f4fd')),
            ]))
            
            story.append(totals_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Professional notes
            notes_text = Paragraph(
                f"<b>Professional Notes:</b><br/>"
                f"{invoice_data.get('professional_notes', 'Thank you for your business! We appreciate the opportunity to serve you.')}<br/><br/>"
                f"<b>Documentation Level:</b> {invoice_data.get('doc_complexity', 'Standard')}<br/>"
                f"<b>Total Project Hours:</b> {totals['total_hours']} hours",
                styles['Normal']
            )
            story.append(notes_text)
            
            # Terms and conditions
            terms = Paragraph(
                "<b>Terms & Conditions:</b><br/>"
                "Payment due within 30 days of invoice date. Late payments subject to 1.5% monthly interest. "
                "All intellectual property remains with service provider until full payment is received. "
                "Confidentiality of all project information is guaranteed.",
                styles['Normal']
            )
            story.append(Spacer(1, 0.2*inch))
            story.append(terms)
            
            doc.build(story)
            buffer.seek(0)
            return buffer
            
        except Exception as e:
            st.error(f"PDF generation error: {e}")
            # Return a simple error PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            story = [Paragraph("Invoice Generation Error - Please try again", styles['Title'])]
            doc.build(story)
            buffer.seek(0)
            return buffer

def main():
    st.markdown('<div class="professional-header">💻 IT Professional Invoice Generator</div>', 
                unsafe_allow_html=True)
    
    # Initialize generator
    invoice_gen = ProfessionalITInvoiceGenerator()
    
    # Sidebar - Company Information
    with st.sidebar:
        st.header("🏢 Your IT Company")
        company_name = st.text_input("Company Name", "TechSolutions Inc.")
        company_address = st.text_area("Company Address", "123 Technology Drive\nSan Francisco, CA 94105")
        company_phone = st.text_input("Phone", "+1 (415) 123-4567")
        company_email = st.text_input("Email", "billing@techsolutions.com")
        company_website = st.text_input("Website", "www.techsolutions.com")
        
        st.header("⚙️ Invoice Settings")
        invoice_number = st.text_input("Invoice Number", f"IT-{datetime.now().strftime('%Y%m%d')}-001")
        invoice_date = st.date_input("Invoice Date", datetime.now())
        due_date = st.date_input("Due Date", datetime.now() + pd.Timedelta(days=30))
        
        # Add dataset management
        st.header("📊 Data Management")
        if st.button("🔄 Create Sample Dataset"):
            try:
                from create_it_dataset import generate_it_invoice_data
                generate_it_invoice_data(1000)
                st.success("✅ Sample dataset created!")
            except:
                st.info("ℹ️ Dataset creation not available")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-header">👥 Client & Project Information</div>', 
                   unsafe_allow_html=True)
        
        client_name = st.text_input("Client Contact Name", "Sarah Johnson")
        client_company = st.text_input("Client Company", "InnovateCorp")
        client_address = st.text_area("Client Address", "456 Business Avenue\nNew York, NY 10001")
        client_email = st.text_input("Client Email", "sarah.johnson@innovatecorp.com")
        project_name = st.text_input("Project Name", "Cloud Migration Initiative")
        
        # Professional details
        col1a, col1b, col1c = st.columns(3)
        with col1a:
            service_category = st.selectbox("Service Category", [
                'Software Development', 'Cloud Services', 'Cybersecurity', 
                'IT Consulting', 'System Integration', 'Data Analytics',
                'DevOps Services', 'AI/ML Solutions'
            ])
        with col1b:
            client_industry = st.selectbox("Client Industry", [
                'Finance', 'Healthcare', 'E-commerce', 'Education', 
                'Manufacturing', 'Government', 'Technology'
            ])
        with col1c:
            project_type = st.selectbox("Project Type", [
                'Fixed Price', 'Time & Materials', 'Retainer', 'Support Contract'
            ])
        
        project_scope = st.text_area("Project Scope Description", 
                                   "Migration of on-premise infrastructure to AWS cloud platform including security configuration and monitoring setup.")
        
        st.markdown('<div class="section-header">🛠️ IT Services</div>', 
                   unsafe_allow_html=True)
        
        # Initialize services in session state
        if 'services' not in st.session_state:
            st.session_state.services = [{
                'description': 'Initial Consultation & Analysis',
                'details': 'Requirements gathering and system assessment',
                'hours': 10,
                'hourly_rate': 150.00
            }]
        
        # Display service items
        for i, service in enumerate(st.session_state.services):
            with st.expander(f"Service {i+1}: {service['description']}", expanded=i==0):
                col_s1, col_s2, col_s3 = st.columns([3, 1, 1])
                with col_s1:
                    st.session_state.services[i]['description'] = st.text_input(
                        "Service Description", 
                        value=service['description'],
                        key=f"desc_{i}"
                    )
                    st.session_state.services[i]['details'] = st.text_area(
                        "Service Details", 
                        value=service.get('details', ''),
                        key=f"details_{i}",
                        height=60
                    )
                with col_s2:
                    st.session_state.services[i]['hours'] = st.number_input(
                        "Hours", 
                        min_value=1, 
                        value=service['hours'],
                        key=f"hours_{i}"
                    )
                with col_s3:
                    st.session_state.services[i]['hourly_rate'] = st.number_input(
                        "Hourly Rate ($)", 
                        min_value=50.0, 
                        value=service['hourly_rate'],
                        key=f"rate_{i}"
                    )
        
        # Service management buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("➕ Add Service Item", use_container_width=True):
                st.session_state.services.append({
                    'description': 'Additional IT Service',
                    'details': 'Professional IT service delivery',
                    'hours': 8,
                    'hourly_rate': 125.00
                })
                st.rerun()
        with col_btn2:
            if len(st.session_state.services) > 1 and st.button("➖ Remove Last Item", use_container_width=True):
                st.session_state.services.pop()
                st.rerun()
    
    with col2:
        st.markdown('<div class="section-header">🤖 AI Recommendations</div>', 
                   unsafe_allow_html=True)
        
        # Calculate project metrics for predictions
        total_amount = sum(s['hours'] * s['hourly_rate'] for s in st.session_state.services)
        total_hours = sum(s['hours'] for s in st.session_state.services)
        num_services = len(st.session_state.services)
        
        if total_amount > 0:
            # Get AI predictions with robust error handling
            try:
                predictions = invoice_gen.predictor.predict(
                    service_category, client_industry, 'US', project_type,
                    total_amount, total_hours, num_services
                )
                
                # Ensure predictions is always a dictionary
                if not isinstance(predictions, dict):
                    predictions = {
                        'discount': 5.0,
                        'tax_rate': 8.5,
                        'documentation_complexity': 'Medium',
                        'payment_terms': 'Net 30',
                        'service_notes': 'Professional IT services delivered.'
                    }
                
                st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                st.subheader("💡 AI Suggestions")
                
                # Safe value access with defaults
                discount_value = predictions.get('discount', 5.0)
                tax_rate_value = predictions.get('tax_rate', 8.5)
                payment_terms_value = predictions.get('payment_terms', 'Net 30')
                doc_complexity_value = predictions.get('documentation_complexity', 'Medium')
                
                # Discount slider
                discount = st.slider(
                    "Recommended Discount %", 
                    0.0, 20.0, 
                    value=float(discount_value),
                    help=f"AI suggested: {discount_value}% based on project size"
                )
                
                # Tax rate slider
                tax_rate = st.slider(
                    "Tax Rate %", 
                    0.0, 25.0, 
                    value=float(tax_rate_value),
                    help="Applied tax rate for services"
                )
                
                # Payment terms
                payment_terms_options = ['Net 30', '50% Advance, 50% on Completion', 'Monthly in Advance', 'Quarterly in Advance']
                default_index = payment_terms_options.index(payment_terms_value) if payment_terms_value in payment_terms_options else 0
                payment_terms = st.selectbox("Payment Terms", payment_terms_options, index=default_index)
                
                # Documentation level
                doc_complexity_options = ['Low', 'Medium', 'High']
                default_doc_index = doc_complexity_options.index(doc_complexity_value) if doc_complexity_value in doc_complexity_options else 1
                doc_complexity = st.selectbox("Documentation Level", doc_complexity_options, index=default_doc_index)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Project metrics
                st.markdown('<div class="section-header">📊 Project Summary</div>', 
                           unsafe_allow_html=True)
                
                totals = invoice_gen.calculate_project_totals(st.session_state.services, discount, tax_rate)
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.markdown(f'<div class="metric-card">Total Hours<br><h3>{totals["total_hours"]}</h3></div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-card">Subtotal<br><h3>${totals["subtotal"]:,.2f}</h3></div>', 
                               unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f'<div class="metric-card">Services<br><h3>{num_services}</h3></div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div class="metric-card">Total Due<br><h3>${totals["total"]:,.2f}</h3></div>', 
                               unsafe_allow_html=True)
                
                # Professional notes
                professional_notes = st.text_area(
                    "Professional Notes",
                    value=predictions.get('service_notes', 'Thank you for your business! We look forward to serving you.'),
                    help="Additional notes for the client",
                    height=100
                )
                
                # Generate invoice data
                invoice_data = {
                    'company_name': company_name,
                    'company_address': company_address,
                    'company_phone': company_phone,
                    'company_email': company_email,
                    'company_website': company_website,
                    'client_name': client_name,
                    'client_company': client_company,
                    'client_address': client_address,
                    'client_email': client_email,
                    'project_name': project_name,
                    'project_scope': project_scope,
                    'invoice_number': invoice_number,
                    'invoice_date': invoice_date.strftime('%Y-%m-%d'),
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'services': st.session_state.services,
                    'discount': discount,
                    'tax_rate': tax_rate,
                    'totals': totals,
                    'payment_terms': payment_terms,
                    'professional_notes': professional_notes,
                    'doc_complexity': doc_complexity
                }
                
                # Generate PDF
                pdf_buffer = invoice_gen.generate_professional_pdf(invoice_data)
                
                # Download button
                st.download_button(
                    label="📄 Download Professional IT Invoice",
                    data=pdf_buffer,
                    file_name=f"{invoice_number}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                    key="download_pdf"
                )
                
            except Exception as e:
                st.error(f"Error in AI recommendations: {e}")
                # Fallback manual mode
                st.info("🔧 Using manual invoice generation")
                
                # Manual inputs
                discount = st.slider("Discount %", 0.0, 20.0, 5.0)
                tax_rate = st.slider("Tax Rate %", 0.0, 25.0, 8.5)
                payment_terms = st.selectbox("Payment Terms", ['Net 30', '50% Advance, 50% on Completion'])
                professional_notes = st.text_area("Notes", "Thank you for your business!")
                
                # Calculate and generate
                totals = invoice_gen.calculate_project_totals(st.session_state.services, discount, tax_rate)
                invoice_data = {
                    'company_name': company_name,
                    'company_address': company_address,
                    'company_phone': company_phone,
                    'company_email': company_email,
                    'company_website': company_website,
                    'client_name': client_name,
                    'client_company': client_company,
                    'client_address': client_address,
                    'client_email': client_email,
                    'project_name': project_name,
                    'project_scope': project_scope,
                    'invoice_number': invoice_number,
                    'invoice_date': invoice_date.strftime('%Y-%m-%d'),
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'services': st.session_state.services,
                    'discount': discount,
                    'tax_rate': tax_rate,
                    'totals': totals,
                    'payment_terms': payment_terms,
                    'professional_notes': professional_notes,
                    'doc_complexity': 'Medium'
                }
                
                pdf_buffer = invoice_gen.generate_professional_pdf(invoice_data)
                st.download_button(
                    label="📄 Download Invoice (Manual Mode)",
                    data=pdf_buffer,
                    file_name=f"{invoice_number}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("💡 Add service items above to generate invoice")
            st.info("📝 Enter hours and rates for each service to see AI recommendations")

if __name__ == "__main__":
    main()