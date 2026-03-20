import streamlit as st
import openai
import pandas as pd
import json
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from io import BytesIO

# Page config
st.set_page_config(
    page_title="ChefHelper - AI Kitchen Manager",
    page_icon="🍳",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0f0f0f;
    }
    .stApp {
        background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
    }
    .title {
        font-size: 3em !important;
        font-weight: bold;
        color: #ff6b35 !important;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 2em;
    }
    .feature-card {
        background: #1e1e1e;
        padding: 1.5em;
        border-radius: 12px;
        border: 1px solid #333;
        margin: 0.5em 0;
    }
    .feature-title {
        color: #ff6b35;
        font-size: 1.2em;
        font-weight: bold;
    }
    .success-box {
        background: #1a3d1a;
        border: 1px solid #2d5a2d;
        padding: 1em;
        border-radius: 8px;
        color: #4ade80;
    }
    .warning-box {
        background: #3d2a1a;
        border: 1px solid #5a3d2d;
        padding: 1em;
        border-radius: 8px;
        color: #fbbf24;
    }
    .info-box {
        background: #1a2d3d;
        border: 1px solid #2d3d5a;
        padding: 1em;
        border-radius: 8px;
        color: #60a5fa;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'recipes' not in st.session_state:
    st.session_state.recipes = []
if 'menus' not in st.session_state:
    st.session_state.menus = []
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'haccp_logs' not in st.session_state:
    st.session_state.haccp_logs = []

# OpenAI setup
def get_openai_client():
    api_key = None
    
    # Try Streamlit Cloud secrets
    if hasattr(st, 'secrets'):
        try:
            api_key = st.secrets.get('OPENAI_API_KEY')
        except:
            pass
    
    # Fallback to environment variable
    if not api_key:
        api_key = os.environ.get('OPENAI_API_KEY')
    
    if not api_key:
        st.error("⚠️ OpenAI API key not configured. Add it in Streamlit Cloud secrets.")
        st.info("Get your API key at: https://platform.openai.com/api-keys")
        return None
    return openai.OpenAI(api_key=api_key)

# AI Recipe Generator
def generate_recipe(cuisine, ingredients, dietary, season, difficulty, client):
    prompt = f"""Create a professional recipe with the following details:
- Cuisine: {cuisine}
- Available ingredients: {ingredients}
- Dietary restrictions: {dietary}
- Season: {season}
- Difficulty: {difficulty}

Return a JSON with exactly this structure:
{{
    "name": "Recipe Name",
    "description": "Brief description",
    "prep_time": "X minutes",
    "cook_time": "Y minutes",
    "servings": Z,
    "ingredients": ["item 1", "item 2", ...],
    "instructions": ["step 1", "step 2", ...],
    "tips": ["tip 1", "tip 2"],
    "allergens": ["allergen 1", "allergen 2"],
    "nutrition_per_serving": {{"calories": X, "protein": "Yg", "carbs": "Zg", "fat": "Wg"}}
}}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# PDF Generator
def generate_menu_pdf(menu_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, spaceAfter=30)
    story.append(Paragraph(f"Menu: {menu_data['name']}", title_style))
    story.append(Spacer(1, 20))

    # Items
    for item in menu_data.get('items', []):
        story.append(Paragraph(f"**{item['name']}** - €{item['price']}", styles['Heading3']))
        story.append(Paragraph(item.get('description', ''), styles['BodyText']))
        story.append(Spacer(1, 10))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Sidebar
with st.sidebar:
    st.title("👨‍🍳 ChefHelper")
    st.markdown("---")
    
    page = st.radio("Navigate", [
        "🏠 Home",
        "🍳 AI Recipe Generator", 
        "📋 Menu Builder",
        "📊 Inventory",
        "🛡️ HACCP Logs",
        "⚙️ Settings"
    ])

    st.markdown("---")
    st.markdown("### 💡 Quick Stats")
    st.metric("Recipes", len(st.session_state.recipes))
    st.metric("Menus", len(st.session_state.menus))
    st.metric("Inventory Items", len(st.session_state.inventory))

# Pages
if page == "🏠 Home":
    st.markdown('<p class="title">👨‍🍳 ChefHelper</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Kitchen Management</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🍳 AI Recipes</div>
            Generate recipes with AI based on ingredients, cuisine, and season.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📋 Menu Builder</div>
            Create beautiful menus with pricing and export to PDF.
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Inventory</div>
            Track ingredients, get low-stock alerts.
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🛡️ HACCP</div>
            EU-compliant food safety logs.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.info("Go to **Settings** to configure your OpenAI API key, then start creating recipes!")

elif page == "🍳 AI Recipe Generator":
    st.title("🍳 AI Recipe Generator")
    
    with st.form("recipe_form"):
        col1, col2 = st.columns(2)
        with col1:
            cuisine = st.selectbox("Cuisine", ["Italian", "French", "Japanese", "Mexican", "Indian", "Thai", "American", "Mediterranean", "Asian Fusion", "Other"])
            season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter", "Year-round"])
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Professional"])
        with col2:
            dietary = st.multiselect("Dietary Restrictions", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free", "Low-Carb", "Keto"])
            ingredients = st.text_area("Available Ingredients", placeholder="chicken, garlic, olive oil, tomatoes...")
        
        generate_btn = st.form_submit_button("✨ Generate Recipe", use_container_width=True)
    
    if generate_btn and ingredients:
        client = get_openai_client()
        if client:
            with st.spinner("🤖 AI is cooking up your recipe..."):
                try:
                    recipe = generate_recipe(cuisine, ingredients, ", ".join(dietary), season, difficulty, client)
                    st.session_state.recipes.append(recipe)
                    st.markdown('<div class="success-box">✅ Recipe generated successfully!</div>', unsafe_allow_html=True)
                    
                    # Display recipe
                    st.subheader(recipe['name'])
                    st.markdown(f"*{recipe['description']}*")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Prep Time", recipe['prep_time'])
                    with col2:
                        st.metric("Cook Time", recipe['cook_time'])
                    with col3:
                        st.metric("Servings", recipe['servings'])
                    with col4:
                        st.metric("Calories", recipe['nutrition_per_serving']['calories'])
                    
                    with st.expander("📝 View Full Recipe"):
                        st.write("### Ingredients")
                        for ing in recipe['ingredients']:
                            st.write(f"- {ing}")
                        
                        st.write("### Instructions")
                        for i, inst in enumerate(recipe['instructions'], 1):
                            st.write(f"{i}. {inst}")
                        
                        if recipe.get('tips'):
                            st.write("### Tips")
                            for tip in recipe['tips']:
                                st.write(f"- {tip}")
                        
                        if recipe.get('allergens'):
                            st.warning(f"⚠️ Allergens: {', '.join(recipe['allergens'])}")
                    
                    # Save to session
                    st.session_state.recipes.append(recipe)
                    
                except Exception as e:
                    st.error(f"Error generating recipe: {str(e)}")

    # Show saved recipes
    if st.session_state.recipes:
        st.markdown("---")
        st.subheader("📚 Saved Recipes")
        for i, recipe in enumerate(st.session_state.recipes):
            with st.expander(f"{recipe['name']} - {recipe['servings']} servings"):
                st.json(recipe)

elif page == "📋 Menu Builder":
    st.title("📋 Menu Builder")
    
    # Create new menu
    with st.expander("➕ Create New Menu", expanded=True):
        menu_name = st.text_input("Menu Name")
        menu_description = st.text_area("Menu Description")
        
        if st.session_state.recipes:
            st.write("### Add Items from Recipes")
            selected_recipes = st.multiselect("Select Recipes", [r['name'] for r in st.session_state.recipes])
            
            menu_items = []
            for recipe_name in selected_recipes:
                recipe = next((r for r in st.session_state.recipes if r['name'] == recipe_name), None)
                if recipe:
                    price = st.number_input(f"Price for {recipe_name}", min_value=0.0, value=25.0, step=0.5, key=f"price_{recipe_name}")
                    menu_items.append({
                        'name': recipe['name'],
                        'description': recipe['description'],
                        'price': price,
                        'recipe': recipe
                    })
            
            if st.button("💾 Save Menu"):
                if menu_name:
                    st.session_state.menus.append({
                        'name': menu_name,
                        'description': menu_description,
                        'items': menu_items,
                        'created': datetime.now().isoformat()
                    })
                    st.success(f"Menu '{menu_name}' saved!")
                else:
                    st.warning("Please enter a menu name")
        else:
            st.info("No recipes yet. Go to AI Recipe Generator to create some!")

    # Display menus
    if st.session_state.menus:
        st.markdown("---")
        st.subheader("📋 Your Menus")
        for i, menu in enumerate(st.session_state.menus):
            with st.expander(f"{menu['name']} ({len(menu['items'])} items)"):
                st.write(f"*{menu['description']}*")
                st.write("### Items")
                total = 0
                for item in menu['items']:
                    st.write(f"**{item['name']}** - €{item['price']}")
                    total += item['price']
                st.write(f"**Total: €{total:.2f}**")
                
                # Export to PDF
                pdf_data = generate_menu_pdf(menu)
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_data,
                    file_name=f"{menu['name'].replace(' ', '_')}_menu.pdf",
                    mime="application/pdf"
                )

elif page == "📊 Inventory":
    st.title("📊 Inventory Management")
    
    # Add item
    with st.expander("➕ Add Inventory Item", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            item_name = st.text_input("Item Name")
            category = st.selectbox("Category", ["Proteins", "Vegetables", "Dairy", "Grains", "Spices", "Oils", "Other"])
        with col2:
            quantity = st.number_input("Quantity", min_value=0, value=0)
            unit = st.selectbox("Unit", ["kg", "g", "L", "ml", "pcs", "boxes"])
        with col3:
            min_stock = st.number_input("Min Stock Level", min_value=0, value=5)
            location = st.text_input("Storage Location")
        
        if st.button("➕ Add Item"):
            if item_name:
                st.session_state.inventory.append({
                    'name': item_name,
                    'category': category,
                    'quantity': quantity,
                    'unit': unit,
                    'min_stock': min_stock,
                    'location': location
                })
                st.success(f"Added {item_name}")
            else:
                st.warning("Please enter item name")

    # Display inventory
    if st.session_state.inventory:
        df = pd.DataFrame(st.session_state.inventory)
        
        # Low stock alerts
        low_stock = df[df['quantity'] <= df['min_stock']]
        if not low_stock.empty:
            st.markdown("""
            <div class="warning-box">
                ⚠️ Low Stock Alerts: {} items below minimum level!
            </div>
            """.format(len(low_stock)), unsafe_allow_html=True)
            st.dataframe(low_stock, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No inventory items yet. Add some above!")

elif page == "🛡️ HACCP Logs":
    st.title("🛡️ HACCP Food Safety Logs")
    
    # EU HACCP Templates
    st.subheader("📝 Temperature Log")
    
    col1, col2 = st.columns(2)
    with col1:
        log_date = st.date_input("Date", datetime.now())
        product = st.text_input("Product Name")
        target_temp = st.number_input("Target Temp (°C)", value=-18.0, step=0.5)
    with col2:
        actual_temp = st.number_input("Actual Temp (°C)", value=-20.0, step=0.5)
        logged_by = st.text_input("Logged By")
        notes = st.text_area("Notes")
    
    if st.button("💾 Save Temperature Log"):
        st.session_state.haccp_logs.append({
            'type': 'temperature',
            'date': str(log_date),
            'product': product,
            'target_temp': target_temp,
            'actual_temp': actual_temp,
            'logged_by': logged_by,
            'notes': notes,
            'compliant': actual_temp <= target_temp
        })
        status = "✅ Compliant" if actual_temp <= target_temp else "❌ NON-COMPLIANT"
        st.success(f"Log saved! {status}")

    # Display logs
    if st.session_state.haccp_logs:
        st.markdown("---")
        st.subheader("📋 Recent Logs")
        df = pd.DataFrame(st.session_state.haccp_logs)
        st.dataframe(df, use_container_width=True)
    
    # Templates
    with st.expander("📄 HACCP Templates"):
        st.write("### Available Templates")
        st.write("- Daily Temperature Log")
        st.write("- Receiving Temperature Log")
        st.write("- Storage Temperature Log")
        st.write("- Cooking Temperature Log")
        st.write("- Cooling Temperature Log")
        st.write("- Allergen Tracking Sheet")
        st.write("- Cleaning Schedule")
        st.write("- Supplier Approval Form")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.markdown("### 🔑 API Configuration")
    
    api_key = st.text_input("OpenAI API Key", type="password", help="Get your key at platform.openai.com")
    if api_key:
        os.environ['OPENAI_API_KEY'] = api_key
        st.success("API key configured! (Session only)")
    
    st.markdown("---")
    st.markdown("### 💾 Data Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Export All Data"):
            data = {
                'recipes': st.session_state.recipes,
                'menus': st.session_state.menus,
                'inventory': st.session_state.inventory,
                'haccp_logs': st.session_state.haccp_logs
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(data, indent=2),
                file_name="chefhelper_backup.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🗑️ Clear All Data"):
            st.session_state.recipes = []
            st.session_state.menus = []
            st.session_state.inventory = []
            st.session_state.haccp_logs = []
            st.success("All data cleared!")