#!/usr/bin/env python3
"""
PDF Page Splitter - Split each page into left and right halves

This script takes a PDF file and splits each page into two separate pages:
one containing the left half and one containing the right half.
The script properly adjusts both the page dimensions and content position
to ensure compatibility with all PDF readers, including legacy ones.

Usage:
    python split_pdf_pages.py input.pdf [output.pdf]

Requirements:
    pip install pypdf
"""

import sys
from pathlib import Path

try:
    from pypdf import PageObject, PdfReader, PdfWriter, Transformation
except ImportError:
    print("Error: pypdf library not found.")
    print("Please install it using: pip install pypdf")
    sys.exit(1)


def split_pdf_pages(input_path, output_path=None):
    """
    Split each page of a PDF into left and right halves.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file (optional)
    """
    # Set default output path if not provided
    if output_path is None:
        input_file = Path(input_path)
        output_path = input_file.parent / f"{input_file.stem}_split{input_file.suffix}"

    # Read the input PDF
    reader = PdfReader(input_path)
    writer = PdfWriter()

    print(f"Processing {len(reader.pages)} pages...")

    # Process each page
    for page_num, original_page in enumerate(reader.pages, 1):
        # Get the original page dimensions
        media_box = original_page.mediabox
        lower_left_x = float(media_box.lower_left[0])
        lower_left_y = float(media_box.lower_left[1])
        upper_right_x = float(media_box.upper_right[0])
        upper_right_y = float(media_box.upper_right[1])

        # Calculate dimensions
        width = upper_right_x - lower_left_x
        height = upper_right_y - lower_left_y
        half_width = width / 2

        # Create LEFT half page
        left_page = PageObject.create_blank_page(width=half_width, height=height)
        left_page.merge_page(original_page)
        # Crop to show only left half
        left_page.mediabox.lower_left = (lower_left_x, lower_left_y)
        left_page.mediabox.upper_right = (lower_left_x + half_width, upper_right_y)
        left_page.cropbox.lower_left = (lower_left_x, lower_left_y)
        left_page.cropbox.upper_right = (lower_left_x + half_width, upper_right_y)
        writer.add_page(left_page)

        # Create RIGHT half page
        right_page = PageObject.create_blank_page(width=half_width, height=height)
        right_page.merge_page(original_page)
        # Shift content left and crop to show only right half
        right_page.add_transformation(Transformation().translate(tx=-half_width, ty=0))
        right_page.mediabox.lower_left = (0, lower_left_y)
        right_page.mediabox.upper_right = (half_width, upper_right_y)
        right_page.cropbox.lower_left = (0, lower_left_y)
        right_page.cropbox.upper_right = (half_width, upper_right_y)
        writer.add_page(right_page)

        print(
            f"  Page {page_num}: Split into left and right halves (each {half_width:.1f} x {height:.1f})"
        )

    # Write the output PDF
    with open(output_path, "wb") as output_file:
        writer.write(output_file)

    print(f"\nSuccess! Created {output_path}")
    print(f"Original pages: {len(reader.pages)}")
    print(f"Output pages: {len(writer.pages)}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python split_pdf_pages.py input.pdf [output.pdf]")
        print("\nExample:")
        print("  python split_pdf_pages.py document.pdf")
        print("  python split_pdf_pages.py document.pdf document_split.pdf")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None

    # Check if input file exists
    if not Path(input_pdf).exists():
        print(f"Error: Input file '{input_pdf}' not found.")
        sys.exit(1)

    try:
        split_pdf_pages(input_pdf, output_pdf)
    except Exception as e:
        print(f"Error processing PDF: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
