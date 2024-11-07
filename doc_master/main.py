import base64
import mimetypes
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Union

import docx
import pandas as pd
import pypdf


class AutoFileReader:
    """
    Automatically detect and read any file into a string format.
    Handles text files, documents, images, and more with minimal dependencies.
    """

    def __init__(self, use_ocr: bool = False):
        """
        Initialize the AutoFileReader.

        Args:
            use_ocr (bool): OCR capability flag (not implemented in simplified version)
        """
        self.use_ocr = use_ocr
        # Initialize mimetypes
        mimetypes.init()

    def read_file(self, file_path: Union[str, Path], **kwargs) -> str:
        """
        Read any file and convert it to string format.

        Args:
            file_path: Path to the file
            **kwargs: Additional arguments for specific file types
                encoding: Optional explicit encoding for text files
                sheet_name: Sheet name/index for Excel files

        Returns:
            str: Content of the file as string

        Raises:
            Exception: If file cannot be read or processed
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(
                    f"File not found: {file_path}"
                )

            # Get mime type using mimetypes
            mime_type, _ = mimetypes.guess_type(str(file_path))
            if mime_type is None:
                # Default to text/plain for unknown types
                mime_type = "text/plain"

            # Detect encoding for text files
            encoding = kwargs.get("encoding", "utf-8")

            # Process based on mime type
            if mime_type.startswith("text/"):
                return self._read_text(file_path, encoding)
            elif mime_type == "application/pdf":
                return self._read_pdf(file_path)
            elif mime_type in [
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ]:
                return self._read_excel(file_path, **kwargs)
            elif mime_type in [
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ]:
                return self._read_docx(file_path)
            elif mime_type == "application/xml":
                return self._read_xml(file_path)
            elif mime_type.startswith("image/"):
                return self._read_image(file_path)
            else:
                # Try to read as text, if fails, return base64
                try:
                    return self._read_text(file_path, encoding)
                except UnicodeDecodeError:
                    return self._read_binary(file_path)

        except Exception as e:
            raise Exception(
                f"Error processing file {file_path}: {str(e)}"
            )

    def _read_text(
        self, file_path: Path, encoding: Optional[str] = None
    ) -> str:
        """Read text files with specified encoding."""
        encoding = encoding or "utf-8"
        try:
            with open(file_path, "r", encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try to detect encoding if initial read fails
            for enc in ["utf-8", "latin-1", "ascii", "iso-8859-1"]:
                try:
                    with open(file_path, "r", encoding=enc) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
            raise UnicodeDecodeError(
                f"Could not decode file {file_path} with any common encoding"
            )

    def _read_pdf(self, file_path: Path) -> str:
        """Read PDF files."""
        text_content = []
        with open(file_path, "rb") as f:
            pdf = pypdf.PdfReader(f)
            for page in pdf.pages:
                text_content.append(page.extract_text())
        return "\n".join(text_content)

    def _read_excel(self, file_path: Path, **kwargs) -> str:
        """Read Excel files."""
        sheet_name = kwargs.get("sheet_name", 0)
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        return df.to_string()

    def _read_docx(self, file_path: Path) -> str:
        """Read Word documents."""
        doc = docx.Document(file_path)
        return "\n".join(
            [paragraph.text for paragraph in doc.paragraphs]
        )

    def _read_xml(self, file_path: Path) -> str:
        """Read XML files."""
        tree = ET.parse(file_path)
        return ET.tostring(
            tree.getroot(), encoding="unicode", method="xml"
        )

    def _read_image(self, file_path: Path) -> str:
        """Read image files and return base64 representation."""
        return self._image_to_base64(file_path)

    def _read_binary(self, file_path: Path) -> str:
        """Read binary files as base64."""
        return self._file_to_base64(file_path)

    def _file_to_base64(self, file_path: Path) -> str:
        """Convert any file to base64 string."""
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def _image_to_base64(self, file_path: Path) -> str:
        """Convert image to base64 string with format prefix."""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return f"data:{mime_type};base64,{self._file_to_base64(file_path)}"


def read_single_file(file_path: str) -> str:
    """Read a single file and return its contents."""
    reader = AutoFileReader()
    try:
        return reader.read_file(file_path)
    except Exception as e:
        print(f"Error: {e}")
        return None


def read_all_files_in_folder(
    folder_path: str, output_type: str = "string"
) -> Union[dict, str]:
    """
    Read all files in a specified folder and return their contents using multi-threading.

    Args:
        folder_path (str): Path to the folder containing files.
        output_type (str): Specify the output type. Options are "dict" or "string".

    Returns:
        Union[dict, str]: Dictionary with file names as keys and contents as values,
                         or string representation of all contents.
    """
    if output_type not in ["dict", "string"]:
        raise ValueError(
            "Invalid output_type. Expected 'dict' or 'string'."
        )

    results = {} if output_type == "dict" else ""
    folder = Path(folder_path)

    if not folder.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {folder_path}"
        )

    def process_file(file_path: Path) -> tuple:
        try:
            content = read_single_file(str(file_path))
            return file_path.name, content
        except Exception as e:
            return (
                file_path.name,
                f"Error processing file {file_path}: {str(e)}",
            )

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(process_file, file_path)
            for file_path in folder.iterdir()
            if file_path.is_file()
        ]
        for future in futures:
            file_name, content = future.result()
            if output_type == "dict":
                results[file_name] = content
            else:
                results += f"{content}\n"

    return results if output_type == "dict" else results.strip()


def doc_master(
    file_path: str = None,
    folder_path: str = None,
    output_type: str = "string",
) -> Union[str, dict]:
    """
    Main function to read a single file or all files in a folder.

    Args:
        file_path: Path to single file
        folder_path: Path to folder containing files
        output_type: "string" or "dict"

    Returns:
        File contents as string or dictionary
    """
    if file_path is not None:
        output = read_single_file(file_path)
    elif folder_path is not None:
        output = read_all_files_in_folder(folder_path, output_type)
    else:
        raise ValueError(
            "Either file_path or folder_path must be provided"
        )

    return output
