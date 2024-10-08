import os
import argparse
from PIL import Image
import math

def exe_to_hex(filepath):
    with open(filepath, 'rb') as file:
        return file.read().hex()

def hex_to_decimal(hex_string):
    decimal_values = [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]
    return decimal_values

def calculate_dimensions(data_length):
    num_pixels = data_length // 3
    width = height = int(math.sqrt(num_pixels))
    
    while width * height < num_pixels:
        width += 1
        height = (num_pixels + width - 1) // width
    
    return width, height

def create_image_from_data(data, output_filepath):
    width, height = calculate_dimensions(len(data))
    
    expected_size = width * height * 3
    if len(data) < expected_size:
        data.extend([0] * (expected_size - len(data)))
    elif len(data) > expected_size:
        data = data[:expected_size]

    image_data = []
    for i in range(height):
        for j in range(width):
            index = (i * width + j) * 3
            if index + 3 <= len(data):
                image_data.append((data[index], data[index+1], data[index+2]))

    image = Image.new('RGB', (width, height))
    image.putdata(image_data)
    image.save(output_filepath)

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if os.path.splitext(filename)[1]:
                exe_path = os.path.join(root, filename)
                hex_data = exe_to_hex(exe_path)
                decimal_data = hex_to_decimal(hex_data)
                
                output_directory = output_dir + 'non_malware'
                
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                
                output_file = os.path.join(output_directory, os.path.splitext(filename)[0] + '.png')
                
                try:
                    create_image_from_data(decimal_data, output_file)
                    print(f"Processed {filename} into image {output_file}")
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert .exe files to images.')
    parser.add_argument('input_dir', type=str, help='Directory containing .exe files.')
    parser.add_argument('output_dir', type=str, help='Directory to save generated images.')
    
    args = parser.parse_args()
    
    process_directory(args.input_dir, args.output_dir)

if __name__ == '__main__':
    main()
