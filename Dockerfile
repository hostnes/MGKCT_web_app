FROM python:3.9

#USER www-data

RUN mkdir /project
WORKDIR /project

COPY . /project

RUN pip install --upgrade pip

# RUN pip install --no-cache-dir -r requirements.txt

#RUN apt-get update && apt-get install -y \
#      chromium \
#      chromium-l10n \
#      fonts-liberation \
#      fonts-roboto \
#      hicolor-icon-theme \
#      libcanberra-gtk-module \
#      libexif-dev \
#      libgl1-mesa-dri \
#      libgl1-mesa-glx \
#      libpangox-1.0-0 \
#     libv4l-0 \
#      fonts-symbola \
#      --no-install-recommends \
#    && rm -rf /var/lib/apt/lists/* \
#    && mkdir -p /etc/chromium.d/ \

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 777 /project/scripts/start_celery_worker.sh /project/scripts/start_celery_beat.sh
