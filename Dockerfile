#dockerfile , dockerimage ,  dockercontainer

FROM python:3.9-slim-buster

WORKDIR /app



#ADD ocr.py .

# Copy the requirements files first to utilize Docker caching
COPY requirements.txt requirements_cpu.txt ./

# Install dependencies


# Copy your scripts and directories
COPY api.py detect_and_crop.py CIN_TN.py Card_ID_ancien.py PASSEPORT.py Sejour.py ID_FR.py new_weights.pt ./
COPY utils ./utils
#COPY templates ./templates
COPY models ./models
#COPY Multilingual_PP-OCRv3_det_infer.tar ch_ppocr_mobile_v#2.0_cls_infer.tar arabic_PP-OCRv3_rec_infer.tar  ./



RUN pip install flask 
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements_cpu.txt
RUN sudo apt-get install -y libgl1-mesa-glx libgomp1 libglib2.0-0 
#RUN apt-get install -y '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
#RUN apt-get install qt5-default
#RUN export QT_QPA_PLATFORM=offscreen
#RUN pip uninstall opencv-python

RUN python -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
#RUN pip install paddlepaddle
RUN pip install "paddleocr>=2.0.1" # Recommend to use version 2.0.1+
#RUN pip uninstall -y opencv-python
#RUN pip install opencv-python-headless

#RUN apt-get install -y ffmpeg libsm6 libxext6  -y
#RUN apt install -y libxkbcommon-x11-0


EXPOSE 8050



CMD ["python3", "-m", "api", "run", "--host=0.0.0.0"]

#CMD ["python","./ocr.py"]

#https://paddleocr.bj.bcebos.com/PP-OCRv3/multilingual/Multilingual_PP-OCRv3_det_infer.tar
#https://paddleocr.bj.bcebos.com/PP-OCRv3/multilingual/arabic_PP-OCRv3_rec_infer.tar
#https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar