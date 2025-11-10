import os, tempfile
from typing import List, Tuple
import torch
from transformers import pipeline
from PIL import Image
import cv2
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from detoxify import Detoxify

caption_filter = Detoxify('unbiased')
CAP_THRES = 0.75

MODEL_ID = "Falconsai/nsfw_image_detection"
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline("image-classification", model=MODEL_ID, device=device)
THRESHOLD = 0.75

def classify_images(images: List[Image.Image]) -> Tuple[bool, int, float]:
    """Classify batch of images. Returns (blocked, nsfw_count, max_score)"""
    if not images:
        return (False, 0, 0.0)
    
    outputs = classifier(images)
    nsfw_count = 0
    max_score = 0.0
   
    for res in outputs:
        nsfw_pred = next((p for p in res if p['label'].lower() == 'nsfw'), None)
        if nsfw_pred and nsfw_pred['score'] >= THRESHOLD:
            nsfw_count += 1
            max_score = max(max_score, nsfw_pred['score'])
    
    return (nsfw_count > 0, nsfw_count, max_score)


def extract_video_frames(video_bytes: bytes, max_frames: int = 30, every_secs: float = 1.0) -> List[Image.Image]:
    """Extract frames using scene detection + uniform sampling"""
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp.write(video_bytes)
        tmp_path = tmp.name
    
    try:
        # Scene detection
        scene_frames = []
        try:
            video = open_video(tmp_path)
            sm = SceneManager()
            sm.add_detector(ContentDetector(threshold=27.0)) # tune if req.
            sm.detect_scenes(video)
            scenes = sm.get_scene_list()
            # middle frame per scene
            for s, e in scenes[:max_frames]:
                mid = (s.get_frames() + e.get_frames()) // 2
                scene_frames.append(mid)
        except:
            scene_frames = []
        
        # Uniform sampling backup
        cap = cv2.VideoCapture(tmp_path)
        fps = float(cap.get(cv2.CAP_PROP_FPS) or 25.0)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        stride = max(1,int(round(fps*every_secs)))
        uniform_frames = list(range(0, total, stride))[:max_frames]
        cap.release()
        
        # Merge and dedupe
        frame_indices = sorted(set(scene_frames + uniform_frames))[:max_frames]
        if not frame_indices:
            frame_indices = [0, total // 2, total - 1]
        
        # Read frames
        cap = cv2.VideoCapture(tmp_path)
        images = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Downscale for speed
                h, w = frame.shape[:2]
                if max(h, w) > 512:
                    scale = 512 / max(h, w)
                    frame = cv2.resize(frame, (int(w*scale), int(h*scale)),interpolation=cv2.INTER_AREA)
                images.append(Image.fromarray(frame))
        cap.release()
        return images
    
    finally:
        os.unlink(tmp_path)

def filter_caption(caption):
    result = caption_filter.predict(caption)
    block = False
    for k,v in result.items():
        if v > CAP_THRES:
            block = True
    return block



