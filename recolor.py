#!/usr/bin/env python3
from __future__ import print_function, unicode_literals
import re
import glob
import os
import colorsys
from PyInquirer import prompt, print_json

def hex_to_rgb(hex_string):
  """ Converts a hex string to an rgb tuple. """
  hex = normalize_hex_color(hex_string).lstrip('#')
  return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
  """ Converts an rgb tuple to a normalized hex string. """
  r, g, b = rgb
  return f"#{r:02x}{g:02x}{b:02x}".upper()

def is_valid_hex_color(input_string):
  """ Returns true if the input is a valid hex color string. """
  pattern = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
  return re.match(pattern, input_string)

def search_hex_values(input_string):
  """ Returns a list with all hex color values in input_string.
      Duplicates included. """
  pattern = r'#(?:[0-9a-fA-F]{3}){1,2}'
  return re.findall(pattern, input_string)

def create_color_dict(hex_values):
  """ Creates a dict with color:color for color in hex_values. """
  return { x: x for x in hex_values }

def replace_single_color(input_string, old, new):
  """ Replaces all occurences of old with new. """
  return input_string.replace(old, new)

def replace_colors(input_string, color_dict):
  """ Replaces all color_dict.keys() with color_dict.values(). """
  for old, new in color_dict.items():
    input_string = input_string.replace(old, new)
  return input_string

def normalize_hex_color(color):
  """ Converts #fff to #FFFFFF. """
  if(len(color) == 4):
    color = ''.join([x*2 for x in color])[1:]
  return color.upper()

def normalize_all_colors(input_string):
  """ Normalizes all hex colors found in input_string. """
  colors = search_hex_values(input_string)
  for c in colors:
    input_string = input_string.replace(c, normalize_hex_color(c))
  return input_string

def list_directory(dir, ext):
  """ Lists all files in the directory which have the proper file extension. """
  return glob.glob(os.path.join(dir, f"*.{ext}"))

def validate_input_directory(dir):
  """ Checks if the directory exists and if it contains any SVG files. """
  if not os.path.isdir(dir):
    return 'Directory does not exist.'
  if len(list_directory(dir, 'svg')) == 0:
    return 'No SVG files found in the directory.'
  return True

def select_input_directory():
  question = [{
    'type': 'input',
    'name': 'directory',
    'message': 'Please select an input directory:',
    'validate': validate_input_directory,
    'filter': os.path.normpath
  }]
  answer = prompt(question)
  return answer['directory']

def validate_output_directory(dir):
  """ Checks if the output directory exists and creates it if it doesn't. """
  if os.path.isdir(dir):
    return True
  try:
    os.makedirs(dir)
  except:
    return 'The directory can not be created.'
  return True

def select_output_directory():
  question = [{
    'type': 'input',
    'name': 'directory',
    'message': 'Where do you want to save the output?',
    'validate': validate_output_directory,
    'filter': os.path.normpath
  }]
  answer = prompt(question)
  return answer['directory']

def confirm_overwrite():
  question = [{
    'type': 'confirm',
    'name': 'overwrite',
    'message': 'Some files will be overwritten. Continue anyway?'
  }]
  answer = prompt(question)
  return answer['overwrite']

def main():
  """
  Prompts the user to select an input directory. Then allows him to
  replace colors for all SVGs in that directory and save them to an
  output directory.
  """
  input_dir = select_input_directory()
  # Find all svg files in cwd.
  filelist = {}
  for file in list_directory(input_dir, 'svg'):
    with open(file, 'r') as f:
      contents = f.read()
      filelist[file] = normalize_all_colors(contents)
  print(f'Found {len(filelist)} SVGs in the input directory.')

  # Find all hex color values in those files.
  all_contents = '\n'.join(filelist.values())
  colors = create_color_dict(search_hex_values(all_contents))

  # Replace colors in dictionary.
  while True:
    choices = [f'{k} ({v})' for k, v in colors.items()] + ['Save..', 'Cancel']
    # Select a color.
    questions = [{
      'type': 'list',
      'name': 'replace',
      'message': 'Select a color to replace (current replacement displayed in braces):',
      'choices': choices,
      'filter': lambda x: x[:7]
    }]
    selection = prompt(questions)
    if selection['replace'] == 'Save..':
      break
    if selection['replace'] == 'Cancel':
      return
    # Replace the color.
    questions = [{
      'type': 'input',
      'name': 'color',
      'message': 'Please choose a new value for {}:'.format(selection['replace']),
      'validate': lambda x: True if is_valid_hex_color(x) else "Not a valid hex color.",
      'filter': normalize_hex_color
    }]
    answer = prompt(questions)
    colors[selection['replace']] = answer['color']

  # Select an output directory.
  while True:
    output_dir = select_output_directory()
    output_files = { os.path.join(output_dir, os.path.basename(file)): replace_colors(content, colors) for file, content in filelist.items() }
    files_exist = any([ os.path.isfile(file) for file in output_files.keys() ])
    if not files_exist or confirm_overwrite():
      for file, content in output_files.items():
        with open(file, 'w') as f:
          f.write(content)
      break

if __name__ == '__main__':
  main()