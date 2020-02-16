from docx2csv import extract_tables, extract
import requests

tables = extract_tables('30012020.docx')
for lists in tables:
    for list in lists:
        for bytes in list:
            print(bytes.decode("utf-8"))



 def download_images(self, photo_urls):
        """
        download images
        :return: self.images
        """
        images_paths = []
        for photo_url in photo_urls:
            response = requests.get(photo_url, stream=True)
            path_to_download = self.sources + photo_url.split("/")[-1]
            images_paths.append(path_to_download)
            with open(path_to_download, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
        self.images = os.listdir(path=self.sources)
        logging.debug("All photos has been downloaded")
        return images_paths