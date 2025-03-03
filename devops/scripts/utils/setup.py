import os
import nltk

nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')

os.environ['OCR_AGENT'] = 'unstructured.partition.utils.ocr_models.tesseract_ocr.OCRAgentTesseract'