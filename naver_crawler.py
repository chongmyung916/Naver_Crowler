import os
import time
import requests
from PIL import Image
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.chrome.options import Options  
import os
import cv2
import numpy as np
from glob import glob
from tqdm import tqdm
from io import BytesIO

def naver_image_crawler(query, max_images=100, save_dir='images'):
    # 저장 폴더 생성
    os.makedirs(save_dir, exist_ok=True)

    # Chrome 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver 경로 지정 (본인 환경에 맞게 수정)
    driver_path = '/usr/local/bin/chromedriver'  # 또는 '~/Downloads/chromedriver' 등

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={query}")
    time.sleep(2)

    # 페이지 스크롤 다운
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    image_elements = driver.find_elements(By.CSS_SELECTOR, "img._fe_image_tab_content_thumbnail_image")

    image_urls = []
    for img in image_elements:
        url = img.get_attribute('src')
        if url and url.startswith('http'):
            image_urls.append(url)
        if len(image_urls) >= max_images:
            break

    driver.quit()

    print(f" 총 {len(image_urls)}개의 이미지 URL 수집됨. 저장 시작...")

    for i, url in enumerate(tqdm(image_urls)):
        try:
            response = requests.get(url, timeout=5)
            image = Image.open(BytesIO(response.content)).convert("RGB")
            image.save(os.path.join(save_dir, f"{query}_{i+1}.jpg"))
        except Exception as e:
            print(f"[오류] 이미지 저장 실패: {e}")

    print(" 이미지 저장 완료!")


# === 전처리 함수들 ===
def is_blurry(image, threshold=100.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var() < threshold

def process_image(path, output_path, size=(640, 640)):
    try:
        image = cv2.imread(path)
        if image is None:
            return False

        h, w = image.shape[:2]
        if h < 300 or w < 300:
            return False
        if h < size[0] or w < size[1]:
            return False
        if is_blurry(image):
            return False

        resized = cv2.resize(image, size)
        cv2.imwrite(output_path, resized)
        return True
    except:
        return False

# === 전처리 실행 함수 ===
def preprocess_all_images(base_dir, bread_types):
    for bread in bread_types:
        safe_name = bread.replace(" ", "_")
        image_dir = os.path.join(base_dir, safe_name)
        os.makedirs(image_dir, exist_ok=True)
        image_paths = glob(os.path.join(image_dir, "*"))

        print(f"Processing images for: {bread} ({len(image_paths)} files)")

        for idx, path in enumerate(tqdm(image_paths)):
            output_path = os.path.join(image_dir, f"{idx:04d}.jpg")
            success = process_image(path, output_path)
            if not success and os.path.exists(output_path):
                os.remove(output_path)

    print(" All image preprocessing completed.")
    
# 실행 예시
if __name__ == "__main__":
    bread_types = ["도넛", "에그타르트"]  
    base_dir = "./naver_images"

    # (1) 이미지 크롤링 실행 (naver_image_crawler 함수 호출)
    for bread in bread_types:
        save_path = os.path.join(base_dir, bread.replace(" ", "_"))
        os.makedirs(save_path, exist_ok=True)
        naver_image_crawler(bread, max_images=50, save_dir=save_path)

    # (2) 전처리 실행
    preprocess_all_images(base_dir, bread_types)

