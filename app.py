# AI Resume Generator (Desktop App - Local Version)

# --- Library Imports ---
import tkinter as tk
from tkinter import messagebox, scrolledtext, LabelFrame, Frame, Label, Entry, Button, Checkbutton, BooleanVar
import requests
import json
import textwrap
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, HRFlowable, Table
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
from reportlab.lib.colors import black, blue
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.colors import black, blue

# --- Configuration ---
# You need to get your own API key from Google AI Studio and paste it here.
# Follow these steps:
# 1. Go to https://aistudio.google.com/app/apikey
# 2. Click "Create API Key in new project"
# 3. Copy the key and paste it below, replacing the placeholder text.
API_KEY = "AIzaSyAuMzoW6zw4-zVY8Ebfk4NcR2nsRTo6WY8"

class AIResumeApp:
    """
    Main application class for the AI Resume Generator.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume & Cover Letter Generator")
        self.root.geometry("780x800")
        self.root.configure(bg='#f0f0f0')

        self.main_frame = Frame(root, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill='both')

        # Use a canvas and scrollbar to make the main frame scrollable
        self.canvas = tk.Canvas(self.main_frame, bg='#f0f0f0')
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg='#f0f0f0', padx=20, pady=20)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.work_experience_frames = []
        self.project_frames = []
        self.achievement_frames = []
        self.create_widgets()

    def create_widgets(self):
        """Builds the main UI elements."""
        title_label = Label(self.scrollable_frame, text="AI Resume & Cover Letter Generator", font=("Helvetica", 24, "bold"), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=(0, 20))

        # Core Details Frame
        self.core_details_frame = LabelFrame(self.scrollable_frame, text="Core Details", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        self.core_details_frame.pack(fill='x', pady=10)

        Label(self.core_details_frame, text="Name:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = Entry(self.core_details_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, "John Doe")
        
        Label(self.core_details_frame, text="Contact Info:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.contact_info_entry = Entry(self.core_details_frame, width=30)
        self.contact_info_entry.grid(row=1, column=1, padx=5, pady=5)
        self.contact_info_entry.insert(0, "john.doe@email.com | (555) 555-5555 | linkedin.com/in/johndoe")

        Label(self.core_details_frame, text="Job Title:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.job_title_entry = Entry(self.core_details_frame, width=30)
        self.job_title_entry.grid(row=2, column=1, padx=5, pady=5)
        
        Label(self.core_details_frame, text="Domain:", bg='white').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.domain_entry = Entry(self.core_details_frame, width=30)
        self.domain_entry.grid(row=3, column=1, padx=5, pady=5)

        Label(self.core_details_frame, text="Years of Experience:", bg='white').grid(row=4, column=0, sticky='w', padx=5, pady=5)
        self.years_entry = Entry(self.core_details_frame, width=30)
        self.years_entry.grid(row=4, column=1, padx=5, pady=5)

        # Summary Frame
        summary_frame = LabelFrame(self.scrollable_frame, text="Professional Summary", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        summary_frame.pack(fill='x', pady=10)
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, height=5)
        self.summary_text.pack(fill='both', expand=True, padx=5, pady=5)

        generate_summary_btn = Button(summary_frame, text="Generate Summary", command=self.generate_summary, bg='#3498db', fg='white', font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        generate_summary_btn.pack(pady=5)
        
        # Work Experience Frame
        self.work_experience_container = LabelFrame(self.scrollable_frame, text="Work Experience", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        self.work_experience_container.pack(fill='x', pady=10)
        
        self.add_work_btn = Button(self.work_experience_container, text="Add Job", command=self.add_work_experience, bg='#555', fg='white', relief=tk.RAISED)
        self.add_work_btn.pack(side=tk.TOP, pady=5)

        # Skills Frame
        skills_frame = LabelFrame(self.scrollable_frame, text="Skills", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        skills_frame.pack(fill='x', pady=10)
        Label(skills_frame, text="List your skills (comma-separated):", bg='white').pack(anchor='w', padx=5, pady=2)
        self.skills_text = scrolledtext.ScrolledText(skills_frame, wrap=tk.WORD, height=3)
        self.skills_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Education Frame
        education_frame = LabelFrame(self.scrollable_frame, text="Education", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        education_frame.pack(fill='x', pady=10)
        Label(education_frame, text="Education Details (semicolon-separated):", bg='white').pack(anchor='w', padx=5, pady=2)
        self.education_text = scrolledtext.ScrolledText(education_frame, wrap=tk.WORD, height=3)
        self.education_text.pack(fill='both', expand=True, padx=5, pady=5)

        # Projects Frame
        self.projects_container = LabelFrame(self.scrollable_frame, text="Projects", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        self.projects_container.pack(fill='x', pady=10)
        
        self.add_project_btn = Button(self.projects_container, text="Add Project", command=self.add_project, bg='#555', fg='white', relief=tk.RAISED)
        self.add_project_btn.pack(side=tk.TOP, pady=5)
        
        # Achievements & Certifications Frame
        self.achievements_container = LabelFrame(self.scrollable_frame, text="Achievements & Certifications", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        self.achievements_container.pack(fill='x', pady=10)
        
        self.add_achievement_btn = Button(self.achievements_container, text="Add Achievement", command=self.add_achievement, bg='#555', fg='white', relief=tk.RAISED)
        self.add_achievement_btn.pack(side=tk.TOP, pady=5)

        # Cover Letter Frame
        self.generate_cl_var = BooleanVar()
        cl_frame = LabelFrame(self.scrollable_frame, text="Cover Letter", font=("Helvetica", 12, "bold"), padx=10, pady=10, bg='white', fg='#333')
        cl_frame.pack(fill='x', pady=10)
        
        cl_check = Checkbutton(cl_frame, text="Generate a Cover Letter", variable=self.generate_cl_var, bg='white')
        cl_check.pack(anchor='w', padx=5, pady=5)
        
        self.cl_details_frame = Frame(cl_frame, bg='white')
        self.cl_details_frame.pack(fill='x')
        
        Label(self.cl_details_frame, text="Target Company:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.target_company_entry = Entry(self.cl_details_frame, width=30)
        self.target_company_entry.grid(row=0, column=1, padx=5, pady=5)
        
        Label(self.cl_details_frame, text="Key Skill from Job Desc:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.cl_skill_entry = Entry(self.cl_details_frame, width=30)
        self.cl_skill_entry.grid(row=1, column=1, padx=5, pady=5)
        
        Label(self.cl_details_frame, text="Key Responsibility from Job Desc:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.cl_resp_entry = Entry(self.cl_details_frame, width=30)
        self.cl_resp_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.generate_cl_var.trace_add('write', self.toggle_cl_details)
        self.toggle_cl_details()

        # Action Buttons Frame
        button_frame = Frame(self.scrollable_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)

        generate_pdf_btn = Button(button_frame, text="Generate & Save PDF", command=self.generate_pdf, bg='#27ae60', fg='white', font=("Helvetica", 12, "bold"), relief=tk.RAISED, padx=10, pady=5)
        generate_pdf_btn.pack(side=tk.LEFT, padx=10)

        # Initial call to add first sections
        self.add_work_experience()
        self.add_project()
        self.add_achievement()

    def toggle_cl_details(self, *args):
        if self.generate_cl_var.get():
            self.cl_details_frame.pack(fill='x')
        else:
            self.cl_details_frame.pack_forget()

    def add_work_experience(self):
        work_frame = LabelFrame(self.work_experience_container, padx=10, pady=10, bg='white')
        work_frame.pack(fill='x', pady=5)

        fields_frame = Frame(work_frame, bg='white')
        fields_frame.pack(fill='x')
        
        Label(fields_frame, text="Company:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        company_entry = Entry(fields_frame, width=30)
        company_entry.grid(row=0, column=1, padx=5, pady=2)

        Label(fields_frame, text="Job Title:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        job_title_entry = Entry(fields_frame, width=30)
        job_title_entry.grid(row=1, column=1, padx=5, pady=2)
        
        Label(fields_frame, text="Dates:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=2)
        dates_entry = Entry(fields_frame, width=30)
        dates_entry.grid(row=2, column=1, padx=5, pady=2)

        Label(work_frame, text="Responsibilities (comma-separated for AI):", bg='white').pack(anchor='w', padx=5, pady=2)
        resp_entry = Entry(work_frame, width=60)
        resp_entry.pack(fill='x', padx=5, pady=5)
        
        Label(work_frame, text="Bullet Points:", bg='white').pack(anchor='w', padx=5, pady=2)
        bullet_text = scrolledtext.ScrolledText(work_frame, wrap=tk.WORD, height=4)
        bullet_text.pack(fill='both', padx=5, pady=5)
        
        gen_bullets_btn = Button(work_frame, text="Generate Bullets", command=lambda: self.generate_bullets(
            company_entry, job_title_entry, resp_entry, bullet_text
        ), bg='#3498db', fg='white', font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        gen_bullets_btn.pack(pady=5)
        
        remove_btn = Button(work_frame, text="Remove", command=lambda: self.remove_section(work_frame, self.work_experience_frames), bg='#e74c3c', fg='white', relief=tk.RAISED)
        remove_btn.pack(pady=5)

        self.work_experience_frames.append({
            'frame': work_frame,
            'company': company_entry,
            'job_title': job_title_entry,
            'dates': dates_entry,
            'responsibilities': resp_entry,
            'bullets': bullet_text
        })
        self.update_scrollregion()

    def add_project(self):
        project_frame = LabelFrame(self.projects_container, padx=10, pady=10, bg='white')
        project_frame.pack(fill='x', pady=5)
        
        Label(project_frame, text="Project Name:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        project_name_entry = Entry(project_frame, width=30)
        project_name_entry.grid(row=0, column=1, padx=5, pady=2)
        
        gen_desc_btn = Button(project_frame, text="Generate Description", command=lambda: self.generate_project_desc(
            project_name_entry, project_desc_text
        ), bg='#3498db', fg='white', font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        gen_desc_btn.grid(row=0, column=2, padx=10, pady=2)
        
        Label(project_frame, text="Project Description:", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        project_desc_text = scrolledtext.ScrolledText(project_frame, wrap=tk.WORD, height=4)
        project_desc_text.grid(row=2, column=0, columnspan=3, sticky='ew', padx=5, pady=5)

        remove_btn = Button(project_frame, text="Remove", command=lambda: self.remove_section(project_frame, self.project_frames), bg='#e74c3c', fg='white', font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        remove_btn.grid(row=3, columnspan=3, pady=5)

        self.project_frames.append({
            'frame': project_frame,
            'name': project_name_entry,
            'description': project_desc_text
        })
        self.update_scrollregion()
        
    def add_achievement(self):
        achievement_frame = LabelFrame(self.achievements_container, padx=10, pady=10, bg='white')
        achievement_frame.pack(fill='x', pady=5)
        
        Label(achievement_frame, text="Achievement Title:", bg='white').grid(row=0, column=0, sticky='w', padx=5, pady=2)
        ach_title_entry = Entry(achievement_frame, width=30)
        ach_title_entry.grid(row=0, column=1, padx=5, pady=2)
        
        Label(achievement_frame, text="URL (Optional):", bg='white').grid(row=1, column=0, sticky='w', padx=5, pady=2)
        ach_url_entry = Entry(achievement_frame, width=30)
        ach_url_entry.grid(row=1, column=1, padx=5, pady=2)
        
        gen_desc_btn = Button(achievement_frame, text="Generate Description", command=lambda: self.generate_achievement_desc(
            ach_title_entry, ach_desc_text
        ), bg='#3498db', fg='white', font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        gen_desc_btn.grid(row=0, column=2, padx=10, pady=2)
        
        Label(achievement_frame, text="Description:", bg='white').grid(row=2, column=0, sticky='w', padx=5, pady=2)
        ach_desc_text = scrolledtext.ScrolledText(achievement_frame, wrap=tk.WORD, height=4)
        ach_desc_text.grid(row=3, column=0, columnspan=3, sticky='ew', padx=5, pady=5)

        remove_btn = Button(achievement_frame, text="Remove", command=lambda: self.remove_section(achievement_frame, self.achievement_frames), bg='#e74c3c', fg='white', font=("Helvetica", 10, "bold"), relief=tk.RAISED)
        remove_btn.grid(row=4, columnspan=3, pady=5)

        self.achievement_frames.append({
            'frame': achievement_frame,
            'title': ach_title_entry,
            'url': ach_url_entry,
            'description': ach_desc_text
        })
        self.update_scrollregion()

    def remove_section(self, frame, frame_list):
        for i, item in enumerate(frame_list):
            if item['frame'] == frame:
                frame.destroy()
                del frame_list[i]
                break
        self.update_scrollregion()
        
    def update_scrollregion(self):
        self.root.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def call_gemini_api(self, prompt):
        """Sends a request to the Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "tools": [{"google_search": {}}]
        }
        
        if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
            messagebox.showerror("API Error", "Please provide a valid Gemini API key.")
            return "API key is missing."

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            return result['candidates'][0]['content']['parts'][0].get('text', '')
        except Exception as e:
            messagebox.showerror("API Error", f"An error occurred: {e}")
            return "Failed to generate content."

    def generate_summary(self):
        """Generates a professional summary and updates the UI."""
        job_title = self.job_title_entry.get()
        domain = self.domain_entry.get()
        years = self.years_entry.get()

        if not all([job_title, domain, years]):
            messagebox.showwarning("Missing Info", "Please fill in Job Title, Domain, and Years of Experience.")
            return

        prompt = f"Write a 3-4 sentence professional summary for a resume. The candidate is a {job_title} with {years}+ years of experience in the {domain} sector. The summary should highlight key skills and professional goals."
        
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert('1.0', "Generating summary...")
        self.root.update_idletasks()
        
        summary = self.call_gemini_api(textwrap.dedent(prompt))
        
        self.summary_text.delete('1.0', tk.END)
        self.summary_text.insert('1.0', summary)

    def generate_bullets(self, company_entry, job_title_entry, resp_entry, bullet_text_widget):
        """Generates bullet points for a single work experience entry."""
        company = company_entry.get()
        job_title = job_title_entry.get()
        responsibilities = resp_entry.get().split(',')

        if not all([company, job_title, responsibilities]):
            messagebox.showwarning("Missing Info", "Please fill in Company, Job Title, and Responsibilities.")
            return
        
        # Updated prompt to remove introductory text
        prompt = f"Write 3 to 4 impactful bullet points for a resume. The role is {job_title} at {company}. The responsibilities include: {', '.join(responsibilities)}. The bullet points must start with a strong action verb and highlight accomplishments. Do not include any introductory sentences like 'Here are the bullet points...' or 'Here are 3-4 impactful bullet points...' Just provide the bullet points."
        
        bullet_text_widget.delete('1.0', tk.END)
        bullet_text_widget.insert('1.0', "Generating bullet points...")
        self.root.update_idletasks()
        
        bullets = self.call_gemini_api(textwrap.dedent(prompt))
        
        bullet_text_widget.delete('1.0', tk.END)
        bullet_text_widget.insert('1.0', bullets.replace('**', ''))

    def generate_project_desc(self, project_name_entry, desc_text_widget):
        """Generates a project description."""
        project_name = project_name_entry.get()
        domain = self.domain_entry.get()
        skills = self.skills_text.get('1.0', tk.END).strip().replace('\n', '')

        if not all([project_name, domain, skills]):
            messagebox.showwarning("Missing Info", "Please fill in Project Name, Domain, and Skills.")
            return

        # Updated prompt to remove introductory text
        prompt = f"Write 3-4 impactful bullet points for a resume project section. The project is titled {project_name}. It belongs to the {domain} domain. The skills used are: {skills}. The bullet points must start with an action verb and highlight the project's impact and key achievements. Do not include any introductory sentences like 'Here are the bullet points...' or 'Here are 3-4 impactful bullet points...' Just provide the bullet points."
        
        desc_text_widget.delete('1.0', tk.END)
        desc_text_widget.insert('1.0', "Generating description...")
        self.root.update_idletasks()
        
        description = self.call_gemini_api(textwrap.dedent(prompt))
        
        desc_text_widget.delete('1.0', tk.END)
        desc_text_widget.insert('1.0', description.replace('**', ''))
        
    def generate_achievement_desc(self, ach_title_entry, ach_desc_text_widget):
        """Generates a description for an achievement."""
        ach_title = ach_title_entry.get()
        if not ach_title:
            messagebox.showwarning("Missing Info", "Please enter the Achievement Title.")
            return
            
        prompt = f"Write a brief, impactful description (1-2 sentences) for a resume achievement or certification. The title is: {ach_title}. Focus on the accomplishment and its value. Do not include any introductory sentences like 'Here is a description...'"

        ach_desc_text_widget.delete('1.0', tk.END)
        ach_desc_text_widget.insert('1.0', "Generating description...")
        self.root.update_idletasks()
        
        description = self.call_gemini_api(textwrap.dedent(prompt))
        
        ach_desc_text_widget.delete('1.0', tk.END)
        ach_desc_text_widget.insert('1.0', description)

    def get_data(self):
        """Collects all data from the UI and returns a dictionary."""
        work_experience = []
        for frame_dict in self.work_experience_frames:
            work_experience.append({
                'company': frame_dict['company'].get(),
                'job_title': frame_dict['job_title'].get(),
                'dates': frame_dict['dates'].get(),
                'bullet_points': frame_dict['bullets'].get('1.0', tk.END).strip().split('\n')
            })

        projects = []
        for frame_dict in self.project_frames:
            projects.append({
                'name': frame_dict['name'].get(),
                'description': frame_dict['description'].get('1.0', tk.END).strip()
            })
            
        achievements = []
        for frame_dict in self.achievement_frames:
            achievements.append({
                'title': frame_dict['title'].get(),
                'url': frame_dict['url'].get(),
                'description': frame_dict['description'].get('1.0', tk.END).strip()
            })

        return {
            "name": self.name_entry.get(),
            "contact_info": self.contact_info_entry.get(),
            "job_title": self.job_title_entry.get(),
            "domain": self.domain_entry.get(),
            "years_of_experience": self.years_entry.get(),
            "summary": self.summary_text.get('1.0', tk.END).strip(),
            "work_experience": work_experience,
            "skills": [s.strip() for s in self.skills_text.get('1.0', tk.END).strip().split(',')],
            "education": [e.strip() for e in self.education_text.get('1.0', tk.END).strip().split(';')],
            "projects": projects,
            "achievements": achievements,
            "generate_cover_letter": self.generate_cl_var.get(),
            "target_company": self.target_company_entry.get(),
            "job_description": {
                "key_skill_1": self.cl_skill_entry.get(),
                "key_responsibility_1": self.cl_resp_entry.get()
            }
        }

    def generate_pdf(self):
        """Gathers data and generates a PDF file."""
        data = self.get_data()

        if not data["summary"]:
            messagebox.showwarning("Missing Summary", "Please generate a summary first.")
            return

        # Resume PDF
        resume_doc = SimpleDocTemplate("resume.pdf", pagesize=letter)
        resume_story = self._build_resume_story(data)
        
        try:
            resume_doc.build(resume_story)
            messagebox.showinfo("Success", "PDF resume saved as 'resume.pdf' in the same directory.")
        except Exception as e:
            messagebox.showerror("PDF Error", f"Failed to generate resume PDF: {e}")
            return
        
        # Cover Letter PDF
        if data['generate_cover_letter']:
            cover_letter_doc = SimpleDocTemplate("cover_letter.pdf", pagesize=letter)
            cover_letter_story = self._build_cover_letter_story(data)
            
            try:
                cover_letter_doc.build(cover_letter_story)
                messagebox.showinfo("Success", "PDF cover letter saved as 'cover_letter.pdf'.")
            except Exception as e:
                messagebox.showerror("PDF Error", f"Failed to generate cover letter PDF: {e}")

    def _build_resume_story(self, data):
        """Builds the story for the resume PDF."""
        styles = getSampleStyleSheet()
        story = []

        header_style = ParagraphStyle('Header', parent=styles['Heading1'], fontSize=24, spaceAfter=6, textColor=black, alignment=TA_JUSTIFY)
        contact_style = ParagraphStyle('Contact', parent=styles['Normal'], fontSize=10, spaceAfter=24, textColor=black)
        section_title_style = ParagraphStyle('SectionTitle', parent=styles['Heading2'], fontSize=14, spaceAfter=8, textColor=black)
        section_body_style = ParagraphStyle('SectionBody', parent=styles['Normal'], fontSize=10, spaceAfter=12)
        job_title_style = ParagraphStyle('JobTitle', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold', spaceBefore=6, spaceAfter=2)
        job_dates_style = ParagraphStyle('JobDates', parent=styles['Normal'], fontSize=10, textColor=black)
        bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], fontSize=10, leftIndent=18, bulletIndent=0)
        
        # Name and Contact Info
        story.append(Paragraph(data["name"], header_style))
        contact_info_text = self._format_contact_info(data["contact_info"])
        story.append(Paragraph(contact_info_text, contact_style))
        story.append(Spacer(1, 12))
        
        story.append(HRFlowable(width="100%", thickness=1, color=black))
        story.append(Spacer(1, 12))

        # Summary
        story.append(Paragraph("Summary", section_title_style))
        summary_text = data["summary"].replace('**', '')
        story.append(Paragraph(summary_text, section_body_style))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=1, color=black))
        story.append(Spacer(1, 12))

        # Work Experience
        if data['work_experience']:
            story.append(Paragraph("Work Experience", section_title_style))
            for job in data['work_experience']:
                story.append(Paragraph(f"<b>{job['job_title']}</b> at {job['company']}", job_title_style))
                story.append(Paragraph(job['dates'], job_dates_style))
                list_items = [ListItem(Paragraph(bp, bullet_style)) for bp in job['bullet_points'] if bp.strip()]
                story.append(ListFlowable(list_items, bulletType='bullet', start='circle', bulletFontSize=8, leftIndent=15))
                story.append(Spacer(1, 12))
            story.append(HRFlowable(width="100%", thickness=1, color=black))
            story.append(Spacer(1, 12))

        # Projects
        if data['projects']:
            story.append(Paragraph("Projects", section_title_style))
            for proj in data['projects']:
                if proj['description'].strip():
                    story.append(Paragraph(f"<b>{proj['name']}</b>", job_title_style))
                    bullet_points = proj['description'].strip().split('\n')
                    list_items = [ListItem(Paragraph(bp, bullet_style)) for bp in bullet_points if bp.strip()]
                    story.append(ListFlowable(list_items, bulletType='bullet', start='circle', bulletFontSize=8, leftIndent=15))
                    story.append(Spacer(1, 12))
            story.append(HRFlowable(width="100%", thickness=1, color=black))
            story.append(Spacer(1, 12))

        # Achievements & Certifications
        if data['achievements']:
            story.append(Paragraph("Achievements & Certifications", section_title_style))
            for ach in data['achievements']:
                if ach['title'].strip():
                    if ach['url'].strip():
                        story.append(Paragraph(f"<link href='{ach['url']}'><u><b>{ach['title']}</b></u></link>", job_title_style))
                    else:
                        story.append(Paragraph(f"<b>{ach['title']}</b>", job_title_style))
                    
                    if ach['description'].strip():
                        story.append(Paragraph(ach['description'], section_body_style))
                        story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=1, color=black))
            story.append(Spacer(1, 12))
        
        # Skills
        if data['skills']:
            story.append(Paragraph("Skills", section_title_style))
            story.append(Paragraph(", ".join(data['skills']), section_body_style))
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=1, color=black))
            story.append(Spacer(1, 12))

        # Education
        if data['education']:
            story.append(Paragraph("Education", section_title_style))
            for edu_str in data['education']:
                parts = edu_str.split(',')
                if len(parts) >= 2:
                    institution = parts[0].strip()
                    degree = parts[1].strip()
                    year = parts[2].strip() if len(parts) > 2 else ''

                    edu_table_style = ParagraphStyle('EducationTable', parent=styles['Normal'], fontSize=10, leading=12)
                    
                    # Institution and Year
                    institution_para = Paragraph(f"<b>{institution}</b>", edu_table_style)
                    year_para = Paragraph(f"{year}", ParagraphStyle('Year', parent=edu_table_style, alignment=TA_RIGHT))
                    
                    story.append(Table([[institution_para, year_para]], colWidths=[4*inch, 2*inch], style=[('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0)]))
                    
                    # Degree
                    story.append(Paragraph(degree, ParagraphStyle('Degree', parent=edu_table_style, spaceAfter=12)))
                    
                else:
                    story.append(Paragraph(edu_str, section_body_style))
            story.append(HRFlowable(width="100%", thickness=1, color=black))
            story.append(Spacer(1, 12))

        return story

    def _format_contact_info(self, text):
        """Formats contact info with hyperlinks."""
        parts = text.split('|')
        formatted_parts = []
        for part in parts:
            part = part.strip()
            # Simple regex to find common URL patterns
            url_match = re.search(r'(https?://\S+)', part)
            if url_match:
                url = url_match.group(0)
                link_text = part.replace(url, '').strip()
                if not link_text:
                    if 'linkedin' in url:
                        link_text = 'LinkedIn'
                    elif 'github' in url:
                        link_text = 'GitHub'
                    else:
                        link_text = 'Website'
                formatted_parts.append(f"<link href='{url}'><u><font color='blue'>{link_text}</font></u></link>")
            else:
                formatted_parts.append(part)
        return " | ".join(formatted_parts)

    def _build_cover_letter_story(self, data):
        """Builds the story for the cover letter PDF."""
        # Use a generic job title if not provided for a less structured prompt
        job_title = data['job_title'] if data['job_title'].strip() else "the advertised position"
        target_company = data['target_company'] if data['target_company'].strip() else "Hiring Manager"

        prompt = f"""
        Generate a professional, well-formatted cover letter addressed to the Hiring Manager at {target_company} for the role of {job_title}.

        **Crucial Instruction:** Immediately begin the letter with "Dear Hiring Manager," followed by the body paragraphs. Do NOT include any placeholders, introductory, or conversational text outside the letter's content.

        **Candidate Data:**
        - Name: {data['name']}
        - Job Title/Target: {data['job_title']}
        - Experience: {data['years_of_experience']} years in {data['domain']}
        - Key Skills: {', '.join(data['skills'])}
        - Relevant Experience Summary (if available): {json.dumps(data['work_experience'])}

        **Job Alignment Focus:**
        - Target Company: {data['target_company']}
        - Key Skill Match: {data['job_description']['key_skill_1']}
        - Key Responsibility Match: {data['job_description']['key_responsibility_1']}
        """

        cover_letter_content = self.call_gemini_api(textwrap.dedent(prompt))

        styles = getSampleStyleSheet()
        story = []
        
        # Header and Date (will be handled by the PDF building logic later)
        
        # --- Start of Letter Content ---
        
        # 1. Add Dear Hiring Manager/Recipient
        recipient = data['target_company'] if data['target_company'].strip() else "Hiring Manager"
        story.append(Paragraph(f"Dear {recipient},", styles['Normal']))
        story.append(Spacer(1, 12))

        # 2. Add Body Paragraphs (split by double newline)
        paragraphs = [Paragraph(p.strip(), styles['Normal']) for p in cover_letter_content.split('\n\n') if p.strip()]
        story.extend(paragraphs)
        
        # 3. Closing
        story.append(Spacer(1, 12))
        story.append(Paragraph("Sincerely,", styles['Normal']))
        story.append(Paragraph(data['name'], styles['h2']))

        return story
        
    def _get_cover_letter_prompt(self, data):
        # This function remains for consistency but the prompt logic is now embedded directly in _build_cover_letter_story
        # for more immediate control over the final output format.
        return f"""
        Generate a professional, well-formatted cover letter. Do NOT include any conversational or template placeholders.

        **Crucial Instruction:** Immediately begin the letter with "Dear Hiring Manager," followed by the body paragraphs.

        **Candidate Data:**
        - Name: {data['name']}
        - Job Title/Target: {data['job_title']}
        - Experience: {data['years_of_experience']} years in {data['domain']}
        - Key Skills: {', '.join(data['skills'])}
        - Relevant Experience Summary (if available): {json.dumps(data['work_experience'])}

        **Job Alignment Focus:**
        - Target Company: {data['target_company']}
        - Key Skill Match: {data['job_description']['key_skill_1']}
        - Key Responsibility Match: {data['job_description']['key_responsibility_1']}
        """

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AIResumeApp(root)
    root.mainloop()
