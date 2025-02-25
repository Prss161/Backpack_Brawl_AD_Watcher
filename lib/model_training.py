import os
import lxml
import torchvision.transforms as T
import torch
import xml.etree.ElementTree as ET
from PIL import Image


class PascalVOCDataset:
    def __init__(self, xml_dir):
        self.xml_dir = xml_dir

    def get_data_boxes(self, xml_filename):
        import lxml.etree

        xml_path = f"{self.xml_dir}/{xml_filename}"
        tree = lxml.etree.parse(xml_path)
        root = tree.getroot()
        boxes = []
        for obj in root.findall(".//object"):
            xmin = int(obj.find(".//bndbox/xmin").text)
            ymin = int(obj.find(".//bndbox/ymin").text)
            xmax = int(obj.find(".//bndbox/xmax").text)
            ymax = int(obj.find(".//bndbox/ymax").text)
            boxes.append([xmin, ymin, xmax, ymax])
        return boxes

    def get_data_labels(self, xml_filename):
        xml_path = f"{self.xml_dir}/{xml_filename}"
        tree = lxml.etree.parse(xml_path)
        root = tree.getroot()
        labels = [obj.find("name").text for obj in root.findall(".//object")]
        result = {value: index for index, value in enumerate(labels)}
        return result

    def get_data_image_id(self, xml_filename):
        return xml_filename.split(".")[0]

    def get_data_area(self, xml_filename):
        boxes = self.get_data_boxes(xml_filename)
        areas = [(xmax - xmin) * (ymax - ymin) for xmin, ymin, xmax, ymax in boxes]
        return areas


def pytorch__dataset():
    dir = os.listdir("./img/")
    xml_files = [file for file in dir if file.endswith(".xml")]
    img_files = [file[:-4] for file in dir if file.endswith(".png")]

    for xml_file in xml_files:
        if xml_file[:-4] in img_files:
            xml_path = xml_file
            img_path = xml_file[:-4] + ".png"
            dataset = PascalVOCDataset("./img")
            boxes = dataset.get_data_boxes(xml_path)
            class_labels = dataset.get_data_labels(xml_path)
            class_ids = list(class_labels.values())
            image_id = dataset.get_data_image_id(xml_path)
            area = dataset.get_data_area(xml_path)

            image = Image.open("./img/" + img_path).convert("RGB")
            transform = T.ToTensor()
            image = transform(image)
            target = {
                "boxes": torch.tensor(boxes, dtype=torch.float32),
                "labels": torch.tensor(class_ids, dtype=torch.int64),
                "image_id": torch.tensor([image_id]),
                "area": torch.tensor(area, dtype=torch.float32),
                "iscrowd": torch.zeros((len(boxes),), dtype=torch.int64),
            }


dataset = PascalVOCDataset("./img")
print(dataset.get_data_labels("screenshot_2025-02-15_21-51-34.xml"))
print(dataset.get_data_area("screenshot_2025-02-15_21-51-34.xml"))
