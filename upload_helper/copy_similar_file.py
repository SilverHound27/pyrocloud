from shutil import copyfile
import os
import time


async def copy_file(input_file, output_dir):
    output_file = os.path.join(
        output_dir,
        str(time.time()) + ".jpg"
    )
    
    copyfile(input_file, output_file)
    return output_file
