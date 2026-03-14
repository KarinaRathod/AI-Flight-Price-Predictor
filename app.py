import streamlit as st
import pandas as pd
import pickle
import time

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Flight Price AI", page_icon="✈️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .price-box { 
        padding: 25px; 
        border-radius: 12px; 
        background: linear-gradient(135deg, #ffffff 0%, #f1f3f5 100%);
        border: 1px solid #dee2e6; 
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .price-text { font-size: 2.5rem; color: #0d6efd; font-weight: bold; margin: 10px 0; }
    .label-text { font-size: 1.1rem; color: #6c757d; text-transform: uppercase; letter-spacing: 1px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD ASSETS ---
@st.cache_resource
def load_assets():
    model = pickle.load(open("flight_model.pkl", "rb"))
    encoders = pickle.load(open("encoders.pkl", "rb"))
    return model, encoders

try:
    model, encoders = load_assets()
except FileNotFoundError:
    st.error("Model or Encoder files not found. Please ensure 'flight_model.pkl' and 'encoders.pkl' are in the directory.")
    st.stop()

# --- HELPER FUNCTION ---
def get_price_trend(base_input_df, model):
    """Generates prediction data for the next 30 days to show a trend line."""
    trend_data = []
    # Test prices for 1 to 30 days left
    for days in range(1, 31, 2): 
        temp_df = base_input_df.copy()
        temp_df["days_left"] = days
        price = model.predict(temp_df)[0]
        trend_data.append({"Days to Departure": days, "Estimated Fare (₹)": price})
    
    return pd.DataFrame(trend_data).set_index("Days to Departure")

# --- UI APP MAIN ---
st.title("✈️ Smart Fare Predictor")
st.markdown("Plan your trip and discover the best time to book with our AI pricing engine.")
st.divider()

# --- INPUT FORM ---
# Using a form prevents the app from rerunning on every single dropdown change
with st.form("booking_form"):
    st.subheader("Trip Details")
    
    col1, col2 = st.columns(2)
    with col1:
        source_city = st.selectbox("🛫 From", encoders["source_city"].classes_)
        departure_time = st.selectbox("🌅 Departure Window", encoders["departure_time"].classes_)
        airline = st.selectbox("🏢 Preferred Airline", encoders["airline"].classes_)
        days_left = st.slider("📅 Days Until Departure", 1, 60, 15)

    with col2:
        destination_city = st.selectbox("🛬 To", encoders["destination_city"].classes_)
        arrival_time = st.selectbox("🌆 Arrival Window", encoders["arrival_time"].classes_)
        flight_class = st.selectbox("💺 Travel Class", encoders["class"].classes_)
        duration = st.number_input("⏱️ Estimated Duration (Hours)", min_value=0.5, max_value=50.0, value=2.5, step=0.5)

    stops = st.select_slider("🚦 Number of Stops", options=encoders["stops"].classes_)
    
    # Submit button for the form
    submit_button = st.form_submit_button("Calculate Best Fare", use_container_width=True)

# --- LOGIC & PREDICTION ---
if submit_button:
    if source_city == destination_city:
        st.error("⚠️ Source and Destination cities cannot be the same. Please adjust your route.")
    else:
        with st.spinner('Analyzing historical flight trends...'):
            time.sleep(0.8) # Aesthetic delay
            
            # Prepare Data
            input_df = pd.DataFrame({
                "airline": [encoders["airline"].transform([airline])[0]],
                "source_city": [encoders["source_city"].transform([source_city])[0]],
                "departure_time": [encoders["departure_time"].transform([departure_time])[0]],
                "stops": [encoders["stops"].transform([stops])[0]],
                "arrival_time": [encoders["arrival_time"].transform([arrival_time])[0]],
                "destination_city": [encoders["destination_city"].transform([destination_city])[0]],
                "class": [encoders["class"].transform([flight_class])[0]],
                "duration": [duration],
                "days_left": [days_left]
            })

            prediction = model.predict(input_df)[0]
            
            # Display Main Result
            st.markdown("---")
            res_col1, res_col2, res_col3 = st.columns([1, 2, 1])
            
            with res_col2:
                st.markdown(f"""
                    <div class="price-box">
                        <p class="label-text">Estimated Fare</p>
                        <p class="price-text">₹ {int(prediction):,}</p>
                        <p style="font-size: 0.8rem; color: #888; margin-bottom: 0;">*Prices are subject to airline availability</p>
                    </div>
                """, unsafe_allow_html=True)
                
            # Display Trend Chart
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📉 Price Trend Forecast")
            st.markdown("See how the price might change depending on how many days in advance you book.")
            
            trend_df = get_price_trend(input_df, model)
            st.line_chart(trend_df, color="#0d6efd")
            
            st.balloons()