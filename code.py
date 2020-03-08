"""Stev0 Adafruit Bsides SD module.

Some of these routines were ripped from examples, others are custom

Run as is, it will cycle through all various defined `routine_*` functions
randomly for RUN_SECONDS  seconds.

To disable the cycle functionality and run a single routine on boot, set
`USE_TIMER` to False
"""
# pylint: disable=import-error, invalid-name
import time
import random
import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

RUN_SECONDS = 5
USE_TIMER = True

NUM_LEDS = 5
BOARD = board.APA102_MOSI

NO_COLOR = fancy.CHSV(0, 0, 0).pack()

# Declare a 6-element RGB rainbow palette
PALETE = [
    fancy.CRGB(1.0, 0.0, 0.0), # Red
    fancy.CRGB(0.5, 0.5, 0.0), # Yellow
    fancy.CRGB(0.0, 1.0, 0.0), # Green
    fancy.CRGB(0.0, 0.5, 0.5), # Cyan
    fancy.CRGB(0.0, 0.0, 1.0), # Blue
    fancy.CRGB(0.5, 0.0, 0.5), # Magenta
]


def _rand_color():
    rval = random.randrange(0, 255)
    _r1 = rval
    _r2 = 255
    _r3 = 255
    return fancy.CHSV(_r1, _r2, _r3).pack()

def _all_off(pixels):
    for i in range(NUM_LEDS):
        pixels[i] = NO_COLOR
    pixels.show()

def _blink(pixels, sleep, cycles):
    state = [
        i
        for i in pixels
    ]
    for _ in range(cycles):
        _all_off(pixels)
        time.sleep(sleep)
        for idx, _ in enumerate(pixels):
            pixels[idx] = state[idx]
        pixels.show()

def _switch_set(pixels, slots, color):
    for i in slots:
        pixels[i] = color
    for i in range(NUM_LEDS):
        if i not in slots:
            pixels[i] = NO_COLOR
    pixels.show()



def routine_1():
    """Original Routine to come with the badge."""
    with neopixel.NeoPixel(
            BOARD,
            NUM_LEDS,
            auto_write=False,
            brightness=0.1
        ) as pixels:
        start = time.monotonic()
        while True:
            now = time.monotonic()
            if abs(now - start) > RUN_SECONDS and USE_TIMER:
                break
            for i in range(256):
                color = fancy.CHSV(i, 255, 255).pack()
                pixels.fill(color)
                pixels.show()
                time.sleep(0.01)

def routine_2():
    """Adafruit Example 2."""
    # Declare a NeoPixel object on pin D6 with num_leds pixels, no auto-write.
    # Set brightness to max because we'll be using FancyLED's brightness control.
    with neopixel.NeoPixel(
            BOARD,
            NUM_LEDS,
            brightness=1.0,
            auto_write=False
        ) as pixels:
        offset = 0  # Positional offset into color palette to get it to 'spin'
        start = time.monotonic()
        while True:
            now = time.monotonic()
            if abs(now - start) > RUN_SECONDS and USE_TIMER:
                break
            for i in range(NUM_LEDS):
                # Load each pixel's color from the palette using an offset, run it
                # through the gamma function, pack RGB value and assign to pixel.
                color = fancy.palette_lookup(PALETE, offset + i / NUM_LEDS)
                color = fancy.gamma_adjust(color, brightness=0.25)
                pixels[i] = color.pack()
            pixels.show()

            offset += 0.01  # Bigger number = faster spin

def routine_3():
    """Original Routine to come with the badge."""
    with neopixel.NeoPixel(
            BOARD,
            NUM_LEDS,
            auto_write=False,
            brightness=0.75
        ) as pixels:
        start = time.monotonic()
        while True:
            now = time.monotonic()
            if abs(now - start) > RUN_SECONDS and USE_TIMER:
                break
            for i in range(NUM_LEDS):
                time.sleep(0.01)
                pixels[i] = _rand_color()
            pixels.show()


def routine_4():
    """Original Routine to come with the badge."""
    sleep_time = .5
    blink_time = .01
    cycles = 50
    with neopixel.NeoPixel(
            BOARD,
            NUM_LEDS,
            auto_write=False,
            brightness=.5
        ) as pixels:
        start = time.monotonic()
        while True:
            now = time.monotonic()
            if abs(now - start) > RUN_SECONDS and USE_TIMER:
                break

            color = _rand_color()

            _switch_set(pixels, [0, 4], color)
            _blink(pixels, blink_time, cycles)
            time.sleep(sleep_time)

            _switch_set(pixels, [1, 3], color)
            _blink(pixels, blink_time, cycles)
            time.sleep(sleep_time)

            _switch_set(pixels, [2], color)
            _blink(pixels, blink_time, cycles)
            time.sleep(sleep_time)

def routine_5():
    """Original Routine to come with the badge."""
    sleep_time = .05
    blink_time = .005
    cycles = 20
    with neopixel.NeoPixel(
            BOARD,
            NUM_LEDS,
            auto_write=False,
            brightness=.5
        ) as pixels:
        start = time.monotonic()

        color = _rand_color()

        while True:
            now = time.monotonic()
            if abs(now - start) > RUN_SECONDS and USE_TIMER:
                break


            for i in range(NUM_LEDS):
                _switch_set(pixels, [i], color)
                _blink(pixels, blink_time, cycles)
                time.sleep(sleep_time)

def routine_6():
    """routine 6."""
    # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
    # NeoPixels must be connected to D10, D12, D18 or D21 to work.
    pixel_pin = BOARD

    # The number of NeoPixels
    num_pixels = 30

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB


    with neopixel.NeoPixel(
            pixel_pin,
            num_pixels,
            brightness=0.2,
            auto_write=False,
            pixel_order=ORDER,
        ) as pixels:

        def wheel(pos):
            # Input a value 0 to 255 to get a color value.
            # The colours are a transition r - g - b - back to r.
            if pos < 0 or pos > 255:
                r = g = b = 0
            elif pos < 85:
                r = int(pos * 3)
                g = int(255 - pos*3)
                b = 0
            elif pos < 170:
                pos -= 85
                r = int(255 - pos*3)
                g = 0
                b = int(pos*3)
            else:
                pos -= 170
                r = 0
                g = int(pos*3)
                b = int(255 - pos*3)
            return (r, g, b) if ORDER in [neopixel.RGB, neopixel.GRB] else (r, g, b, 0)


        def rainbow_cycle(wait):
            for j in range(255):
                for i in range(num_pixels):
                    pixel_index = (i * 256 // num_pixels) + j
                    pixels[i] = wheel(pixel_index & 255)
                pixels.show()
                time.sleep(wait)


        start = time.monotonic()
        while True:
            now = time.monotonic()
            if abs(now - start) > RUN_SECONDS and USE_TIMER:
                break
            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((255, 0, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 255, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 255, 0, 0))
            pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 0, 255))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 0, 255, 0))
            pixels.show()
            time.sleep(1)

            rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step


FUNCS = [
    routine_1,
    routine_2,
    routine_3,
    routine_4,
    routine_5,
    routine_6,
]

def func_loop():
    """Randomize functions in a loop."""
    while True:
        run_val = random.randrange(0, len(FUNCS))
        FUNCS[run_val]()


def main():
    """Run main function."""
    func_loop()


if __name__ == '__main__':
    main()
