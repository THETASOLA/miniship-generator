from PIL import Image
from PIL import ImageEnhance


class ImageResizer:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.addIcon = []
        
    def acquire_new_size(self, image, target_width=191, target_height=121):
        # Calculate the aspect ratio
        aspect_ratio = image.width / image.height

        # Calculate the new height based on the target width and aspect ratio
        new_height = int(target_height / aspect_ratio)
        return (int(new_height * aspect_ratio), new_height)
        
    
    def acquire_black_lines(self, image):
        original_image = Image.open(image)
        for y in range(original_image.height):
            for x in range(original_image.width):
                if original_image.getpixel((x, y))[0] > 20 and original_image.getpixel((x, y))[1] > 20 and original_image.getpixel((x, y))[2] > 20 and original_image.getpixel((x, y))[3] != 255:
                    if original_image.getpixel((x, y))[0] < 20 and original_image.getpixel((x, y))[1] < 20 and original_image.getpixel((x, y))[2] < 20:
                        original_image.putpixel((x, y), (0, 0, 0, 255))
                    else:
                        original_image.putpixel((x, y), (0, 0, 0, 0))
                
        return original_image
    
    def setup_add_icon(self, image):
        start = Image.open("customizeUI/section_start.png")
        middle_var = Image.open("customizeUI/section_middle.png")
        end = Image.open("customizeUI/section_end.png")
        
        position = [10, 7]
        
        if len(self.addIcon) > 0:
            image.paste(start, (position[0]-3, position[1]), start)
            position[0] += start.width
            for i in range(len(self.addIcon) - 1):
                upped = 3
                if type(self.addIcon[i]) == list:
                    upped = 3 + self.addIcon[i][1]
                    icon = Image.open(self.addIcon[i][0])
                else:
                    icon = Image.open(self.addIcon[i])
                middle = middle_var.copy()
                
                middle = middle.resize((icon.width+3, middle.height), Image.BILINEAR)
                image.paste(middle, (position[0]-3, position[1]), middle)
                image.paste(icon, (position[0], position[1] + upped), icon)
                
                position[0] += icon.width + 3
            
            upped = 3
            middle = middle_var.copy()

            if type(self.addIcon[len(self.addIcon) - 1]) == list:
                upped = 3 + self.addIcon[len(self.addIcon) - 1][1]
                icon = Image.open(self.addIcon[len(self.addIcon) - 1][0])
            else:
                icon = Image.open(self.addIcon[len(self.addIcon) - 1])

            middle = middle.resize((icon.width+3, middle.height), Image.BILINEAR)
            image.paste(middle, (position[0]-3, position[1]), middle)
            position[0] += icon.width
            image.paste(end, (position[0], position[1]), end)
            image.paste(icon, (position[0]- icon.width, position[1] + upped), icon)
    
    def setup_add_icon_temp(self, image, icon_path, elevation = 0):
        self.addIcon.append([icon_path, elevation])
        self.setup_add_icon(image)
        self.addIcon.remove([icon_path, elevation])
            
    
    def upsize_black_lines(self, image):
        black_lines = self.acquire_black_lines(image)
        for i in range(1):
            for y in range(1, black_lines.height):
                for x in range(1, black_lines.width):
                    if black_lines.getpixel((x, y)) == (0, 0, 0, 255):
                        try:
                            black_lines.putpixel((x-1, y-1), (0, 0, 0, 255))
                        except:
                            pass
        black_lines = black_lines.resize(self.acquire_new_size(black_lines), Image.BILINEAR)
        return black_lines
    
    def sharpen(self, image, sharpness=4.0):
        return ImageEnhance.Sharpness(image).enhance(sharpness)

    def resize_image(self, target_width=191, target_height=121):

        result_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        original_image = Image.open(self.input_path)

        resized_image = original_image.resize(self.acquire_new_size(original_image), Image.NEAREST)
        paste_position = ((target_width - resized_image.width) // 2, (target_height - resized_image.height) // 2)
        
        result_image.alpha_composite(resized_image, paste_position)
        result_image.alpha_composite(self.upsize_black_lines(self.input_path), paste_position)

        return result_image

    def save_image(self, image, path):
        image.save(path)
