[![Multi-Modality](agorabanner.png)](https://discord.com/servers/agora-999382051935506503)

# Doc Master 📚

[![Join our Discord](https://img.shields.io/badge/Discord-Join%20our%20server-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/agora-999382051935506503) [![Subscribe on YouTube](https://img.shields.io/badge/YouTube-Subscribe-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@kyegomez3242) [![Connect on LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kye-g-38759a207/) [![Follow on X.com](https://img.shields.io/badge/X.com-Follow-1DA1F2?style=for-the-badge&logo=x&logoColor=white)](https://x.com/kyegomezb)


[![PyPI version](https://badge.fury.io/py/doc-master.svg)](https://badge.fury.io/py/doc-master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord](https://img.shields.io/discord/999382051935506503?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/agora-999382051935506503)

A powerful, lightweight Python library for automated file reading and content extraction. Doc Master simplifies the process of reading various file formats into string representations, making it perfect for data processing, content analysis, and document management systems.

## 🚀 Features

- **Universal File Reading**: Seamlessly handle multiple file formats including:
  - PDF documents
  - Microsoft Word documents (.docx)
  - Excel spreadsheets
  - Text files
  - XML documents
  - Images (with base64 encoding)
  - Binary files

- **Smart Format Detection**: Automatic file type detection and appropriate processing
- **Flexible Output**: Choose between string or dictionary output formats
- **Batch Processing**: Process entire folders of documents efficiently
- **Encoding Detection**: Smart encoding detection for text files
- **Enterprise-Ready**: Built with stability and performance in mind

## 📦 Installation

```bash
pip install -U doc-master
```

## 🔧 Quick Start

```python
from doc_master import doc_master

# Read all files in a folder
results = doc_master(folder_path="path/to/folder", output_type="dict")

# Or read a single file
content = doc_master(file_path="path/to/file.docx")
```

## 📋 Requirements

- Python 3.8+
- pandas
- pypdf
- python-docx
- Pillow

## 🤝 Contributing

We love your input! We want to make contributing to Doc Master as easy and transparent as possible. Here's how you can help:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Check out our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 🌟 Support the Project

If you find Doc Master useful, please consider:
- Starring the repository ⭐
- Following us on GitHub
- Joining our [Discord community](https://discord.gg/agora-999382051935506503)
- Sharing the project with others

## 📖 Documentation

For detailed documentation, visit our [Wiki](https://github.com/The-Swarm-Corporation/doc-master/wiki).

### Basic Usage Examples

```python
# Read a PDF file
content = read_single_file("document.pdf")

# Read an Excel file with specific sheet
reader = AutoFileReader()
content = reader.read_file("spreadsheet.xlsx", sheet_name="Data")

# Process a folder of documents
results = doc_master(
    folder_path="documents/",
    output_type="dict"
)
```

## 🔍 Error Handling

The library includes comprehensive error handling:

```python
try:
    content = read_single_file("file.pdf")
except Exception as e:
    print(f"Error processing file: {e}")
```

## 🛣️ Roadmap

- [ ] Add OCR capabilities for image processing
- [ ] Support for additional file formats
- [ ] Performance optimizations for large files
- [ ] Async file processing
- [ ] CLI interface

## 💬 Community and Support

- Join our [Discord server](https://discord.gg/agora-999382051935506503) for discussions and support
- Check out our [GitHub Issues](https://github.com/The-Swarm-Corporation/doc-master/issues) for bug reports and feature requests
- Follow our [GitHub Discussions](https://github.com/The-Swarm-Corporation/doc-master/discussions) for general questions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- All our amazing contributors
- The open-source community
- The Swarm Corporation team

---

<p align="center">
  Made with ❤️ by The Swarm Corporation
</p>

<p align="center">
  <a href="https://github.com/The-Swarm-Corporation/doc-master/stargazers">⭐ Star us on GitHub!</a>
</p>