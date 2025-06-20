import streamlit as st
import fitz
import tempfile
import os
import base64

def combine_pdf_pages_4up_direct(input_pdf_path, output_pdf_path):
    src_doc = fitz.open(input_pdf_path)
    dst_doc = fitz.open()
    total_pages = len(src_doc)

    page_rect = src_doc[0].rect
    width = page_rect.width
    height = page_rect.height

    for i in range(0, total_pages, 4):
        new_page = dst_doc.new_page(width=width, height=height)
        for j in range(4):
            page_index = i + j
            if page_index >= total_pages:
                break
            src_page = src_doc.load_page(page_index)
            col = j % 2
            row = j // 2
            target_rect = fitz.Rect(
                col * width / 2,
                row * height / 2,
                (col + 1) * width / 2,
                (row + 1) * height / 2
            )
            new_page.show_pdf_page(target_rect, src_doc, page_index)

    dst_doc.save(output_pdf_path)

st.title("4ページを1ページに結合")

uploaded_file = st.file_uploader("PDFファイルをアップロード", type=["pdf"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_in:
        temp_in.write(uploaded_file.read())
        temp_in_path = temp_in.name

    output_path = temp_in_path.replace(".pdf", "_4up.pdf")
    combine_pdf_pages_4up_direct(temp_in_path, output_path)

    with open(output_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode()

    href = f'''
        <a id="dl" href="data:application/pdf;base64,{base64_pdf}" download="output.pdf"></a>
        <script>
            document.getElementById("dl").click();
        </script>
    '''
    st.markdown("PDF生成完了。ダウンロードが自動で始まらない場合は以下をクリック：")
    st.markdown(href, unsafe_allow_html=True)

    os.remove(temp_in_path)
    os.remove(output_path)
