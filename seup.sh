# for the base
conda create -n its490 python=3.7
conda activate its490
# for ai
conda install -c fastchan fastai
# for www
conda install -c conda-forge starlette
conda install -c conda-forge uvicorn
conda install -c conda-forge aiohttp
conda install -c conda-forge python-multipart