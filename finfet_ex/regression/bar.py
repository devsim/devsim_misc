
import pygmsh
geom = pygmsh.opencascade.Geometry(
    characteristic_length_min=0.1,
  characteristic_length_max=0.1,
)

def create_vol_volume(geom, h, w, l, x, z, cr, lcar=100):
  f = 0.5*w
  y = [-f,-f+cr, +f-cr, +f]
  z = [z, z + (h-cr), z + h]
  f = 0.5 * cr
  points = []
  points.append(geom.add_point((x, y[0], z[0]), lcar=lcar))
  points.append(geom.add_point((x, y[0], z[1]), lcar=lcar))
  points.append(geom.add_point((x, y[1], z[1]), lcar=lcar))
  points.append(geom.add_point((x, y[1], z[2]), lcar=lcar))
  points.append(geom.add_point((x, y[2], z[2]), lcar=lcar))
  points.append(geom.add_point((x, y[2], z[1]), lcar=lcar))
  points.append(geom.add_point((x, y[3], z[1]), lcar=lcar))
  points.append(geom.add_point((x, y[3], z[0]), lcar=lcar))

  lines = []
  lines.append(geom.add_line(points[0], points[1]))
  lines.append(geom.add_circle_arc(points[1], points[2], points[3]))
  
  lines.append(geom.add_line(points[3], points[4]))
  lines.append(geom.add_circle_arc(points[4], points[5], points[6]))
  lines.append(geom.add_line(points[6], points[7]))
  lines.append(geom.add_line(points[7], points[0]))

  line_loop=geom.add_line_loop(lines)
  surface=geom.add_plane_surface(line_loop)
  vol = geom.extrude(surface, translation_axis=[l, 0, 0])[1]
  return vol


h_top=40
corner_radius=2.5

z_vol=0
h_vol=25
w_vol=10
l_vol=100
x_vol=-0.5*l_vol
vol=create_vol_volume(geom, h=h_vol, w=w_vol, l=l_vol, x=x_vol, z=z_vol, cr=corner_radius)

z_vol2=0
l_vol2=50
t_vol2=1
w_vol2=w_vol+2*t_vol2
h_vol2=h_vol+t_vol2
x_vol2=x_vol + 0.5*(l_vol-l_vol2)
vol2=create_vol_volume(geom, h=h_vol2, w=w_vol2, l=l_vol2, x=x_vol2, z=z_vol2, cr=corner_radius)
vol2=geom.boolean_difference([vol2], [vol], delete_first=True, delete_other=False)
geom.boolean_fragments([vol2, vol], [], delete_first=True, delete_other=False)
print(geom.get_code())

