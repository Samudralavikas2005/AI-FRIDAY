# study_planner/pdf_generator.py
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class PDFGenerator:
    def __init__(self):
        pass
    
    def create_study_pdf(self, study_plan, filename="study_plan.pdf"):
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph("Smart Study Plan", title_style))
            story.append(Spacer(1, 20))
            
            # Summary
            summary_style = ParagraphStyle(
                'Summary',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=12
            )
            
            total_days = len(study_plan.get('daily_schedule', {}))
            total_subjects = len(study_plan.get('subjects', []))
            hours_per_day = study_plan.get('available_hours_per_day', 4)
            
            summary_text = f"""
            <b>Study Plan Summary:</b><br/>
            • Total Subjects: {total_subjects}<br/>
            • Study Period: {total_days} days<br/>
            • Daily Study Hours: {hours_per_day}<br/>
            • Created on: {datetime.date.today().strftime('%B %d, %Y')}
            """
            story.append(Paragraph(summary_text, summary_style))
            story.append(Spacer(1, 20))
            
            # Subjects Overview
            if study_plan.get('subjects'):
                story.append(Paragraph("<b>Subjects Overview:</b>", styles['Heading2']))
                subject_data = [['Subject', 'Exam Date', 'Days Left', 'Priority']]
                for subject in study_plan['subjects']:
                    try:
                        exam_date = datetime.datetime.strptime(subject['exam_date'], "%Y-%m-%d")
                        formatted_date = exam_date.strftime("%d %B %Y")
                    except:
                        formatted_date = subject.get('exam_date', 'Unknown')
                    
                    days_left = subject.get('days_until_exam', 'Unknown')
                    if isinstance(days_left, int):
                        days_left = str(days_left)
                    
                    priority_rank = subject.get('priority_rank', 'N/A')
                    
                    subject_data.append([
                        Paragraph(subject.get('name', 'Unknown'), styles['Normal']),
                        Paragraph(formatted_date, styles['Normal']),
                        Paragraph(days_left, styles['Normal']),
                        Paragraph(f"#{priority_rank}", styles['Normal'])
                    ])
                
                subject_table = Table(subject_data, colWidths=[2*inch, 1.5*inch, 1.2*inch, 0.8*inch])
                subject_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('WORDWRAP', (0, 0), (-1, -1), True),
                ]))
                story.append(subject_table)
                story.append(Spacer(1, 30))
            
            # Daily Schedule
            if study_plan.get('daily_schedule'):
                story.append(Paragraph("<b>Daily Study Schedule:</b>", styles['Heading2']))
                
                for date, schedule in list(study_plan['daily_schedule'].items())[:7]:
                    story.append(Spacer(1, 15))
                    
                    try:
                        schedule_date = datetime.datetime.strptime(date, "%Y-%m-%d")
                        formatted_date = schedule_date.strftime("%A, %d %B %Y")
                    except:
                        formatted_date = date
                    
                    date_style = ParagraphStyle(
                        'DateHeader',
                        parent=styles['Heading3'],
                        fontSize=12,
                        textColor=colors.darkblue,
                        spaceAfter=8
                    )
                    story.append(Paragraph(f"{formatted_date}", date_style))
                    
                    if not schedule:
                        story.append(Paragraph("No study sessions scheduled", styles['Normal']))
                        story.append(Spacer(1, 15))
                        continue
                        
                    session_data = [[
                        Paragraph('<b>Time</b>', styles['Normal']),
                        Paragraph('<b>Subject</b>', styles['Normal']),
                        Paragraph('<b>Hours</b>', styles['Normal']),
                        Paragraph('<b>Topics</b>', styles['Normal'])
                    ]]
                    
                    current_time = datetime.datetime.strptime("09:00", "%H:%M")
                    for session in schedule:
                        end_time = current_time + datetime.timedelta(hours=session.get('hours', 1))
                        time_slot = f"{current_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"
                        
                        topics = session.get('topics', [])
                        if isinstance(topics, list):
                            topics_text = ", ".join(topics) if topics else "General Study"
                        else:
                            topics_text = str(topics)
                        
                        session_data.append([
                            Paragraph(time_slot, styles['Normal']),
                            Paragraph(session.get('subject', 'Unknown'), styles['Normal']),
                            Paragraph(f"{session.get('hours', 1)}h", styles['Normal']),
                            Paragraph(topics_text, styles['Normal'])
                        ])
                        
                        current_time = end_time + datetime.timedelta(minutes=15)
                    
                    daily_table = Table(session_data, colWidths=[1.8*inch, 1.5*inch, 0.7*inch, 3*inch])
                    daily_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('WORDWRAP', (0, 0), (-1, -1), True),
                        ('LEFTPADDING', (0, 0), (-1, -1), 6),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ]))
                    
                    story.append(daily_table)
                    story.append(Spacer(1, 20))
            
            # Tips section
            story.append(Spacer(1, 20))
            story.append(Paragraph("<b>Study Tips:</b>", styles['Heading2']))
            tips = [
                "• Take regular breaks every 45-60 minutes",
                "• Review previous day's topics before starting new ones", 
                "• Stay hydrated and maintain a healthy diet",
                "• Get adequate sleep for better retention",
                "• Use active recall and spaced repetition techniques"
            ]
            
            for tip in tips:
                story.append(Paragraph(tip, styles['Normal']))
                story.append(Spacer(1, 5))
            
            doc.build(story)
            print(f"✅ PDF created successfully: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ PDF creation error: {e}")
            import traceback
            traceback.print_exc()
            return None
