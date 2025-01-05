import rawpy
import argparse
import os
import cv2


# Setup argument parser
parser = argparse.ArgumentParser()

parser.add_argument("source", 
                    help="The image-file or folder (containing images) you want to modify")

parser.add_argument("-t", "--target",
                    help="Filename or folder where results should be stored. Default is same location as input")

parser.add_argument("--no_denoise", action = "store_true",
                    help="Wether or not to apply NL means denoising. Default is True. Adding this parameter disables the denoising")

def has_valid_fileending(path: str, target_ending = ".nef") -> bool:
    ending = path[-4:]
    if ending.lower() == target_ending:
        return True
    return False

def replace_ending(path: str, new_ending="jpg") -> str:
    new_ending = new_ending.replace(".", "")
    all_parts = path.split(".")

    return ".".join(all_parts[:-1] + [new_ending])



if __name__ == "__main__":
    args = parser.parse_args()
    source: str = os.path.normpath(args.source)
    target: str = args.target
    denoise: bool = args.no_denoise

    # Input parameter checking
    if not os.path.exists(source):
        print(f"Error: The given path '{source}' does not exist")
        exit(1)

    # Check input data
    input_filepaths: list[str] = []
    if os.path.isdir(source):
        input_filepaths = [os.path.join(source, x) for x in os.listdir(source) if has_valid_fileending(x)]
        if len(input_filepaths) == 0:
            print(f"Error: The given folder '{source}' contains no valid input images")
            exit(1)
    elif has_valid_fileending(source):
        input_filepaths = [os.path.normpath(source)]
    else:
        print(f"Error: The given path '{source}' is neither a valid folder nor file")
        exit(1)

    # Check output location

    output_filepaths: list[str] = []
    if target is None:
        output_filepaths = [replace_ending(x, "jpg") for x in input_filepaths]

    elif has_valid_fileending(target, ".jpg") and len(input_filepaths) == 1:
        output_filepaths = [target]

    elif os.path.isdir(target):
        output_filepaths = [os.path.join(target, replace_ending(os.path.basename(x), "jpg")) for x in input_filepaths]
    
    else:
        print("Error: Fileending of target is invalid or folder doesn't exist.")
        exit(1)

    assert len(output_filepaths) == len(input_filepaths)

    # input_filepaths contains all files that need to be processed
    # output_filepaths has a valid output path with valid ending for each entry in input_filepaths

    # Main transform loop
    for i in range(len(input_filepaths)):
        in_path = input_filepaths[i]
        out_path = output_filepaths[i]

        with rawpy.imread(in_path) as rawpy_image:

            raw_image = rawpy_image.postprocess(output_bps=8, fbdd_noise_reduction = rawpy.FBDDNoiseReductionMode(1), use_auto_wb=True,
                                                auto_bright_thr=0.0001, highlight_mode = rawpy.HighlightMode.Clip) # Test highlight modes
            print(raw_image.shape)

            out_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
            if denoise:
                out_image = cv2.fastNlMeansDenoisingColored(out_image)
            cv2.imwrite(out_path, out_image)

    # Delete later
    # for i in range(len(input_filepaths)):
    #     inpt = input_filepaths[i]
    #     out = output_filepaths[i]
    #     print(f"{inpt} \t--\t {out}")