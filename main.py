import streamlit as st
import pandas as pd
import base64
import random
import datetime
import google.generativeai as genai
from serpapi import GoogleSearch
from streamlit_tags import st_tags
from PIL import Image
import pymysql
import plotly.express as px
import youtube_dl
import os
import fitz  
from paddleocr import PaddleOCR


cnx = pymysql.connect(
    host="localhost",
    user="root",
    password="Your Database Password",
    database="sra"
)
genai.configure(api_key="Your Gemini -API Key")


def extract_text(pdf_path, dpi=300, output_dir="./images"):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    zoom = dpi / 72
    magnify = fitz.Matrix(zoom, zoom)
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    all_text = []
    
    for count, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=magnify)
        image_path = os.path.join(output_dir, f"{base_name}_{count}.png")
        pix.save(image_path)
        ocr_result = ocr.ocr(image_path)
        page_text = ""
        for res in ocr_result:
            for line in res:
                page_text += line[-1][0] + " "
        all_text.append(page_text)
    
    return "\n".join(all_text)


def recommend_jobs(skill_set):
    user_skills = ' '.join(skill_set)
    params = {
        "engine": "google_jobs",
        "q": "jobs " + user_skills,
        "hl": "en",
        "api_key": "Your Serp API Key"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    jobs_results = results.get("jobs_results", [])  

    jobs_data = []
    for job in jobs_results:
        job_info = {
            "Title": job.get('title', 'N/A'),
            "DESCRIPTION": job.get('description', 'N/A'),
            "location": job.get('location', 'N/A'),
            "Link": job.get('link', '#')
        }
        jobs_data.append(job_info)

    jobs_df = pd.DataFrame(jobs_data)
    return jobs_df


def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

video_recommendations = {
    'Python': [
        'https://www.youtube.com/watch?v=rfscVS0vtbw',
        'https://www.youtube.com/watch?v=YYXdXT2l-Gg',
        'https://www.youtube.com/watch?v=H1jWq1Q8_54',
        'https://www.youtube.com/watch?v=QnDWb3OeZ0g',
        'https://www.youtube.com/watch?v=7MZgALM7fY8'
    ],
    'Machine Learning': [
        'https://www.youtube.com/watch?v=ukzFI9rgwfU',
        'https://www.youtube.com/watch?v=pHiMN_gy9mk',
        'https://www.youtube.com/watch?v=Gv9_4yMHFhI',
        'https://www.youtube.com/watch?v=GxB3JWwVqMk',
        'https://www.youtube.com/watch?v=7eh4d6sabA0'
    ],
    'Data Analysis': [
        'https://www.youtube.com/watch?v=WbTOutpwPHs',
        'https://www.youtube.com/watch?v=0Q7VvqVllN8',
        'https://www.youtube.com/watch?v=G8x8DHDfZzY',
        'https://www.youtube.com/watch?v=QeH7n8aR8Qw',
        'https://www.youtube.com/watch?v=3uY7u3W6S8o'
    ],
    'Web Development': [
        'https://www.youtube.com/watch?v=UB1O30fR-EE',
        'https://www.youtube.com/watch?v=QnDWb3OeZ0g',
        'https://www.youtube.com/watch?v=J1zFh-43B2c',
        'https://www.youtube.com/watch?v=1Rs2ND1dyU8',
        'https://www.youtube.com/watch?v=7CqJlxBYjyI'
    ],
    'Data Science': [
        'https://www.youtube.com/watch?v=ua-CiDNNj30',
        'https://www.youtube.com/watch?v=7eh4d6sabA0',
        'https://www.youtube.com/watch?v=5b2XW_VrBjo',
        'https://www.youtube.com/watch?v=c8Z6c1D1PQA',
        'https://www.youtube.com/watch?v=Gv0Z1U3fWm0'
    ],
    'DevOps Engineer': [
        'https://www.youtube.com/watch?v=8Kp-8yC47p8',
        'https://www.youtube.com/watch?v=0W7m2FjE8zM',
        'https://www.youtube.com/watch?v=5Z4pHQmF8Gk',
        'https://www.youtube.com/watch?v=3d1WVR9QYq0',
        'https://www.youtube.com/watch?v=KKg4lm0NT6A'
    ],
    'Data Engineer': [
        'https://www.youtube.com/watch?v=53Fh73pYt9g',
        'https://www.youtube.com/watch?v=UIA1E8sA1Dg',
        'https://www.youtube.com/watch?v=n6B16s20K6w',
        'https://www.youtube.com/watch?v=4y8rXWClP1Q',
        'https://www.youtube.com/watch?v=6QMLF0Vx4C8'
    ],
    'Artificial Intelligence Engineer': [
        'https://www.youtube.com/watch?v=2ePf9rue1Ao',
        'https://www.youtube.com/watch?v=K9R6L1ET3C4',
        'https://www.youtube.com/watch?v=dN6CMfQ4K6E',
        'https://www.youtube.com/watch?v=8Uj-2MFMkGg',
        'https://www.youtube.com/watch?v=Ik_-VgAqP8E'
    ],
    'Cloud Engineer': [
        'https://www.youtube.com/watch?v=2MucgW5RO2I',
        'https://www.youtube.com/watch?v=oOVLwbPwiF8',
        'https://www.youtube.com/watch?v=5Qavd4eQ9dI',
        'https://www.youtube.com/watch?v=VM-2K1bPeTE',
        'https://www.youtube.com/watch?v=2Yf_Dj_0k-4'
    ],
    'Business Analyst': [
        'https://www.youtube.com/watch?v=3V2j-XT1c2A',
        'https://www.youtube.com/watch?v=ijLt2E1iU7I',
        'https://www.youtube.com/watch?v=FWPiycQ39MQ',
        'https://www.youtube.com/watch?v=mEk22llXAE8',
        'https://www.youtube.com/watch?v=Pt2-qBDH4Ds'
    ],
    'Human Resources (HR)': [
        'https://www.youtube.com/watch?v=QdLq1Qd2lxY',
        'https://www.youtube.com/watch?v=MM-T8D8ivgA',
        'https://www.youtube.com/watch?v=UybngMjMEyM',
        'https://www.youtube.com/watch?v=1huQ0O1HRL4',
        'https://www.youtube.com/watch?v=PrD6KXyCj_c'
    ],
    'UI/UX Designer': [
        'https://www.youtube.com/watch?v=FjN4S8K2VvA',
        'https://www.youtube.com/watch?v=w7XW-4jCfq0',
        'https://www.youtube.com/watch?v=nIXIdtk-4jE',
        'https://www.youtube.com/watch?v=qT8gKHCbwkc',
        'https://www.youtube.com/watch?v=F7s1P1Qi9aU'
    ],
    'Software Engineer': [
        'https://www.youtube.com/watch?v=0U6L2cZrA_Q',
        'https://www.youtube.com/watch?v=Vlv6uA4yHpg',
        'https://www.youtube.com/watch?v=Hl-4q27B6iA',
        'https://www.youtube.com/watch?v=3PS-c0Cz_Ug',
        'https://www.youtube.com/watch?v=zIbbK5PmW8U'
    ],
    'Product Manager': [
        'https://www.youtube.com/watch?v=dY5m3PTz6ow',
        'https://www.youtube.com/watch?v=8Dzh_8F2w2A',
        'https://www.youtube.com/watch?v=DDx5-l3AaJc',
        'https://www.youtube.com/watch?v=Wq4WlZZ_5wo',
        'https://www.youtube.com/watch?v=Vt7DQFIda9M'
    ]
}

position_skills_videos = [
    {
        'position': 'Python Developer',
        'skills': ['Python', 'OOP', 'Data Structures'],
        'video_links': video_recommendations['Python']
    },
    {
        'position': 'Machine Learning Engineer',
        'skills': ['Machine Learning', 'Deep Learning', 'Python'],
        'video_links': video_recommendations['Machine Learning']
    },
    {
        'position': 'Data Analyst',
        'skills': ['Data Analysis', 'Statistics', 'SQL'],
        'video_links': video_recommendations['Data Analysis']
    },
    {
        'position': 'Web Developer',
        'skills': ['HTML', 'CSS', 'JavaScript'],
        'video_links': video_recommendations['Web Development']
    },
    {
        'position': 'Data Scientist',
        'skills': ['Data Science', 'Machine Learning', 'Python', 'R'],
        'video_links': video_recommendations['Data Science']
    },
    {
        'position': 'DevOps Engineer',
        'skills': ['CI/CD', 'Docker', 'Kubernetes', 'Cloud'],
        'video_links': video_recommendations['DevOps Engineer']
    },
    {
        'position': 'Data Engineer',
        'skills': ['ETL', 'Data Warehousing', 'SQL', 'Python'],
        'video_links': video_recommendations['Data Engineer']
    },
    {
        'position': 'AI Engineer',
        'skills': ['Machine Learning', 'Deep Learning', 'Python', 'TensorFlow'],
        'video_links': video_recommendations['Artificial Intelligence Engineer']
    },
    {
        'position': 'Cloud Engineer',
        'skills': ['Cloud Services', 'AWS', 'Azure', 'DevOps'],
        'video_links': video_recommendations['Cloud Engineer']
    },
    {
        'position': 'Business Analyst',
        'skills': ['Requirements Gathering', 'Data Analysis', 'SQL'],
        'video_links': video_recommendations['Business Analyst']
    },
    {
        'position': 'Human Resources (HR)',
        'skills': ['Recruitment', 'Employee Relations', 'Performance Management'],
        'video_links': video_recommendations['Human Resources (HR)']
    },
    {
        'position': 'UI/UX Designer',
        'skills': ['User Research', 'Prototyping', 'Wireframing', 'UI Design'],
        'video_links': video_recommendations['UI/UX Designer']
    },
    {
        'position': 'Software Engineer',
        'skills': ['Programming', 'System Design', 'Algorithms'],
        'video_links': video_recommendations['Software Engineer']
    },
    {
        'position': 'Product Manager',
        'skills': ['Product Strategy', 'Market Research', 'Agile Methodologies'],
        'video_links': video_recommendations['Product Manager']
    }
]


prompt = """
Based on the given skills and position define the skills that the user should know with respect to the 
position what skills should be the person recommended with in order to improve its skillset .
Pass in the form of array .["Machine Learning" , "Streamlit "]"""

from serpapi import GoogleSearch

def extract_video_links(position, skills):
    skills = " ".join(skills)
    
    params = {
  "engine": "youtube",
  "search_query": position + skills,
  "api_key": "Your SerpAPI key"}

    search = GoogleSearch(params)
    results = search.get_dict()
    video_results = results["video_results"]

    video_links = []
    thumbnails = []

    for movie in video_results:
        link = movie.get('link')
        thumbnail = movie.get('thumbnail', '')  
        if link:
            video_links.append(link)
        if thumbnail:
            thumbnails.append(thumbnail)

    return video_links[:5], thumbnails[:5] 


def fetch_yt_video_title(video_link):
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(video_link, download=False)
            return info.get('title', 'Unknown')
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Unknown"


prompt = """
You have given the Extracted Text of the Resume. From that, based on the extracted Text, you need to find the
relevant details in the format: 'name': None, 'email': None, 'mobile_number': None, 'no_of_pages': None, 'skills': [].
Return the Text in this same format, split by new line characters ('\n').
"""

def parse_resume_text(text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + text)
    generated_text = response.text.strip()

    data = {
        'name': None,
        'email': None,
        'mobile_number': None,
        'no_of_pages': None,
        'skills': []
    }
    
    if "'name':" in generated_text:
        data['name'] = generated_text.split("'name':")[1].split(",")[0].strip().strip("'")
    
    if "'email':" in generated_text:
        data['email'] = generated_text.split("'email':")[1].split(",")[0].strip().strip("'")
    
    if "'mobile_number':" in generated_text:
        data['mobile_number'] = generated_text.split("'mobile_number':")[1].split(",")[0].strip().strip("'")
    
    if "'no_of_pages':" in generated_text:
        no_of_pages = generated_text.split("'no_of_pages':")[1].split(",")[0].strip().strip("'")
        data['no_of_pages'] = None if no_of_pages == 'None' else int(no_of_pages)
    
    if "'skills':" in generated_text:
        skills_text = generated_text.split("'skills':")[1].split("]")[0].strip().strip("[").strip("'")
        data['skills'] = [skill.strip() for skill in skills_text.split(',')]

    return data

def insert_user_data(name, email, resume_score, page_no, predicted_field, user_level, actual_skills, recommended_skills, recommended_courses):
    try:
        # Database connection
        connection = pymysql.connect(host='localhost', user='root', password='Prusshita@1234', database='sra')
        
        # SQL query for inserting data
        insert_query = """
        INSERT INTO user_data (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Handle input validation and default values
        if name and len(name) > 100:
            name = name[:100]
        if name == "None":
            name = "Hey"
        if email == "None":
            email = "sdaa@example.com"  # Default or dummy email

        recommended_skills = "Machine Learning"  # Set default or dynamic recommended skills
        timestamp = datetime.datetime.now()  # Current timestamp
        
        # Execute the insert query
        cursor = connection.cursor()
        cursor.execute(insert_query, (name, email, resume_score, timestamp, page_no, predicted_field, user_level, actual_skills, recommended_skills, recommended_courses))
        connection.commit()
        
        st.success("User data inserted successfully!")
    except Exception as e:
        st.error(f"Error inserting user data: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


def admin_insert_section():
    st.subheader("Insert User Data")
    name = st.text_input("Name")
    email = st.text_input("Email")
    resume_score = st.number_input("Resume Score", min_value=0.0, max_value=100.0, step=0.1)
    page_no = st.number_input("Page Number", min_value=1, step=1)
    predicted_field = st.text_input("Predicted Field")
    user_level = st.selectbox("User Level", ["Beginner", "Intermediate", "Advanced"])
    actual_skills = st.text_input("Actual Skills")
    recommended_skills = st.text_input("Recommended Skills")
    recommended_courses = st.text_input("Recommended Courses")

    if st.button("Insert"):
        if name and email and predicted_field and user_level and actual_skills and recommended_skills and recommended_courses:
            insert_user_data(name, email, resume_score, page_no, predicted_field, user_level, actual_skills, recommended_skills, recommended_courses)
        else:
            st.warning("Please fill in all required fields.")


def run():
    st.title("Smart Resume Analyzer")
    st.sidebar.markdown("Choose User")
    activities = ["Normal User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)

    if choice == 'Normal User':
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            save_path = f'./Uploaded_Resumes/{pdf_file.name}'
            with open(save_path, 'wb') as f:
                f.write(pdf_file.getbuffer())
            
            text = extract_text(save_path)
            resume_data = parse_resume_text(text)

            st.header("**Resume Analysis**")
            st.success(f"Hello {resume_data['name']}")
            st.subheader("**Your Basic Info**")
            st.text(f"Name: {resume_data['name']}")
            st.text(f"Email: {resume_data['email']}")
            st.text(f"Contact: {resume_data['mobile_number']}")
            st_tags(label='### Extracted Skills:', text='Skills found in resume', value = resume_data['skills'], key='1')
            print(resume_data['skills'])
            prompt = """
            Based on the given skills identify the best Matching role for the position. Just return the 
            Job Position such as Data Analyst, Machine Learning Engineer, Web Developer, etc."""
            
            model = genai.GenerativeModel("gemini-pro")
            resume_skills = ", ".join(resume_data['skills'])
            print(resume_skills)
            position_suggested = model.generate_content(prompt + resume_skills)
            st.write(position_suggested.text)
            
            myfile = genai.upload_file(save_path)

            model1 = genai.GenerativeModel("gemini-1.5-flash")
            Score = model1.generate_content(
                [myfile, "\n\n", """
            On the basis of the Given Resume . Give the ATS Score for the Resume out of 10 . Also
            Define the improvements that can be done in the resume . That is what skills can be added 
            or what points to be highlighted"""]
            )
            st.write(Score.text)
            st.subheader("**Job Recommendations**")
            recommended_jobs = recommend_jobs(position_suggested.text)
            for index, row in recommended_jobs.iterrows():
                st.write(f"Job Title: {row['Title']}")
                st.write(f"Location: {row['location']}")
                st.write(f"[Job Link]({row["Link"]})")
                st.write("---")

            st.subheader("**Video Recommendations**")
            video_links, thumbnails = extract_video_links(position= position_suggested.text , skills= resume_data['skills'])
            if video_links and thumbnails:
                for link, thumbnail in zip(video_links, thumbnails):
                    if isinstance(thumbnail, dict):
                        thumbnail_url = thumbnail.get('static', '')
                    else:
                        thumbnail_url = thumbnail

                    st.image(thumbnail_url, caption='Watch Video', use_column_width=True)
                    st.markdown(f'<a href="{link}" target="_blank"><img src="https://img.icons8.com/ios-filled/50/000000/link.png" alt="Link" style="width: 25px; height: 25px;"/></a>', unsafe_allow_html=True)

            else:
                st.write("No video recommendations available.")

    elif choice == 'Admin': 
        st.success('Welcome to Admin Panel')
        ad_user = st.text_input("Username")
        ad_password = st.text_input("Password", type='password')
        if st.button('Login'):
            if ad_user == 'admin' and ad_password == 'admin123':
                st.success("Welcome Admin")
                cursor = cnx.cursor()
                cursor.execute("SELECT * FROM user_data")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email_ID', 'Resume Score', 'Timestamp',
                                                 'Page_no', 'Predicted_Field', 'User_level',
                                                 'Actual_skills', 'Recommended_skills', 'Recommended_courses'])

                st.header("**User's Data**")
                st.dataframe(df)
                st.markdown(get_table_download_link(df, 'User_Data.csv', 'Download Report'), unsafe_allow_html=True)
                admin_insert_section()

                st.subheader("📈 **Predicted Field Recommendations**")
                fig1 = px.pie(df, names='Predicted_Field', title='Predicted Field according to the Skills')
                st.plotly_chart(fig1)

                st.subheader("📈 **User Experience Level**")
                fig2 = px.pie(df, names='User_level', title="User's Experienced Level")
                st.plotly_chart(fig2)

            else:
                st.error("Invalid credentials")

if __name__ == '__main__':
    run()
