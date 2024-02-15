from pdf2image.exceptions import PDFPageCountError
from pdf2image import convert_from_path
from tools.ocr_extractor import OCRExtractor
import os
import shutil

class PDFConverter:
    def convert_to_jpg(self, pdf_path, output_path, dpi=300):
        try:
            # Get list of PDF files in the specified directory
            pdf_files = [file for file in os.listdir(pdf_path) if file.endswith('.pdf')]

            for pdf_file in pdf_files:
                try:
                    pages = convert_from_path(os.path.join(pdf_path, pdf_file), dpi)

                    # Create output directory if it doesn't exist
                    os.makedirs(output_path, exist_ok=True)

                    # Save pages as images
                    for i, page in enumerate(pages):
                        image_path = os.path.join(output_path, f"{pdf_file}_page_{i + 1}.jpg")
                        page.save(image_path, 'JPEG')

                    print(f"Conversion successful for {pdf_file}")
                except PDFPageCountError:
                    print(f"Error: Unable to get page count for {pdf_file}. Skipping.")
                except Exception as e:
                    print(f"Error processing {pdf_file}: {e}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # Convert pdf to jpg
    pdf_converter = PDFConverter()
    base_folder = os.getcwd()
    print(base_folder)
    pdf_converter.convert_to_jpg('../sparrow-data/docs/input/invoices/Dataset with valid information',
                                 '../sparrow-data/docs/input/invoices/processed/images')

    # Define the source and destination directory
    src_dir = "../sparrow-data/docs/input/invoices/processed/images"
    dst_dir = "docs/images"

    # Get list of files in the source directory
    files = os.listdir(src_dir)

    # Loop through all files in the source directory and copy to the destination directory
    for f in files:
        src_file = os.path.join(src_dir, f)
        dst_file = os.path.join(dst_dir, f)
        shutil.copy(src_file, dst_file)

    # OCR
    ocr_extractor = OCRExtractor('db_resnet50', 'crnn_vgg16_bn', pretrained=True)
    ocr_extractor.extract('../sparrow-data/docs/input/invoices/processed', show_prediction=False)
