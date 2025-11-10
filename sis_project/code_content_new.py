"""
Code of Ethical Conduct Content Management
This file handles reading and managing the Code of Ethical Conduct content from Word documents (.docx)
"""

import os
from docx import Document
from django.conf import settings

# Document file paths (relative to project root)
DOCUMENT_PATHS = {
    'uzbek': 'documents/code_of_conduct/uzbek_code.docx',
    'russian': 'documents/code_of_conduct/russian_code.docx', 
    'english': 'documents/code_of_conduct/english_code.docx'
}

# PDF file paths (relative to project root)
PDF_PATHS = {
    'uzbek': 'documents/code_of_conduct/uzbek_code.pdf',
    'russian': 'documents/code_of_conduct/russian_code.pdf', 
    'english': 'documents/code_of_conduct/english_code.pdf'
}

# Default titles (updated with correct titles)
DEFAULT_TITLES = {
    'uzbek': "Samarqand xalqaro texnologiya universitetining odob-axloq kodeksi",
    'russian': "Кодекс этического поведения Самаркандского международного технологического университета",
    'english': "Code of Ethical Conduct of the Samarkand International University of Technology"
}

# Content with download links (simplified without bullet points)
CONTENT_WITH_DOWNLOAD = {
    'uzbek': {
        'title': DEFAULT_TITLES['uzbek'],
        'content': """
⚖️ MUHIM ESLATMA:
Bu kodeksga amal qilish har bir jamoa a'zosining burchi va majburiyatidir.

📥 KODEKSNING TO'LIQ MATNI:
Axloqiy kodeksning to'liq mazmuni bilan tanishish uchun quyidagi PDF faylni yuklab oling:

🔗 <a href="/media/documents/code_of_conduct/uzbek_code.pdf" target="_blank" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
    </svg>
    Axloqiy kodeksni yuklab olish (PDF)
</a>
        """
    },
    'russian': {
        'title': DEFAULT_TITLES['russian'],
        'content': """
⚖️ ВАЖНОЕ ЗАМЕЧАНИЕ:
Соблюдение данного кодекса является долгом и обязанностью каждого члена сообщества.

📥 ПОЛНЫЙ ТЕКСТ КОДЕКСА:
Для ознакомления с полным содержанием этического кодекса скачайте PDF файл:

🔗 <a href="/media/documents/code_of_conduct/russian_code.pdf" target="_blank" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
    </svg>
    Скачать этический кодекс (PDF)
</a>
        """
    },
    'english': {
        'title': DEFAULT_TITLES['english'],
        'content': """
⚖️ IMPORTANT NOTE:
Adherence to this code is the duty and obligation of every community member.

📥 COMPLETE CODE TEXT:
To review the full content of the Code of Ethical Conduct, download the PDF file:

🔗 <a href="/media/documents/code_of_conduct/english_code.pdf" target="_blank" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
    </svg>
    Download Code of Ethical Conduct (PDF)
</a>
        """
    }
}

def read_docx_content(file_path):
    """
    Extract text content from a Word document (.docx)
    Returns tuple: (title, content)
    """
    try:
        # Get absolute path
        if not os.path.isabs(file_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, file_path)
        
        if not os.path.exists(file_path):
            return None, None
        
        # Read document
        doc = Document(file_path)
        
        # Extract title (usually first paragraph or first heading)
        title = None
        content_paragraphs = []
        
        for i, paragraph in enumerate(doc.paragraphs):
            text = paragraph.text.strip()
            if not text:
                continue
                
            # First meaningful paragraph might be title
            if i == 0 and len(text) < 200:
                title = text
            else:
                content_paragraphs.append(text)
        
        # Join content with double newlines for better formatting
        content = '\n\n'.join(content_paragraphs)
        
        return title, content
        
    except Exception as e:
        print(f"Error reading document {file_path}: {str(e)}")
        return None, None

def get_code_content():
    """
    Get the Code of Ethical Conduct content for all languages.
    Returns a dictionary with language codes as keys.
    """
    content = {}
    
    for lang, doc_path in DOCUMENT_PATHS.items():
        title, doc_content = read_docx_content(doc_path)
        
        if title and doc_content:
            # Use content from .docx file
            content[lang] = {
                'title': title,
                'content': doc_content,
                'source': 'document'
            }
        else:
            # Use content with download links
            content[lang] = {
                'title': CONTENT_WITH_DOWNLOAD[lang]['title'],
                'content': CONTENT_WITH_DOWNLOAD[lang]['content'],
                'source': 'download_link'
            }
    
    return content

def update_document_files(uzbek_file=None, russian_file=None, english_file=None):
    """
    Helper function to update document file paths.
    Usage:
        update_document_files(
            uzbek_file='path/to/uzbek_code.docx',
            russian_file='path/to/russian_code.docx',
            english_file='path/to/english_code.docx'
        )
    """
    global DOCUMENT_PATHS
    
    if uzbek_file:
        DOCUMENT_PATHS['uzbek'] = uzbek_file
    if russian_file:
        DOCUMENT_PATHS['russian'] = russian_file
    if english_file:
        DOCUMENT_PATHS['english'] = english_file
    
    print("Document paths updated:")
    for lang, path in DOCUMENT_PATHS.items():
        print(f"  {lang}: {path}")

def test_document_reading():
    """
    Test function to check if documents can be read
    """
    print("🔍 Testing document reading...")
    
    for lang, doc_path in DOCUMENT_PATHS.items():
        print(f"\n📄 Testing {lang.upper()} document:")
        print(f"   Path: {doc_path}")
        
        title, content = read_docx_content(doc_path)
        if title and content:
            print(f"   ✅ Successfully read document")
            print(f"   📝 Title: {title[:50]}...")
            print(f"   📄 Content length: {len(content)} characters")
        else:
            print(f"   ❌ File not found or error reading")
            print(f"   🔄 Will use fallback content")

if __name__ == "__main__":
    test_document_reading()