# utils/pdf_generator.py

import os
from weasyprint import HTML

def generate_summary_pdf(user_id, summary):
    output_dir = "summaries"
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, f"{user_id}_summary.pdf")

    # Fix the newline issue here
    formatted_summary = summary.replace('\n', '<br>')

    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    padding: 20px;
                    line-height: 1.6;
                }}
                h1 {{
                    color: #2c3e50;
                }}
                p {{
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <h1>Medical Summary for {user_id}</h1>
            <p>{formatted_summary}</p>
        </body>
    </html>
    """

    HTML(string=html_content).write_pdf(file_path)
    return file_path
