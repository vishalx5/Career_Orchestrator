import streamlit as st
from dotenv import load_dotenv
from services.resume_parser import extract_resume_text
from agents.skills_agent import discover_skills
from agents.skill_gap_agent import analyze_skill_gap
from agents.learning_agent import create_learning_pathway
from agents.market_agent import get_market_intelligence
from agents.job_matching_agent import match_jobs

load_dotenv()


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Career Orchestrator",
    page_icon="💼",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("💼 Career Orchestrator")
st.subheader("AI-Powered Inclusive Workforce Platform")

st.write(
    "A skills-first platform that helps professionals "
    "return to work through personalized career guidance."
)

st.divider()

# --------------------------------------------------
# CANDIDATE PROFILE
# --------------------------------------------------

st.header("👤 Candidate Profile")

name = st.text_input("Candidate Name")
location = st.text_input("Location")
career_goal = st.text_input("Target Career")

if st.button("Create Candidate Profile"):

    if name and location and career_goal:

        st.success("Candidate profile created successfully!")

        st.write("### Profile")
        st.write(f"**Name:** {name}")
        st.write(f"**Location:** {location}")
        st.write(f"**Career Goal:** {career_goal}")

    else:
        st.warning("Please fill in all fields.")

st.divider()

# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.header("📄 Resume Upload")

resume = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

# --------------------------------------------------
# RESUME PROCESSING
# --------------------------------------------------
resume_text = ""
if resume is not None:

    resume_text = extract_resume_text(resume)

    st.success("Resume uploaded and read successfully!")

    with st.expander("View extracted resume text"):
        st.text(resume_text)

    st.divider()

    # --------------------------------------------------
    # SKILLS DISCOVERY
    # --------------------------------------------------

    st.header("🧠 Skills Discovery")
found_technical = []
found_transferable = []

if resume_text:
    found_technical, found_transferable = discover_skills(resume_text)

   # ---------------------------------------------
# PROFESSIONAL SKILLS
# ---------------------------------------------

st.subheader("🛠️ Professional Skills")

if found_technical:
    for skill in found_technical:
        st.success(f"✓ {skill}")
else:
    st.info("No professional skills detected.")

# ---------------------------------------------
# TRANSFERABLE SKILLS
# ---------------------------------------------

st.subheader("🤝 Transferable Skills")

if found_transferable:
    for skill in found_transferable:
        st.success(f"✓ {skill}")
else:
    st.info("No transferable skills detected.")

    # --------------------------------------------------
    # SKILL GAP ANALYSIS
    # --------------------------------------------------

    st.divider()

    st.header("📊 Skill Gap Analysis")

    required_skills, missing_skills = analyze_skill_gap(
    found_technical,
    career_goal
    )

    st.write(
        f"### Target Role: "
        f"{career_goal if career_goal else 'Software Developer'}"
    )

    st.write("**Required skills for this role:**")

    for skill in required_skills:
        st.write(f"• {skill}")

    st.write("### 🚧 Skills Gap")

    if missing_skills:

        for skill in missing_skills:
            st.warning(
                f"Missing / Needs Development: {skill}"
            )

    else:

        st.success(
            "Great! The candidate has all the required skills."
        )

    # --------------------------------------------------
    # PERSONALIZED LEARNING PATHWAY
    # --------------------------------------------------

    st.divider()

    st.header("📚 Personalized Learning Pathway")

    st.write(
        "Recommended learning sequence based on the "
        "candidate's current skill gaps."
    )

    learning_path = create_learning_pathway(missing_skills)

    if learning_path:

        for index, item in enumerate(learning_path, start=1):

            st.markdown(
                f"### {index}. {item['skill']}"
            )

            st.write(
                f"**Level:** {item['level']}"
            )

            st.write(
                f"**Why learn it:** {item['why']}"
            )

            st.write(
                f"**Recommended next step:** {item['next_step']}"
            )

            st.divider()

    else:

        st.success(
            "No additional learning is required for the selected role."
        )
            # --------------------------------------------------
    # MARKET INTELLIGENCE
    # --------------------------------------------------

    st.divider()

    st.header("📈 Market Intelligence")

    st.write(
        "A market snapshot showing the skills currently "
        "associated with the candidate's target career."
    )

    market = get_market_intelligence(career_goal)
    # Market demand
    st.subheader("🔥 Market Demand")

    st.success(
        f"Demand for {career_goal if career_goal else 'Software Developer'}: "
        f"{market['demand']}"
    )

    # In-demand skills
    st.subheader("🛠️ In-Demand Skills")

    for skill in market["top_skills"]:
        st.write(f"• {skill}")

    # Market outlook
    st.subheader("📊 Market Outlook")

    st.info(market["growth"])

    # Career opportunities
    st.subheader("💼 Potential Opportunities")

    for opportunity in market["opportunities"]:
        st.write(f"• {opportunity}")
        
        # --------------------------------------------------
    # INCLUSIVE JOB MATCHING
    # --------------------------------------------------

    st.divider()

    st.header("💼 Inclusive Job Matching")

    st.write(
        "Matching career opportunities with the candidate's "
        "current skills and career goal."
    )

    matches = match_jobs(
        found_technical,
        career_goal
    )

    st.subheader("🎯 Recommended Opportunities")

    for job in matches:

        st.markdown(
            f"### 💼 {job['title']}"
        )

        st.write(
            f"**Company:** {job['company']}"
        )

        st.write(
            f"**Match Score:** {job['match_percentage']}%"
        )

        st.write(
            f"**Location:** {job['location']}"
        )

        st.write(
            f"**Job Type:** {job['type']}"
        )

        if job["matching_skills"]:

            st.write("**Skills Matched:**")

            for skill in job["matching_skills"]:
                st.write(f"✓ {skill}")

        st.divider()