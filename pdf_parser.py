import fitz  # PyMuPDF
import os


def extract_from_pdf(pdf_path, output_image_folder="extracted_images"):
    """
    Extract text and images from a PDF file.
    Returns: (full_text: str, image_paths: list)
    """
    os.makedirs(output_image_folder, exist_ok=True)
    doc = fitz.open(pdf_path)

    full_text = ""
    image_paths = []

    for page_num, page in enumerate(doc):
        # Extract text
        full_text += f"\n--- Page {page_num + 1} ---\n"
        full_text += page.get_text()

        # Extract images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                img_bytes = base_image["image"]
                ext = base_image["ext"]
                # Skip tiny images (icons/artifacts)
                if len(img_bytes) < 5000:
                    continue
                img_filename = os.path.join(
                    output_image_folder,
                    f"page{page_num + 1}_img{img_index + 1}.{ext}"
                )
                with open(img_filename, "wb") as f:
                    f.write(img_bytes)
                image_paths.append(img_filename)
            except Exception as e:
                print(f"Could not extract image on page {page_num + 1}: {e}")

    doc.close()
    return full_text, image_paths


def get_pdf_metadata(pdf_path):
    """Extract basic metadata from PDF."""
    doc = fitz.open(pdf_path)
    meta = doc.metadata
    page_count = len(doc)
    doc.close()
    return {
        "title": meta.get("title", "Unknown"),
        "author": meta.get("author", "Unknown"),
        "pages": page_count
    }
