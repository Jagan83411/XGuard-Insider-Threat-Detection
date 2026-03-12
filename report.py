
from fpdf import FPDF
from datetime import datetime


def generate_report(employee_name, risk_score, reasons):
    pdf = FPDF()
    pdf.add_page()

    # Header background
    pdf.set_fill_color(31, 78, 121)
    pdf.rect(0, 0, 210, 30, 'F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_xy(10, 8)
    pdf.cell(0, 10, "XGuard - Insider Threat Alert Report")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(10, 20)
    pdf.cell(
        0,
        6,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  Team Codex  |  REVA University"
    )

    # Employee Section
    pdf.set_xy(10, 40)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Employee: {employee_name}")

    # Risk score color
    if risk_score > 70:
        color = (220, 50, 50)
    elif risk_score > 40:
        color = (255, 165, 0)
    else:
        color = (0, 180, 0)

    pdf.set_fill_color(*color)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 20)

    pdf.set_xy(10, 55)
    pdf.cell(60, 20, f"Risk Score: {risk_score}/100", align="C", fill=True)

    # Explanation Section
    pdf.set_text_color(0, 0, 0)
    pdf.set_xy(10, 85)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Why was this person flagged?")

    pdf.set_font("Helvetica", "", 11)

    for i, reason in enumerate(reasons, 1):
       safe_reason = str(reason).replace("—", "-").replace("–", "-")
       pdf.set_x(15)
       pdf.multi_cell(0, 7, f"{i}. The employee {safe_reason}")

    # Recommended Action
    pdf.set_xy(10, pdf.get_y() + 10)

    pdf.set_fill_color(255, 240, 200)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Recommended Action:", fill=True)

    pdf.set_font("Helvetica", "", 11)

    if risk_score > 70:
        action = "IMMEDIATE REVIEW REQUIRED. Escalate to security team and HR."
    elif risk_score > 40:
        action = "Schedule a review. Monitor activity for next 7 days."
    else:
        action = "Low risk. Continue routine monitoring."

    pdf.set_x(15)
    pdf.multi_cell(0, 7, action)

    # Footer
    pdf.set_fill_color(31, 78, 121)
    pdf.rect(0, 280, 210, 20, 'F')

    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "", 9)

    pdf.set_xy(10, 284)
    pdf.cell(
        0,
        6,
        "XGuard | Team Codex | REVA University, Bangalore | GDPR Compliant"
    )

    filename = f"report_{employee_name.replace(' ', '_')}.pdf"
    pdf.output(filename)

    print(f"Report saved: {filename}")
    return filename


if __name__ == "__main__":
    generate_report(
        "Test Employee",
        91,
        [
            "accessed 500 files - 8x their normal amount",
            "logged in at 2:00 AM - unusual login time",
            "connected an external USB device"
        ]
    )