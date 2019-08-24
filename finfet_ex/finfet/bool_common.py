
def create_fin_volume(geom, h, w, l, x, z, cr, lcar, half_device=False):
  f = 0.5*w
  y = [-f,-f+cr, +f-cr, +f, 0.0]
  z = [z, z + (h-cr), z + h]
  points = []
  lines = []

  if f < cr:
    raise RuntimeError("width must be at least twice the corner radius")

  if half_device:
    points.append(geom.add_point((x, y[4], z[0]), lcar=lcar))
  else:
    points.append(geom.add_point((x, y[0], z[0]), lcar=lcar))
    points.append(geom.add_point((x, y[0], z[1]), lcar=lcar))
    lines.append(geom.add_line(points[-2], points[-1]))

    points.append(geom.add_point((x, y[1], z[1]), lcar=lcar))
    points.append(geom.add_point((x, y[1], z[2]), lcar=lcar))
    lines.append(geom.add_circle_arc(points[-3], points[-2], points[-1]))

  if cr == f:
    points.append(geom.add_point((x, y[4], z[2]), lcar=lcar))
  else: #if cr < f:
    points.append(geom.add_point((x, y[4], z[2]), lcar=lcar))
    lines.append(geom.add_line(points[-2], points[-1]))
    points.append(geom.add_point((x, y[2], z[2]), lcar=lcar))
    lines.append(geom.add_line(points[-2], points[-1]))


  points.append(geom.add_point((x, y[2], z[1]), lcar=lcar))
  points.append(geom.add_point((x, y[3], z[1]), lcar=lcar))
  lines.append(geom.add_circle_arc(points[-3], points[-2], points[-1]))

  points.append(geom.add_point((x, y[3], z[0]), lcar=lcar))

  lines.append(geom.add_line(points[-2], points[-1]))

  
  lines.append(geom.add_line(points[-1], points[0]))

  line_loop=geom.add_line_loop(lines)
  surface=geom.add_plane_surface(line_loop)
  vol = geom.extrude(surface, translation_axis=[l, 0, 0])[1]
  return vol

def create_box_volume(geom, h, w, l, x, z, lcar, half_device=False):
  f = 0.5*w
  if half_device:
    y = [0.0,+f]
  else:
    y = [-f,+f]

  z = [z, z + h]
  points = []
  lines = []

  points.append(geom.add_point((x, y[0], z[0]), lcar=lcar))
  points.append(geom.add_point((x, y[0], z[1]), lcar=lcar))
  lines.append(geom.add_line(points[-2], points[-1]))

  points.append(geom.add_point((x, y[1], z[1]), lcar=lcar))
  lines.append(geom.add_line(points[-2], points[-1]))

  points.append(geom.add_point((x, y[1], z[0]), lcar=lcar))
  lines.append(geom.add_line(points[-2], points[-1]))
  lines.append(geom.add_line(points[-1], points[0]))

  line_loop=geom.add_line_loop(lines)
  surface=geom.add_plane_surface(line_loop)
  vol = geom.extrude(surface, translation_axis=[l, 0, 0])[1]
  return vol
