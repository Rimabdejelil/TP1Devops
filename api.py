import io
import base64
import subprocess
import re
import ast
from tt import run_sejourAncienVerso
import torch
#import redis
from models.experimental import attempt_load
from flask import Flask, render_template, jsonify, request
import cv2
from subprocess import Popen
#ocr = PaddleOCR(use_angle_cls = True ,lang='fr')
# -*- coding: utf-8 -*-
from flask import Flask, request , jsonify
#from paddleocr import PaddleOCR
import numpy as np
import cv2
import sys
from PIL import Image

import os
from flask import render_template,flash,redirect
from PIL import Image
import locale
import time
sys.stdout.reconfigure(encoding='utf-8')
import sys
import io
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from SejourAncien import run_sejourAncien
from verso import run_verso_one , run_verso_two
from CIN_TN import run_cin
from Sejour2 import run_sejour2
from ID_FR2 import run_CINFR2
from PASSEPORT2 import run_PASSEPORT2
from Card_ID_ancien2 import run_CINFR_ancien2
from flask import Flask, request, jsonify, send_file
import subprocess
import os
#from detect_and_crop import detect
import glob
#from detect_and_crop import detect
import numpy as np
from utils.torch_utils import select_device, TracedModel
from PasseportTun import run_PassTN
sys.stdout.reconfigure(encoding='utf-8')
import cv2


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#def detect_id_card(path):
#    try:
        #process = Popen(["python", "detect_and_crop.py", '--source', path, "--conf", "0.3", "--weights", "tinyy.pt"])
        #process.wait()
    #    path = os.path.join("detected_cards.json")
     #   return path
    #except Exception as e:
     #   print(f"An error occurred during detection: {e}")
      #  return None

#@app.route('/')
#def index():
    #return render_template('index.html')

# Configuration de la connexion Redis

    
@app.route('/kyc', methods=['POST'])
def kyc():
    

    image_file = request.files['file']
    input_image_path = f"input_image_{int(time.time())}.jpg"  # Utilisation d'un horodatage pour le nom du fichier
    image_file.save(input_image_path)

        # Appeler le script detect_and_crop.py en tant que sous-processus
    process = subprocess.Popen(["python", "detect_and_crop1.py", '--source', input_image_path , "--conf", "0.4", "--weights", "best.pt"], stdout=subprocess.PIPE)
    process.wait()

    # Lire la sortie du processus
    output = process.stdout.read().decode('utf-8')

    # Utiliser une expression régulière pour extraire le texte du tenseur
    start_index = output.find('[[')
    end_index = output.find(']]', start_index)

# Extraire le texte du tenseur
    tensor_text = output[start_index:end_index + 2]
    if (tensor_text) :
        try:

# Évaluer le texte du tenseur en tant que liste de listes
            tensor_data = ast.literal_eval(tensor_text)

# Convertir la liste de listes en un tenseur torch
        


            pred = torch.tensor(tensor_data)
        #print(pred)

        #detect_id_card(input_image_path)

        
            detected_cards = []
            for *xyxy, conf, cls in pred:
                if conf > 0.45:
                    xyxy_np = np.array(xyxy)
                    if (0 <= int(cls) <= 4) or (int(cls) == 8) or (int(cls) == 9)  :
                        detected_cards.append({"type": "recto", "class": int(cls), "coordinates": xyxy_np.tolist()})
                    elif (5 <= int(cls) <= 7) or (5 <= int(cls) == 10) :
                        detected_cards.append({"type": "verso", "class": int(cls), "coordinates": xyxy_np.tolist()})

        
        #path = detect_id_card(input_image_path)

        #detected_cards = []

        #with open(path, "r") as f:
         #   detected_cards = json.load(f)
        
            output = []
            combined_info = {}
        
            for card in detected_cards:
                card_type = card["type"]
                card_class = card["class"]
                card_coordinates = card["coordinates"]

                card_info = {}

                if card_type == "recto":
                    if card_class == 0:
                        try:
                            card_info.update(run_cin(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during CIN processing: {e}")
                            return jsonify({"error": "Error during CIN processing"})
                    elif card_class == 1:
                        try:
                            card_info.update(run_sejour2(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during Sejour processing: {e}")
                            return jsonify({"error": "Error during Sejour processing"})
                    elif card_class == 2:
                        try:
                            card_info.update(run_PASSEPORT2(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during PASSEPORT processing: {e}")
                            return jsonify({"error": "Error during PASSEPORT processing"})
                    elif card_class == 3:
                        try:
                            card_info.update(run_CINFR_ancien2(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during CINFRANCIEN processing: {e}")
                            return jsonify({"error": "Error during CINFRANCIEN processing"})
                    elif card_class == 4:
                        try:
                            card_info.update(run_CINFR2(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during CINFR processing: {e}")
                            return jsonify({"error": "Error during CINFR processing"})
                    elif card_class == 8:
                        try:
                            card_info.update(run_PassTN(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during PasseportTN processing: {e}")
                            return jsonify({"error": "Error during PasseportTN processing"})
                    elif card_class == 9:
                        try:
                            card_info.update(run_sejourAncien(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during SejourAncien processing: {e}")
                            return jsonify({"error": "Error during SejourAncien processing"})

        
        
                elif card_type == "verso":
                    if card_class == 5:
                        try:
                            card_info.update(run_verso_two(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during CINFRANCIENVERSO processing: {e}")
                            return jsonify({"error": "Error during CINFRANCIENVERSO processing"})
                    elif card_class == 6:
                        try:
                            card_info.update(run_verso_one(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during TitreSejourFRVerso processing: {e}")
                            return jsonify({"error": "Error during TitreSejourFRVerso processing"})
                    elif card_class == 7 :
                        try:
                            card_info.update(run_verso_one(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during CINFRVerso processing: {e}")
                            return jsonify({"error": "Error during CINFRVerso processing"})
                        
                    elif card_class == 10 :
                        try:
                            card_info.update(run_sejourAncienVerso(input_image_path, card_coordinates))
                        except Exception as e:
                            print(f"An error occurred during SejourFrAncienVerso processing: {e}")
                            return jsonify({"error": "Error during SejourFrAncienVerso processing"})
                combined_info.update(card_info)
            output.append(combined_info)
            os.remove(input_image_path)
            return jsonify(output)
        except Exception as e:
            print(f"An error in the image format: {e}")
            return jsonify({"error": "Error in the image format"})

    #except Exception as e:
     #   print(f"An error occurred during image processing: {e}")
      #  return jsonify({"error": "Error during image processing"})
    
    
     
    
    else :
        os.remove(input_image_path)
        return jsonify({"error": "Error in the image format"})
    
      

   #return(jsonify(output))
    # Render the template with the output
    #return render_template('index.html', result=output)
    #return(jsonify(output))


if __name__ == "__main__":
    # Disable debug mode when not in development environment
    app.run(host='0.0.0.0',debug=True, port=9025)
