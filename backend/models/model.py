import tensorflow as tf

import tensorflow.keras.applications.vgg19 as vgg19
import base64
from tqdm import tqdm
tf.enable_eager_execution()

class StyleTransfer:
    def __init__(self):
        self.model = None
        self.opt = tf.train.AdamOptimizer(learning_rate=0.05, beta1=0.99, epsilon=1e-1)
        self.style_targets = None
        self.content_targets = None
        self.style_layers = ['block1_conv1',
                             'block2_conv1',
                             'block3_conv1',
                             'block4_conv1',
                             'block5_conv1']
        self.content_layers = ['block5_conv2']
        self.num_style_layers = len(self.style_layers)
        self.num_content_layers = len(self.content_layers)
        self.style_weight = 1e-2
        self.content_weight = 1e4
        self.total_variation_weight = 1e8


    def initialize_model(self):
        layer_names = self.content_layers + self.style_layers

        vgg = vgg19.VGG19(include_top=True, weights='imagenet')
        vgg.trainable = False

        outputs = [vgg.get_layer(name).output for name in layer_names]

        self.model = tf.keras.models.Model([vgg.input], outputs)

        return None

    def load_and_preprocess_image(self, base64_image):
        image = base64.decodestring(base64_image)
        return self.preprocess_image(image)

    def preprocess_image(self, image):
        max_dim = 512
        image = tf.image.decode_image(image, channels=3)
        image = tf.image.convert_image_dtype(image, tf.float32)

        shape = tf.cast(tf.shape(image)[:-1], tf.float32)
        long_dim = max(shape)
        scale = max_dim / long_dim

        new_shape = tf.cast(shape * scale, tf.int32)

        image = tf.image.resize_images(image, new_shape)
        image = image[tf.newaxis, :]
        return image

    def create_gram_matrix(self, input_tensor):
        # lets denote input_tensor[0] as b, [1] as i, [2] as j, and [3] as c = d
        # einsum to square input_tensor[0][1][2] then sum by [1][2] and display [0][3][3]
        result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
        input_shape = tf.shape(input_tensor)
        # cast 2 ints to float
        num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)

        return result / (num_locations)

    def call_model(self, inputs):
        inputs = inputs * 255.0
        preprocessed_input = vgg19.preprocess_input(inputs)
        model_outputs = self.model(preprocessed_input)

        style_outputs, content_outputs = (model_outputs[:self.num_style_layers],
                                          model_outputs[self.num_style_layers:])
        style_outputs = [self.create_gram_matrix(style_output)
                         for style_output in style_outputs]

        content_dict = {content_name: value
                        for content_name, value
                        in zip(self.content_layers, content_outputs)}

        style_dict = {style_name: value
                      for style_name, value
                      in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 'style': style_dict}

    def clip_image(self, image):
        return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

    def style_content_loss(self, outputs):
        style_outputs = outputs['style']
        content_outputs = outputs['content']
        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - self.style_targets[name]) ** 2)
                               for name in style_outputs.keys()])
        style_loss *= self.style_weight / self.num_style_layers

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - self.content_targets[name]) ** 2)
                                 for name in content_outputs.keys()])
        content_loss *= self.content_weight / self.num_content_layers
        loss = style_loss + content_loss
        return loss

    def high_pass_x_y(self, image):
        x_var = image[:, :, 1:, :] - image[:, :, :-1, :]
        y_var = image[:, 1:, :, :] - image[:, :-1, :, :]

        return x_var, y_var

    def total_variation_loss(self, image):
        x_deltas, y_deltas = self.high_pass_x_y(image)
        return tf.reduce_mean(x_deltas ** 2) + tf.reduce_mean(y_deltas ** 2)

    def train_step(self, image):
        with tf.GradientTape() as tape:
            outputs = self.call_model(image)
            loss = self.style_content_loss(outputs)
            loss += self.total_variation_weight * self.total_variation_loss(image)
        grad = tape.gradient(loss, image)
        self.opt.apply_gradients([(grad, image)])
        image.assign(self.clip_image(image))

    def preprocess_images(self, content_path, style_path):
        style_image = self.load_and_preprocess_image(style_path)
        content_image = self.load_and_preprocess_image(content_path)

        self.style_targets = self.call_model(style_image)['style']
        self.content_targets = self.call_model(content_image)['content']

        image = tf.Variable(content_image)

        return image