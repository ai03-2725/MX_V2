import argparse
import sys
from pathlib import Path
import uuid
import keysizes


class FootprintParser:
    # Parses footprint files (and similar lisp-like notations)

    def __init__(self, input_string, debug):
        self.debug = debug
        if self.debug:
            print("Footprint parser launching with given string:")
            print(input_string)
        self.processed_list = self.parse_list(input_string, 1)["item"]

    def parse_list(self, input_string, start_index):
        ret_list = []
        loop_index = start_index
        while True:
            if loop_index >= len(input_string):
                print("Footprint parsing failed: Unexpected end of file",
                      file=sys.stderr)
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
                print("Footprint parsing failed: Unexpected end of file",
                      file=sys.stderr)
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
                    print(
                        "Creating the following token (at delimiter closing parenthesis):")
                    print(token)
                return {"item": token, "end_index": loop_index}

            # Other = Add to built string and continue on
            token += input_string[loop_index]
            loop_index += 1


class FootprintEncoder:

    def __init__(self, footprint, debug):
        self.debug = debug
        self.encoded_footprint = self.list_to_string(footprint)
        if self.debug:
            print("Encoded footprint:")
            print(self.encoded_footprint)

    def list_to_string(self, input_list):
        string_elements = []
        for element in input_list:
            if isinstance(element, list):
                return_string = self.list_to_string(element)
                string_elements.append(return_string)
            elif isinstance(element, str):
                string_elements.append(element)
        return f"({' '.join(string_elements)})"


class FootprintsGenerator:

    def __init__(self, input_file, output_dir, keysizes_type, family_name, unit_width, unit_height, debug):
        self.debug = debug

        # Choose which unit sizes to generate
        if keysizes_type == "mx":
            self.keysizes = keysizes.KEYSIZES_MX
        elif keysizes_type == "alps":
            self.keysizes = keysizes.KEYSIZES_ALPS
        elif keysizes_type == "alps_mx_stabilizers":
            self.keysizes = keysizes.KEYSIZES_ALPS_MX_STABILIZERS
        elif keysizes_type == "gateron_ks33":
            self.keysizes = keysizes.KEYSIZES_GATERON_KS33
        elif keysizes_type == "kailh_pg1353":
            self.keysizes = keysizes.KEYSIZES_KAILH_PG1353
        else:  # mx_alps
            self.keysizes = keysizes.KEYSIZES_MX_ALPS

        # Generate footprint data
        footprint = self.parse_input(input_file=input_file)
        if self.debug:
            print("Generated footprint data:")
            print(footprint)

        # For each keysize, inject outlines and necessary addons (stabilizer holes and similar)
        for keysize_def in self.keysizes:

            # Inject outline and stabilizers
            footprint_with_outlines = self.generate_footprint_outlines(
                base_footprint=footprint, keysize_def=keysize_def, unit_width=unit_width, unit_height=unit_height)
            final_footprints = self.generate_footprint_stabilizers(
                base_footprint=footprint_with_outlines, keysize_def=keysize_def, keysizes_type=keysizes_type)
            
            # Write each created variant
            for final_footprint in final_footprints:
                encoded_footprint = FootprintEncoder(
                    footprint=final_footprint['footprint'], debug=self.debug)
                keysize_human_readable = keysize_def.get('keysize')
                if isinstance(keysize_def.get('keysize'), (int, float)):
                    keysize_human_readable = f"{keysize_def.get('keysize')}U"
                key_variant_name = f"{keysize_human_readable}{final_footprint['variant_name'] or ''}"
                save_path = output_dir / \
                    f"{family_name}-{key_variant_name}.kicad_mod"

                output_data = encoded_footprint.encoded_footprint.replace("Template", key_variant_name)
                
                with save_path.open(mode='w') as save_file:
                    save_file.write(output_data)
                    save_file.close()

    def parse_input(self, input_file):

        # Parse input file - More or less Lisp format
        # Can contain parentheses legally within quotes
        input_file_opened = input_file.open()

        # Read and convert to single line
        input_string = input_file_opened.read().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

        # Use FootprintParser to convert to a tokenized list
        footprint_elements = FootprintParser(
            input_string=input_string, debug=self.debug).processed_list
        if self.debug:
            print(footprint_elements)

        return footprint_elements

    # Takes footprint object (nested list style) and injects outline box
    def generate_footprint_outlines(self, base_footprint, keysize_def, unit_width, unit_height):
        # (fp_line (start -66.675 -9.525) (end 66.675 -9.525) (layer Dwgs.User) (width 0.15) (tstamp 4de36ae6-8d67-4c45-bd5c-19be16f828ed))
        keysize = keysize_def.get('keysize')
        footprint = base_footprint[:]
        if keysize == "ISO":
            # TODO: Scale ISO based on unit size
            footprint.append(
                f"(fp_line (start -11.90625 19.05) (end -11.90625 0) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start -11.90625 0) (end -16.66875 0) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start -16.66875 -19.05) (end 11.90625 -19.05) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start 11.90625 -19.05) (end 11.90625 19.05) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start -11.90625 19.05) (end 11.90625 19.05) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start -16.66875 -19.05) (end -16.66875 0) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
        elif keysize == "ISO-Rotated":
            footprint.append(
                f'(fp_line (start 19.05 11.90625) (end 19.05 -11.90625) (layer "Dwgs.User") (width 0.15) (tstamp {uuid.uuid4()}))')
            footprint.append(
                f'(fp_line (start 0 11.90625) (end 0 16.66875) (layer "Dwgs.User") (width 0.15) (tstamp {uuid.uuid4()}))')
            footprint.append(
                f'(fp_line (start -19.05 -11.90625) (end 19.05 -11.90625) (layer "Dwgs.User") (width 0.15) (tstamp {uuid.uuid4()}))')
            footprint.append(
                f'(fp_line (start -19.05 16.66875) (end -19.05 -11.90625) (layer "Dwgs.User") (width 0.15) (tstamp {uuid.uuid4()}))')
            footprint.append(
                f'(fp_line (start 19.05 11.90625) (end 0 11.90625) (layer "Dwgs.User") (width 0.15) (tstamp {uuid.uuid4()}))')
            footprint.append(
                f'(fp_line (start -19.05 16.66875) (end 0 16.66875) (layer "Dwgs.User") (width 0.15) (tstamp {uuid.uuid4()}))')
        elif keysize == "6U-Offcenter":
            footprint.append(
                f"(fp_line (start {unit_width * -3.5} {unit_height / 2}) (end {unit_width * 2.5} {unit_height / 2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width * -3.5} {unit_height / -2}) (end {unit_width * 2.5} {unit_height / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width * -3.5} {unit_height / 2}) (end {unit_width * -3.5} {unit_height / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width * 2.5} {unit_height / 2}) (end {unit_width * 2.5} {unit_height / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
        elif keysize == "2U-Vertical":
            footprint.append(
                f"(fp_line (start {unit_width / 2} {unit_height * 2 / 2}) (end {unit_width / -2} {unit_height * 2 / 2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width / 2} {unit_height * 2 / -2}) (end {unit_width / -2} {unit_height * 2 / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width / 2} {unit_height * 2 / 2}) (end {unit_width / 2} {unit_height * 2 / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width / -2} {unit_height * 2 / 2}) (end {unit_width / -2} {unit_height * 2 / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
        else:  # Numerical value
            footprint.append(
                f"(fp_line (start {unit_width * keysize / 2} {unit_height / 2}) (end {unit_width * keysize / -2} {unit_height / 2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width * keysize / 2} {unit_height / -2}) (end {unit_width * keysize / -2} {unit_height / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width * keysize / 2} {unit_height / 2}) (end {unit_width * keysize / 2} {unit_height / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")
            footprint.append(
                f"(fp_line (start {unit_width * keysize / -2} {unit_height / 2}) (end {unit_width * keysize / -2} {unit_height / -2}) (layer Dwgs.User) (width 0.15) (tstamp {uuid.uuid4()}))")

        return footprint

    # Takes footprint object and injects stabilizer holes
    # Returns a list of
    # {
    #     "footprint": footprint,
    #     "variant_name": variant name (appendable to footprint name)
    # }
    def generate_footprint_stabilizers(self, base_footprint, keysize_def, keysizes_type):

        if not keysize_def.get("stabilizer_dist"):
            return [{
                "footprint": base_footprint[:],
                "variant_name": None
            }]

        stabilizer_dist_left = keysize_def.get("stabilizer_dist")
        stabilizer_dist_right = keysize_def.get("stabilizer_dist_right") or keysize_def.get("stabilizer_dist")
        stabilizer_vert = keysize_def.get("stabilizer_vert")

        ret_list = []

        if keysizes_type in ["mx", "mx_alps", "alps_mx_stabilizers"]:
            for variant in [None, "-ReversedStabilizers"]:
                footprint_variant_copy = base_footprint[:]
                flip_multiplier = 1
                if variant:
                    flip_multiplier = -1
                if stabilizer_vert:
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {6.985 * flip_multiplier} {stabilizer_dist_left}) (size 3.048 3.048) (drill 3.048) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {6.985 * flip_multiplier} {stabilizer_dist_right * -1}) (size 3.048 3.048) (drill 3.048) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {-8.255 * flip_multiplier} {stabilizer_dist_left}) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {-8.255 * flip_multiplier} {stabilizer_dist_right * -1}) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                else:
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {stabilizer_dist_left * -1} {-6.985 * flip_multiplier}) (size 3.048 3.048) (drill 3.048) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {stabilizer_dist_right} {-6.985 * flip_multiplier}) (size 3.048 3.048) (drill 3.048) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {stabilizer_dist_left * -1} {8.255 * flip_multiplier}) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    footprint_variant_copy.append(f'(pad "" np_thru_hole circle (at {stabilizer_dist_right} {8.255 * flip_multiplier}) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu *.Mask) (tstamp {uuid.uuid4()}))')
                    
                ret_list.append({
                    "footprint": footprint_variant_copy,
                    "variant_name": variant
                })
        elif keysizes_type in [""]:
            # TODO: Generate plate-mount stabilizer keepout zones for KS-33 footprint types
            ret_list = [{
                "footprint": base_footprint[:],
                "variant_name": None
            }]
        else:
            ret_list = [{
                "footprint": base_footprint[:],
                "variant_name": None
            }]
        
        return ret_list


if __name__ == '__main__':

    # Parse args

    description_cmd = "Generates a footprint library from a single template footprint."
    arg_parser = argparse.ArgumentParser(
        description=description_cmd, formatter_class=argparse.RawTextHelpFormatter)

    description_input = "Specify the input footprint file (i.e. a kicad_mod file without the outer key bounding rectangle)."
    arg_parser.add_argument(
        "-i", "--input-file", dest="input_file", help=description_input, required=True)

    description_output = "Set the output directory (i.e. an empty .pretty folder)."
    arg_parser.add_argument(
        "-o", "--output-dir", dest="output_dir", help=description_output, required=True)

    description_keysizes_type = """Choose the key sizes type that gets generated.
  - mx: Generate standard MX sizes
  - alps: Generate standard alps keysizes (such as 6.5U AEK space)
  - mx_alps: Generate hybrid MX/alps sizes
  - alps_mx_stabilizers: Generate alps keysizes with MX PCB-mount stabilizers (for DCS and similar)
  - gateron_ks33: Generate gateron KS-33 (low-profile v2.0) sizes
  - kailh_pg1353: Generate kailh PG1353 (choc V2) sizes"""
    arg_parser.add_argument("-t", "--keysizes-type", dest="keysizes_type",
                            help=description_keysizes_type, choices=["mx", "alps", "mx_alps", "alps_mx_stabilizers", "gateron_ks33", "kailh_pg1353"], required=True)

    description_family_name = "Specify the output footprint family name (i.e. the MX-Hotswap part of MX-Hotswap-1U.pretty)."
    arg_parser.add_argument(
        "-n", "--family-name", dest="family_name", help=description_family_name, required=True)

#     description_stabilizer_type = """Choose the stabilizer type that gets generated.
#   - mx: Generates standard MX stabilizers, their reversed variants (north/south-facing), and no-stabilizer variants.
#   - none: Generates no stabilizers at all (for Alps and similar where stabilizers are mostly plate mount)."""
#     arg_parser.add_argument("-s", "--stabilizers-type", dest="stabilizers_type",
#                             help=description_stabilizer_type, choices=["mx", "none"], required=True)

    description_unit_width = "Optional: Override unit width. Defaults to 19.05mm."
    arg_parser.add_argument("-uw", "--unit-width", dest="unit_width",
                            help=description_unit_width, type=float, default=19.05)

    description_unit_height = "Optional: Override unit height. Defaults to 19.05mm."
    arg_parser.add_argument("-uh", "--unit-height", dest="unit_height",
                            help=description_unit_height, type=float, default=19.05)

    description_debug = "Optional: Enable debug mode."
    arg_parser.add_argument("-d", "--debug", dest="debug",
                            help=description_debug, action="store_true")

    args = arg_parser.parse_args()
    if args.debug:
        print(args)

    # Sanity check args

    input_file = Path(args.input_file)
    if not input_file.is_file():
        print("Input file invalid", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir)
    if not output_dir.is_dir():
        print("Output dir invalid", file=sys.stderr)
        sys.exit(1)

    # Launch generator

    footprints_generator = FootprintsGenerator(input_file=input_file, output_dir=output_dir, keysizes_type=args.keysizes_type, family_name=args.family_name,
                                               unit_width=args.unit_width, unit_height=args.unit_height, debug=args.debug)
