"""
Create a sample job description PDF for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_sample_jd_pdf():
    """Create a sample job description PDF"""
    
    filename = "sample_job_description.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1*inch, height - 1*inch, "Senior Full Stack Developer")
    
    # Company
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.4*inch, "Tech Company Inc.")
    c.drawString(1*inch, height - 1.7*inch, "Remote / Hybrid")
    
    # Job Description
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 2.2*inch, "Job Description")
    
    c.setFont("Helvetica", 11)
    description = [
        "We are seeking a talented Senior Full Stack Developer to join our growing team.",
        "You will be responsible for designing, developing, and maintaining our web applications",
        "using modern technologies and best practices."
    ]
    
    y = height - 2.5*inch
    for line in description:
        c.drawString(1*inch, y, line)
        y -= 0.25*inch
    
    # Requirements
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y - 0.3*inch, "Requirements")
    
    c.setFont("Helvetica", 11)
    requirements = [
        "• 5+ years of professional software development experience",
        "• Strong proficiency in Python and JavaScript/TypeScript",
        "• Experience with FastAPI, Django, or Flask",
        "• Frontend skills: React, Vue.js, or Angular",
        "• Database knowledge: PostgreSQL, MongoDB",
        "• Cloud platforms: AWS, GCP, or Azure",
        "• Experience with Docker and Kubernetes",
        "• Strong understanding of RESTful APIs and microservices",
        "• Excellent problem-solving and communication skills",
    ]
    
    y = y - 0.6*inch
    for req in requirements:
        c.drawString(1*inch, y, req)
        y -= 0.25*inch
    
    # Nice to Have
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, y - 0.3*inch, "Nice to Have")
    
    c.setFont("Helvetica", 11)
    nice_to_have = [
        "• Experience with CI/CD pipelines",
        "• Knowledge of GraphQL",
        "• Familiarity with machine learning concepts",
        "• Open source contributions",
    ]
    
    y = y - 0.6*inch
    for item in nice_to_have:
        c.drawString(1*inch, y, item)
        y -= 0.25*inch
    
    c.save()
    print(f"✅ Created {filename}")
    print(f"   You can use this file to test the file upload feature")


if __name__ == "__main__":
    try:
        create_sample_jd_pdf()
    except ImportError:
        print("⚠️  reportlab not installed")
        print("   Install with: pip install reportlab")
        print("\n   Or manually create a PDF file with job description text")
