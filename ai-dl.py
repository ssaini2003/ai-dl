import aiohttp
import asyncio
import aiofiles
import uuid
import urllib
import json
import os
import argparse

BASE_URL = "https://bf.dallemini.ai/generate"
MAX_IMAGES = 9


class AiDL:
    def __init__(self):
        self.headers = {}
        self.headers["Content-Type"] = "application/json"
        
    
    async def download_image(self, saveloc: str, prompt: str, amnt: int):
        req_info = {"prompt": prompt}

        await asyncio.sleep(1)

        data = json.dumps(req_info)

        to_json = None
        async with aiohttp.ClientSession() as session:
            async with session.post(
                BASE_URL, data=data, headers=self.headers
            ) as resp:
                to_json = await resp.json()

        saved_uuids = []

        # the template to strip out
        data_url_template = "data:image/jpeg;base64,"

        for i in range(0, amnt):
            
            img_id = uuid.uuid4()
            url_fmt = "{}{}".format(data_url_template, to_json["images"][i])
        

            response = urllib.request.urlopen(url_fmt)
            save_direct = "{}/{}.png".format(saveloc, img_id)

            path = save_direct

            async with aiofiles.open(save_direct, mode="wb") as f:
                await f.write(response.file.read())

            saved_uuids.append(img_id)

        return saved_uuids


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--loc', dest='location_arg', type=str, required=False, help="The location to save the images.")
    parser.add_argument('--amnt', dest='amount_arg', type=int, required=False, help="Have a specific amount of images generated.")
    parser.add_argument('--prompt', dest='prompt_arg', type=str, required=True, help="The prompt that will be fed to the generator.")
    args = parser.parse_args()
    amnt = args.amount_arg

    if if amnt is None:
        amnt = 1
    elif or amnt<=0 or amnt>9:        
        print("Invalid amount provided. (Maximum 9 images)")
        
    loc = args.location_arg
    if loc == None:
        loc = os.getcwd()
    prompt = args.prompt_arg



    image_generator = AiDL()
    asyncio.run(image_generator.download_image(loc, prompt, amnt))
