from PIL import Image, ImageFont, ImageDraw


filename = "static/image.JPEG"

class Text:
    def __init__(self, text: str, font: ImageFont):
        self.text = text
        self.font = font
        
        bbox = self.font.getbbox(text)
        self.width = abs(bbox[0] - bbox[2])
        self.height = abs(bbox[1] - bbox[3])
    
    
    def wrap_text(self, max_width):
        lines = []
        current_line = Text("", self.font)
        words = self.text.split(" ")
        
        # TODO: Figure out how to update Text class self.width/height every time self.text is updated
        for word in words:
            word = Text(word, self.font)
            if word.width + current_line.width >= max_width:
                lines.append(current_line)
                current_line.text = ""
            else:
                current_line.text += word.text + " "
        print(lines)
        return lines
    
        
    def get_center_coordinates(self, bbox_width, bbox_height):
        """
        Get the coordinates that would center the text in a given bounding box.
        """
        center_x = (bbox_width - self.width) // 2
        center_y = (bbox_height - self.height) // 2
        
        center = [center_x, center_y]
        return center
    
    
    def draw(self, draw, xy, fill):
        draw.text(
            xy,
            self.text,
            fill=fill,
            font=self.font
        )


class PhotoEditor:
    def __init__(self, filename):
        self.photo = Image.open(filename)
        self.width, self.height = self.photo.size
        self.draw = ImageDraw.Draw(self.photo, "RGBA")
        
        # This is the offset of the rectangle that is drawn over the photo for better readability
        rectangle_x_offset = 50
        rectangle_y_offset = 100 
        
        # This is the rectangle 's xy coordinates
        self.rectangle_x0 = rectangle_x_offset
        self.rectangle_x1 = self.width - rectangle_x_offset
        self.rectangle_y0 = rectangle_y_offset
        self.rectangle_y1 = self.height - rectangle_y_offset
        
    
    def draw_rectangle(self):
        """
        Draw a semi-transparent rectangle over the photo, similar to how quotes are displayed on Instagram. This effect mimics the style where stock photos are paired with a transparent rectangle, and text is written on top of it for better readability.
        """
        xy = (self.rectangle_x0, self.rectangle_y0, self.rectangle_x1, self.rectangle_y1)
        transparency = 200
        self.draw.rectangle(
            xy = xy, 
            fill = (255, 255, 255, transparency), 
            outline = (255, 255, 255), 
        )
        
    
    def draw_quote(self, quote, quotee):
        """
        Draw the quote on top of the photo. It is centered in relation to the transparent rectangle that can be drawn with 'draw_rectangle()'.
        """
        rectangle_width = self.rectangle_x1 - self.rectangle_x0
        rectangle_height = self.rectangle_y1 - self.rectangle_y0
        
        quote_font_size = 300
        quote_font = ImageFont.truetype("fonts/georgia.ttf", quote_font_size)
        quote_text = Text(quote, quote_font)
        
        wrapped_quote_text = quote_text.wrap_text(rectangle_width)
        for i in wrapped_quote_text:
            print(i.text)
        
        quote_xy = quote_text.get_center_coordinates(rectangle_width, rectangle_height)
        
        quote_fill = (0, 0, 0)
        quote_text.draw(self.draw, quote_xy, quote_fill)
        
        quotee_font_size = 250
        quotee_font = ImageFont.truetype("fonts/georgiai.ttf", quotee_font_size)
        quotee_text = Text(quotee, quotee_font)

        quotee_xy = quotee_text.get_center_coordinates(rectangle_width, rectangle_height)
        
        # Offset the quotee's y position by the quote's height and a bit of padding
        padding = 10
        quotee_xy[1] += quote_text.height + padding

        quotee_transparency = 150
        quotee_fill = (117, 128, 129, quotee_transparency)
        quotee_text.draw(self.draw, quotee_xy, quotee_fill)
    
    
    def save_photo(self, file):
        """
        Save the photo.
        """
        self.photo.save(file)
    
    
    def edit_photo(self, quote, quotee, file):
        """
        Execute both 'draw_rectangle()' and 'draw_quote()', and save the Image to 'file'.
        """
        self.draw_rectangle()
        self.draw_quote(quote, quotee)
        self.save_photo(file)

p = PhotoEditor(filename)
p.edit_photo("Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma - which is living with the results of other people's thinking.", "Steve Jobs", filename)