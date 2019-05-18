import unittest
import recolor
from recolor import search_hex_values, create_color_dict, replace_single_color, replace_colors, normalize_hex_color, is_valid_hex_color, normalize_all_colors


class TestColorParsing(unittest.TestCase):
  def test_is_valid_hex_color(self):
    valid = "#fff"
    self.assertTrue(is_valid_hex_color(valid))
    valid = "#AABC34"
    self.assertTrue(is_valid_hex_color(valid))
    invalid = "#AABC4"
    self.assertFalse(is_valid_hex_color(invalid))


  def test_search_hex_values(self):
    haystack = 'This #fff text #5Abd3C includes #AAABBB five #fff hex #FFa423 values.'
    needles = search_hex_values(haystack)
    self.assertEqual(len(needles), 5, "Should be 5.")

  def test_create_color_dict(self):
    hex_values = ['#fff', '#5Abd3c', '#fff', '#FFa423']
    color_dict = create_color_dict(hex_values)
    self.assertEqual(len(color_dict), 3, "Should be 3.")

  def test_replace_single_color(self):
    haystack = 'This #fff text #fff includes #AAABBB white.'
    replaced = replace_single_color(haystack, '#fff', '#000')
    self.assertEqual(replaced, 'This #000 text #000 includes #AAABBB white.', "Should include #000.")

  def test_replace_colors(self):
    haystack = 'This #fff text #fff includes #AAABBB white.'
    color_dict = { '#fff': '#000', '#AAABBB': '#AB24CB' }
    replaced = replace_colors(haystack, color_dict)
    self.assertEqual(replaced, 'This #000 text #000 includes #AB24CB white.', "Should include #000 and #AB24CB.")

  def test_normalize_color(self):
    input_color = '#fff'
    output_color = normalize_hex_color(input_color)
    expected_color = '#FFFFFF'
    self.assertEqual(output_color, expected_color, "Should be #FFFFFF.")

  def test_normalize_all_colors(self):
    input_string = 'This #fff is a #FF string with #FAFAFA hex values #000.'
    output_string = normalize_all_colors(input_string)
    expected_output = 'This #FFFFFF is a #FF string with #FAFAFA hex values #000000.'
    self.assertEqual(output_string, expected_output)

  def test_hex_to_rgb(self):
    self.assertEqual((0, 0, 0), recolor.hex_to_rgb('#000000'))
    self.assertEqual((255, 255, 255), recolor.hex_to_rgb('#FFF'))
    self.assertEqual((190, 80, 80), recolor.hex_to_rgb('#be5050'))

  def test_rgb_to_hex(self):
    self.assertEqual('#000000', recolor.rgb_to_hex((0, 0, 0)))
    self.assertEqual('#FFFFFF', recolor.rgb_to_hex((255, 255, 255)))
    self.assertEqual('#BE5050', recolor.rgb_to_hex((190, 80, 80)))




if __name__ == '__main__':
  unittest.main()