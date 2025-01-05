import rawpy
import argparse
import os


# Setup argument parser
parser = argparse.ArgumentParser()

parser.add_argument("source", 
                    help="The image-file or folder (containing images) you want to modify")

parser.add_argument("-t", "--target",
                    help="Filename or folder where results should be stored. Default is same location as input")

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


    for i in range(len(input_filepaths)):
        inpt = input_filepaths[i]
        out = output_filepaths[i]
        print(f"{inpt} \t--\t {out}")