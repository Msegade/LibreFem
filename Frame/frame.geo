cl1=100;
Point(1) = {0, -1000, 0, cl1};
Point(2) = {0, -1000, 1000, cl1};
Point(3) = {0, -500, 1000, cl1};
Point(4) = {0, 0, 1000, cl1};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Symmetry {0, 1, 0, 0} {
  Duplicata { Line{2, 3, 1}; }
}
Physical Line("topbeam") = {2, 3, 5, 4};
Physical Line("mast") = {1, 6};
Physical Point("groundS") = {1};
Physical Point("groundN") = {13};
Physical Point("loadS") = {3};
Physical Point("massN") = {6};

