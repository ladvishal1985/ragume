from reportlab.pdfgen import canvas
import os

def create_pdf(path):
    c = canvas.Canvas(path)
    c.drawString(100, 750, "Hello, this is a test PDF for RAG ingestion.")
    c.drawString(100, 730, "It contains sample data to verify the embedding pipeline.")
    c.drawString(100, 710, "Milvus should store this content.")
    c.save()
    print(f"Created PDF at {path}")

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.pdf")
    output_path = os.path.abspath(output_path)
    try:
        create_pdf(output_path)
    except ImportError:
        print("ReportLab not installed. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "reportlab"])
        create_pdf(output_path)
