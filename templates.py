def get_styled_html(name, phone, email, linkedin, location, education, skills, bullets):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{ size: A4; margin: 1in; }}
            body {{ font-family: Calibri, Arial, sans-serif; line-height: 1.5; color: #222; }}
            .container {{ max-width: 8.5in; margin: 0 auto; }}
            h1 {{ font-size: 32px; margin: 0; color: #1e40af; text-align: center; letter-spacing: 1px; }}
            .contact {{ text-align: center; font-size: 11pt; color: #555; margin: 10px 0 25px; }}
            h2 {{ font-size: 13pt; color: #1e40af; border-bottom: 2px solid #1e40af; padding-bottom: 4px; margin: 25px 0 10px 0; text-transform: uppercase; letter-spacing: 1px; }}
            .skills {{ font-weight: bold; color: #1e40af; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{name}</h1>
            <div class="contact">{phone} • {email} • {linkedin or '—'} • {location}</div>

            <h2>Education</h2>
            <p>{education}</p>

            <h2>Technical Skills</h2>
            <p class="skills">{skills}</p>

            <h2>Experience & Projects</h2>
            <ul>
                {''.join(f"<li>{b.strip('• ')}</li>" for b in bullets.split('\n') if b.strip())}
            </ul>
        </div>
    </body>
    </html>
    """
