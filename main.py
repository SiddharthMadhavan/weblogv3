import pandas as pd
import html
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Application version
VERSION = '4.01'

# Module-level cached functions for better performance
@st.cache_data
def load_csv_data(file):
    """
    Load and parse CSV file with validation.
    
    Args:
        file: Uploaded file object
    
    Returns:
        DataFrame containing the parsed CSV data
    """
    return pd.read_csv(file)

@st.cache_resource
def fit_arima_model(_train_data, order=(12, 2, 13)):
    """
    Fit ARIMA model to training data.
    
    Args:
        _train_data: Training dataset. The underscore prefix tells Streamlit 
                     to skip hashing this parameter for cache validation, which 
                     is necessary for pandas Series/DataFrame objects.
        order: ARIMA order (p, d, q) tuple
    
    Returns:
        Fitted ARIMA model
    """
    return ARIMA(_train_data, order=order).fit()

# Set Streamlit page layout
st.set_page_config(page_title='Web Log Analysis App', layout='wide', page_icon=":fax:")

# Function to style text with HTML escaping for security
def styled_text(text, font_size=18, color='black', weight='normal', align='left'):
    """
    Create styled HTML text with proper escaping to prevent XSS and CSS injection attacks.
    
    Args:
        text: The text content to display
        font_size: Font size in pixels (validated to be positive integer)
        color: Text color (validated against safe CSS colors)
        weight: Font weight (validated against safe values)
        align: Text alignment (validated against safe values)
    
    Returns:
        HTML string with escaped text and validated styles
    """
    # Validate and sanitize parameters
    safe_colors = ['black', 'white', 'red', 'blue', 'green', 'orange', 'purple', 'gray', 'yellow']
    safe_weights = ['normal', 'bold', 'lighter', 'bolder']
    safe_aligns = ['left', 'center', 'right', 'justify']
    
    # Use defaults for invalid values
    font_size = int(font_size) if isinstance(font_size, (int, float)) and font_size > 0 else 18
    color = color if color in safe_colors else 'black'
    weight = weight if weight in safe_weights else 'normal'
    align = align if align in safe_aligns else 'left'
    
    escaped_text = html.escape(str(text))
    return f'<p style="font-size:{font_size}px; color:{color}; font-weight:{weight}; text-align:{align};">{escaped_text}</p>'

# Function to create colorful boxes with HTML escaping
def colored_box(title, content, color):
    """
    Create a colored box with title and content, with HTML escaping for security.
    
    Args:
        title: Box title
        content: Box content
        color: Background color (validated against safe CSS colors)
    
    Returns:
        HTML string with escaped content and validated color
    """
    # Validate color parameter
    safe_colors = ['blue', 'green', 'orange', 'red', 'lightgreen', 'lightblue', 
                   'lightyellow', 'lightgray', 'purple', 'pink', 'cyan']
    color = color if color in safe_colors else 'lightgray'
    
    escaped_title = html.escape(str(title))
    escaped_content = html.escape(str(content))
    return f'<div style="background-color:{color}; padding: 10px; border-radius: 5px;"><h2>{escaped_title}</h2><p>{escaped_content}</p></div>'

# Function to create expandable sections
def expandable_section(title, content):
    """
    Create an expandable section in Streamlit.
    
    Args:
        title: Section title
        content: Section content
    """
    with st.expander(title, expanded=True):
        st.write(content)

# Code for website design
st.title('Web Log Analysis App')
st.subheader(f'V {VERSION}')

# Disclaimer
with st.expander('Disclaimer', expanded=True):
    st.markdown('[T&Cs](https://docs.google.com/document/d/1ej4FDVM_NPhB3BDbsRZ4ygkt738de62WUlap42gy4ZY/edit?usp=sharing)')
    st.markdown('[Privacy Policy](https://docs.google.com/document/d/1d5BDiJyufvRkGjB0BjwW3PGpdCEUKi2MYFkL4B1UKe0/edit?usp=sharing)')
    button1 = st.radio("Please agree to continue:", ('Agree', 'Disagree'))

if (button1 == 'Agree'):
    st.expander('Disclaimer', expanded=False)
    st.header('About App')
    st.write('The Web Log Analysis App is a powerful tool designed to analyze and gain insights from web server logs. It provides valuable information about website traffic, user behavior, errors, and performance. With this app, you can make data-driven decisions to optimize your website, improve user experience, and enhance security.')

    # Starting off with an input given by the user
    uploaded_file = st.file_uploader("Upload your file here...")

    if uploaded_file is not None:
        # Validate file size (limit to 100MB)
        max_file_size = 100 * 1024 * 1024  # 100 MB in bytes
        if uploaded_file.size > max_file_size:
            st.error("File size exceeds 100MB limit. Please upload a smaller file.")
        else:
            try:
                # Use module-level cached function for data loading
                log_data = load_csv_data(uploaded_file)
                
                # Validate that required columns exist
                required_columns = ['Time', 'IP', 'URL', 'Status']
                missing_columns = [col for col in required_columns if col not in log_data.columns]
                
                if missing_columns:
                    st.error(f"CSV file is missing required columns: {', '.join(missing_columns)}")
                    st.stop()
                    
            except pd.errors.EmptyDataError:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
                st.stop()
            except pd.errors.ParserError:
                st.error("Error parsing the CSV file. Please ensure it's a valid CSV format.")
                st.stop()
            except Exception as e:
                st.error(f"Error loading file: {str(e)}")
                st.stop()

            # Perform initial data exploration
            st.write(log_data.head())  # Display the first few rows of the dataset

            # Create new columns for day, month, year, and time
            try:
                log_data['Date'] = log_data['Time'].str.extract(r'\[(\d{2}/\w+/\d{4})')
                log_data['Day'] = log_data['Date'].str.extract(r'(\d{2})/')
                log_data['Month'] = log_data['Date'].str.extract(r'/(\w+)/')
                log_data['Year'] = log_data['Date'].str.extract(r'/(\d{4})')
                log_data['Time'] = log_data['Time'].str.extract(r':(\d{2}:\d{2}:\d{2})')
                log_data['URL'] = log_data['URL'].str.extract(r'(\S+)\sHTTP/1\.1')
            except Exception as e:
                st.error(f"Error parsing log data: {str(e)}")
                st.stop()

            page_views = log_data['URL'].value_counts()  # Count of page views for each URL
            unique_ips = log_data['IP'].nunique()  # Count the number of unique IP addresses
            unique_urls = log_data['URL'].nunique()  # Count the number of unique URLs
            status_counts = log_data['Status'].value_counts()  # Count the occurrences of each status code
            # Perform exploratory analysis
            total_requests = len(log_data)  # Total number of requests


            # Exploratory Analysis Results Styling
            st.header("Exploratory Analysis Results:")

            st.write(styled_text("Analysis Results:", font_size=24, weight='bold', color='white', align='center'), unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(colored_box("Unique IP Addresses:", str(unique_ips), 'blue'), unsafe_allow_html=True)
            with col2:
                st.write(colored_box("Unique URLs:", str(unique_urls), 'green'), unsafe_allow_html=True)
            with col3:
                st.write(colored_box("Total Requests:", str(total_requests), 'orange'), unsafe_allow_html=True)
                
            st.subheader("Additional Information:")
    
            st.write(colored_box("Status Code Counts:", "", 'lightgreen'), unsafe_allow_html=True)
            st.table(status_counts)

            st.write(colored_box("Page Views:", "", 'lightgreen'), unsafe_allow_html=True)
            st.table(page_views.head(20))

            # Data Visualization
            st.header('Data Visualization:')
            st.subheader("Page Views Frequency:")
            fig = px.line(page_views, title='Page Views')
            st.plotly_chart(fig)

            # Aggregate data by date
            aggregated_data = log_data.groupby('Date').agg({'IP': 'count'}).reset_index()
            aggregated_data.columns = ['Date', 'request_count']
            aggregated_data.set_index('Date', inplace=True)
            target_variable = aggregated_data['request_count']

            # Prepare data for ARIMA modeling
            model_input = target_variable    

            # Split the Data
            train_data = model_input[:-30]
            test_data = model_input[-30:]

            # Fit the ARIMA Model using module-level cached function
            try:
                order = (12, 2, 13)
                model = fit_arima_model(train_data, order)
                
                # Evaluate the Model
                predictions = model.forecast(30)
                predictions.index = test_data.index
                mse = mean_squared_error(test_data, predictions)
                rmse = np.sqrt(mse)
                mae = mean_absolute_error(test_data, predictions)
                st.write(f"RMSE: {rmse:.2f}")
                st.write(f"MAE: {mae:.2f}")
            except Exception as e:
                st.error(f"Error fitting ARIMA model: {str(e)}")
                st.stop()

            # Forecast with the Model
            st.subheader("Forecasting:")

            prediction_count = st.text_input("Enter the required number of predictions:")

            if prediction_count:
                try:
                    pred_no = int(prediction_count)
                    if pred_no <= 0:
                        st.error("Please enter a positive number.")
                        st.stop()
                    elif pred_no > 365:
                        st.warning("Warning: Predicting more than 365 days ahead may be unreliable.")
                        
                    future_predictions = model.forecast(steps=pred_no)
                    st.subheader('Predictions:')

                    # Create a Line Plot with Forecasted Predictions
                    fig = go.Figure()

                    # Add the historical data to the plot
                    fig.add_trace(go.Scatter(
                        x=target_variable.index,
                        y=target_variable,
                        name='Historical Data'
                    ))

                    # Add the forecasted predictions to the plot
                    fig.add_trace(go.Scatter(
                        x=future_predictions.index,
                        y=future_predictions,
                        name='Forecasted Predictions'
                    ))

                    # Customize the plot layout
                    fig.update_layout(
                        title='Web Log Data Forecast',
                        xaxis_title='Timestamp',
                        yaxis_title='Total Requests'
                    )

                    # Show the plot
                    st.plotly_chart(fig)

                    st.write("In conclusion, the Web Log Analysis App offers an invaluable resource for website owners and administrators to delve into their web server logs and extract meaningful insights. By harnessing data-driven decisions derived from this analysis, website owners can effectively optimize their online platforms, elevate user experiences, and bolster the overall security of their websites. The app's intuitive interface and powerful visualizations enable users to effortlessly identify patterns, track trends, and make informed decisions to enhance the performance and user engagement of their web presence. With the Web Log Analysis App at their disposal, website administrators are empowered to take their online ventures to new heights of success and efficiency.")
                    
                except ValueError:
                    st.error("Please enter a valid integer for the number of predictions.")
                except Exception as e:
                    st.error(f"Error generating predictions: {str(e)}")
          
    else:
        st.warning('Please upload a file to proceed.')
else:
    st.warning('Please agree to use our service!')
