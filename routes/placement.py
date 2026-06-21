from flask import (
    Blueprint,
    render_template,
    request,
    jsonify
)

bp = Blueprint(
    "placement",
    __name__,
    url_prefix="/placement"
)


# ==========================================
# Placement Assistant Page
# ==========================================

@bp.route("/")
def index():

    return render_template(
        "placement/index.html"
    )


# ==========================================
# Placement Assistant API
# ==========================================

@bp.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json() or {}

    role = data.get(
        "role",
        ""
    ).strip().lower()

    questions = []

    # ==========================================
    # Cyber Security
    # ==========================================

    if any(x in role for x in [
        "cyber security",
        "cybersecurity",
        "security analyst",
        "soc analyst",
        "ethical hacker",
        "penetration tester"
    ]):

        questions = [
            "What is Phishing?",
            "What is SQL Injection?",
            "What is XSS?",
            "What is CSRF?",
            "What is IDS?",
            "What is IPS?",
            "Explain CIA Triad.",
            "What is OWASP Top 10?",
            "What is Firewall?",
            "What is VPN?"
        ]

    # ==========================================
    # Network Engineer
    # ==========================================

    elif any(x in role for x in [
        "network engineer",
        "network administrator",
        "networking"
    ]):

        questions = [
            "Explain OSI Model.",
            "Difference between TCP and UDP?",
            "What is DNS?",
            "What is DHCP?",
            "What is NAT?",
            "What is ARP?",
            "What is Routing?",
            "What is Subnetting?",
            "What is VLAN?",
            "Difference between Hub and Switch?"
        ]

    # ==========================================
    # Data Analyst
    # ==========================================

    elif any(x in role for x in [
        "data analyst",
        "business analyst",
        "data science",
        "data scientist"
    ]):

        questions = [
            "What is Data Cleaning?",
            "What is Data Visualization?",
            "Difference between SQL and NoSQL?",
            "What is Pandas?",
            "What is NumPy?",
            "What is Power BI?",
            "What is Tableau?",
            "Explain ETL Process.",
            "What is Data Mining?",
            "What is Dashboard?"
        ]

    # ==========================================
    # Cloud Engineer
    # ==========================================

    elif any(x in role for x in [
        "cloud engineer",
        "cloud architect",
        "aws",
        "azure",
        "gcp"
    ]):

        questions = [
            "What is Cloud Computing?",
            "What is AWS EC2?",
            "What is S3?",
            "What is IAM?",
            "What is VPC?",
            "What is Load Balancer?",
            "What is Auto Scaling?",
            "What is Docker?",
            "What is Kubernetes?",
            "Difference between IaaS, PaaS and SaaS?"
        ]

    # ==========================================
    # DevOps
    # ==========================================

    elif any(x in role for x in [
        "devops",
        "site reliability",
        "sre"
    ]):

        questions = [
            "What is CI/CD?",
            "What is Jenkins?",
            "What is Docker?",
            "What is Kubernetes?",
            "What is GitHub Actions?",
            "What is Terraform?",
            "What is Ansible?",
            "What is Monitoring?",
            "What is Infrastructure as Code?",
            "Explain Blue-Green Deployment."
        ]

    # ==========================================
    # AI / ML Engineer
    # ==========================================

    elif any(x in role for x in [
        "ai engineer",
        "machine learning",
        "ml engineer",
        "artificial intelligence"
    ]):

        questions = [
            "What is Machine Learning?",
            "Difference between AI and ML?",
            "What is Supervised Learning?",
            "What is Unsupervised Learning?",
            "What is Overfitting?",
            "What is Underfitting?",
            "What is Neural Network?",
            "What is Deep Learning?",
            "What is LLM?",
            "What is Prompt Engineering?"
        ]

    # ==========================================
    # Software Engineer
    # ==========================================

    elif any(x in role for x in [
        "software engineer",
        "software developer",
        "full stack",
        "backend",
        "frontend",
        "web developer",
        "python developer",
        "java developer",
        "mern"
    ]):

        questions = [
            "What is OOP?",
            "Difference between List and Tuple?",
            "What is REST API?",
            "What is JSON?",
            "What is Git?",
            "What is Database Normalization?",
            "Difference between Stack and Queue?",
            "What is Multithreading?",
            "What is Exception Handling?",
            "What is MVC Architecture?"
        ]

    # ==========================================
    # Default HR Round
    # ==========================================

    else:

        questions = [
            "Tell me about yourself.",
            "What are your strengths?",
            "What are your weaknesses?",
            "Why should we hire you?",
            "Why do you want this role?",
            "Describe a challenge you faced.",
            "What motivates you?",
            "Where do you see yourself in 5 years?",
            "How do you handle pressure?",
            "Do you have any questions for us?"
        ]

    return jsonify({
        "success": True,
        "role": role,
        "questions": questions
    })