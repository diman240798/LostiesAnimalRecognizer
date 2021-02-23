import tensorflow as tf, sys

 #image_path = 'animals/my/dog.jpg'

def classify_animal_image(image_path):
    # Read in the image_data
    image_data = tf.io.gfile.GFile(image_path, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                       in tf.io.gfile.GFile('./animal_types/retrained_labels.txt')]

    # Unpersists graph from file
    with tf.io.gfile.GFile("./animal_types/retrained_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        animal_value = list(map(lambda x: {label_lines[x]: predictions[0][x]}, top_k))

        maximum = -1
        for i in animal_value:
            value = list(i.values())[0]
            if value > maximum:
                maximum = value
                item = i

        return list(item.keys())[0]


