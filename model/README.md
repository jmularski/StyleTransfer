# Model part

Build with Tensorflow with help of [this tutorial](https://www.tensorflow.org/alpha/tutorials/generative/style_transfer) and [this paper](https://arxiv.org/abs/1508.06576).

## How to run it in file

```python
from model import StyleTransfer

style_path = "test_data.jpg" # path of the picture you want to take style from
content_path = "training_data.jpg" # path of the picture you want to move style to

model = StyleTransfer()
model.initialize_model() # prebuilds vgg19 and other stuff, wont run without that line
image = model.predict(content_path, style_path) # returns final image after 100 iterations of model
```
