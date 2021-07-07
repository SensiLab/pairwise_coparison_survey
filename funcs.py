from datetime import datetime
import math
def updateRating(s, r, rd, r_other, rd_other):
    # s is the result of comparison (1 if selected, .5 if can't decide, 0 if not selected    
    q = 0.00575646273   #constant (magic number?)

    g_rd_other = 1/math.sqrt(1 + (3 * (q**2)*(rd_other**2)/pow(math.pi,2)))
    e_exp = -g_rd_other * (r0 - r_other)/400
    e = 1/(1 + pow(10,e_exp))
    d_square = pow(pow(q,2) * pow(g_rd_other,2)*e*(1-e),-1)
    r = r0 + (q/(1/(pow(rd,2)+(1/d_square))) * g_rd_other * (s - e))
