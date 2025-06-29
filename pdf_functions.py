from fpdf import FPDF


def create_pdf(text): 

    # Create a PDF instance
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)


    # Add text line by line
    pdf.multi_cell(0, 10, txt=text)

    # Save the PDF
    pdf.output("static/files/output_letter.pdf")

