"""Hardware-free tests for temporary ASUS TUF RGB effects."""
import contextlib
import importlib.util
import io
import pathlib
import unittest

MODULE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "rgb_effects.py"
spec = importlib.util.spec_from_file_location("rgb_effects", MODULE)
rgb = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(rgb)


class ColorProtocolTests(unittest.TestCase):
    def test_uses_only_temporary_static_mode(self):
        self.assertEqual(rgb.rgb_command((255, 180, 140)), "0 0 255 180 140 0\n")
        for name in rgb.EFFECTS:
            for color in rgb.frames_for(name, rgb.PEACH):
                command = rgb.rgb_command(color)
                self.assertTrue(command.startswith("0 0 "), (name, command))
                self.assertTrue(command.endswith(" 0\n"), (name, command))

    def test_rgb_validation(self):
        for invalid in ((256, 0, 0), (-1, 2, 3), (0, 0), (12, 2, 3.2)):
            with self.subTest(color=invalid):
                with self.assertRaises(ValueError):
                    rgb.rgb_command(invalid)

    def test_hex_parser(self):
        self.assertEqual(rgb.parse_hex("#FFB48C"), rgb.PEACH)
        self.assertEqual(rgb.parse_hex("00D3B8"), (0, 211, 184))

    def test_all_frames_in_range(self):
        for name in rgb.EFFECTS:
            frames = list(rgb.frames_for(name, rgb.PEACH))
            self.assertGreater(len(frames), 10)
            self.assertTrue(all(len(c) == 3 and all(0 <= n <= 255 for n in c)
                                for c in frames), name)

    def test_fade_palette_loops_back_towards_start(self):
        for name in rgb.PALETTES:
            frames = list(rgb.palette_frames(name))
            self.assertEqual(frames[0], rgb.PALETTES[name][0])
            last = frames[-1]
            first = frames[0]
            self.assertLess(max(abs(a - b) for a, b in zip(last, first)), 24)

    def test_dry_run_does_not_need_hardware(self):
        for name in rgb.EFFECTS:
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(rgb.main([name, "--dry-run", "--cycles", "1"]), 0)
            commands = output.getvalue().splitlines()
            self.assertGreater(len(commands), 10)
            self.assertTrue(all(line.startswith("0 0 ") for line in commands))

    def test_defaults_to_one_cycle_in_dry_run(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(rgb.main(["heartbeat", "--dry-run"]), 0)
        self.assertEqual(len(output.getvalue().splitlines()), 16)

    def test_rejects_unsafe_speed(self):
        for interval in ("0", "0.01", "nan", "inf", "9"):
            with self.subTest(interval=interval), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    rgb.main(["warm", "--dry-run", "--interval", interval])


if __name__ == "__main__":
    unittest.main()
