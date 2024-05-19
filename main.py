import streamlit as st
import pandas as pd
import base64
import random
import datetime
from streamlit_tags import st_tags
from PIL import Image
import pymysql
import plotly.express as px
from pdfminer.high_level import extract_text
import youtube_dl
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pdfminer.high_level import extract_text

cnx = pymysql.connect(
    host="localhost",
    user="root",
    password="Prusshita@1234",
    database="sra"
)
csv_file_path = r"C:\Users\HP\Downloads\archive (4)\amazon_jobs_dataset.csv"
jobs_df = pd.read_csv(csv_file_path)
jobs_df['Combined_Text'] = jobs_df['Title'] + ' ' + jobs_df['DESCRIPTION'] + ' ' + jobs_df['BASIC QUALIFICATIONS'] + ' ' + jobs_df['PREFERRED QUALIFICATIONS']
jobs_df.dropna(subset=['Combined_Text'], inplace=True)

vectorizer = TfidfVectorizer()
job_matrix = vectorizer.fit_transform(jobs_df['Combined_Text'])

def recommend_jobs(skill_set):
    user_skills = ' '.join(skill_set)
    user_vector = vectorizer.transform([user_skills])
    similarity_scores = cosine_similarity(user_vector, job_matrix)
    top_indices = similarity_scores.argsort()[0][::-1][:5]  
    return jobs_df.iloc[top_indices]


def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    
    return href

video_recommendations = {
    'Python': ['https://www.youtube.com/watch?v=rfscVS0vtbw', 'https://www.youtube.com/watch?v=YYXdXT2l-Gg'],
    'Machine Learning': ['https://www.youtube.com/watch?v=ukzFI9rgwfU', 'https://www.youtube.com/watch?v=pHiMN_gy9mk'],
    'Data Analysis': ['https://www.youtube.com/watch?v=WbTOutpwPHs', 'https://www.youtube.com/watch?v=0Q7VvqVllN8']
}

def fetch_yt_video_title(video_link):
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(video_link, download=False)
            return info.get('title', 'Unknown')
    except Exception as e:
        print(f"Error fetching video title: {e}")
        return "Unknown"

def parse_resume_text(text):
    data = {
        'name': None,
        'email': None,
        'mobile_number': None,
        'no_of_pages': None,
        'skills': []
    }
    if 'Name:' in text:
        data['name'] = text.split('Name:')[1].split('\n')[0].strip()

    if 'Email:' in text:
        data['email'] = text.split('Email:')[1].split('\n')[0].strip()

    if 'Mobile:' in text:
        data['mobile_number'] = text.split('Mobile:')[1].split('\n')[0].strip()

    data['no_of_pages'] = text.count('\x0c')
    skills_list = ['Python', 'Machine Learning', 'Data Analysis']  
    data['skills'] = skills_list

    return data

def insert_user_data(name, email, resume_score, page_no, predicted_field, user_level, actual_skills, recommended_skills, recommended_courses):
    try:
        connection = pymysql.connect(host='localhost', user='root', password='Prusshita@1234', database='sra')
        
        insert_query = """
        INSERT INTO user_data (Name, Email_ID, resume_score, Timestamp, Page_no, Predicted_Field, User_level, Actual_skills, Recommended_skills, Recommended_courses)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        if name and len(name) > 100:
            name = name[:100]
        if name == "None":
            name = "Hey"
        if email == "None":
            email = "sdaa"
            
        recommended_skills = "Machine Learning"
        timestamp = datetime.datetime.now()
        
        cursor = connection.cursor()
        cursor.execute(insert_query, (name, email, resume_score, timestamp, page_no, predicted_field, user_level, actual_skills, recommended_skills, recommended_courses))
        connection.commit()
        st.success("User data inserted successfully!")
    except Exception as e:
        st.error(f"Error inserting user data: {e}")
    finally:
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
    img = Image.open(r'C:\New folder\logo.png')
    img = img.resize((250, 250))
    st.image(img)

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
            st.text(f"Resume pages: {resume_data['no_of_pages']}")

            st.subheader("**Skills Recommendation💡**")
            keywords = st_tags(label='### Skills that you have',
                               text='See our skills recommendation',
                               value=resume_data['skills'], key='1')

            if resume_data['skills']:
                st.markdown("### Recommended Videos")
                for skill in resume_data['skills']:
                    if skill in video_recommendations:
                        st.subheader(f"Videos for {skill}")
                        recommended_videos = video_recommendations[skill]
                        video_link = random.choice(recommended_videos)
                        st.subheader(fetch_yt_video_title(video_link))
                        st.video(video_link)

                st.markdown("### Recommended Jobs")
                recommended_jobs = recommend_jobs(resume_data['skills'])
                if not recommended_jobs.empty:
                    st.dataframe(recommended_jobs[['Title', 'DESCRIPTION', 'location']])  
                else:
                    st.warning("No jobs found based on your skills.")
        else:
            st.warning("Please upload a PDF file.")

    else:  
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
