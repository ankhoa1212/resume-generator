from fpdf import FPDF
import json

# Define a font variable to use throughout the file
FONT_FAMILY = "CMUSerif"
FONT_PATH = "cmunrm.ttf"  # Ensure this TTF file is in your project directory
BOLD_FONT_PATH = "cmunbx.ttf"
ITALIC_FONT_PATH = "cmunti.ttf"


class PDF(FPDF):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_font(FONT_FAMILY, "", FONT_PATH, uni=True)
        self.add_font(FONT_FAMILY, "B", BOLD_FONT_PATH, uni=True)
        self.add_font(FONT_FAMILY, "I", ITALIC_FONT_PATH, uni=True)
        self.set_font(FONT_FAMILY, "", 12)

    def header(self):
        # You can add a header with a logo or a decorative line if you like.
        pass

    def footer(self):
        # You can add a footer with page numbers here.
        pass


def load_data():
    # Load personal data from personal.json
    with open("personal.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def add_horizontal_line(pdf):
    # Draw a horizontal line across the page
    page_width = pdf.w - 2 * pdf.l_margin
    y = pdf.get_y()
    pdf.set_draw_color(0, 0, 0)
    pdf.line(pdf.l_margin, y, pdf.l_margin + page_width, y)
    pdf.ln(2)


def add_contact_info(pdf, data):
    # --- Contact Information Section ---
    pdf.set_font(FONT_FAMILY, "B", 16)
    pdf.cell(0, 10, data.get("name", "John Doe"), 0, 1, "C")
    pdf.set_font(FONT_FAMILY, "", 10)
    phone = data.get("phone", "123-456-7890")
    email = data.get("email", "johndoe@email.com")
    linkedin = data.get("linkedin", "linkedin.com/in/johndoe")
    pdf.cell(0, 5, f"{phone} | {email} | {linkedin}", 0, 1, "C")
    pdf.ln(10)
    add_horizontal_line(pdf)


def add_summary(pdf, data):
    # --- Summary Section ---
    pdf.set_font(FONT_FAMILY, "B", 12)
    pdf.cell(0, 10, "Summary", 0, 1)
    pdf.set_font(FONT_FAMILY, "", 10)
    summary_text = data.get(
        "summary",
        "Highly motivated and results-oriented professional with a strong background in software development and project management. Seeking to leverage skills in a challenging new role.",
    )
    pdf.multi_cell(0, 5, summary_text)
    pdf.ln(5)


def add_education(pdf, data):
    # --- Education Section ---
    pdf.set_font(FONT_FAMILY, "B", 12)
    pdf.cell(0, 10, "Education", 0, 1)
    for edu in data.get("education", []):
        pdf.set_font(FONT_FAMILY, "B", 10)
        school = edu.get("school", "")
        year = edu.get("year", "")
        # School left, year right, same line
        pdf.cell(0, 5, school, 0, 0, "L")
        pdf.set_font(FONT_FAMILY, "", 10)  # unbold the year
        pdf.cell(0, 5, year, 0, 1, "R")

        pdf.set_font(FONT_FAMILY, "", 10)
        degree = edu.get("degree", "")
        pdf.cell(0, 5, degree, 0, 1)
        pdf.ln(5)
    add_horizontal_line(pdf)


def add_experience(pdf, data):
    # --- Experience Section ---
    pdf.set_font(FONT_FAMILY, "B", 12)
    pdf.cell(0, 10, "Experience", 0, 1)

    for job in data.get("experience", []):
        company = job.get("company", "")
        title = job.get("title", "")
        location = job.get("location", "")
        dates = job.get("dates", "")

        # Company (bold), Title (italic), location (regular) left; dates right
        pdf.set_font(FONT_FAMILY, "B", 10)
        left_text = company
        pdf.cell(pdf.get_string_width(left_text), 5, left_text, 0, 0, "L")

        pdf.set_font(FONT_FAMILY, "I", 10)
        title_text = f", {title}" if title else ""
        pdf.cell(pdf.get_string_width(title_text), 5, title_text, 0, 0, "L")

        if location:
            pdf.set_font(FONT_FAMILY, "", 10)
            location_text = f" ({location})"
            pdf.cell(pdf.get_string_width(location_text), 5, location_text, 0, 0, "L")

        pdf.set_font(FONT_FAMILY, "", 10)
        pdf.cell(0, 5, dates, 0, 1, "R")

        pdf.set_font(FONT_FAMILY, "", 10)
        for bullet in job.get("bullets", []):
            pdf.multi_cell(0, 5, f"- {bullet}")
        pdf.ln(5)
    add_horizontal_line(pdf)


def add_projects(pdf, data):
    # --- Projects Section ---
    pdf.set_font(FONT_FAMILY, "B", 12)
    pdf.cell(0, 10, "Projects", 0, 1)

    for project in data.get("projects", []):
        name = project.get("name", "")
        technologies = project.get("technologies", [])
        dates = project.get("dates", "")
        bullets = project.get("bullets", [])

        # Project name (bold) left, dates right
        pdf.set_font(FONT_FAMILY, "B", 10)
        pdf.cell(0, 5, name, 0, 0, "L")
        pdf.set_font(FONT_FAMILY, "", 10)
        pdf.cell(0, 5, dates, 0, 1, "R")

        # Technologies used
        if technologies:
            tech_text = f"Technologies: {', '.join(technologies)}"
            pdf.set_font(FONT_FAMILY, "I", 10)
            pdf.cell(0, 5, tech_text, 0, 1)

        # Bullet points
        pdf.set_font(FONT_FAMILY, "", 10)
        for bullet in bullets:
            pdf.multi_cell(0, 5, f"- {bullet}")
        pdf.ln(5)

    add_horizontal_line(pdf)


def add_skills(pdf, data):
    # --- Skills Section ---
    pdf.set_font(FONT_FAMILY, "B", 12)
    pdf.cell(0, 10, "Skills", 0, 1)
    pdf.set_font(FONT_FAMILY, "", 10)
    skills = data.get("skills", {})
    skills_text = ""
    for category, items in skills.items():
        skills_text += f"{category}: {', '.join(items)}\n"
    pdf.multi_cell(0, 5, skills_text.strip())
    add_horizontal_line(pdf)


def create_resume_pdf(pdf):
    data = load_data()  # load personal data

    # Set up basic document properties
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font(FONT_FAMILY, "", 12)

    add_contact_info(pdf, data)
    add_education(pdf, data)
    add_skills(pdf, data)
    add_experience(pdf, data)
    add_projects(pdf, data)


if __name__ == "__main__":
    pdf = PDF(unit="mm")
    create_resume_pdf(pdf)
    pdf.output("resume.pdf")
    print("Resume generated as resume.pdf")
