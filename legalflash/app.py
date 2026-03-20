import streamlit as st
import openai
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="LegalFlash - AI Legal Documents",
    page_icon="⚖️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0a0a0a;
    }
    .stApp {
        background: linear-gradient(180deg, #0f0f0f 0%, #0a0a0a 100%);
    }
    .title {
        font-size: 3em !important;
        font-weight: bold;
        color: #22c55e !important;
    }
    .subtitle {
        color: #666;
        font-size: 1.2em;
    }
    .feature-card {
        background: #1a1a1a;
        padding: 1.5em;
        border-radius: 12px;
        border: 1px solid #333;
    }
    .feature-title {
        color: #22c55e;
        font-size: 1.2em;
        font-weight: bold;
    }
    .success-box {
        background: #1a2d1a;
        border: 1px solid #2d5a2d;
        padding: 1.5em;
        border-radius: 8px;
        color: #4ade80;
    }
    .doc-box {
        background: #1a1a1a;
        border: 1px solid #333;
        padding: 1.5em;
        border-radius: 8px;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .price-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        border: 2px solid #22c55e;
        border-radius: 16px;
        padding: 2em;
        text-align: center;
    }
    .price {
        font-size: 3em;
        font-weight: bold;
        color: #22c55e;
    }
    .price-period {
        color: #666;
        font-size: 1em;
    }
</style>
""", unsafe_allow_html=True)

# OpenAI client
def get_openai_client():
    if hasattr(st, 'secrets'):
        try:
            api_key = st.secrets.get('OPENAI_API_KEY')
            if api_key:
                return openai.OpenAI(api_key=api_key)
        except:
            pass
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return openai.OpenAI(api_key=api_key)
    return None

# Sidebar
with st.sidebar:
    st.title("⚖️ LegalFlash")
    st.markdown("---")
    
    page = st.radio("Navigate", [
        "🏠 Home",
        "📄 Privacy Policy",
        "📄 Terms of Service", 
        "📄 Cookie Policy",
        "💰 Pricing"
    ])

    st.markdown("---")
    st.markdown("### Why LegalFlash?")
    st.info("Generate GDPR-compliant legal documents in seconds. Save €500+ vs lawyers.")

# Home Page
if page == "🏠 Home":
    st.markdown('<p class="title">⚖️ LegalFlash</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Legal Documents for Your Website</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📄 Privacy Policy</div>
            GDPR & CCPA compliant privacy policies for your website or app.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📄 Terms of Service</div>
            Comprehensive ToS protecting your business and users.
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🍪 Cookie Policy</div>
            GDPR-compliant cookie consent and policy generation.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 How It Works")
    st.write("1. **Select** the document type you need")
    st.write("2. **Answer** a few simple questions about your business")
    st.write("3. **Download** your custom legal document instantly")
    
    st.markdown("---")
    st.markdown("### 💰 Pricing")
    st.write("• **Free:** 1 document")
    st.write("• **Pro (€19/mo):** Unlimited documents")
    st.write("• **Business (€49/mo):** Priority support + custom branding")
    
    st.markdown("---")
    if st.button("Get Started - Generate Free Privacy Policy", use_container_width=True):
        st.switch_page("📄 Privacy Policy")

# Privacy Policy Generator
elif page == "📄 Privacy Policy":
    st.title("📄 Privacy Policy Generator")
    st.markdown("Generate a GDPR & CCPA compliant Privacy Policy in seconds")
    
    with st.form("privacy_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            website_url = st.text_input("Website URL", placeholder="https://example.com")
            contact_email = st.text_input("Contact Email")
        with col2:
            business_type = st.selectbox("Business Type", ["Website", "Web App", "Mobile App", "E-commerce", "SaaS"])
            data_collected = st.multiselect("Data You Collect", 
                ["Email addresses", "Names", "Phone numbers", "Payment info", "IP addresses", 
                 "Cookies", "Location data", "Device info", "Social media profiles"])
        
        serves_eu = st.checkbox("Do you serve EU customers? (GDPR)")
        serves_us = st.checkbox("Do you serve US customers? (CCPA)")
        
        generate_btn = st.form_submit_button("⚡ Generate Privacy Policy", use_container_width=True)
    
    if generate_btn and company_name and contact_email:
        client = get_openai_client()
        if client:
            with st.spinner("Generating your Privacy Policy..."):
                prompt = f"""Generate a professional, GDPR and {'CCPA ' if serves_us else ''}compliant Privacy Policy for {company_name} ({website_url}).

Company type: {business_type}
Data collected: {', '.join(data_collected) if data_collected else 'Basic usage data'}
Contact email: {contact_email}
{'Serves EU customers - include GDPR requirements' if serves_eu else ''}
{'Serves US customers - include CCPA requirements' if serves_us else ''}

Include these sections:
1. Introduction
2. Data We Collect
3. How We Use Data
4. Data Sharing & Third Parties
5. Cookies
6. Data Retention
7. User Rights (GDPR/CCPA)
8. Security
9. Children
10. Changes to Policy
11. Contact Information

Write in professional legal language but make it accessible. Include effective date at top."""
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=3000
                    )
                    privacy_policy = response.choices[0].message.content
                    
                    st.markdown('<div class="success-box">✅ Privacy Policy Generated!</div>', unsafe_allow_html=True)
                    
                    st.markdown("### 📄 Your Privacy Policy")
                    st.markdown(f'<div class="doc-box">{privacy_policy}</div>', unsafe_allow_html=True)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download as Text",
                        data=privacy_policy,
                        file_name="privacy_policy.txt",
                        mime="text/plain"
                    )
                    
                    st.markdown("---")
                    st.info("💡 Tip: Have a lawyer review this document before using it commercially.")
                    
                except Exception as e:
                    st.error(f"Error generating: {str(e)}")
        else:
            st.error("OpenAI API key not configured")
    elif generate_btn:
        st.warning("Please fill in Company Name and Contact Email")

# Terms of Service
elif page == "📄 Terms of Service":
    st.title("📄 Terms of Service Generator")
    st.markdown("Comprehensive Terms of Service to protect your business")
    
    with st.form("tos_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            website_url = st.text_input("Website URL")
            support_email = st.text_input("Support Email")
        with col2:
            business_type = st.selectbox("Business Type", ["Website", "Web App", "Mobile App", "E-commerce", "SaaS"])
        
        has_accounts = st.checkbox("Users create accounts?", value=True)
        has_payments = st.checkbox("You process payments?")
        has_user_content = st.checkbox("Users can upload content?")
        
        generate_btn = st.form_submit_button("⚡ Generate Terms of Service", use_container_width=True)
    
    if generate_btn and company_name:
        client = get_openai_client()
        if client:
            with st.spinner("Generating your Terms of Service..."):
                prompt = f"""Generate a comprehensive Terms of Service for {company_name} ({website_url}).

Business type: {business_type}
{'Users create accounts on the platform' if has_accounts else ''}
{'Processes payments from users' if has_payments else ''}
{'Users can upload/post content' if has_user_content else ''}

Include these sections:
1. Acceptance of Terms
2. Description of Service
3. User Accounts ({'Required' if has_accounts else 'Not required'})
4. User Conduct
5. Content Ownership
6. Payment Terms ({'Included' if has_payments else 'Not applicable'})
7. Limitation of Liability
8. Disclaimer
9. Indemnification
10. Termination
11. Governing Law
12. Dispute Resolution
13. Changes to Terms
14. Contact Information

Write in clear, professional language."""
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=3000
                    )
                    tos = response.choices[0].message.content
                    
                    st.markdown('<div class="success-box">✅ Terms of Service Generated!</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="doc-box">{tos}</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Download as Text",
                        data=tos,
                        file_name="terms_of_service.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.error("OpenAI API key not configured")
    elif generate_btn:
        st.warning("Please enter Company Name")

# Cookie Policy
elif page == "📄 Cookie Policy":
    st.title("🍪 Cookie Policy Generator")
    st.markdown("GDPR-compliant cookie policy for your website")
    
    with st.form("cookie_form"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            website_url = st.text_input("Website URL")
        with col2:
            cookie_types = st.multiselect("Cookies You Use", 
                ["Essential/Required", "Analytics (Google Analytics)", "Advertising/Ads", 
                 "Functional/Preferences", "Social Media", "Security", "Session"])
        
        has_banner = st.checkbox("You have a cookie consent banner?", value=True)
        
        generate_btn = st.form_submit_button("⚡ Generate Cookie Policy", use_container_width=True)
    
    if generate_btn and company_name:
        client = get_openai_client()
        if client:
            with st.spinner("Generating Cookie Policy..."):
                prompt = f"""Generate a GDPR-compliant Cookie Policy for {company_name} ({website_url}).

Cookie types used: {', '.join(cookie_types) if cookie_types else 'Essential cookies'}
{'Has cookie consent banner' if has_banner else 'No consent banner yet - recommend adding one'}

Include:
1. What are cookies
2. Types of cookies we use (detailed table)
3. How we use cookies
4. Third-party cookies
5. Cookie management (how users can disable)
6. Updates to policy
7. Contact info

Make it practical and GDPR-aligned."""
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=2000
                    )
                    cookie_policy = response.choices[0].message.content
                    
                    st.markdown('<div class="success-box">✅ Cookie Policy Generated!</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="doc-box">{cookie_policy}</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Download as Text",
                        data=cookie_policy,
                        file_name="cookie_policy.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.error("OpenAI API key not configured")
    elif generate_btn:
        st.warning("Please enter Company Name")

# Pricing Page
elif page == "💰 Pricing":
    st.title("💰 Pricing")
    st.markdown("Choose the plan that works for you")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="price-card">
            <h2>Free</h2>
            <p class="price">€0</p>
            <p class="price-period">forever</p>
            <hr>
            <p>1 legal document</p>
            <p>Basic templates</p>
            <p>Personal use only</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Get Started", key="free")
    
    with col2:
        st.markdown("""
        <div class="price-card" style="border-color: #22c55e;">
            <h2>Pro</h2>
            <p class="price">€19</p>
            <p class="price-period">per month</p>
            <hr>
            <p>Unlimited documents</p>
            <p>All document types</p>
            <p>Auto-updates when laws change</p>
            <p>Commercial license</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Go Pro", key="pro")
    
    with col3:
        st.markdown("""
        <div class="price-card">
            <h2>Business</h2>
            <p class="price">€49</p>
            <p class="price-period">per month</p>
            <hr>
            <p>Everything in Pro</p>
            <p>Priority processing</p>
            <p>Custom branding</p>
            <p> Lawyer review add-on</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("Contact Sales", key="biz")
    
    st.markdown("---")
    st.markdown("### 💳 Payment")
    st.info("Stripe integration coming soon! Contact us to get early access.")
