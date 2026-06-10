from flask import Flask, render_template, request
import fitz
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def analyze_resume(pdf_path):

    score = 0

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    text_lower = text.lower()

    # --------------------------
    # Skills
    # --------------------------

    skills = [
        "python",
        "sql",
        "html",
        "css",
        "c",
        "dbms"
    ]

    skills_found = []
    skills_missing = []

    for skill in skills:

        if skill in text_lower:

            skills_found.append(skill)

            project_match = False

            project_patterns = [
                f"{skill} project",
                f"using {skill}",
                f"developed using {skill}",
                f"built with {skill}",
                f"{skill}-based"
            ]

            for pattern in project_patterns:
                if pattern in text_lower:
                    project_match = True
                    break

            if project_match:
                score += 10
            else:
                score += 8

        else:
            skills_missing.append(skill)

    # --------------------------
    # LinkedIn
    # --------------------------

    linkedin_found = "linkedin" in text_lower

    if linkedin_found:
        score += 5

    # --------------------------
    # GitHub
    # --------------------------

    github_found = "github" in text_lower

    if github_found:
        score += 5

    # --------------------------
    # Education
    # --------------------------

    education_keywords = [
        "education",
        "b.tech",
        "btech",
        "bachelor",
        "university",
        "college",
        "cgpa"
    ]

    education_found = any(
        word in text_lower
        for word in education_keywords
    )

    if education_found:
        score += 10

    # --------------------------
    # Projects
    # --------------------------

    project_skills = [
    "python",
    "sql",
    "html",
    "css",
    "c",
    "dbms",
    "flask",
    "javascript"
]

    project_found = any(
        word in text_lower
        for word in project_skills
    )

    if project_found:
        score += 10

    return {
        "score": score,
        "skills_found": skills_found,
        "skills_missing": skills_missing,
        "linkedin_found": linkedin_found,
        "github_found": github_found,
        "education_found": education_found,
        "project_found": project_found
    }


@app.route("/")
def home():
    return render_template("dash.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a PDF"

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(filepath)

    result = analyze_resume(filepath)

    return render_template(
        "dash.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)

