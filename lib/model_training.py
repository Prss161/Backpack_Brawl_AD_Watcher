import os
import lxml
import torch
import torchvision
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
        return labels

    def get_data_image_id(self, xml_filename):
        return xml_filename.split(".")[0]

    def get_data_area(self, xml_filename):
        boxes = self.get_data_boxes(xml_filename)
        areas = [(xmax - xmin) * (ymax - ymin) for xmin, ymin, xmax, ymax in boxes]
        return areas


dataset = PascalVOCDataset("./img")
print(dataset.get_data_labels("screenshot_2025-02-15_21-51-34.xml"))
print(dataset.get_data_area("screenshot_2025-02-15_21-51-34.xml"))
