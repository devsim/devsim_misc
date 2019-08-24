// This code was created by pygmsh v4.1.2.
SetFactory("OpenCASCADE");
Mesh.CharacteristicLengthMin = 0.1;
Mesh.CharacteristicLengthMax = 0.1;
p0 = newp;
Point(p0) = {-50.0, -5.0, 0, 100};
p1 = newp;
Point(p1) = {-50.0, -5.0, 22.5, 100};
p2 = newp;
Point(p2) = {-50.0, -2.5, 22.5, 100};
p3 = newp;
Point(p3) = {-50.0, -2.5, 25, 100};
p4 = newp;
Point(p4) = {-50.0, 2.5, 25, 100};
p5 = newp;
Point(p5) = {-50.0, 2.5, 22.5, 100};
p6 = newp;
Point(p6) = {-50.0, 5.0, 22.5, 100};
p7 = newp;
Point(p7) = {-50.0, 5.0, 0, 100};
l0 = newl;
Line(l0) = {p0, p1};
l1 = newl;
Circle(l1) = {p1, p2, p3};
l2 = newl;
Line(l2) = {p3, p4};
l3 = newl;
Circle(l3) = {p4, p5, p6};
l4 = newl;
Line(l4) = {p6, p7};
l5 = newl;
Line(l5) = {p7, p0};
ll0 = newll;
Line Loop(ll0) = {l0, l1, l2, l3, l4, l5};
s0 = news;
Plane Surface(s0) = {ll0};
ex1[] = Extrude{100,0,0}{Surface{s0};};
p8 = newp;
Point(p8) = {-25.0, -6.0, 0, 100};
p9 = newp;
Point(p9) = {-25.0, -6.0, 23.5, 100};
p10 = newp;
Point(p10) = {-25.0, -3.5, 23.5, 100};
p11 = newp;
Point(p11) = {-25.0, -3.5, 26, 100};
p12 = newp;
Point(p12) = {-25.0, 3.5, 26, 100};
p13 = newp;
Point(p13) = {-25.0, 3.5, 23.5, 100};
p14 = newp;
Point(p14) = {-25.0, 6.0, 23.5, 100};
p15 = newp;
Point(p15) = {-25.0, 6.0, 0, 100};
l6 = newl;
Line(l6) = {p8, p9};
l7 = newl;
Circle(l7) = {p9, p10, p11};
l8 = newl;
Line(l8) = {p11, p12};
l9 = newl;
Circle(l9) = {p12, p13, p14};
l10 = newl;
Line(l10) = {p14, p15};
l11 = newl;
Line(l11) = {p15, p8};
ll1 = newll;
Line Loop(ll1) = {l6, l7, l8, l9, l10, l11};
s2 = news;
Plane Surface(s2) = {ll1};
ex2[] = Extrude{50,0,0}{Surface{s2};};
bo1[] = BooleanDifference{ Volume{ex2[1]}; Delete; } { Volume{ex1[1]}; };
bo2[] = BooleanFragments{ Volume{bo1[]};Volume{ex1[1]}; Delete; } {  };
