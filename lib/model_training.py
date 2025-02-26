import os
import lxml.etree
import torchvision.transforms as T
import torch
from PIL import Image


class PascalVOCDataset:
    def __init__(self, xml_dir, img_dir):
        self.xml_dir = xml_dir
        self.img_dir = img_dir
        self.xml_files = [file for file in os.listdir(xml_dir) if file.endswith(".xml")]

    def __len__(self):
        return len(self.xml_files)

    def __getitem__(self, idx):
        xml_filename = self.xml_files[idx]
        img_filename = xml_filename.replace(".xml", ".png")

        boxes = self.get_data_boxes(xml_filename)
        labels = self.get_data_labels(xml_filename)
        image_id = int(idx)
        area = self.get_data_area(xml_filename)

        image = Image.open(os.path.join(self.img_dir, img_filename)).convert("RGB")
        transform = T.ToTensor()
        image = transform(image)

        target = {
            "boxes": torch.tensor(boxes, dtype=torch.float32),
            "labels": torch.tensor(labels, dtype=torch.int64),
            "image_id": torch.tensor([image_id]),
            "area": torch.tensor(area, dtype=torch.float32),
            "iscrowd": torch.zeros((len(boxes),), dtype=torch.int64),
        }
        return image, target

    def get_data_boxes(self, xml_filename):
        xml_path = os.path.join(self.xml_dir, xml_filename)
        tree = lxml.etree.parse(xml_path)
        root = tree.getroot()
        boxes = [
            [
                int(obj.find(".//bndbox/xmin").text),
                int(obj.find(".//bndbox/ymin").text),
                int(obj.find(".//bndbox/xmax").text),
                int(obj.find(".//bndbox/ymax").text),
            ]
            for obj in root.findall(".//object")
        ]
        return boxes

    def get_data_labels(self, xml_filename):
        xml_path = os.path.join(self.xml_dir, xml_filename)
        tree = lxml.etree.parse(xml_path)
        root = tree.getroot()
        labels = [
            1 if obj.find("name").text == "Close" else 2
            for obj in root.findall(".//object")
        ]
        return labels

    def get_data_area(self, xml_filename):
        boxes = self.get_data_boxes(xml_filename)
        areas = [(xmax - xmin) * (ymax - ymin) for xmin, ymin, xmax, ymax in boxes]
        return areas


dataset = PascalVOCDataset("./img", "./img")
