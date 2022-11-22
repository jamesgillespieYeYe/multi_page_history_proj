import math
import sympy as sym
'''
This contains implementations for constructions Euclid
took as postulates: 
You may draw a circle centered at one point, passing through another
You may draw a line segment from one point to another
You may extend a line segment indefinitely 
(A postulate that he uses, but does not explicitly state, is that
you may take the intersection of two lines)
'''
#(Point Shape, Point Shape)
def circle(alist,style=False, opacity=1):
    print("style: ", style)
    passing_through = []
    center = []
    center.append(alist[0].shape['x0'])
    center.append(alist[0].shape['y0'])
    passing_through.append(alist[1].shape['x0'])
    passing_through.append(alist[1].shape['y0'])
    r = math.sqrt((passing_through[0] - center[0])** 2 + (passing_through[1] - center[1])** 2)
    rref = (center[0] + r, center[1] + r)
    lref = (center[0] - r, center[1] - r)
    color_string = 'rgba(0, 128, 255, '
    color_string += str(opacity) + ")"
    ret = {
    "type": "circle",
    "xref": "x",
    "yref":"y",
    "x0": lref[0], 
    "y0": lref[1], 
    "x1": rref[0], 
    "y1": rref[1],
    "line_color": color_string,
    }
    if (style == True):
        ret['line_dash'] = 'dot'
    return ret

#Return y = ... for a shape
def equation(shape, x):
    if shape['type'] == 'line': #y = mx + b
        m = (shape['y1'] - shape['y0']) / (shape['x1'] - shape['x0'])
        b = shape['y1'] - m*shape['x1']
        eq = m*x + b 
        return eq
   


    return None

def solve(shapeA, shapeB, x, y):
    Eqs = []
    for shape in [shapeA, shapeB]:
        if shape['type'] == 'line':
            m = (shape['y1'] - shape['y0']) / (shape['x1'] - shape['x0'])
            b = shape['y1'] - m*shape['x1']
            Eqs.append(sym.Eq(y, m*x + b))
        elif shape['type'] == 'circle':
            center = (shape['x0'] + .5*(shape['x1'] - shape['x0']), 
                shape['y0'] + .5*(shape['y1'] - shape['y0']))
            r = center[1] - shape['y0']
            Eqs.append(sym.Eq(r**2, (x - center[0])**2 + (y - center[1])**2))

    sol = sym.solve((Eqs[0], Eqs[1]), (x, y))
    return sol
            

def intersection(alist, style=False, opacity=1):
    A = alist[0]
    B = alist[1]
    xCor = -100
    yCor = -100
    #return point([xCor,yCor])
    x = sym.Symbol('x')
    equationA = equation(A.shape, x)
    equationB = equation(B.shape, x)
    if (equationA != None and equationB != None):
        solset = sym.solve(equationA - equationB)
        x0 = list(solset)[0]
        y0 = equationB.subs(x, x0).evalf()
        return point([float(x0), float(y0)])
    else:
        y = sym.Symbol('y')
        sols = solve(A.shape, B.shape, x, y)
        if (len(sols) == 1):
            return point([float(sols[0][0]), float(sols[0][1])], style, opacity)
        else:
            ret = []
            for s in sols:
                ret.append(point([float(s[0]), float(s[1])],style, opacity))
            return ret

    return point([xCor,yCor])

#(Point Shape, Point Shape)
def segment(alist, style=False, opacity=1):
    #print("line: alist: ", alist)
    print("opacity: ", opacity)
    P = alist[0]
    Q = alist[1]
    color_string = 'rgba(255, 0, 0, '
    color_string += str(opacity) + ")"
    ret = {
        "type": "line",
        "xref": "x", 
        "yref": "y", 
        "x0": P.shape['x0'],
        "y0": P.shape['y0'],
        "x1": Q.shape['x0'],
        "y1": Q.shape['y0'],
        "line_color": color_string
    }
    if (style == True):
        ret['line_dash'] = 'dot'
    return ret

def segment_color(alist, style=False, opacity=1):
    print("alist: ", alist)
    P = alist[0]
    Q = alist[1]
    color = alist[2][1:len(alist[2])]
    dash = alist[3][1:len(alist[3])]
    print("color: ", color)
    ret = {
        "type": "line",
        "xref": "x", 
        "yref": "y", 
        "x0": P.shape['x0'],
        "y0": P.shape['y0'],
        "x1": Q.shape['x0'],
        "y1": Q.shape['y0'],
        "line_color": color
    }
    if (dash != "None"):
        ret['line_dash'] = dash
    return ret

def lineR(alist, style=False, opacity=1):
    seg = segment(alist, style=False)
    x = sym.Symbol('x')
    eq = equation(seg, x)
    P = alist[0]
    Q = alist[1]
    x1 = Q.shape['x0'] + 10
    y1 = eq.subs(x, x1).evalf()
    ret = {
        "type": "line",
        "xref": "x", 
        "yref": "y", 
        "x0": P.shape['x0'],
        "y0": P.shape['y0'],
        "x1": x1,
        "y1": float(y1),
        "line_color": "yellow"
    }
    if (style == True):
        ret['line_dash'] = 'dot'
    return ret


#(x, y)
def point(P, style=False, opacity=1):
    off = .05
    color_string = 'rgba(122, 0, 122, '
    color_string += str(opacity) + ")"
    ret =  {
        "type": "line", #type is line so it actually shows up on graph
        "xref": "x", 
        "yref": "y", 
        "x0": P[0],
        "y0": P[1],
        "x1": P[0] + off, #^
        "y1": P[1] + off,
        "line_color": color_string
    }
    return ret