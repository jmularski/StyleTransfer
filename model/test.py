from model import StyleTransfer

style_path = "test_data.jpg"
content_path = "training_data.jpg"

model = StyleTransfer()
model.initialize_model()
model.predict(content_path, style_path)