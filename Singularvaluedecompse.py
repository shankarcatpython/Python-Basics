from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

image_url_in  = r'C:\Users\email\OneDrive\Desktop\TestPhotos\Input\SVD Image.JPG'

# Convering the image to gray scale

img = Image.open(image_url_in)
imggray = img.convert('LA')
#imggray.show()

# Converting the image to mp array

imgmat = np.array(list(imggray.getdata(band=0)),float)
imgmat.shape = (imggray.size[1],imggray.size[0])
imgmat = np.matrix(imgmat)
plt.imshow(imgmat,cmap='gray')

# Singular value decomposistion

u , sigma , V = np.linalg.svd(imgmat)
print(imgmat.shape,u.shape,sigma.shape,V.shape)

#reconating = np.matrix(u[:,:1] * np.diag(sigma[:1])* np.matrix(V[:1,:]))
#plt.imshow(reconating,cmap='gray')

# selecting only few sets of eigen vetors with eigen values with higher values 

for i in [2,4,8,16,32,64,128,256,512,1024]:
    reconating = np.matrix(u[:,:i] * np.diag(sigma[:i])* np.matrix(V[:i,:]))
    plt.imshow(reconating,cmap='gray')
    title = "n = %s" % i
    plt.title(title)
    plt.show()