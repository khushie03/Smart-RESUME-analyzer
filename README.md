# Smart Resume Analyzer

The Smart Resume Analyzer is a Streamlit-based web application that analyzes resumes, provides skill recommendations, and suggests job opportunities and learning resources. It also has an admin panel to manage user data and visualize valuable insights.

## Features

### Normal User
- **Resume Upload**: Users can upload their resume in PDF format.
- **Resume Analysis**: Extracts basic information and skills from the resume.
- **Skills Recommendation**: Recommends skills based on the extracted resume data.
- **Video Recommendations**: Provides links to YouTube videos for learning recommended skills.
- **Job Recommendations**: Suggests job opportunities that match the user's skills.

### Admin
- **Admin Login**: Secure login for the admin.
- **User Data Management**: View and manage user data.
- **Data Download**: Download user data as a CSV file.
- **Insights Visualization**: Visualize user data insights with pie charts.

## Installation

### Prerequisites
- Python 3.6 or higher
- Required Python packages listed in `requirements.txt`

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/khushie03/email_extraction.git
    cd email_extraction
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Update the database connection settings in the code as per your MySQL configuration:
    ```python
    cnx = pymysql.connect(
        host="localhost",
        user="root",
        password="Your sql password",
        database="sra"
    )
    ```

4. Place your dataset file (`amazon_jobs_dataset.csv`) in the specified path:
    ```bash
    C:\Users\HP\Downloads\archive (4)\amazon_jobs_dataset.csv
    ```

## Running the Application

1. Navigate to the project directory:
    ```bash
    cd /path/to/email_extraction
    ```

2. Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```

3. Open your web browser and go to `http://localhost:8501` to access the application.

## Usage

### Normal User
1. Upload your resume in PDF format.
2. View the extracted information and recommendations.
3. Explore the recommended videos and job opportunities.

### Admin
1. Log in with the admin credentials (`admin`/`admin123`).
2. View and manage user data.
3. Download user data as a CSV file.
4. Visualize insights using pie charts.

## File Structure

```
email_extraction/
├── app.py                  # Main application file
├── requirements.txt        # Required Python packages
├── README.md               # This README file
├── archive/                # Directory for the dataset file
│   └── amazon_jobs_dataset.csv
└── Uploaded_Resumes/       # Directory for uploaded resume files
```
