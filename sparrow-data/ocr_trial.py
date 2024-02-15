#from tools.pdf_converter import PDFConverter
from tools.ocr_extractor import OCRExtractor
import os
# Convert pdf to jpg

from pdf2image import convert_from_path

pdf_path = r"C:\Users\Deepesh Alwani\Desktop\test\Inv_081559683_from_STAR_ELECTRIC_51660-1700068228619.pdf"  # Replace with the path to your PDF file
output_path = r"C:\Users\Deepesh Alwani\Desktop\test\converted\output.jpg"  # Replace with the desired output JPG file path

images = convert_from_path(pdf_path)

if images:
    # Assuming there's only one page, save the first image
    images[0].save(output_path, "JPEG")
    print(f"Conversion successful. Saved as {output_path}")
else:
    print("Error: No images found in the PDF.")

data_path = r"C:\Users\Deepesh Alwani\Desktop\test\converted\final"  # Use the correct destination path
ocr_extractor = OCRExtractor('db_resnet50', 'crnn_vgg16_bn', pretrained=True)
abc = ocr_extractor.extract(data_path, show_prediction=True)
print(abc)
