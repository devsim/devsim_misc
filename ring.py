import pygmsh

#def output(geom, volumes):
#    print(geom.get_code())
#    ivol = 0
#    isurf = 0
#    for vol in volumes:
#        if vol[1] == 'vol':
#            print('Physical Volume("%s") = {vol%d};'%(vol[0], ivol))
#            ivol +=1
#        else:
#            print('Physical Surface("%s") = {s%d};'%(vol[0], isurf))
#            isurf +=1
        
def geometry():
    geom = pygmsh.opencascade.Geometry(
        characteristic_length_min=0.1,
        characteristic_length_max=0.1,
    )

    # p-implants 
    disk = geom.add_cylinder([0.0, 0.0, 0.0],   [0,0,.1], 0.75)

    # n-bulk
    bulk = geom.add_box([-1.0, -1.0, 0.0], [2, 2,-1.5])

    # n-layer
    nlayer = geom.add_box([-1.0, -1.0, -1.5], [2, 2, -0.1])

    # contact regions used to identify contacts
    top = geom.add_cylinder([0.0, 0.0, 0.1],   [0,0,.1], 0.75)
    bot = geom.add_box([-1.0, -1.0, -1.6], [2, 2, -0.1])

    #geom.add_physical(top_vol, 'top')
    geom.add_physical(top, 'top_volume')
    geom.add_physical(bot, 'bot_volume')
    geom.add_physical(disk, 'disk')
    geom.add_physical(bulk, 'bulk')
    geom.add_physical(nlayer, 'nlayer')
    #geom.add_physical(top_vol, 'top')

    # merge shapes
    # this is important for interfaces and contacts
    geom.add_raw_code('Coherence;\n')

    with open('ring.geo', 'w') as f:
      f.write(geom.get_code())

    with open('ring.yaml', 'w') as f:
      f.write('''
name_priority:
  - top
  - bot
  - disk
  - bulk
  - nlayer
contact_regions:
  - contact: top_volume
    remove: True
  - contact: bot_volume
    remove: True
regions:
  - region: disk
  - region: bulk
  - region: nlayer
interfaces:
  - interface: top
    regions: [top_volume, disk]
  - interface: bot
    regions: [bot_volume, nlayer]
''')
    

if __name__ == '__main__':
    geometry()

