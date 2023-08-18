# import cv2
# import albumentations as A

# import torch

from typing import Any
# from api_server.libs.model import BuildModel
# from albumentations.pytorch.transforms import ToTensorV2


# def transform() -> Any:
#     return A.Compose([A.Normalize(
#         mean = [0.485, 0.456, 0.406], 
#         std = [0.229, 0.224, 0.225], 
#         max_pixel_value = [255.0], 
#         p = 1.0), # 正規化。
#             ToTensorV2(p = 1.0) # 歸一化
#             ], p = 1.0)


class Inference:
    def __init__(self) -> None:
        self.model = None

    def run(sef, models_name_list, file_path) -> str:
        return "test"
    # @torch.no_grad()
    # def run((sef, models_name_list, file_path) -> str:
    #     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #     transforms = transform()

    #     image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    #     image = cv2.resize(image, (512, 512), interpolation = cv2.INTER_LINEAR)
    #     image = transforms(image = image)['image'].unsqueeze(0)
    #     image = image.to(device)

    #     ensemble_percentage = 0.0
    #     for model_name in models_name_list:
    #         model = BuildModel()
    #         state = torch.load("model/" + model_name, map_location= device)['model']
    #         model.load_state_dict(state, strict = True)
    #         model = model.to(device)
    #         model.eval()

    #         prediction = model(image)
    #         ensemble_percentage += prediction.sigmoid().cpu().numpy()[0][0]

    #     ensemble_percentage = ensemble_percentage / len(model_name_list)
    #     if ensemble_percentage > 0.5:
    #         return "ok (" + str(ensemble_percentage) + ")"
    #     else:
    #         return "ok (" + str(ensemble_percentage) + ")"
