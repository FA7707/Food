# UECFoodPIX Food Image Classifier

A food image classification system trained on the [UECFoodPIXCOMPLETE](http://mm.cs.uec.ac.jp/uecfoodpix/) dataset. Uses a fine-tuned ResNet-50 to classify images into 102 food categories (plus a background class), with support for GPU training and Windows 11 NPU inference via ONNX Runtime DirectML.

## Overview

| Detail | Value |
|---|---|
| Model | ResNet-50 (pretrained on ImageNet, fine-tuned) |
| Classes | 103 (0 = background, 1–102 = food types) |
| Training images | 9,000 |
| Test images | 1,000 |
| Input size | 224 × 224 |
| Optimizer | AdamW with Cosine Annealing |
| Inference | PyTorch (training) + ONNX Runtime / DirectML (deployment) |

## Requirements

- Python 3.9+
- Windows 11 with NPU support (optional, for DirectML inference)
- CUDA-capable GPU (optional, for faster training)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Download the dataset

Download the **UECFoodPIXCOMPLETE** dataset from the [official source](http://mm.cs.uec.ac.jp/uecfoodpix/) and place it so the directory layout matches:

```
UECFoodPIXCOMPLETE-SPC4001/
└── UECFOODPIXCOMPLETE/
    └── data/
        ├── train9000.txt          # Image IDs for training split
        ├── test1000.txt           # Image IDs for test split
        ├── category.txt           # Category ID → food name mapping
        └── UECFoodPIXCOMPLETE/
            ├── train/
            │   ├── img/           # Training images (.jpg)
            │   └── mask/          # Segmentation masks (.png)
            └── test/
                ├── img/           # Test images (.jpg)
                └── mask/          # Segmentation masks (.png)
```

## Usage

### Train

Trains the model from pretrained ImageNet weights. Saves the best checkpoint as `food_classifier.pth` and automatically exports to `food_classifier.onnx` when training finishes.

```bash
python food_classifier.py --mode train --data_dir ./UECFOODPIXCOMPLETE/data
```

Optional flags:

```bash
--epochs 20        # Number of training epochs (default: 20)
--batch_size 32    # Batch size (default: 32)
--lr 0.001         # Learning rate (default: 0.001)
```

### Test

Evaluates the trained model on the 1,000 test images and prints Top-1 and Top-5 accuracy with a per-class breakdown.

```bash
python food_classifier.py --mode test --data_dir ./UECFOODPIXCOMPLETE/data
```

### Predict (single image)

Runs inference on a single image and prints the predicted food category and confidence.

```bash
python food_classifier.py --mode predict --image path/to/image.jpg
```

### Export to ONNX

Exports the saved PyTorch checkpoint to ONNX format for use with ONNX Runtime.

```bash
python food_classifier.py --mode export
```

### Full evaluation with CSV output

Runs a detailed evaluation and exports per-image predictions and per-class accuracy to `evaluation_results.csv`.

```bash
python evaluate.py --data_dir ./UECFOODPIXCOMPLETE/data
```

## Output Files

| File | Description |
|---|---|
| `food_classifier.pth` | Best model weights (PyTorch checkpoint) |
| `food_classifier.onnx` | Exported model for ONNX Runtime inference |
| `evaluation_results.csv` | Per-image predictions and per-class accuracy |

## How It Works

### Data loading (`UECFoodDataset`)

The dataset class reads the train/test split files to get image IDs, then loads each `.jpg` image alongside its corresponding `.png` segmentation mask. The ground-truth label is extracted from the red channel of the mask — whichever food class appears most frequently (excluding background) is used as the image-level label.

### Model (`build_model`)

ResNet-50 is loaded with pretrained ImageNet weights. Its final fully-connected layer is replaced with a new layer outputting 103 logits (one per class). Only the new head and the final residual block are fine-tuned by default.

### Training pipeline (`train`)

1. Images are augmented (random crop, horizontal flip, color jitter) and normalised with ImageNet statistics.
2. AdamW optimises CrossEntropyLoss; a Cosine Annealing scheduler decays the learning rate each epoch.
3. The checkpoint with the lowest validation loss is saved to `food_classifier.pth`.
4. After training, the model is automatically exported to ONNX.

### NPU/GPU inference (`npu_predict`)

At inference time the ONNX model is loaded into ONNX Runtime. On Windows 11 the DirectML execution provider is used to run inference on the NPU or GPU. If DirectML is unavailable the session falls back to the CPU provider. Softmax is applied to the raw logits to produce a probability distribution over the 103 classes.

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.
