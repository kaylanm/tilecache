# BSD Licensed, Copyright (c) 2006-2010 TileCache Contributors

from TileCache.Layer import MetaLayer
import TileCache.Client as WMSClient

class WMS(MetaLayer):
    config_properties = [
      {'name':'name', 'description': 'Name of Layer'}, 
      {'name':'url', 'description': 'URL of Remote Layer'},
      {'name':'user', 'description': 'Username of remote server: used for basic-auth protected backend WMS layers.'},
      {'name':'password', 'description': 'Password of remote server: Use for basic-auth protected backend WMS layers.'},
    ] + MetaLayer.config_properties  
     
    def __init__ (self, name, url = None, user = None, password = None, **kwargs):
        MetaLayer.__init__(self, name, **kwargs) 
        self.url = url
        self.user = user
        self.password = password

    def renderTile(self, tile):
        wms = WMSClient.WMS( self.url, {
          "bbox": tile.bbox(), 
          "format": self.mime_type,
          "layer": self.layers,
          "TileCol": tile.x,
          "TileRow": tile.y,
          "TileMatrix": 'EPSG:4326:%s' % (tile.z)
        }, self.user, self.password)
        tile.data, response = wms.fetch()
        return tile.data 
