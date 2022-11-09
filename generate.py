import argparse, sys
from pathlib import Path

class FootprintParser:

  def __init__(self, input_string, debug):
    self.debug = debug
    if self.debug:
      print("Footprint parser launching with given string:")
      print(input_string)
    self.processed_list = self.parse_list(input_string, 1)

  def parse_list(self, input_string, start_index):
    ret_list = []
    loop_index = start_index
    while True:
      if loop_index >= len(input_string):
        print("Footprint parsing failed: Unexpected end of file", file=sys.stderr)
        sys.exit(1)

      # Opening parenthesis = start of a list
      if input_string[loop_index] == '(':
        ret = self.parse_list(input_string, loop_index + 1)
        ret_list.append(ret["item"])
        loop_index = ret["end_index"] + 1
        continue

      # Closing parenthesis = end of a list
      elif input_string[loop_index] == ')':
        if self.debug:
          print("Returning the following list:")
          print(ret_list)
        return {"item": ret_list, "end_index": loop_index}

      # Non-space char = beginning of a literal token
      elif input_string[loop_index] != ' ':
        ret = self.parse_literal(input_string, loop_index)
        ret_list.append(ret["item"])
        loop_index = ret["end_index"]
        continue

      # Space = pass
      loop_index += 1
      continue

  def parse_literal(self, input_string, start_index):
    token = ""
    loop_index = start_index
    within_quotes = False
    while True:
      if loop_index >= len(input_string):
        print("Footprint parsing failed: Unexpected end of file", file=sys.stderr)
        sys.exit(1)

      # Quote = invert within_quotes (allow space)
      if input_string[loop_index] == '"':
        within_quotes = not within_quotes
      
      # Space + not within_quotes = end of a token
      elif input_string[loop_index] == ' ' and not within_quotes:
        if self.debug:
          print("Creating the following token (at delimiter space):")
          print(token)
        return {"item": token, "end_index": loop_index}

      # End parenthesis + not within_quotes = end of a token
      elif input_string[loop_index] == ')' and not within_quotes:
        if self.debug:
          print("Creating the following token (at delimiter closing parenthesis):")
          print(token)
        return {"item": token, "end_index": loop_index}

      # Other = Add to built string and continue on
      token += input_string[loop_index]
      loop_index += 1


class FootprintsGenerator:

  # Choose which unit sizes to generate
  KEYSIZES_MX = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.75, 3, 6, 6.25, 7, 8, 9, 10, "iso", "6U-offcenter"]
  KEYSIZES_ALPS = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.75, 3, 6.25, 6.5, 7, "iso"]

  def __init__(self, input_file, output_dir, keysizes_type, stabilizers_type, debug):
    if args.keysizes_type is "mx":
      self.keysizes = self.KEYSIZES_MX
    elif args.keysizes_type is "alps":
      self.keysizes = self.KEYSIZES_ALPS
    else: #mx_alps hybrid
      self.keysizes = list(set(self.KEYSIZES_MX + self.KEYSIZES_ALPS))

    self.debug = debug
    self.parse_input(input_file=input_file)

  def parse_input(self, input_file):
    # Parse input file - More or less Lisp format
    # Can contain parentheses legally within quotes
    input_file_opened = input_file.open()
    input_string = input_file_opened.read().replace('\n', ' ').replace('\r', ' ')

    footprint_elements = FootprintParser(input_string=input_string, debug=self.debug).processed_list
    print(footprint_elements)



if __name__ == '__main__':

# Parse args 

  description_cmd = "Generates a footprint library from a single template footprint."
  arg_parser = argparse.ArgumentParser(description=description_cmd)

  description_input = "Set input footprint file (i.e. a kicad_mod file without the outer key bounding rectangle)"
  arg_parser.add_argument("-i", "--input-file", dest="input_file", help=description_input, required=True)

  description_output = "Set the output directory (i.e. an empty .pretty folder)"
  arg_parser.add_argument("-o", "--output-dir", dest="output_dir", help=description_output, required=True)

  description_keysizes_type = """Choose the key sizes type that gets generated.
  - mx: Generate standard MX sizes
  - alps: Generate standard alps keysizes (such as 6.5U AEK space)
  - mx_alps: Generate hybrid MX/alps sizes"""
  arg_parser.add_argument("-t", "--keysizes-type", dest="keysizes_type", help=description_keysizes_type, choices=["mx", "alps", "mx_alps"], required=True)

  description_stabilizer_type = """Choose the stabilizer type that gets generated.
  - mx: Generates standard MX stabilizers, their reversed variants (north/south-facing), and no-stabilizer variants.
  - none: Generates no stabilizers at all (for Alps and similar where stabilizers are mostly plate mount)."""
  arg_parser.add_argument("-s", "--stabilizers-type", dest="stabilizers_type", help=description_stabilizer_type, choices=["mx", "none"], required=True)

  description_debug = "Enable debug mode"
  arg_parser.add_argument("-d", "--debug", dest="debug", action="store_true")

  args = arg_parser.parse_args()
  if args.debug:
    print(args)

  input_file = Path(args.input_file)
  if not input_file.is_file():
    print("Input file invalid", file=sys.stderr)
    sys.exit(1)

  output_dir = Path(args.output_dir)
  if not output_dir.is_dir():
    print("Output dir invalid", file=sys.stderr)
    sys.exit(1)

  footprints_generator = FootprintsGenerator(input_file=input_file, output_dir=output_dir, keysizes_type=args.keysizes_type, stabilizers_type=args.stabilizers_type, debug=args.debug)





