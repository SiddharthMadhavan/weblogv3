# Web Log Analysis App V4
*By Siddharth Madhavan*

The Web Log Analysis App is a powerful tool designed to analyze and gain insights from web server logs. It provides valuable information about website traffic, user behavior, errors, and performance. With this app, you can make data-driven decisions to optimize your website, improve user experience, and enhance security. 

Web log analysis is an exciting field that involves the use of web analytics software to parse server log files from a web server. This software analyzes the values contained in the log files and provides valuable insights into website performance and user behavior. It helps businesses understand their website traffic, identify popular pages, track conversions, and make data-driven decisions. Web log analysis also provides visual representations of data through bar graphs, pie charts, and reports in formats like PDF. This makes it easier for businesses to interpret the data and gain actionable insights. Overall, web log analysis is a powerful tool that allows businesses to optimize their websites and enhance the user experience.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SiddharthMadhavan/weblogv3.git
cd weblogv3
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Run the Streamlit application:
```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

### Usage

1. Accept the terms and conditions
2. Upload a CSV file containing web log data with the following columns:
   - `Time`: Timestamp of the request
   - `IP`: IP address of the requester
   - `URL`: Requested URL
   - `Status`: HTTP status code
3. View analytics and insights
4. Generate forecasts by entering the desired number of predictions

## Features

- **Data Exploration**: View statistics on unique IPs, URLs, total requests, and visitors
- **Status Code Analysis**: See distribution of HTTP status codes
- **Page Views Tracking**: Monitor most visited pages
- **Data Visualization**: Interactive charts and graphs
- **ARIMA Forecasting**: Predict future traffic patterns
- **Security**: HTML escaping to prevent XSS attacks
- **File Validation**: Automatic validation of uploaded files

## Screenshots

**Step 1**

![Screenshot 2023-08-05 171352](https://github.com/HuntingHack/weblogv3/assets/79624807/757b1fad-98a6-4979-bdf3-ac78a6849c73)

**Step 2**

![Screenshot 2023-08-05 171522](https://github.com/HuntingHack/weblogv3/assets/79624807/31a747b3-4657-4a6a-87d5-853b0dab07d8)

**Step 3**

![Screenshot (9)](https://github.com/HuntingHack/weblogv3/assets/79624807/5d320777-9b8a-4c8a-8e98-fc94d9250625)

**Step 4**

![Screenshot 2023-08-05 171649](https://github.com/HuntingHack/weblogv3/assets/79624807/d648464f-072a-4435-88b7-0eb713b608cc)

**Output**

![Screenshot 2023-08-05 171725](https://github.com/HuntingHack/weblogv3/assets/79624807/ac692e82-781a-483f-887d-3846bb4720a3)

![Screenshot 2023-08-05 171755](https://github.com/HuntingHack/weblogv3/assets/79624807/00c5822b-6ffb-4e80-aadd-c37ffb2ee4e9)

## Security Features

- HTML escaping for all user-generated content
- File size validation (max 100MB)
- CSV structure validation
- Input sanitization for predictions

## License

See T&Cs and Privacy Policy links in the application.

*End of ReadMe File*
