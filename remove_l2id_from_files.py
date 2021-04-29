import shutil
import glob
from tqdm.auto import tqdm

dir_src = 'C:/Users/R/PycharmProjects/Thesis_Saatchi_scraper/images'
dir_dst = 'C:/Users/R/PycharmProjects/Thesis_Saatchi_scraper/images_no_id/'

l = glob.glob(dir_src + '/*.jpg')

for file in tqdm(l):
    filename = file.split('\\')[-1]
    new_filename = filename.split('_', 1)[1:][0]
    shutil.copy(file, dir_dst + new_filename)