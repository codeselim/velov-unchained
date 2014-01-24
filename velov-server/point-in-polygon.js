function isPointInPoly(poly, pt){
    for(var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
        ((poly[i].lat <= pt.lat && pt.lat < poly[j].lat) || (poly[j].lat <= pt.lat && pt.lat < poly[i].lat))
        && (pt.long < (poly[j].long - poly[i].long) * (pt.lat - poly[i].lat) / (poly[j].lat - poly[i].lat) + poly[i].long)
        && (c = !c);
    return c;
}


points = [{"lat": 45.772552,"long": 4.854326},{"lat": 45.772911,"long": 4.85836},{"lat": 45.784764,"long": 4.85939},{"lat": 45.783626,"long": 4.852009},{"lat": 45.780873,"long": 4.847374},{"lat": 45.777371,"long": 4.844885}];

pointIn1 = {"lat": 45.7763834667481,"long":4.851837158203125 };
pointIn2= {"lat": 45.77746099967389,"long":4.846129417419434 };
pointIn3 = {"lat": 45.78072340295856,"long": 4.857759475708008};
pointOut1 = {"lat": 45.773210609996745,"long": 4.847888946533203};
pointOut2 = {"lat": 45.78144170464571,"long": 4.844841957092285};
pointOut3 = {"lat": 45.78811548202083,"long": 4.8624372482299805};

console.log(isPointInPoly(points,pointIn1));
console.log(isPointInPoly(points,pointIn2));
console.log(isPointInPoly(points,pointIn3));
console.log(isPointInPoly(points,pointOut1));
console.log(isPointInPoly(points,pointOut2));
console.log(isPointInPoly(points,pointOut3));
