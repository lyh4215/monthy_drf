from PIL import Image as PILImage
import io
# 이미지 파일을 읽어와서 표시
# 이미지 데이터를 PIL 이미지 객체로 변환

def png(graph):
    image_data = graph.get_graph().draw_mermaid_png()
    image = PILImage.open(io.BytesIO(image_data))
    # 이미지 표시
    image.show()