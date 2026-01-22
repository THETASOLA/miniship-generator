from PIL import Image
from PIL import ImageEnhance


class ImageResizer:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.addIcon = []
        self.already_resized = False
        self.black_lines_cache = [None] * 6
        self.image_position = None
        self.addIcon_bottom = None
        self.addIcon_bottom_right = None

        sizeX, sizeY = Image.open(input_path).width, Image.open(input_path).height
        if sizeX < 200 or sizeY < 130:
            self.already_resized = True
        
    def acquire_new_size(self, image, target_width=191, target_height=121):
        image_width, image_height = image.size
        new_width = target_width - 5
        new_height = int(image_height * new_width / image_width)
        if new_height > target_height:
            new_height = target_height - 5
            new_width = int(image_width * new_height / image_height)
        return (new_width, new_height)
        
    def acquire_black_lines(self, image):
        original_image = Image.open(image)
        # Convert to RGBA mode if necessary
        if original_image.mode != "RGBA":
            original_image = original_image.convert("RGBA")
            
        for y in range(original_image.height):
            for x in range(original_image.width):
                if original_image.getpixel((x, y))[0] < 20 and original_image.getpixel((x, y))[1] < 20 and original_image.getpixel((x, y))[2] < 20 and original_image.getpixel((x, y))[3] > 0:
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
        
        if self.addIcon_bottom and self.addIcon_bottom != "None":
            cpy = Image.open("customizeUI/bbox/"+self.addIcon_bottom)
            image.paste(cpy, (0, 0), cpy)
            
        if self.addIcon_bottom_right and self.addIcon_bottom_right != "None":
            cpy = Image.open("customizeUI/elite/"+self.addIcon_bottom_right)
            image.paste(cpy, (0, 0), cpy)
    
    def setup_add_icon_temp(self, image, icon_path, elevation = 0):
        self.addIcon.append([icon_path, elevation])
        self.setup_add_icon(image)
        self.addIcon.remove([icon_path, elevation])
    
    def cache_black_lines(self, image):

        for i in range(6):
            self.upsize_black_lines(image, Image.new("RGBA", (191, 121)), i)
        
    def upsize_black_lines(self, image, miniship_image, count=1):
        if self.black_lines_cache[count] != None:
            miniship_image.alpha_composite(self.black_lines_cache[count], self.image_position)
            return
        
        black_lines = self.acquire_black_lines(image)
        target_size = self.acquire_new_size(black_lines)
        
        for i in range(count,0,-1):
            for y in range(1, black_lines.height):
                for x in range(1, black_lines.width):
                    if black_lines.getpixel((x, y))[3] > 0:
                        black_lines.putpixel((x, y), (0, 0, 0, 255))
            black_lines = black_lines.resize((target_size[0]*i, target_size[1]*i), Image.BILINEAR)
        black_lines = black_lines.resize((target_size[0], target_size[1]), Image.BILINEAR)
            
        miniship_image.alpha_composite(black_lines, self.image_position)
        self.black_lines_cache[count] = black_lines
    
    def sharpen(self, image, sharpness=4.0):
        if self.already_resized:
            return image
        return ImageEnhance.Sharpness(image).enhance(sharpness)

    def resize_image(self, target_width=191, target_height=121):
        
        if self.already_resized:
            img = Image.open(self.input_path)
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            return img

        result_image = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        original_image = Image.open(self.input_path)
        
        # Convert to RGBA mode if necessary
        if original_image.mode != "RGBA":
            original_image = original_image.convert("RGBA")

        resized_image = original_image.resize(self.acquire_new_size(original_image), Image.NEAREST)
        self.image_position = ((target_width - resized_image.width) // 2, (target_height - resized_image.height) // 2)
        paste_position = (self.image_position)
        
        # Ensure resized image is in RGBA mode for alpha_composite
        if resized_image.mode != "RGBA":
            resized_image = resized_image.convert("RGBA")
            
        result_image.alpha_composite(resized_image, paste_position)

        return result_image

    def save_image(self, image, path):
        image.save(path)
