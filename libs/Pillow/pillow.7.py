from PIL import Image

# load the image
image = Image.open('opera_house.jpg')

# report the size of the image
print(image.size)

# create a thumbnail and preserve aspect ratio
image.thumbnail((100,100))

# report the size of the thumbnail
print(image.size)

image.show()
