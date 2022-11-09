import astropy.io.fits as pyfits
import astropy.wcs as pywcs
import astropy.utils.data as ap_utils
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def gen_LS_url(ra, dec, layer, pixscale, size):
    parsedURL = urlparse('http://legacysurvey.org/viewer/cutout.fits?ra=0.00&dec=0.00&layer=name&pixscale=0.0&size=0')
    query = parse_qs(parsedURL.query)
    query['ra'] = ra
    query['dec'] = dec
    query['layer'] = layer
    query['pixscale'] = pixscale
    query['size'] = size
    newQuery = urlencode(query, doseq=True)
    parsedURL = parsedURL._replace(query=newQuery)
    return urlunparse(parsedURL)

class Image:
    def __init__(self, name, data, hdr, wcs, url):
        self.name = name
        self.data = data
        self.hdr = hdr
        self.wcs = wcs
        self.url = url
    
    def setBoxCoords(self, x0, x1, y0, y1):
        self.x0 = x0; self.x1 = x1
        self.y0 = y0; self.y1 = y1

class MultiWVSource:
    def __init__(self, ra, dec, lsDownload=True):
        self.ra = ra
        self.dec = dec

        if lsDownload: self.downloadLSImages()

    def downloadLSImages(self, layers=['vlass1.2', 'unwise-neo4'], pixscale=0.3514, size=256):
        urlList = []
        for layer in layers:
            urlList.append(gen_LS_url(self.ra, self.dec, layer, pixscale, size))
        
        self.images = []
        imagePaths = ap_utils.download_files_in_parallel(urlList, cache=True)
        for path in imagePaths:
            with pyfits.open(path) as hdulist:
                hdr = hdulist[0].header
                wcs = pywcs.WCS(hdr)
                url = urlList[imagePaths.index(path)]
                if len(hdulist[0].data.shape) == 2: 
                    name = layers[imagePaths.index(path)]+'_0'
                    data = hdulist[0].data
                    self.images.append(Image(name, data, hdr, wcs, url))
                else:
                    for i in range(hdulist[0].data.shape[0]):
                        name = layers[imagePaths.index(path)]+'_'+str(i)
                        data = hdulist[0].data[i]
                        self.images.append(Image(name, data, hdr, wcs, url))
    
    def setAllCoords(self, x0, x1, y0, y1):
        for image in self.images:
            image.setBoxCoords(x0, x1, y0, y1)

    def setComplexity(self, complexity):
        self.complexity = complexity

    '''def getBoxRaDec(self):
        # Use header to calculate ra/dec from pixel coords
        raDecBox = []
        for [x,y] in [[self.x1,self.y1],[self.x2,self.y2]]:
            skycoord = self.wcs_img.pixel_to_world(x,y)
            ra = skycoord.ra.deg
            dec = skycoord.dec.deg
            raDecBox.append([ra,dec])
        [[self.ra1, self.dec1], [self.ra2, self.dec2]] = raDecBox
        return np.array(raDecBox).flat

    def getBoxRaDecCenter(self):
        return [np.mean([self.ra1, self.ra2]),np.mean([self.dec1,self.dec2])]

    def getSourceData(self):
        xyCoords = [self.x1, self.y1, self.x2, self.y2]
        raDecCoords = self.getBoxRaDec
        return [self.ra, self.dec, xyCoords, raDecCoords, self.images, self.wcs_img]'''