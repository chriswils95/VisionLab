from dataset import ImageClassificationDataset
import torchvision.transforms as transforms


class Train_model():
  def __init__(self, directory, CATEGORIES):
   self.directory = directory
   self.categories = CATEGORIES
   self.TRANSFORMS = transforms.Compose([
       transforms.ColorJitter(0.2,0.2,0.2,0.2),
       transforms.Resize((224,224)),
       transforms.ToTensor(),
       transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
   ])
   self.dataset = ImageClassificationDataset(self.directory, self.categories, self.TRANSFORMS)

