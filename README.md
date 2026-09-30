# 🎯 Online Hobby & Skills Tracker with Community Sharing on Cloud

A cloud-based application that helps users **track hobbies and skills, set learning goals, record practice sessions, monitor progress, and share achievements with a community**.

The project is designed as a **Cloud Computing project** and demonstrates concepts such as cloud deployment, user-specific data, database storage, analytics, community sharing, file uploads, authentication, security, and scalable application architecture.

---

## 🌐 Live Demo

🚀 **Streamlit Cloud:**
`https://cloud-hobby-skills-tracker-bwdhhtfkchcfrxjngp3tds.streamlit.app/`

📂 **GitHub Repository:**
`https://github.com/Neha-Joshi05/Cloud-Hobby-Skills-Tracker.git`

---

## 📌 Project Overview

The **Online Hobby & Skills Tracker** provides a centralized platform where users can manage their personal learning and hobby activities.

Users can:

* Create and manage their profile
* Add hobbies and skills
* Set learning goals
* Record practice sessions
* Track progress
* Monitor practice streaks
* Create milestones
* Upload achievement proof
* Share achievements with the community
* Like community posts
* Comment on posts
* View personal analytics
* Access their data through a cloud-hosted application

The project follows the concept:

```text
Profile
   ↓
Create Hobby / Skill
   ↓
Set Goal
   ↓
Record Practice
   ↓
Calculate Progress
   ↓
Track Streaks
   ↓
Upload Achievement
   ↓
Share Community Post
   ↓
Likes + Comments
   ↓
Analytics Dashboard
```

The project requirements specifically focus on cloud hosting, authentication, authorization, cloud databases, object storage, APIs, user-specific data, community sharing, analytics, security, scalability, testing, and deployment.

---

# 🎯 Problem Statement

People often start hobbies or learning activities but stop because they lack:

* Consistent tracking
* Clear goals
* Progress visibility
* Motivation
* Accountability
* Community interaction

Traditional notebooks or locally stored applications do not provide easy cross-device access or community interaction.

This project provides a centralized cloud-based platform where users can record their activities, monitor progress, and share achievements.

---

# 💡 Objectives

The main objectives are:

1. Build a cloud-based hobby and skill tracking application.
2. Allow users to create and manage skills.
3. Allow users to define measurable learning goals.
4. Record daily practice sessions.
5. Calculate progress automatically.
6. Track practice streaks.
7. Provide analytics through dashboards.
8. Allow achievement sharing.
9. Provide a community feed.
10. Support likes and comments.
11. Demonstrate cloud computing concepts.
12. Deploy the application online.

---

# ✨ Features

## 👤 User Profile

Users can maintain their personal profile containing:

* Name
* Username
* Email
* Profile picture
* Bio
* Interests
* Account creation information

---

## 🎯 Hobby & Skill Management

Users can add skills/hobbies such as:

* Coding
* Photography
* Guitar
* Painting
* Cooking
* Chess
* Fitness
* Writing
* Gardening
* Graphic Design
* Video Editing
* Public Speaking

Each skill can contain:

* Skill name
* Category
* Current level
* Target level
* Start date
* Target date
* Status
* Description

### Skill Levels

```text
BEGINNER
INTERMEDIATE
ADVANCED
```

### Skill Status

```text
ACTIVE
PAUSED
COMPLETED
```

---

# 🏆 Goals & Milestones

Users can create measurable goals for their skills.

### Example

```text
Skill: Guitar

Goal: Practice Guitar

Target: 30 Hours

Completed: 18 Hours

Progress: 60%
```

### Progress Formula

```text
Progress % = (Current Value / Target Value) × 100
```

The displayed progress is limited to a maximum of 100%.

Example milestones:

```text
5 Hours
10 Hours
20 Hours
30 Hours
```

---

# ⏱️ Practice Session Tracking

Users can record their practice sessions.

Each session can contain:

* Skill
* Date
* Duration
* Activity
* Notes

### Example

```text
Skill: Photography

Duration: 60 minutes

Activity:
Practiced portrait photography

Notes:
Worked on natural-light composition.
```

Practice data can be used to calculate:

* Total practice time
* Weekly practice
* Monthly practice
* Goal progress
* Practice streak

---

# 🔥 Practice Streaks

The application can calculate consecutive practice activity.

For example:

```text
Monday    ✓
Tuesday   ✓
Wednesday ✓
Thursday  ✓
Friday    ✓
```

Current streak:

```text
🔥 5 Days
```

Streaks help users maintain consistency.

---

# 🏅 Achievements & Badges

The application can recognize milestones and achievements.

Example:

```text
🔥 7-Day Streak
🏆 1000 Minutes Practiced
🎯 Goal Completed
⭐ Skill Milestone Achieved
```

---

# 🌐 Community Sharing

Users can share their achievements with the community.

Example:

> Completed 30 hours of guitar practice! 🎸

A post may contain:

* User
* Skill
* Achievement
* Text
* Image
* Timestamp
* Likes
* Comments

---

# ❤️ Likes & Comments

Community members can interact with posts.

Supported actions include:

```text
Like
Unlike
Comment
Delete Own Comment
```

Duplicate likes should be prevented.

Users should only be allowed to modify their own content.

---

# 📊 Analytics Dashboard

The dashboard provides useful progress information.

### Main Metrics

* Total Practice Hours
* Weekly Practice
* Monthly Practice
* Most Practiced Skill
* Current Streak
* Longest Streak
* Goals Completed
* Active Goals
* Milestones Achieved
* Number of Posts
* Likes Received
* Comments Received

### Charts

The project can visualize:

* Practice Hours by Skill
* Weekly Practice Trend
* Monthly Progress
* Goal Completion
* Skill Distribution

---

# ☁️ Cloud Computing Concepts

This project demonstrates several important cloud computing concepts.

| Concept              | Project Usage                                 |
| -------------------- | --------------------------------------------- |
| Cloud Computing      | Application deployed online                   |
| Cloud Database       | Stores application data                       |
| Authentication       | User login/account management                 |
| Authorization        | Controls access to user data                  |
| Cloud Storage        | Stores uploaded files/images                  |
| REST API             | Application communication                     |
| Serverless Computing | Optional cloud functions                      |
| Analytics            | Progress and activity analysis                |
| Scalability          | Architecture can support increasing users     |
| Availability         | Cloud-hosted application                      |
| Security             | Authentication, validation and protected data |
| Deployment           | Application deployed to cloud                 |

The project blueprint specifically identifies cloud database, object storage, authentication, REST APIs, analytics, security, scalability and cloud deployment as core requirements.

---

# 🏗️ System Architecture

For the Streamlit implementation:

```text
             👤 User
                │
                ▼
       ┌─────────────────┐
       │ Streamlit Cloud  │
       │   Web App        │
       └────────┬────────┘
                │
       ┌────────┴────────┐
       │                 │
       ▼                 ▼
   Application       Analytics
     Logic             Engine
       │                 │
       └────────┬────────┘
                │
                ▼
        Cloud / Database
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
   User Data       Community Data
        │               │
        └───────┬───────┘
                ▼
         Progress Dashboard
```

---

# 🛠️ Technology Stack

## Frontend / Application

* Python
* Streamlit

## Data Processing

* Pandas
* NumPy

## Visualization

* Plotly
* Streamlit Charts

## Cloud Deployment

* Streamlit Community Cloud

## Version Control

* Git
* GitHub

## Optional Cloud Services

Depending on the implementation:

* Firebase Authentication
* Firebase Firestore
* Firebase Storage
* Cloud Functions
* Cloud Run

The original project blueprint proposes React + Firebase for the recommended cloud architecture and Firebase Auth, Firestore and Storage as cloud services.

---

# 📂 Project Structure

```text
Cloud-Hobby-Skills-Tracker/
│
├── app.py
│
├── pages/
│   ├── dashboard.py
│   ├── skills.py
│   ├── goals.py
│   ├── practice.py
│   ├── community.py
│   └── profile.py
│
├── services/
│   ├── database.py
│   ├── analytics.py
│   ├── authentication.py
│   └── storage.py
│
├── data/
│   └── sample_data.csv
│
├── assets/
│   └── images/
│
├── tests/
│   └── test_app.py
│
├── screenshots/
│
├── .streamlit/
│   └── secrets.toml
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Neha-Joshi05/Cloud-Hobby-Skills-Tracker.git
```

```bash
cd Cloud-Hobby-Skills-Tracker
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Locally

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will normally open in your browser at:

```text
http://localhost:8501
```

---






## Step 3 — Create App

Select:

```text
Create app
        ↓
Yup, I have an app
```

Then select:

```text
Repository: YOUR_USERNAME/Cloud-Hobby-Skills-Tracker
Branch: main
Main file path: app.py
```

Streamlit's current deployment flow asks for the GitHub repository, branch and entrypoint file.

---

## Step 4 — Configure Secrets

If your application uses external services:

```text
Advanced settings
       ↓
Secrets
```

Paste your required `secrets.toml` configuration there.

Do **not** upload your actual secrets file to GitHub.

---

## Step 5 — Deploy

Click:

```text
Deploy
```

Streamlit will install the dependencies from `requirements.txt` and launch the application.

Your application will receive a URL similar to:

```text
https://your-app-name.streamlit.app
```

---

# 🧪 Testing

Important test cases include:

* User registration
* Login
* Invalid login
* Profile update
* Add skill
* Update skill
* Delete skill
* Create goal
* Log practice session
* Progress calculation
* Milestone completion
* File upload
* Create community post
* Retrieve community feed
* Like post
* Prevent duplicate likes
* Unlike post
* Add comment
* Delete own comment
* Analytics calculation
* User-data isolation
* Authentication expiry

The original project blueprint specifies these testing areas, including user-data isolation, cloud-storage failure and authentication-token expiry.

---

# 🔒 Security

Security considerations include:

* Authentication
* Authorization
* Secure password handling
* HTTPS
* Input validation
* File-type validation
* File-size validation
* Environment variables
* Secrets management
* Protected user data
* Community-content moderation
* Secure cloud storage

Never expose:

```text
API Keys
Passwords
Database Credentials
Secret Keys
Private Tokens
```

The project specification explicitly requires avoiding hardcoded credentials and using environment variables instead.

---

# 📈 Scalability

The architecture can be extended using:

* Managed databases
* Cloud object storage
* CDN
* Caching
* Pagination
* Database indexing
* Serverless functions
* Background workers
* Load balancing

For a larger deployment, community-feed generation can use strategies such as **Fan-out on Read** or **Fan-out on Write**.

---

# 🧠 Cloud Architecture Learning

This project demonstrates how a real-world application can separate:

```text
Application Logic
       ↓
Database
       ↓
File/Object Storage
       ↓
Authentication
       ↓
Analytics
       ↓
Cloud Deployment
```

This separation makes the system easier to maintain and scale.

---

# 📊 Expected Results

The application should allow a user to:

```text
Create Profile
      ↓
Add Skill
      ↓
Create Goal
      ↓
Log Practice
      ↓
Calculate Progress
      ↓
Track Streak
      ↓
Achieve Milestone
      ↓
Share Achievement
      ↓
Receive Likes/Comments
      ↓
View Analytics
```

---

# 🚧 Limitations

The Streamlit version may have limitations compared with a full React + Firebase architecture.

Possible limitations include:

* Limited frontend customization compared with React
* Streamlit session-based interaction
* Authentication may require an external authentication solution
* Real-time social interactions may require additional backend services
* Large-scale community feeds require optimized database queries
* File storage should preferably use dedicated cloud object storage

---

# 🔮 Future Improvements

Possible future enhancements:

* Firebase Authentication
* Firebase Firestore
* Firebase Storage
* User following system
* Direct messaging
* Notifications
* Weekly progress reports
* AI-based hobby recommendations
* AI buddy matching
* Mobile application
* Advanced moderation
* Cloud Functions
* CDN integration
* Advanced analytics
* CSV data export

The original blueprint also proposes optional AI-based hobby suggestions and buddy matching using Sentence-BERT similarity.

---

# 📚 Learning Outcomes

Through this project, the following concepts are demonstrated:

* Cloud Computing
* Cloud Deployment
* Python
* Streamlit
* Database Management
* Authentication
* Authorization
* Cloud Storage
* REST APIs
* Data Analytics
* Data Visualization
* User-generated Content
* Security
* Scalability
* Git
* GitHub
* Software Testing

---

# 👩‍💻 Author

**Neha Joshi**

github : [https://github.com/Neha-Joshi05/Cloud-Hobby-Skills-Tracker.git] | linkedin : [https://www.linkedin.com/in/neha-joshi-0851a2322?utm_source=share_via&utm_content=profile&utm_medium=member_android]
---



